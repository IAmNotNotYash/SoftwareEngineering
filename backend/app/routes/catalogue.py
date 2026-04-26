from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
import os
import uuid
from werkzeug.utils import secure_filename

from app import db
from app.models.catalogue import Catalogue, CatalogueProduct, CatalogueStats, CatalogueView, CatalogueLike
from app.models.user import ArtistProfile, BuyerProfile
from app.models.social import Follow

catalogue_bp = Blueprint('catalogue', __name__)


# ── ARTIST: Get Unique Categories ─────────────────────────────────────────────
@catalogue_bp.route('/categories', methods=['GET'])
def get_unique_categories():
    # Fetch all unique non-null categories from the database
    all_cats = db.session.query(Catalogue.category).filter(Catalogue.category != None).all()
    
    unique_cats = set()
    for (cat_str,) in all_cats:
        if cat_str:
            # Support comma-separated categories in the string
            parts = [c.strip() for c in cat_str.split(',') if c.strip()]
            for p in parts:
                unique_cats.add(p)
    
    return jsonify(sorted(list(unique_cats))), 200



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
    
    # Self-healing: ensure stats record exists
    if not catalogue.stats:
        stats = CatalogueStats(catalogue_id=catalogue.id, total_views=1)
        db.session.add(stats)
    else:
        catalogue.stats.total_views += 1
        catalogue.stats.last_updated = datetime.now(timezone.utc)
        
    db.session.commit()


# ── ARTIST: Upload Catalogue Cover ───────────────────────────────────────────
@catalogue_bp.route('/<string:catalogue_id>/upload-cover', methods=['POST', 'OPTIONS'])
def upload_cover(catalogue_id):
    if request.method == 'OPTIONS':
        return '', 204
    
    from flask_jwt_extended import verify_jwt_in_request
    verify_jwt_in_request()
    
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err: return err

    catalogue = db.session.get(Catalogue, catalogue_id)
    if not catalogue:
        return jsonify({'error': 'Catalogue not found'}), 404

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        filename = f"catalogue_{catalogue_id}.{ext}"
        
        storage_path = os.path.join(current_app.root_path, 'static', 'catalogues_visuals')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path, exist_ok=True)
            
        file_path = os.path.join(storage_path, filename)
        public_url = f"/static/catalogues_visuals/{filename}"
        full_url = f"{request.host_url.rstrip('/')}{public_url}"
        
        try:
            file.save(file_path)
            catalogue.cover_photo_url = public_url
            db.session.commit()
            return jsonify({'url': full_url}), 200
        except Exception as e:
            current_app.logger.error(f"Failed to save catalogue cover: {str(e)}")
            return jsonify({'error': f"FileSystem error: {str(e)}"}), 500


# ── ARTIST: Upload Story frame ───────────────────────────────────────────────
@catalogue_bp.route('/<string:catalogue_id>/upload-story', methods=['POST', 'OPTIONS'])
def upload_story(catalogue_id):
    if request.method == 'OPTIONS':
        return '', 204
    
    from flask_jwt_extended import verify_jwt_in_request
    verify_jwt_in_request()
    
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err: return err

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file:
        # Use random name for uniqueness
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        filename = f"story_{catalogue_id}_{uuid.uuid4().hex[:8]}.{ext}"
        
        storage_path = os.path.join(current_app.root_path, 'static', 'catalogues_stories')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path, exist_ok=True)
            
        file_path = os.path.join(storage_path, filename)
        public_url = f"/static/catalogues_stories/{filename}"
        full_url = f"{request.host_url.rstrip('/')}{public_url}"
        
        try:
            file.save(file_path)
            return jsonify({'url': full_url}), 200
        except Exception as e:
            current_app.logger.error(f"Failed to save story frame: {str(e)}")
            return jsonify({'error': f"FileSystem error: {str(e)}"}), 500


# ── PUBLIC: Browse live catalogues ────────────────────────────────────────────
@catalogue_bp.route('', methods=['GET'])
def list_catalogues():
    status_filter = request.args.get('status', 'live')
    artist_id = request.args.get('artist_id', '')
    user_id = request.args.get('user_id', '')
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    
    current_app.logger.info(f"DEBUG Catalogues: status={status_filter}, artist_id={artist_id}, user_id={user_id}, search={search}, category={category}")

    q = Catalogue.query
    if status_filter:
        q = q.filter_by(status=status_filter)
    
    if user_id:
        artist = _artist_profile(user_id)
        if artist:
            current_app.logger.info(f"DEBUG Catalogues: Found artist profile {artist.id} for user {user_id}")
            q = q.filter_by(artist_id=artist.id)
        else:
            current_app.logger.info(f"DEBUG Catalogues: NO artist profile found for user {user_id}")
            # If no artist profile, return empty
            return jsonify({'catalogues': []}), 200
            
    if artist_id:
        q = q.filter_by(artist_id=artist_id)
    if search:
        q = q.filter(Catalogue.title.ilike(f'%{search}%'))
    if category:
        q = q.filter(Catalogue.category.ilike(f'%{category}%'))

    catalogues = q.order_by(Catalogue.published_at.desc()).all()
    current_app.logger.info(f"DEBUG Catalogues: Returning {len(catalogues)} catalogues")
    return jsonify({'catalogues': [c.to_dict() for c in catalogues]}), 200


