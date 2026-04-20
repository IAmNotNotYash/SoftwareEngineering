from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app import db
from app.models.social import Follow, Post, Review, PostLike
from app.models.user import ArtistProfile, BuyerProfile
from app.models.commerce import Product
from app.models.catalogue import Catalogue
from app.utils.ai_summary import generate_review_summary

social_bp = Blueprint('social', __name__)
import os
import uuid
from flask import current_app


import json

def _get_identity():
    id_str = get_jwt_identity()
    try:
        return json.loads(id_str) if isinstance(id_str, str) else id_str
    except (json.JSONDecodeError, TypeError):
        return id_str

@social_bp.route('/upload-image', methods=['POST', 'OPTIONS'])
def upload_image():
    if request.method == 'OPTIONS':
        return '', 204
        
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        filename = f"post_{uuid.uuid4().hex[:12]}.{ext}"
        
        storage_path = os.path.join(current_app.root_path, 'static', 'post_image')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path, exist_ok=True)
            
        file_path = os.path.join(storage_path, filename)
        public_url = f"/static/post_image/{filename}"
        
        try:
            file.save(file_path)
            return jsonify({'url': f"{request.host_url.rstrip('/')}{public_url}"}), 200
        except Exception as e:
            return jsonify({'error': f"FileSystem error: {str(e)}"}), 500
    
    return jsonify({'error': 'Upload failed'}), 500

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

@social_bp.route('/following', methods=['GET'])
@jwt_required()
def list_following():
    identity = _get_identity()
    if identity['role'] != 'buyer':
        return jsonify({'error': 'Only buyers have a following list'}), 403
    
    buyer = BuyerProfile.query.filter_by(user_id=identity['id']).first()
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404
        
    follows = Follow.query.filter_by(buyer_id=buyer.id).all()
    artists = [f.artist.to_dict() for f in follows if f.artist]
    return jsonify(artists), 200

@social_bp.route('/followers', methods=['GET'])
@jwt_required()
def list_followers():
    identity = _get_identity()
    if identity['role'] != 'artist':
        return jsonify({'error': 'Only artists can view their followers'}), 403
    
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    if not artist:
        return jsonify({'error': 'Artist profile not found'}), 404
        
    follows = Follow.query.filter_by(artist_id=artist.id).all()
    # Return buyer info for each follower
    followers = []
    for f in follows:
        if f.buyer:
            followers.append({
                'id': f.buyer_id,
                'name': f.buyer.full_name,
                'joined': f.created_at.strftime('%Y-%m-%d'),
                'type': 'Follower', # Placeholder for tiers
                'orders': 0, # Placeholder
                'value': '₹0' # Placeholder
            })
    return jsonify(followers), 200

# ── POSTS (STORIES & INSIGHTS) ────────────────────────────────────────────────

@social_bp.route('/posts', methods=['GET'])
@jwt_required(optional=True)
def list_posts():
    post_type = request.args.get('type') # 'story' or 'insight'
    artist_id = request.args.get('artist_id')
    catalogue_id = request.args.get('catalogue_id')
    
    # Determine if we should show unpublished posts
    show_unpublished = False
    identity = _get_identity()
    if identity and identity['role'] == 'artist':
        artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
        if artist and (not artist_id or artist_id == artist.id):
            show_unpublished = True

    if show_unpublished:
        query = Post.query
    else:
        query = Post.query.filter_by(is_published=True)

    if post_type:
        query = query.filter_by(type=post_type)
    if artist_id:
        query = query.filter_by(artist_id=artist_id)
    if catalogue_id:
        query = query.filter_by(catalogue_id=catalogue_id)
        
    posts = query.order_by(Post.published_at.desc()).all()
    
    # Check likes if user is logged in
    identity = _get_identity()
    buyer = None
    if identity and identity.get('role') == 'buyer':
        buyer = BuyerProfile.query.filter_by(user_id=identity['id']).first()
    
    results = []
    for p in posts:
        d = p.to_dict()
        if buyer:
            liked = PostLike.query.filter_by(post_id=p.id, buyer_id=buyer.id).first()
            d['has_liked'] = liked is not None
        else:
            d['has_liked'] = False
        results.append(d)
        
    return jsonify(results), 200

