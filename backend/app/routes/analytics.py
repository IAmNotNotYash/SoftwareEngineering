import json
from datetime import datetime, timedelta, timezone

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models.analytics import AnalyticsSnapshot, ArtistRevenueTrend, PlatformRevenueTrend
from app.models.catalogue import Catalogue
from app.models.commerce import Order, Product
from app.models.social import Review, Follow, Post, PostLike
from app.models.user import ArtistProfile, BuyerProfile
from app.utils.ai_summary import generate_artist_summaries, generate_platform_summary

analytics_bp = Blueprint("analytics", __name__)


def _get_identity():
    raw = get_jwt_identity()
    try:
        return json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        return raw


def _utc_now():
    return datetime.now(timezone.utc)


def _as_utc(dt):
    if dt is None:
        return None
    # Some DB backends return naive datetimes for DateTime columns.
    # Treat them as UTC so stale checks don't crash on aware-vs-naive comparison.
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _ai_runtime():
    provider = (current_app.config.get("AI_PROVIDER", "groq") or "groq").lower()
    if provider == "groq":
        return (
            provider,
            current_app.config.get("GROQ_API_KEY"),
            current_app.config.get("GROQ_MODEL", "llama-3.1-8b-instant"),
        )
    return (
        "gemini",
        current_app.config.get("GEMINI_API_KEY"),
        current_app.config.get("GEMINI_MODEL", "gemini-2.0-flash"),
    )


def _is_stale(snapshot):
    ttl_hours = int(current_app.config.get("AI_SNAPSHOT_TTL_HOURS", 12))
    if not snapshot:
        return True
    generated_at = _as_utc(snapshot.generated_at) or _utc_now()
    return generated_at < (_utc_now() - timedelta(hours=ttl_hours))


def _artist_metrics(artist_id):
    trends = (
        ArtistRevenueTrend.query.filter_by(artist_id=artist_id)
        .order_by(ArtistRevenueTrend.month.asc())
        .all()
    )
    recent = trends[-6:]
    
    # Use direct Order queries for real-time totals, excluding cancelled orders
    # We use subtotal for artist's own revenue (excluding shipping)
    total_revenue_val = db.session.query(db.func.sum(Order.subtotal))\
        .filter(Order.artist_id == artist_id, Order.status != 'cancelled')\
        .scalar() or 0
    total_orders_val = Order.query\
        .filter(Order.artist_id == artist_id, Order.status != 'cancelled')\
        .count()
        
    total_revenue = float(total_revenue_val)
    total_orders = int(total_orders_val)
    
    # Calculate combined live views (Catalogues + Standalone Stories)
    from app.models.catalogue import CatalogueStats, CatalogueView
    
    # 1. Views from Catalogues (Sum of Stats)
    cat_views = db.session.query(db.func.sum(CatalogueStats.total_views))\
        .select_from(Catalogue)\
        .outerjoin(CatalogueStats, Catalogue.id == CatalogueStats.catalogue_id)\
        .filter(Catalogue.artist_id == artist_id)\
        .scalar() or 0
        
    # 2. Views from Stories (Post views_count)
    story_views = db.session.query(db.func.sum(Post.views_count))\
        .filter(Post.artist_id == artist_id)\
        .scalar() or 0
        
    # 3. Double check View Table rows if counts seem off (or just for robustness)
    # This ensures even if Stats record was missing, we see there were rows
    view_table_count = db.session.query(db.func.count(CatalogueView.id))\
        .join(Catalogue, Catalogue.id == CatalogueView.catalogue_id)\
        .filter(Catalogue.artist_id == artist_id)\
        .scalar() or 0
    
    catalogue_views = max(int(cat_views), int(view_table_count)) + int(story_views)
    
    # Calculate live engagement from Posts and Likes
    total_likes = db.session.query(db.func.count(PostLike.id))\
        .join(Post, Post.id == PostLike.post_id)\
        .filter(Post.artist_id == artist_id)\
        .scalar() or 0
    
    follower_count = Follow.query.filter_by(artist_id=artist_id).count()
    
    # Engagement rate: Total Likes / Total Followers (expressed as percentage)
    # If no followers yet, we use a count-based engagement or 0
    if follower_count > 0:
        avg_engagement_pct = (total_likes / follower_count) * 100
    else:
        avg_engagement_pct = total_likes * 5 # Small boost for new artists without followers

    product_ids = [p.id for p in Product.query.filter_by(artist_id=artist_id, is_deleted=False).all()]
    catalogue_ids = [c.id for c in Catalogue.query.filter_by(artist_id=artist_id).all()]

    review_query = Review.query.filter_by(is_deleted=False)
    review_filters = []
    if product_ids:
        review_filters.append(db.and_(Review.target_type == "product", Review.target_id.in_(product_ids)))
    if catalogue_ids:
        review_filters.append(db.and_(Review.target_type == "catalogue", Review.target_id.in_(catalogue_ids)))

    if review_filters:
        review_query = review_query.filter(db.or_(*review_filters))
    else:
        review_query = review_query.filter(db.false())
    reviews = review_query.order_by(Review.created_at.desc()).limit(40).all()
    review_count = len(reviews)
    ratings = [r.rating for r in reviews if r.rating is not None]
    avg_rating = (sum(ratings) / len(ratings)) if ratings else None
    review_texts = [r.body for r in reviews if r.body]

    recent_months = [
        {
            "month": t.month,
            "revenue": float(t.revenue or 0),
            "orders": int(t.orders or 0),
            "catalogue_views": int(t.catalogue_views or 0),
        }
        for t in recent
    ]

    return {
        "artist_id": artist_id,
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "catalogue_views": catalogue_views,
        "avg_story_engagement_pct": round(avg_engagement_pct, 2),
        "review_count": review_count,
        "avg_rating": round(avg_rating, 2) if avg_rating is not None else None,
        "recent_months": recent_months,
    }, review_texts


