from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_current_profile():
    raw_identity = get_jwt_identity()
    try:
        identity = json.loads(raw_identity) if isinstance(raw_identity, str) else raw_identity
    except (json.JSONDecodeError, TypeError):
        identity = raw_identity

    user = db.session.get(User, identity['id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    profile_data = {}
    if user.role == 'buyer' and user.buyer_profile:
        profile_data = user.buyer_profile.to_dict()
    elif user.role == 'artist' and user.artist_profile:
        profile_data = user.artist_profile.to_dict()
    
    # Merge profile data with user basic info for a flat response
    response_data = profile_data.copy()
    response_data.update({
        'user_id': user.id,
        'email': user.email,
        'role': user.role
    })
    
    return jsonify(response_data), 200

@auth_bp.route('/profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    raw_identity = get_jwt_identity()
    try:
        identity = json.loads(raw_identity) if isinstance(raw_identity, str) else raw_identity
    except (json.JSONDecodeError, TypeError):
        identity = raw_identity

    user = db.session.get(User, identity['id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update Buyer Profile
    if user.role == 'buyer' and user.buyer_profile:
        if 'full_name' in data:
            user.buyer_profile.full_name = data['full_name']
        if 'phone' in data:
            user.buyer_profile.phone = data['phone']
            
    # Update Artist Profile
    elif user.role == 'artist' and user.artist_profile:
        if 'full_name' in data:
            user.artist_profile.full_name = data['full_name']
        if 'brand_name' in data:
            user.artist_profile.brand_name = data['brand_name']
        if 'location' in data:
            user.artist_profile.location = data['location']
        if 'bio' in data:
            user.artist_profile.bio = data['bio']

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
