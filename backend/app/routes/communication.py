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

from flask_mail import Message
from app import db, mail
from threading import Thread

# Helper to send email in a separate thread to avoid blocking the request
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@communication_bp.route('/broadcasts', methods=['POST'])
@jwt_required()
def send_broadcast():
    identity = _get_identity()
    if identity['role'] != 'artist':
        return jsonify({'error': 'Only artists can send broadcasts'}), 403
    
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    data = request.get_json()
    
    # Save broadcast to history
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
    
    # 1. Fetch followers to get their emails
    from app.models.user import User
    followers = Follow.query.filter_by(artist_id=artist.id).all()
    
    if followers and 'email' in data.get('platforms', []):
        recipient_emails = [f.buyer.user.email for f in followers if f.buyer and f.buyer.user]
        
        if recipient_emails:
            from flask import current_app
            app = current_app._get_current_object()
            sender_email = app.config.get('MAIL_DEFAULT_SENDER') or app.config.get('MAIL_USERNAME')
            
            if not sender_email or not app.config.get('MAIL_PASSWORD'):
                print("❌ ERROR: Email configuration is missing! Please check MAIL_USERNAME and MAIL_PASSWORD in your .env file.")
                return jsonify({'error': 'Email service not configured on server'}), 500

            # Prepare Email
            subject = f"Kala Update: {data.get('intent', 'News')} from {artist.brand_name or artist.full_name}"
            # Set sender as: "Brand Name <platform-email@gmail.com>"
            sender = (f"{artist.brand_name or artist.full_name}", sender_email)
            
            # Construct the message body
            body_text = f"Hello from {artist.brand_name or artist.full_name}!\n\n{data.get('message')}\n"
            
            # Add catalogue link if present
            cat_id = data.get('catalogue_id')
            if cat_id:
                body_text += f"\n👉 View the full Catalogue here: http://localhost:5173/buyer/catalogue/{cat_id}\n"
                
            body_text += "\nBest,\nTeam Kala"
            
            msg = Message(subject, sender=sender, recipients=recipient_emails)
            msg.body = body_text
            
            print(f"DEBUG: Processing broadcast from {sender_email} to {len(recipient_emails)} followers...")
            # Send in background thread
            Thread(target=send_async_email, args=(app, msg)).start()

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