# ── BUYER: Personalized Feed ──────────────────────────────────────────────────
@catalogue_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_catalogue_feed():
    identity = _get_identity()
    if identity.get('role') != 'buyer':
        # Default to all live catalogues if not a buyer or just for simplicity
        catalogues = Catalogue.query.filter_by(status='live').order_by(Catalogue.published_at.desc()).limit(10).all()
        return jsonify([c.to_dict() for c in catalogues]), 200
    
    buyer = _buyer_profile(identity['id'])
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404
    
    followed_artists = Follow.query.filter_by(buyer_id=buyer.id).all()
    artist_ids = [f.artist_id for f in followed_artists]
    
    if not artist_ids:
        # If not following anyone, return recent
        catalogues = Catalogue.query.filter_by(status='live').order_by(Catalogue.published_at.desc()).limit(3).all()
        return jsonify([c.to_dict() for c in catalogues]), 200
        
    catalogues = Catalogue.query.filter(
        Catalogue.artist_id.in_(artist_ids),
        Catalogue.status == 'live'
    ).order_by(Catalogue.published_at.desc()).limit(10).all()
    
    # NEW: Fallback if followed artists have no live catalogues
    if not catalogues:
        catalogues = Catalogue.query.filter_by(status='live').order_by(Catalogue.published_at.desc()).limit(3).all()
    
    return jsonify([c.to_dict() for c in catalogues]), 200


# ── PUBLIC: Get single catalogue (records a view) ─────────────────────────────
@catalogue_bp.route('/<catalogue_id>', methods=['GET'])
def get_catalogue(catalogue_id):
    catalogue = db.session.get(Catalogue, catalogue_id)
    if not catalogue:
        return jsonify({'error': 'Catalogue not found'}), 404

    for_artist = False
    buyer_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        identity = _get_identity() # Uses my helper
        if identity:
            if identity.get('role') == 'artist':
                artist = _artist_profile(identity['id'])
                if artist and catalogue.artist_id == artist.id:
                    for_artist = True
            elif identity.get('role') == 'buyer':
                bp = _buyer_profile(identity['id'])
                buyer_id = bp.id if bp else None
    except Exception:
        pass

    _bump_views(catalogue, buyer_id)
    return jsonify(catalogue.to_dict(include_products=True, include_stories=True, for_artist=for_artist)), 200


# ── ARTIST: Create a new catalogue ───────────────────────────────────────────
@catalogue_bp.route('', methods=['POST'])
@jwt_required()
def create_catalogue():
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err: return err

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
        category=data.get('category')
    )

    if catalogue.status == 'live':
        catalogue.published_at = datetime.now(timezone.utc)

    db.session.add(catalogue)
    db.session.flush()

    stats = CatalogueStats(catalogue_id=catalogue.id)
    db.session.add(stats)

    product_ids = data.get('product_ids', [])
    if product_ids:
        from app.models.commerce import Product
        for pid in product_ids:
            prod = db.session.get(Product, pid)
            if prod and prod.artist_id == artist.id:
                prod.catalogue_id = catalogue.id

    db.session.commit()
    return jsonify(catalogue.to_dict(include_products=True)), 201


# ── ARTIST: Update catalogue ──────────────────────────────────────────────────
@catalogue_bp.route('/<catalogue_id>', methods=['PATCH'])
@jwt_required()
def update_catalogue(catalogue_id):
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err: return err

    artist = _artist_profile(identity['id'])
    catalogue = db.session.get(Catalogue, catalogue_id)
    if not catalogue or catalogue.artist_id != artist.id:
        return jsonify({'error': 'Catalogue not found or access denied'}), 404

    data = request.get_json() or {}
    EDITABLE = ['title', 'narrative', 'cover_photo_url', 'theme', 'launch_intent',
                'philosophy', 'artist_note', 'category']
    for field in EDITABLE:
        if field in data:
            setattr(catalogue, field, data[field])

    if 'status' in data:
        new_status = data['status']
        catalogue.status = new_status
        if new_status == 'live' and not catalogue.published_at:
            catalogue.published_at = datetime.now(timezone.utc)

    if 'product_ids' in data:
        from app.models.commerce import Product
        # Unlink products that belong to this catalogue but are not in the new list
        current_products = Product.query.filter_by(catalogue_id=catalogue.id).all()
        for p in current_products:
            if p.id not in data['product_ids']:
                p.catalogue_id = None
        
        # Link products in the list
        for pid in data['product_ids']:
            prod = db.session.get(Product, pid)
            if prod and prod.artist_id == artist.id:
                prod.catalogue_id = catalogue.id

    db.session.commit()
    return jsonify(catalogue.to_dict(include_products=True)), 200


# ── ARTIST: Delete (end) catalogue ───────────────────────────────────────────
@catalogue_bp.route('/<catalogue_id>', methods=['DELETE'])
@jwt_required()
def delete_catalogue(catalogue_id):
    identity = _get_identity()
    err = _require_role(identity, 'artist', 'admin')
    if err: return err

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
@catalogue_bp.route('/<catalogue_id>/like', methods=['POST'])
@jwt_required()
def like_catalogue(catalogue_id):
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err: return err

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

        if catalogue.stats:
            catalogue.stats.total_likes += 1
            catalogue.stats.last_updated = datetime.now(timezone.utc)

        db.session.commit()
        return jsonify({'message': 'Liked', 'liked': True}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Already liked'}), 409


# ── BUYER: Unlike a catalogue ─────────────────────────────────────────────────
@catalogue_bp.route('/<catalogue_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_catalogue(catalogue_id):
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err: return err

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
