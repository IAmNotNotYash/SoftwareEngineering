from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app import db
from app.models.communication import Broadcast
from app.models.user import ArtistProfile, BuyerProfile
from app.models.social import Follow

communication_bp = Blueprint('communication', __name__)

import json

def _get_identity():
    id_str = get_jwt_identity()
    try:
        return json.loads(id_str) if isinstance(id_str, str) else id_str
    except (json.JSONDecodeError, TypeError):
        return id_str

@communication_bp.route('/broadcasts', methods=['GET'])
@jwt_required()
def list_broadcasts():
    identity = _get_identity()
    if identity['role'] != 'artist':
        return jsonify({'error': 'Only artists can view their broadcasts'}), 403
    
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    broadcasts = Broadcast.query.filter_by(artist_id=artist.id).order_by(Broadcast.created_at.desc()).all()
    return jsonify([b.to_dict() for b in broadcasts]), 200

@communication_bp.route('/broadcasts', methods=['POST'])
@jwt_required()
def send_broadcast():
    identity = _get_identity()
    if identity['role'] != 'artist':
        return jsonify({'error': 'Only artists can send broadcasts'}), 403
    
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    data = request.get_json()
    
    # In a real app, this would queue emails/SMS etc.
    # For now, we record it and mark it as 'sent' immediately.
    broadcast = Broadcast(
        artist_id=artist.id,
        catalogue_id=data.get('catalogue_id'),
        message=data.get('message'),
        intent=data.get('intent'),
        platforms=data.get('platforms', []),
        status='sent',
        sent_at=datetime.now(timezone.utc)
    )
    
    db.session.add(broadcast)
    db.session.commit()
    return jsonify(broadcast.to_dict()), 201

@communication_bp.route('/audience-size', methods=['GET'])
@jwt_required()
def get_audience_size():
    identity = _get_identity()
    if identity['role'] != 'artist':
        return jsonify({'error': 'Forbidden'}), 403
    
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    count = Follow.query.filter_by(artist_id=artist.id).count()
    return jsonify({'count': count}), 200