def _platform_metrics():
    trends = PlatformRevenueTrend.query.order_by(PlatformRevenueTrend.month.asc()).all()
    recent = trends[-6:]
    
    # Use direct Order queries for real-time totals, excluding cancelled orders
    total_revenue_val = db.session.query(db.func.sum(Order.total))\
        .filter(Order.status != 'cancelled')\
        .scalar() or 0
    total_orders = Order.query.filter(Order.status != 'cancelled').count()
    
    total_revenue = float(total_revenue_val)
    
    registered_artists = ArtistProfile.query.count()
    registered_buyers = BuyerProfile.query.count()
    pending_verifications = ArtistProfile.query.filter_by(verification_status="pending").count()

    recent_months = [
        {
            "month": t.month,
            "revenue": float(t.revenue or 0),
            "new_signups": int(t.new_signups or 0),
            "total_orders": int(t.total_orders or 0),
            "avg_order_value": float(t.avg_order_value or 0),
        }
        for t in recent
    ]

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "registered_artists": registered_artists,
        "registered_buyers": registered_buyers,
        "pending_verifications": pending_verifications,
        "recent_months": recent_months,
    }


def _create_artist_snapshot(artist_id):
    metrics, review_texts = _artist_metrics(artist_id)
    provider, api_key, model = _ai_runtime()
    ai_summary, sentiment_summary = generate_artist_summaries(
        metrics,
        review_texts,
        provider=provider,
        api_key=api_key,
        model=model,
    )
    period = metrics["recent_months"][-1]["month"] if metrics["recent_months"] else "all-time"

    snapshot = AnalyticsSnapshot(
        entity_type="artist",
        entity_id=artist_id,
        period=period,
        metrics=metrics,
        ai_summary=ai_summary,
        sentiment_summary=sentiment_summary,
        generated_at=_utc_now(),
    )
    db.session.add(snapshot)
    db.session.commit()
    return snapshot


def _create_platform_snapshot():
    metrics = _platform_metrics()
    provider, api_key, model = _ai_runtime()
    ai_summary = generate_platform_summary(
        metrics,
        provider=provider,
        api_key=api_key,
        model=model,
    )
    period = metrics["recent_months"][-1]["month"] if metrics["recent_months"] else "all-time"

    snapshot = AnalyticsSnapshot(
        entity_type="platform",
        entity_id=None,
        period=period,
        metrics=metrics,
        ai_summary=ai_summary,
        sentiment_summary=None,
        generated_at=_utc_now(),
    )
    db.session.add(snapshot)
    db.session.commit()
    return snapshot


