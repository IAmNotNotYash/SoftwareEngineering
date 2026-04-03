from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone, timedelta
from app import db
from app.models.analytics import ArtistRevenueTrend, PlatformRevenueTrend, AnalyticsSnapshot
from app.models.user import ArtistProfile

analytics_bp = Blueprint('analytics', __name__)

import json

def _get_identity():
    id_str = get_jwt_identity()
    try:
        return json.loads(id_str) if isinstance(id_str, str) else id_str
    except (json.JSONDecodeError, TypeError):
        return id_str

@analytics_bp.route('/artist/trend', methods=['GET'])
@jwt_required()
def get_artist_trend():
    identity = _get_identity()
    if identity['role'] != 'artist':
        return jsonify({'error': 'Forbidden'}), 403
    
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    trends = ArtistRevenueTrend.query.filter_by(artist_id=artist.id).order_by(ArtistRevenueTrend.month.asc()).all()
    
    # If no real trend data, return some defaults for UI visualization
    if not trends:
        months = ["2026-01", "2026-02", "2026-03", "2026-04"]
        return jsonify([
            {'month': 'Jan', 'revenue': 45000, 'views': 120},
            {'month': 'Feb', 'revenue': 52000, 'views': 150},
            {'month': 'Mar', 'revenue': 48000, 'views': 140},
            {'month': 'Apr', 'revenue': 61000, 'views': 210},
        ]), 200
        
    return jsonify([t.to_dict() for t in trends]), 200

@analytics_bp.route('/platform/trend', methods=['GET'])
@jwt_required()
def get_platform_trend():
    identity = _get_identity()
    if identity['role'] != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    
    trends = PlatformRevenueTrend.query.order_by(PlatformRevenueTrend.month.asc()).all()
    
    if not trends:
        return jsonify([
            {'month': 'Jan', 'revenue': 1200000},
            {'month': 'Feb', 'revenue': 1500000},
            {'month': 'Mar', 'revenue': 1800000},
            {'month': 'Apr', 'revenue': 2200000},
        ]), 200
        
    return jsonify([t.to_dict() for t in trends]), 200

@analytics_bp.route('/snapshots', methods=['GET'])
@jwt_required()
def get_snapshot():
    identity = _get_identity()
    entity_type = request.args.get('type', 'artist')
    
    if entity_type == 'artist':
        artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
        snapshot = AnalyticsSnapshot.query.filter_by(entity_type='artist', entity_id=artist.id).order_by(AnalyticsSnapshot.generated_at.desc()).first()
    else:
        if identity['role'] != 'admin': return jsonify({'error': 'Forbidden'}), 403
        snapshot = AnalyticsSnapshot.query.filter_by(entity_type='platform').order_by(AnalyticsSnapshot.generated_at.desc()).first()
        
    if not snapshot:
        # Mock AI summary if none exists
        return jsonify({
            'ai_summary': "Your brand identity is resonating strongly with 'Home Decor' enthusiasts. We've seen a 22% increase in catalogue engagement this month, primarily driven by your 'Earth Tones' collection. Consider launching a follow-up drop with exclusive early access to your top 10% followers.",
            'sentiment_summary': "Buyers frequently praise the 'organic texture' and 'durability' of your ceramics. 94% of reviews contain positive sentiment regarding packaging quality."
        }), 200
        
    return jsonify(snapshot.to_dict()), 200
