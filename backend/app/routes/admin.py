from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.commerce import Order
from app.models.user import User, ArtistProfile, BuyerProfile
from datetime import datetime, timezone
import json

admin_bp = Blueprint('admin', __name__)

def _require_admin():
    raw_identity = get_jwt_identity()
    try:
        identity = json.loads(raw_identity) if isinstance(raw_identity, str) else raw_identity
    except (json.JSONDecodeError, TypeError):
        identity = raw_identity

    if not identity or not isinstance(identity, dict) or identity.get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    return None

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    err = _require_admin()
    if err: return err

    total_revenue_val = db.session.query(db.func.sum(Order.total))\
        .filter(Order.status != 'cancelled')\
        .scalar() or 0
    total_orders = Order.query.filter(Order.status != 'cancelled').count()
    delivered_orders = Order.query.filter_by(status='delivered').count()
    pending_orders = Order.query.filter(Order.status.in_(['pending', 'processing', 'shipped'])).count()
    
    artist_count = ArtistProfile.query.count()
    buyer_count = BuyerProfile.query.count()
    pending_verifications = ArtistProfile.query.filter_by(verification_status='pending').count()

    return jsonify({
        'totalRevenue': float(total_revenue_val),
        'totalOrders': total_orders,
        'deliveredOrders': delivered_orders,
        'pendingOrders': pending_orders,
        'registeredArtists': artist_count,
        'registeredBuyers': buyer_count,
        'pendingVerifications': pending_verifications
    }), 200

@admin_bp.route('/analytics/artists', methods=['GET'])
@jwt_required()
def get_artist_performance():
    err = _require_admin()
    if err: return err

    results = db.session.query(
        ArtistProfile.full_name,
        ArtistProfile.brand_name,
        db.func.sum(Order.subtotal).label('revenue'),
        db.func.count(Order.id).label('orders')
    ).outerjoin(Order, db.and_(ArtistProfile.id == Order.artist_id, Order.status != 'cancelled'))\
     .group_by(ArtistProfile.id)\
     .all()

    return jsonify([{
        'name': r.full_name,
        'brand': r.brand_name,
        'revenue': float(r.revenue or 0),
        'orders': int(r.orders or 0)
    } for r in results]), 200

@admin_bp.route('/verification/queue', methods=['GET'])
@jwt_required()
def get_verification_queue():
    err = _require_admin()
    if err: return err

    pending = ArtistProfile.query.filter_by(verification_status='pending').all()
    return jsonify([{
        'id': a.id,
        'name': a.full_name,
        'brand': a.brand_name,
        'email': a.user.email if a.user else '',
        'joined': a.created_at.isoformat(),
        'status': a.verification_status
    } for a in pending]), 200

@admin_bp.route('/verification/<string:artist_id>/status', methods=['PATCH'])
@jwt_required()
def update_verification_status(artist_id):
    err = _require_admin()
    if err: return err

    artist = ArtistProfile.query.get(artist_id)
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404

    data = request.get_json()
    status = data.get('status')
    if status not in ('approved', 'rejected'):
        return jsonify({'error': 'Invalid status'}), 400

    artist.verification_status = status
    if status == 'rejected':
        artist.rejection_reason = data.get('rejection_reason')
    elif status == 'approved':
        artist.verified_at = datetime.now(timezone.utc)
        artist.rejection_reason = None

    db.session.commit()
    return jsonify({'message': f'Artist {status} successfully'}), 200

@admin_bp.route('/artists', methods=['GET'])
@jwt_required()
def list_artists():
    err = _require_admin()
    if err: return err

    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    artists = ArtistProfile.query.order_by(ArtistProfile.created_at.desc()).offset(offset).limit(limit).all()
    total = ArtistProfile.query.count()

    return jsonify({
        'artists': [{
            'id': a.id,
            'user_id': a.user_id,
            'name': a.full_name,
            'brand': a.brand_name,
            'email': a.user.email if a.user else '',
            'verified': a.verification_status == 'approved',
            'status': a.verification_status,
            'is_suspended': a.user.is_suspended if a.user else False,
            'joined': a.created_at.isoformat()
        } for a in artists],
        'total': total
    }), 200

@admin_bp.route('/buyers', methods=['GET'])
@jwt_required()
def list_buyers():
    err = _require_admin()
    if err: return err

    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    buyers = BuyerProfile.query.order_by(BuyerProfile.created_at.desc()).offset(offset).limit(limit).all()
    total = BuyerProfile.query.count()

    return jsonify({
        'buyers': [{
            'id': b.id,
            'user_id': b.user_id,
            'name': b.full_name,
            'email': b.user.email if b.user else '',
            'is_suspended': b.user.is_suspended if b.user else False,
            'joined': b.created_at.isoformat(),
            'orders': b.orders.count()
        } for b in buyers],
        'total': total
    }), 200

@admin_bp.route('/users/<string:user_id>/toggle-suspend', methods=['POST'])
@jwt_required()
def toggle_suspend(user_id):
    err = _require_admin()
    if err: return err

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.is_suspended = not user.is_suspended
    db.session.commit()
    
    return jsonify({
        'message': f'User {"suspended" if user.is_suspended else "unsuspended"}',
        'is_suspended': user.is_suspended
    }), 200
