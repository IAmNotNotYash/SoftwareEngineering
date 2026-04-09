from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.catalogue import Catalogue, CatalogueProduct, CatalogueStats, CatalogueView, CatalogueLike
from app.models.user import ArtistProfile, BuyerProfile

catalogue_bp = Blueprint('catalogue', __name__)


# ── Helpers ───────────────────────────────────────────────────────────────────

import json

def _get_identity():
    id_str = get_jwt_identity()
    try:
        if isinstance(id_str, str):
            return json.loads(id_str)
        return id_str
    except (json.JSONDecodeError, TypeError):
        return id_str


def _artist_profile(user_id):
    return ArtistProfile.query.filter_by(user_id=user_id).first()


def _buyer_profile(user_id):
    return BuyerProfile.query.filter_by(user_id=user_id).first()


def _require_role(identity, *roles):
    if identity.get('role') not in roles:
        return jsonify({'error': 'Forbidden'}), 403
    return None


def _bump_views(catalogue, buyer_id=None):
    """Insert a CatalogueView and increment CatalogueStats.total_views atomically."""
    view = CatalogueView(catalogue_id=catalogue.id, buyer_id=buyer_id)
    db.session.add(view)
    if catalogue.stats:
        catalogue.stats.total_views += 1
        catalogue.stats.last_updated = datetime.now(timezone.utc)
    db.session.commit()


# ── PUBLIC: Browse live catalogues ────────────────────────────────────────────
# GET /api/catalogues?artist_id=&status=live&search=
@catalogue_bp.route('', methods=['GET'])
def list_catalogues():
    status_filter = request.args.get('status', 'live')
    artist_id = request.args.get('artist_id', '')
    search = request.args.get('search', '').strip()

    q = Catalogue.query
    if status_filter:
        q = q.filter_by(status=status_filter)
    if artist_id:
        q = q.filter_by(artist_id=artist_id)
    if search:
        q = q.filter(Catalogue.title.ilike(f'%{search}%'))

    catalogues = q.order_by(Catalogue.published_at.desc()).all()
    return jsonify([c.to_dict() for c in catalogues]), 200


# ── PUBLIC: Get single catalogue (records a view) ─────────────────────────────
# GET /api/catalogues/:id
@catalogue_bp.route('/<catalogue_id>', methods=['GET'])
def get_catalogue(catalogue_id):
    catalogue = db.session.get(Catalogue, catalogue_id)
    if not catalogue:
        return jsonify({'error': 'Catalogue not found'}), 404

    # Record view — identify buyer if logged in (optional JWT)
    buyer_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            if isinstance(identity, str):
                import json
                identity = json.loads(identity)
            if identity.get('role') == 'buyer':
                bp = _buyer_profile(identity['id'])
                buyer_id = bp.id if bp else None
    except Exception:
        pass

    _bump_views(catalogue, buyer_id)
    return jsonify(catalogue.to_dict(include_products=True)), 200


# ── ARTIST: Create a new catalogue ───────────────────────────────────────────
# POST /api/catalogues
@catalogue_bp.route('', methods=['POST'])
@jwt_required()
def create_catalogue():
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err:
        return err

    artist = _artist_profile(identity['id'])
    if not artist:
        return jsonify({'error': 'Artist profile not found'}), 404
    if artist.verification_status != 'approved':
        return jsonify({'error': 'Your account must be verified before publishing catalogues'}), 403

    data = request.get_json() or {}
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    catalogue = Catalogue(
        artist_id=artist.id,
        title=title,
        narrative=data.get('narrative'),
        cover_photo_url=data.get('cover_photo_url'),
        theme=data.get('theme', 'earth'),
        launch_intent=data.get('launch_intent', 'live'),
        status=data.get('status', 'draft'),
        philosophy=data.get('philosophy'),
        artist_note=data.get('artist_note'),
    )

    # If publishing immediately
    if catalogue.status == 'live':
        catalogue.published_at = datetime.now(timezone.utc)

    db.session.add(catalogue)
    db.session.flush()

    # Auto-create a CatalogueStats row
    stats = CatalogueStats(catalogue_id=catalogue.id)
    db.session.add(stats)

    # Attach products if provided
    product_ids = data.get('product_ids', [])
    for i, pid in enumerate(product_ids):
        cp = CatalogueProduct(catalogue_id=catalogue.id, product_id=pid, sort_order=i)
        db.session.add(cp)

    db.session.commit()
    return jsonify(catalogue.to_dict(include_products=True)), 201


