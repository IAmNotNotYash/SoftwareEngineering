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
    
    # If no real trend data, return empty list
    if not trends:
        return jsonify([]), 200
        
    return jsonify([t.to_dict() for t in trends]), 200

@analytics_bp.route('/platform/trend', methods=['GET'])
@jwt_required()
def get_platform_trend():
    identity = _get_identity()
    if identity['role'] != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    
    trends = PlatformRevenueTrend.query.order_by(PlatformRevenueTrend.month.asc()).all()
    
    if not trends:
        return jsonify([]), 200
        
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
        # Return empty snapshot
        return jsonify({
            'ai_summary': "No performance narrative available yet. Start launching catalogues to get insights.",
            'sentiment_summary': "No buyer sentiment data available yet."
        }), 200
        
    return jsonify(snapshot.to_dict()), 200
