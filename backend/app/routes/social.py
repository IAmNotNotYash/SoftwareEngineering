from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app import db
from app.models.social import Follow, Post, Review
from app.models.user import ArtistProfile, BuyerProfile
from app.models.commerce import Product
from app.models.catalogue import Catalogue

social_bp = Blueprint('social', __name__)

import json

def _get_identity():
    id_str = get_jwt_identity()
    try:
        return json.loads(id_str) if isinstance(id_str, str) else id_str
    except (json.JSONDecodeError, TypeError):
        return id_str

# ── FOLLOWS ──────────────────────────────────────────────────────────────────

@social_bp.route('/follows', methods=['POST'])
@jwt_required()
def follow_artist():
    identity = _get_identity()
    if identity['role'] != 'buyer':
        return jsonify({'error': 'Only buyers can follow artists'}), 403
    
    buyer = BuyerProfile.query.filter_by(user_id=identity['id']).first()
    data = request.get_json()
    artist_id = data.get('artist_id')
    
    if not artist_id:
        return jsonify({'error': 'artist_id is required'}), 400
    
    existing = Follow.query.filter_by(buyer_id=buyer.id, artist_id=artist_id).first()
    if existing:
        return jsonify({'message': 'Already following'}), 200
        
    follow = Follow(buyer_id=buyer.id, artist_id=artist_id)
    db.session.add(follow)
    db.session.commit()
    return jsonify({'message': 'Followed successfully'}), 201

@social_bp.route('/follows/<string:artist_id>', methods=['DELETE'])
@jwt_required()
def unfollow_artist(artist_id):
    identity = _get_identity()
    buyer = BuyerProfile.query.filter_by(user_id=identity['id']).first()
    
    follow = Follow.query.filter_by(buyer_id=buyer.id, artist_id=artist_id).first()
    if not follow:
        return jsonify({'error': 'Not following this artist'}), 404
        
    db.session.delete(follow)
    db.session.commit()
    return jsonify({'message': 'Unfollowed successfully'}), 200

@social_bp.route('/follows/check/<string:artist_id>', methods=['GET'])
@jwt_required()
def check_follow(artist_id):
    identity = _get_identity()
    buyer = BuyerProfile.query.filter_by(user_id=identity['id']).first()
    if not buyer: return jsonify({'is_following': False}), 200
    
    follow = Follow.query.filter_by(buyer_id=buyer.id, artist_id=artist_id).first()
    return jsonify({'is_following': follow is not None}), 200

# ── POSTS (STORIES & INSIGHTS) ────────────────────────────────────────────────

@social_bp.route('/posts', methods=['GET'])
def list_posts():
    post_type = request.args.get('type') # 'story' or 'insight'
    artist_id = request.args.get('artist_id')
    
    query = Post.query.filter_by(is_published=True)
    if post_type:
        query = query.filter_by(type=post_type)
    if artist_id:
        query = query.filter_by(artist_id=artist_id)
        
    posts = query.order_by(Post.published_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200

@social_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    identity = _get_identity()
    if identity['role'] != 'artist':
        return jsonify({'error': 'Only artists can create posts'}), 403
    
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    data = request.get_json()
    
    post = Post(
        artist_id=artist.id,
        type=data.get('type', 'story'),
        title=data.get('title'),
        body=data.get('body'),
        cover_image_url=data.get('cover_image_url'),
        is_published=data.get('is_published', False)
    )
    if post.is_published:
        post.published_at = datetime.now(timezone.utc)
        
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

# ── REVIEWS ──────────────────────────────────────────────────────────────────

@social_bp.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    identity = _get_identity()
    if identity['role'] != 'buyer':
        return jsonify({'error': 'Only buyers can leave reviews'}), 403
    
    buyer = BuyerProfile.query.filter_by(user_id=identity['id']).first()
    data = request.get_json()
    
    review = Review(
        buyer_id=buyer.id,
        target_type=data.get('target_type'), # 'product' or 'catalogue'
        target_id=data.get('target_id'),
        rating=data.get('rating'),
        body=data.get('body')
    )
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201

@social_bp.route('/reviews/<string:target_type>/<string:target_id>', methods=['GET'])
def list_reviews(target_type, target_id):
    reviews = Review.query.filter_by(target_type=target_type, target_id=target_id, is_deleted=False).all()
    return jsonify([r.to_dict() for r in reviews]), 200