# ── ARTIST: Update catalogue ──────────────────────────────────────────────────
# PATCH /api/catalogues/:id
@catalogue_bp.route('/<catalogue_id>', methods=['PATCH'])
@jwt_required()
def update_catalogue(catalogue_id):
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err:
        return err

    artist = _artist_profile(identity['id'])
    catalogue = db.session.get(Catalogue, catalogue_id)
    if not catalogue or catalogue.artist_id != artist.id:
        return jsonify({'error': 'Catalogue not found or access denied'}), 404

    data = request.get_json() or {}
    EDITABLE = ['title', 'narrative', 'cover_photo_url', 'theme', 'launch_intent',
                'philosophy', 'artist_note']
    for field in EDITABLE:
        if field in data:
            setattr(catalogue, field, data[field])

    # Handle status transition
    if 'status' in data:
        new_status = data['status']
        catalogue.status = new_status
        if new_status == 'live' and not catalogue.published_at:
            catalogue.published_at = datetime.now(timezone.utc)

    # Replace products if provided
    if 'product_ids' in data:
        CatalogueProduct.query.filter_by(catalogue_id=catalogue.id).delete()
        for i, pid in enumerate(data['product_ids']):
            cp = CatalogueProduct(catalogue_id=catalogue.id, product_id=pid, sort_order=i)
            db.session.add(cp)

    db.session.commit()
    return jsonify(catalogue.to_dict(include_products=True)), 200


# ── ARTIST: Delete (end) catalogue ───────────────────────────────────────────
# DELETE /api/catalogues/:id
@catalogue_bp.route('/<catalogue_id>', methods=['DELETE'])
@jwt_required()
def delete_catalogue(catalogue_id):
    identity = _get_identity()
    err = _require_role(identity, 'artist', 'admin')
    if err:
        return err

    catalogue = db.session.get(Catalogue, catalogue_id)
    if not catalogue:
        return jsonify({'error': 'Catalogue not found'}), 404

    if identity.get('role') == 'artist':
        artist = _artist_profile(identity['id'])
        if catalogue.artist_id != artist.id:
            return jsonify({'error': 'Access denied'}), 403

    catalogue.status = 'ended'
    db.session.commit()
    return jsonify({'message': 'Catalogue ended successfully'}), 200


# ── BUYER: Like a catalogue ───────────────────────────────────────────────────
# POST /api/catalogues/:id/like
@catalogue_bp.route('/<catalogue_id>/like', methods=['POST'])
@jwt_required()
def like_catalogue(catalogue_id):
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err:
        return err

    buyer = _buyer_profile(identity['id'])
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404

    catalogue = db.session.get(Catalogue, catalogue_id)
    if not catalogue:
        return jsonify({'error': 'Catalogue not found'}), 404

    try:
        like = CatalogueLike(catalogue_id=catalogue_id, buyer_id=buyer.id)
        db.session.add(like)
        db.session.flush()

        # Update stats
        if catalogue.stats:
            catalogue.stats.total_likes += 1
            catalogue.stats.last_updated = datetime.now(timezone.utc)

        db.session.commit()
        return jsonify({'message': 'Liked', 'liked': True}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Already liked'}), 409


# ── BUYER: Unlike a catalogue ─────────────────────────────────────────────────
# DELETE /api/catalogues/:id/like
@catalogue_bp.route('/<catalogue_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_catalogue(catalogue_id):
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err:
        return err

    buyer = _buyer_profile(identity['id'])
    like = CatalogueLike.query.filter_by(
        catalogue_id=catalogue_id, buyer_id=buyer.id
    ).first()

    if not like:
        return jsonify({'error': 'Like not found'}), 404

    catalogue = db.session.get(Catalogue, catalogue_id)
    db.session.delete(like)

    if catalogue and catalogue.stats and catalogue.stats.total_likes > 0:
        catalogue.stats.total_likes -= 1
        catalogue.stats.last_updated = datetime.now(timezone.utc)

    db.session.commit()
    return jsonify({'message': 'Unliked', 'liked': False}), 200


# ── BUYER: Check if catalogue is liked ───────────────────────────────────────
# GET /api/catalogues/:id/like
@catalogue_bp.route('/<catalogue_id>/like', methods=['GET'])
@jwt_required()
def check_like(catalogue_id):
    identity = _get_identity()
    buyer = _buyer_profile(identity['id'])
    liked = False
    if buyer:
        liked = CatalogueLike.query.filter_by(
            catalogue_id=catalogue_id, buyer_id=buyer.id
        ).first() is not None
    return jsonify({'liked': liked}), 200
