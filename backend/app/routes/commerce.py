"""
Commerce Routes — /api/commerce
=================================
Covers all endpoints for:
  • Products  (public browse + artist management)
  • Cart      (buyer only)
  • Orders    (buyer + artist + admin)
  • Order Tracking Events (artist + admin)

Auth conventions
----------------
- Public endpoints: no JWT required.
- Buyer endpoints: JWT required, role == 'buyer'.
- Artist endpoints: JWT required, role == 'artist'.
- Admin endpoints: JWT required, role == 'admin'.

The helper `_get_identity()` extracts the JWT sub dict that was stored
during login (see auth.py: identity={'id': ..., 'role': ..., 'email': ...}).
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from app import db
from app.models.user import ArtistProfile, BuyerProfile
from app.models.commerce import (
    Product,
    ProductImage,
    CartItem,
    Order,
    OrderItem,
    OrderTrackingEvent,
)
from app.utils.analytics import update_revenue_analytics


commerce_bp = Blueprint('commerce', __name__)

SHIPPING_COST = 500  # flat shipping fee in INR — adjust when real logic is added


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

import json

def _get_identity():
    id_str = get_jwt_identity()
    try:
        return json.loads(id_str) if isinstance(id_str, str) else id_str
    except (json.JSONDecodeError, TypeError):
        return id_str


def _buyer_profile(user_id):
    return BuyerProfile.query.filter_by(user_id=user_id).first()


def _artist_profile(user_id):
    return ArtistProfile.query.filter_by(user_id=user_id).first()


def _require_role(identity, *roles):
    if identity.get('role') not in roles:
        return jsonify({'error': 'Forbidden'}), 403
    return None


# ===========================================================================
# PRODUCTS
# ===========================================================================

# ---------------------------------------------------------------------------
# GET /api/commerce/products
# Public — returns all active (non-deleted) products
# Query params: category, search, artist_id
# ---------------------------------------------------------------------------
@commerce_bp.route('/products', methods=['GET'])
def list_products():
    query = Product.query.filter_by(is_deleted=False)

    category = request.args.get('category')
    search = request.args.get('search')
    artist_id = request.args.get('artist_id')
    user_id = request.args.get('user_id')
    catalogue_id = request.args.get('catalogue_id')

    if category:
        query = query.filter(Product.category.ilike(f'%{category}%'))
    if search:
        query = query.filter(
            db.or_(
                Product.title.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%'),
            )
        )
    if artist_id:
        # artist_id here is the ArtistProfile.id (not user id)
        query = query.filter_by(artist_id=artist_id)
    if user_id:
        from app.models.user import ArtistProfile
        artist = ArtistProfile.query.filter_by(user_id=user_id).first()
        if artist:
            query = query.filter_by(artist_id=artist.id)
        else:
            return jsonify([]), 200
    if catalogue_id:
        query = query.filter_by(catalogue_id=catalogue_id)

    products = query.order_by(Product.created_at.desc()).all()
    return jsonify([p.to_dict() for p in products]), 200


# ---------------------------------------------------------------------------
@commerce_bp.route('/artists', methods=['GET'])
def list_artists():
    artists = ArtistProfile.query.filter_by(verification_status='approved').all()
    return jsonify([{
        'id': a.id,
        'name': a.brand_name,
        'category': a.location or 'Artisan',
        'avatar': a.profile_image_url,
        'followers': 0 # To be replaced with real count (computed from Follow table)
    } for a in artists]), 200


# ---------------------------------------------------------------------------
# GET /api/commerce/artists/<id>
# Public — full artist profile detail
# ---------------------------------------------------------------------------
@commerce_bp.route('/artists/<string:artist_id>', methods=['GET'])
def get_artist(artist_id):
    artist = ArtistProfile.query.filter_by(id=artist_id, verification_status='approved').first()
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404

    # Get live catalogues
    from app.models.catalogue import Catalogue
    catalogues = Catalogue.query.filter_by(artist_id=artist.id, status='live').all()
    
    # Get products
    products = Product.query.filter_by(artist_id=artist.id, is_deleted=False).all()

    return jsonify({
        'id': artist.id,
        'name': artist.brand_name,
        'location': artist.location,
        'bio': artist.bio,
        'avatar': artist.profile_image_url,
        'cover_image_url': artist.cover_image_url,
        'followers': 0, # Placeholder
        'catalogues': [c.to_dict() for c in catalogues],
        'products': [p.to_dict() for p in products]
    }), 200


# ---------------------------------------------------------------------------
# GET /api/commerce/products/<product_id>
# Public — full product detail including image gallery
# ---------------------------------------------------------------------------
@commerce_bp.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = product.to_dict(include_images=True)
    # Also embed artist profile fields the detail page uses
    if product.artist:
        data['artist'] = {
            'id': product.artist.id,
            'name': product.artist.brand_name,
            'avatar': product.artist.profile_image_url,
        }
    return jsonify(data), 200


# ---------------------------------------------------------------------------
# POST /api/commerce/products
# Artist only — create a new product listing
# Body: title, description, materials, dimensions, price, category
# ---------------------------------------------------------------------------
@commerce_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err:
        return err

    artist = _artist_profile(identity['id'])
    if not artist:
        return jsonify({'error': 'Artist profile not found'}), 404
    if artist.verification_status != 'approved':
        return jsonify({'error': 'Your account must be verified before listing products'}), 403

    data = request.get_json()
    title = data.get('title', '').strip()
    price = data.get('price')

    if not title:
        return jsonify({'error': 'title is required'}), 400
    if price is None:
        return jsonify({'error': 'price is required'}), 400

    product = Product(
        artist_id=artist.id,
        title=title,
        description=data.get('description'),
        materials=data.get('materials'),
        dimensions=data.get('dimensions'),
        price=price,
        category=data.get('category'),
        in_stock=data.get('in_stock', True),
        catalogue_id=data.get('catalogue_id')
    )
    db.session.add(product)
    db.session.flush()  # get product.id before adding images

    # Optional: accept initial image URLs in the same request
    for idx, img_data in enumerate(data.get('images', [])):
        image = ProductImage(
            product_id=product.id,
            image_url=img_data.get('image_url') if isinstance(img_data, dict) else img_data,
            is_primary=(idx == 0),
            sort_order=idx,
        )
        db.session.add(image)

    db.session.commit()
    return jsonify(product.to_dict()), 201


# ---------------------------------------------------------------------------
# PATCH /api/commerce/products/<product_id>
# Artist only — update fields of an existing product they own
# ---------------------------------------------------------------------------
@commerce_bp.route('/products/<string:product_id>', methods=['PATCH'])
@jwt_required()
def update_product(product_id):
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err:
        return err

    artist = _artist_profile(identity['id'])
    if not artist:
        return jsonify({'error': 'Artist profile not found'}), 404

    product = Product.query.filter_by(id=product_id, artist_id=artist.id, is_deleted=False).first()
    if not product:
        return jsonify({'error': 'Product not found or not owned by you'}), 404

    data = request.get_json()
    updatable = ['title', 'description', 'materials', 'dimensions', 'price', 'category', 'in_stock', 'catalogue_id']
    for field in updatable:
        if field in data:
            setattr(product, field, data[field])

    db.session.commit()
    return jsonify(product.to_dict()), 200


# ---------------------------------------------------------------------------
# DELETE /api/commerce/products/<product_id>
# Artist only — soft-delete a product
# ---------------------------------------------------------------------------
@commerce_bp.route('/products/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err:
        return err

    artist = _artist_profile(identity['id'])
    if not artist:
        return jsonify({'error': 'Artist profile not found'}), 404

    product = Product.query.filter_by(id=product_id, artist_id=artist.id, is_deleted=False).first()
    if not product:
        return jsonify({'error': 'Product not found or not owned by you'}), 404

    product.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200


# ---------------------------------------------------------------------------
# POST /api/commerce/products/<product_id>/images
# Artist only — add an image to a product
# Body: image_url, is_primary (bool), sort_order (int)
# ---------------------------------------------------------------------------
@commerce_bp.route('/products/<string:product_id>/images', methods=['POST'])
@jwt_required()
def add_product_image(product_id):
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err:
        return err

    artist = _artist_profile(identity['id'])
    if not artist:
        return jsonify({'error': 'Artist profile not found'}), 404

    product = Product.query.filter_by(id=product_id, artist_id=artist.id, is_deleted=False).first()
    if not product:
        return jsonify({'error': 'Product not found or not owned by you'}), 404

    data = request.get_json()
    image_url = data.get('image_url', '').strip()
    if not image_url:
        return jsonify({'error': 'image_url is required'}), 400

    is_primary = data.get('is_primary', False)

    # If new image is primary, demote existing primaries
    if is_primary:
        ProductImage.query.filter_by(product_id=product_id, is_primary=True).update({'is_primary': False})

    existing_count = ProductImage.query.filter_by(product_id=product_id).count()
    image = ProductImage(
        product_id=product_id,
        image_url=image_url,
        is_primary=is_primary,
        sort_order=data.get('sort_order', existing_count),
    )
    db.session.add(image)
    db.session.commit()
    return jsonify(image.to_dict()), 201


# ---------------------------------------------------------------------------
# POST /api/commerce/products/<product_id>/upload-image
# Artist only — upload an actual image file for a product
# ---------------------------------------------------------------------------
@commerce_bp.route('/products/<string:product_id>/upload-image', methods=['POST', 'OPTIONS'])
def upload_product_image_file(product_id):
    if request.method == 'OPTIONS':
        return '', 204
        
    from flask_jwt_extended import verify_jwt_in_request
    verify_jwt_in_request()
    
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err:
        return err

    artist = _artist_profile(identity['id'])
    if not artist:
        return jsonify({'error': 'Artist profile not found'}), 404

    product = Product.query.filter_by(id=product_id, artist_id=artist.id, is_deleted=False).first()
    if not product:
        return jsonify({'error': 'Product not found or not owned by you'}), 404

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        filename = f"product_{product_id}_{uuid.uuid4().hex[:8]}.{ext}"
        
        storage_path = os.path.join(current_app.root_path, 'static', 'product_image')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path, exist_ok=True)
            
        file_path = os.path.join(storage_path, filename)
        public_url = f"/static/product_image/{filename}"
        
        try:
            file.save(file_path)
            
            # Set this new image as primary and demote others
            is_primary = True
            ProductImage.query.filter_by(product_id=product_id, is_primary=True).update({'is_primary': False})
            
            image = ProductImage(
                product_id=product_id,
                image_url=public_url,
                is_primary=is_primary,
                sort_order=0,
            )
            db.session.add(image)
            db.session.commit()
            
            return jsonify({'url': f"{request.host_url.rstrip('/')}{public_url}"}), 200
        except Exception as e:
            current_app.logger.error(f"Failed to save product image: {str(e)}")
            return jsonify({'error': f"FileSystem error: {str(e)}"}), 500
    return jsonify(image.to_dict()), 201


# ---------------------------------------------------------------------------
# DELETE /api/commerce/products/<product_id>/images/<image_id>
# Artist only — remove an image from a product
# ---------------------------------------------------------------------------
@commerce_bp.route('/products/<string:product_id>/images/<string:image_id>', methods=['DELETE'])
@jwt_required()
def delete_product_image(product_id, image_id):
    identity = _get_identity()
    err = _require_role(identity, 'artist')
    if err:
        return err

    artist = _artist_profile(identity['id'])
    if not artist:
        return jsonify({'error': 'Artist profile not found'}), 404

    product = Product.query.filter_by(id=product_id, artist_id=artist.id).first()
    if not product:
        return jsonify({'error': 'Product not found or not owned by you'}), 404

    image = ProductImage.query.filter_by(id=image_id, product_id=product_id).first()
    if not image:
        return jsonify({'error': 'Image not found'}), 404

    db.session.delete(image)
    db.session.commit()
    return jsonify({'message': 'Image deleted'}), 200


# ===========================================================================
# CART
# ===========================================================================

# ---------------------------------------------------------------------------
# GET /api/commerce/cart
# Buyer only — return all items currently in the buyer's cart
# ---------------------------------------------------------------------------
@commerce_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err:
        return err

    buyer = _buyer_profile(identity['id'])
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404

    items = CartItem.query.filter_by(buyer_id=buyer.id).all()
    return jsonify([i.to_dict() for i in items]), 200


# ---------------------------------------------------------------------------
# POST /api/commerce/cart
# Buyer only — add a product to cart (or increment quantity if already present)
# Body: product_id, quantity (default 1)
# ---------------------------------------------------------------------------
@commerce_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err:
        return err

    buyer = _buyer_profile(identity['id'])
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({'error': 'product_id is required'}), 400
    if quantity < 1:
        return jsonify({'error': 'quantity must be at least 1'}), 400

    product = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    if not product.in_stock:
        return jsonify({'error': 'Product is out of stock'}), 400

    existing = CartItem.query.filter_by(buyer_id=buyer.id, product_id=product_id).first()
    if existing:
        existing.quantity += quantity
        db.session.commit()
        return jsonify(existing.to_dict()), 200

    item = CartItem(buyer_id=buyer.id, product_id=product_id, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


# ---------------------------------------------------------------------------
# PATCH /api/commerce/cart/<item_id>
# Buyer only — update quantity of a cart item
# Body: quantity
# ---------------------------------------------------------------------------
@commerce_bp.route('/cart/<string:item_id>', methods=['PATCH'])
@jwt_required()
def update_cart_item(item_id):
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err:
        return err

    buyer = _buyer_profile(identity['id'])
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404

    item = CartItem.query.filter_by(id=item_id, buyer_id=buyer.id).first()
    if not item:
        return jsonify({'error': 'Cart item not found'}), 404

    data = request.get_json()
    quantity = data.get('quantity')
    if quantity is None or int(quantity) < 1:
        return jsonify({'error': 'quantity must be at least 1'}), 400

    item.quantity = int(quantity)
    db.session.commit()
    return jsonify(item.to_dict()), 200


# ---------------------------------------------------------------------------
# DELETE /api/commerce/cart/<item_id>
# Buyer only — remove a specific item from the cart
# ---------------------------------------------------------------------------
@commerce_bp.route('/cart/<string:item_id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(item_id):
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err:
        return err

    buyer = _buyer_profile(identity['id'])
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404

    item = CartItem.query.filter_by(id=item_id, buyer_id=buyer.id).first()
    if not item:
        return jsonify({'error': 'Cart item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 200


# ---------------------------------------------------------------------------
# DELETE /api/commerce/cart
# Buyer only — clear the entire cart
# ---------------------------------------------------------------------------
@commerce_bp.route('/cart', methods=['DELETE'])
@jwt_required()
def clear_cart():
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err:
        return err

    buyer = _buyer_profile(identity['id'])
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404

    CartItem.query.filter_by(buyer_id=buyer.id).delete()
    db.session.commit()
    return jsonify({'message': 'Cart cleared'}), 200


# ===========================================================================
# ORDERS
# ===========================================================================

# ---------------------------------------------------------------------------
# POST /api/commerce/orders
# Buyer only — place an order from the current cart contents
#
# Body: {
#   shipping_address: { label, full_address, city, state, pin_code, country },
#   payment: { method, card_type, last_4, expiry_month, expiry_year }
# }
#
# Business rules:
#   - All cart items must belong to the same artist (single-artist cart).
#   - If the cart spans multiple artists the request is rejected with guidance.
#   - On success: Order + OrderItems + initial OrderTrackingEvent are created,
#     then the buyer's cart is cleared.
# ---------------------------------------------------------------------------
@commerce_bp.route('/orders', methods=['POST'])
@jwt_required()
def place_order():
    identity = _get_identity()
    err = _require_role(identity, 'buyer')
    if err:
        return err

    buyer = _buyer_profile(identity['id'])
    if not buyer:
        return jsonify({'error': 'Buyer profile not found'}), 404

    cart_items = CartItem.query.filter_by(buyer_id=buyer.id).all()
    if not cart_items:
        return jsonify({'error': 'Your cart is empty'}), 400

    # Validate single-artist constraint
    artist_ids = {item.product.artist_id for item in cart_items if item.product}
    if len(artist_ids) != 1:
        return jsonify({
            'error': 'Cart contains products from multiple artists. '
                     'Please checkout one artist at a time.'
        }), 400

    artist_id = artist_ids.pop()

    data = request.get_json() or {}
    shipping_address = data.get('shipping_address')
    payment = data.get('payment')

    if not shipping_address:
        return jsonify({'error': 'shipping_address is required'}), 400
    if not payment:
        return jsonify({'error': 'payment is required'}), 400

    # Calculate totals
    subtotal = sum(
        float(item.product.price) * item.quantity
        for item in cart_items
        if item.product
    )
    total = subtotal + SHIPPING_COST

    order = Order(
        buyer_id=buyer.id,
        artist_id=artist_id,
        subtotal=subtotal,
        shipping_cost=SHIPPING_COST,
        total=total,
        shipping_address_snapshot=shipping_address,
        payment_snapshot=payment,
    )
    db.session.add(order)
    db.session.flush()  # get order.id

    # Create order items (snapshot product details at time of purchase)
    for cart_item in cart_items:
        product = cart_item.product
        if not product:
            continue

        imgs = product.images.all()
        primary = next((i for i in imgs if i.is_primary), None)
        image_url = primary.image_url if primary else (imgs[0].image_url if imgs else None)

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_title_snapshot=product.title,
            product_image_snapshot=image_url,
            artist_name_snapshot=product.artist.brand_name if product.artist else '',
            price_at_purchase=product.price,
            quantity=cart_item.quantity,
        )
        db.session.add(order_item)

    # Log the initial "confirmed" tracking event
    tracking_event = OrderTrackingEvent(
        order_id=order.id,
        event='confirmed',
        note='Order placed successfully.',
    )
    db.session.add(tracking_event)

    # Clear the buyer's cart
    CartItem.query.filter_by(buyer_id=buyer.id).delete()

    db.session.commit()
    return jsonify(order.to_dict(include_items=True, include_tracking=True)), 201


# ---------------------------------------------------------------------------
# GET /api/commerce/orders
# Role-aware list endpoint:
#   - Buyer  → their own order history
#   - Artist → orders received for their products
#   - Admin  → all orders (supports ?status= and ?search= filters)
# ---------------------------------------------------------------------------
@commerce_bp.route('/orders', methods=['GET'])
@jwt_required()
def list_orders():
    identity = _get_identity()
    role = identity.get('role')

    if role == 'buyer':
        buyer = _buyer_profile(identity['id'])
        if not buyer:
            return jsonify({'error': 'Buyer profile not found'}), 404
        orders = (
            Order.query
            .filter_by(buyer_id=buyer.id)
            .order_by(Order.created_at.desc())
            .all()
        )
        return jsonify([o.to_dict(include_items=True) for o in orders]), 200

    elif role == 'artist':
        artist = _artist_profile(identity['id'])
        if not artist:
            return jsonify({'error': 'Artist profile not found'}), 404
        status_filter = request.args.get('status')
        query = Order.query.filter_by(artist_id=artist.id)
        if status_filter:
            query = query.filter_by(status=status_filter)
        orders = query.order_by(Order.created_at.desc()).all()
        return jsonify([o.to_dict(include_items=True) for o in orders]), 200

    elif role == 'admin':
        status_filter = request.args.get('status')
        search = request.args.get('search', '').strip()
        query = Order.query
        if status_filter:
            query = query.filter_by(status=status_filter)
        orders = query.order_by(Order.created_at.desc()).all()

        # Apply search filter post-fetch (search on buyer/artist names)
        if search:
            q = search.lower()
            orders = [
                o for o in orders
                if q in (o.buyer.full_name or '').lower()
                or q in (o.artist.brand_name or '').lower()
                or q in o.display_id.lower()
            ]
        return jsonify([o.to_dict(include_items=True) for o in orders]), 200

    return jsonify({'error': 'Forbidden'}), 403


# ---------------------------------------------------------------------------
# GET /api/commerce/orders/<order_id>
# Role-aware detail endpoint — buyers see own orders, artists see their orders,
# admins see any order.
# ---------------------------------------------------------------------------
@commerce_bp.route('/orders/<string:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    identity = _get_identity()
    role = identity.get('role')

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if role == 'buyer':
        buyer = _buyer_profile(identity['id'])
        if not buyer or order.buyer_id != buyer.id:
            return jsonify({'error': 'Forbidden'}), 403

    elif role == 'artist':
        artist = _artist_profile(identity['id'])
        if not artist or order.artist_id != artist.id:
            return jsonify({'error': 'Forbidden'}), 403

    elif role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    return jsonify(order.to_dict(include_items=True, include_tracking=True)), 200


# ---------------------------------------------------------------------------
# PATCH /api/commerce/orders/<order_id>/status
# Artist or Admin — advance an order to the next status
# Body: { status: 'processing' | 'shipped' | 'delivered' | 'cancelled', note?: str }
#
# Maps each status transition to the corresponding tracking event:
#   pending     → processing  : (no tracking event — internal state)
#   processing  → shipped     : 'dispatched'
#   shipped     → delivered   : 'out_for_delivery' then 'delivered'
#   *           → cancelled   : 'cancelled'
# ---------------------------------------------------------------------------

_STATUS_EVENT_MAP = {
    'processing': None,             # internal; no public tracking event
    'shipped': 'dispatched',
    'delivered': 'delivered',
    'cancelled': 'cancelled',
}

_VALID_TRANSITIONS = {
    'pending': ['processing', 'cancelled'],
    'processing': ['shipped', 'cancelled'],
    'shipped': ['delivered', 'cancelled'],
    'delivered': [],
    'cancelled': [],
}


@commerce_bp.route('/orders/<string:order_id>/status', methods=['PATCH'])
@jwt_required()
def update_order_status(order_id):
    identity = _get_identity()
    role = identity.get('role')

    if role not in ('artist', 'admin'):
        return jsonify({'error': 'Forbidden'}), 403

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Artists may only update orders they received
    if role == 'artist':
        artist = _artist_profile(identity['id'])
        if not artist or order.artist_id != artist.id:
            return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json() or {}
    new_status = data.get('status')
    note = data.get('note')

    if not new_status:
        return jsonify({'error': 'status is required'}), 400

    allowed = _VALID_TRANSITIONS.get(order.status, [])
    if new_status not in allowed:
        return jsonify({
            'error': f"Cannot transition from '{order.status}' to '{new_status}'. "
                     f"Allowed: {allowed}"
        }), 400

    order.status = new_status

    # Log tracking event when applicable
    event_name = _STATUS_EVENT_MAP.get(new_status)
    if event_name:
        event = OrderTrackingEvent(order_id=order.id, event=event_name, note=note)
        db.session.add(event)

    # Update analytics if order is delivered
    if new_status == 'delivered':
        update_revenue_analytics(order)


    db.session.commit()
    return jsonify(order.to_dict(include_items=True, include_tracking=True)), 200


# ---------------------------------------------------------------------------
# GET /api/commerce/orders/<order_id>/tracking
# Buyer / Artist / Admin — return the tracking event timeline for an order
# ---------------------------------------------------------------------------
@commerce_bp.route('/orders/<string:order_id>/tracking', methods=['GET'])
@jwt_required()
def get_order_tracking(order_id):
    identity = _get_identity()
    role = identity.get('role')

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if role == 'buyer':
        buyer = _buyer_profile(identity['id'])
        if not buyer or order.buyer_id != buyer.id:
            return jsonify({'error': 'Forbidden'}), 403
    elif role == 'artist':
        artist = _artist_profile(identity['id'])
        if not artist or order.artist_id != artist.id:
            return jsonify({'error': 'Forbidden'}), 403
    elif role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    events = (
        OrderTrackingEvent.query
        .filter_by(order_id=order_id)
        .order_by(OrderTrackingEvent.created_at.asc())
        .all()
    )
    return jsonify([e.to_dict() for e in events]), 200