@analytics_bp.route("/artist/trend", methods=["GET"])
@jwt_required()
def get_artist_trend():
    identity = _get_identity()
    if identity["role"] != "artist":
        return jsonify({"error": "Forbidden"}), 403

    artist = ArtistProfile.query.filter_by(user_id=identity["id"]).first()
    if not artist:
        return jsonify({"error": "Artist profile not found"}), 404

    trends = (
        ArtistRevenueTrend.query.filter_by(artist_id=artist.id)
        .order_by(ArtistRevenueTrend.month.asc())
        .all()
    )
    
    current_month = datetime.now().strftime("%Y-%m")
    results = []
    
    # Process existing trends
    for t in trends:
        data = t.to_dict()
        if t.month == current_month:
            # Override with live data for the current month
            metrics, _ = _artist_metrics(artist.id)
            data['revenue'] = metrics['total_revenue']
            data['orders'] = metrics['total_orders']
            data['catalogue_views'] = metrics['catalogue_views']
        results.append(data)
    
    # Check if we need to add the current month if it wasn't in trends
    has_current = any(t['month'] == current_month for t in results)
    
    if not has_current:
        # Fetch live totals for this month for the graph
        metrics, _ = _artist_metrics(artist.id)
        results.append({
            "month": current_month,
            "revenue": metrics["total_revenue"],
            "orders": metrics["total_orders"],
            "catalogue_views": metrics["catalogue_views"]
        })

    return jsonify(results), 200


@analytics_bp.route("/platform/trend", methods=["GET"])
@jwt_required()
def get_platform_trend():
    identity = _get_identity()
    if identity["role"] != "admin":
        return jsonify({"error": "Forbidden"}), 403

    trends = PlatformRevenueTrend.query.order_by(PlatformRevenueTrend.month.asc()).all()
    if not trends:
        return jsonify([]), 200
    return jsonify([t.to_dict() for t in trends]), 200


@analytics_bp.route("/snapshots", methods=["GET"])
@jwt_required()
def get_snapshot():
    identity = _get_identity()
    entity_type = request.args.get("type", "artist")
    force_refresh = request.args.get("refresh", "false").lower() in {"1", "true", "yes"}

    if entity_type == "artist":
        if identity.get("role") != "artist":
            return jsonify({"error": "Forbidden"}), 403
        artist = ArtistProfile.query.filter_by(user_id=identity["id"]).first()
        if not artist:
            return jsonify({"error": "Artist profile not found"}), 404
        snapshot = (
            AnalyticsSnapshot.query.filter_by(entity_type="artist", entity_id=artist.id)
            .order_by(AnalyticsSnapshot.generated_at.desc())
            .first()
        )
        if force_refresh or _is_stale(snapshot):
            snapshot = _create_artist_snapshot(artist.id)
        return jsonify(snapshot.to_dict()), 200

    if entity_type == "platform":
        if identity.get("role") != "admin":
            return jsonify({"error": "Forbidden"}), 403
        snapshot = (
            AnalyticsSnapshot.query.filter_by(entity_type="platform")
            .order_by(AnalyticsSnapshot.generated_at.desc())
            .first()
        )
        if force_refresh or _is_stale(snapshot):
            snapshot = _create_platform_snapshot()
        return jsonify(snapshot.to_dict()), 200

    return jsonify({"error": "Invalid type. Use 'artist' or 'platform'"}), 400


@analytics_bp.route("/snapshots/refresh", methods=["POST"])
@jwt_required()
def refresh_snapshot():
    identity = _get_identity()
    entity_type = request.args.get("type", "artist")

    if entity_type == "artist":
        if identity.get("role") != "artist":
            return jsonify({"error": "Forbidden"}), 403
        artist = ArtistProfile.query.filter_by(user_id=identity["id"]).first()
        if not artist:
            return jsonify({"error": "Artist profile not found"}), 404
        snapshot = _create_artist_snapshot(artist.id)
        return jsonify(snapshot.to_dict()), 201

    if entity_type == "platform":
        if identity.get("role") != "admin":
            return jsonify({"error": "Forbidden"}), 403
        snapshot = _create_platform_snapshot()
        return jsonify(snapshot.to_dict()), 201

    return jsonify({"error": "Invalid type. Use 'artist' or 'platform'"}), 400
