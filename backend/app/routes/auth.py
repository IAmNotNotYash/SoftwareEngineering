from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import json
from app import db
from app.models.user import User, BuyerProfile, ArtistProfile

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    first_name = data.get('firstName')
    last_name = data.get('lastName')

    if not email or not password or not role or not first_name or not last_name:
        return jsonify({'error': 'Missing required fields'}), 400

    if role not in ['buyer', 'artist']:
        return jsonify({'error': 'Invalid role'}), 400

    # Check if user exists
    if db.session.query(User).filter_by(email=email).first():
        return jsonify({'error': 'Email is already registered'}), 400

    user = User(email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.flush() # so that user gets an ID for profile creation

    full_name = f"{first_name} {last_name}".strip()

    if role == 'buyer':
        buyer_profile = BuyerProfile(user_id=user.id, full_name=full_name)
        db.session.add(buyer_profile)
    elif role == 'artist':
        brand_name = data.get('brandName')
        if not brand_name:
            # Need to rollback so the user isn't halfway created
            db.session.rollback()
            return jsonify({'error': 'Brand name is required for artists'}), 400
        artist_profile = ArtistProfile(
            user_id=user.id,
            full_name=full_name,
            brand_name=brand_name
        )
        db.session.add(artist_profile)

    db.session.commit()

    access_token = create_access_token(identity=json.dumps({'id': user.id, 'role': user.role, 'email': user.email}))
    return jsonify({
        'message': 'Account created successfully',
        'token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'name': full_name
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400
        
    email = data.get('email')
    password = data.get('password')

    user = db.session.query(User).filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if user.is_suspended:
        return jsonify({'error': 'Your account has been suspended by an administrator'}), 403

    if user.role == 'artist' and user.artist_profile.verification_status == 'rejected':
        reason = user.artist_profile.rejection_reason or "No reason provided."
        return jsonify({
            'error': f'Your account verification was rejected. Reason: {reason}'
        }), 403

    access_token = create_access_token(identity=json.dumps({'id': user.id, 'role': user.role, 'email': user.email}))
    
    name = "Platform Admin"
    brand_name = None
    
    if user.role == 'buyer' and user.buyer_profile:
        name = user.buyer_profile.full_name
    elif user.role == 'artist' and user.artist_profile:
        name = user.artist_profile.full_name
        brand_name = user.artist_profile.brand_name
        
    return jsonify({
        'message': 'Logged in successfully',
        'token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'name': name,
            'brandName': brand_name
        }
    }), 200