@social_bp.route('/posts/<string:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    identity = _get_identity()
    if identity['role'] != 'buyer':
        return jsonify({'error': 'Only buyers can like posts'}), 403
    
    buyer = BuyerProfile.query.filter_by(user_id=identity['id']).first()
    post = Post.query.get_or_404(post_id)
    
    existing = PostLike.query.filter_by(post_id=post_id, buyer_id=buyer.id).first()
    if existing:
        return jsonify({'message': 'Already liked'}), 200
        
    like = PostLike(post_id=post_id, buyer_id=buyer.id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Liked successfully'}), 201

@social_bp.route('/posts/<string:post_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    identity = _get_identity()
    buyer = BuyerProfile.query.filter_by(user_id=identity['id']).first()
    
    like = PostLike.query.filter_by(post_id=post_id, buyer_id=buyer.id).first()
    if not like:
        return jsonify({'error': 'Not liked yet'}), 404
        
    db.session.delete(like)
    db.session.commit()
    return jsonify({'message': 'Unliked successfully'}), 200

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
        catalogue_id=data.get('catalogue_id'),
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

@social_bp.route('/posts/<string:post_id>', methods=['PATCH'])
@jwt_required()
def update_post(post_id):
    identity = _get_identity()
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    
    post = Post.query.get_or_404(post_id)
    if post.artist_id != artist.id:
        return jsonify({'error': 'Acess denied'}), 403
        
    data = request.get_json()
    if 'title' in data: post.title = data['title']
    if 'body' in data: post.body = data['body']
    if 'cover_image_url' in data: post.cover_image_url = data['cover_image_url']
    if 'is_published' in data:
        was_published = post.is_published
        post.is_published = data['is_published']
        if post.is_published and not was_published:
            post.published_at = datetime.now(timezone.utc)
            
    db.session.commit()
    return jsonify(post.to_dict()), 200

@social_bp.route('/posts/<string:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    identity = _get_identity()
    artist = ArtistProfile.query.filter_by(user_id=identity['id']).first()
    
    post = Post.query.get_or_404(post_id)
    if post.artist_id != artist.id:
        return jsonify({'error': 'Access denied'}), 403
        
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200

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


@social_bp.route('/reviews/<string:target_type>/<string:target_id>/summary', methods=['GET'])
def get_review_summary(target_type, target_id):
    if target_type not in ('product', 'catalogue'):
        return jsonify({'error': "target_type must be 'product' or 'catalogue'"}), 400

    if target_type == 'product':
        target = Product.query.filter_by(id=target_id, is_deleted=False).first()
    else:
        target = Catalogue.query.filter_by(id=target_id).first()

    if not target:
        return jsonify({'error': f'{target_type.capitalize()} not found'}), 404

    reviews = (
        Review.query.filter_by(target_type=target_type, target_id=target_id, is_deleted=False)
        .order_by(Review.created_at.desc())
        .limit(50)
        .all()
    )
    review_texts = [r.body for r in reviews if r.body and r.body.strip()]
    ratings = [r.rating for r in reviews if r.rating is not None]

    avg_rating = (sum(ratings) / len(ratings)) if ratings else None
    metrics = {
        'target_type': target_type,
        'target_id': target_id,
        'review_count': len(reviews),
        'avg_rating': round(avg_rating, 2) if avg_rating is not None else None,
        'rating_breakdown': {
            '5': sum(1 for r in ratings if r == 5),
            '4': sum(1 for r in ratings if r == 4),
            '3': sum(1 for r in ratings if r == 3),
            '2': sum(1 for r in ratings if r == 2),
            '1': sum(1 for r in ratings if r == 1),
        }
    }

    provider = (current_app.config.get('AI_PROVIDER', 'groq') or 'groq').lower()
    if provider == 'groq':
        api_key = current_app.config.get('GROQ_API_KEY')
        model = current_app.config.get('GROQ_MODEL', 'llama-3.1-8b-instant')
    else:
        provider = 'gemini'
        api_key = current_app.config.get('GEMINI_API_KEY')
        model = current_app.config.get('GEMINI_MODEL', 'gemini-2.0-flash')

    summary = generate_review_summary(
        metrics=metrics,
        review_texts=review_texts,
        target_label=target_type,
        provider=provider,
        api_key=api_key,
        model=model,
    )

    return jsonify({
        'target_type': target_type,
        'target_id': target_id,
        'review_count': metrics['review_count'],
        'avg_rating': metrics['avg_rating'],
        'summary': summary,
        'generated_at': datetime.now(timezone.utc).isoformat(),
    }), 200
