import uuid
from datetime import datetime, timezone
from app import db


def _now():
    return datetime.now(timezone.utc)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artist_id = db.Column(db.String(36), db.ForeignKey('artist_profiles.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    materials = db.Column(db.Text, nullable=True)
    dimensions = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    in_stock = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    catalogue_id = db.Column(db.String(36), db.ForeignKey('catalogues.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=_now, onupdate=_now)

    # Relationships
    catalogue = db.relationship('Catalogue', backref=db.backref('direct_products', lazy='dynamic'))
    artist = db.relationship('ArtistProfile', backref=db.backref('products', lazy='dynamic'))
    images = db.relationship(
        'ProductImage', backref='product', lazy='dynamic',
        cascade='all, delete-orphan',
        order_by='ProductImage.sort_order'
    )
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')

    def to_dict(self, include_images=True):
        data = {
            'id': self.id,
            'artist_id': self.artist_id,
            'artist_name': self.artist.brand_name if self.artist else None,
            'title': self.title,
            'description': self.description,
            'materials': self.materials,
            'dimensions': self.dimensions,
            'price': float(self.price),
            'category': self.category,
            'in_stock': self.in_stock,
            'catalogue_id': self.catalogue_id,
            'order_count': self.order_items.count(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_images:
            imgs = self.images.all()
            primary = next((i for i in imgs if i.is_primary), None)
            data['image'] = primary.image_url if primary else (imgs[0].image_url if imgs else None)
            data['gallery'] = [i.image_url for i in imgs]
        return data


class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=_now)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'image_url': self.image_url,
            'is_primary': self.is_primary,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat(),
        }


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyer_profiles.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, nullable=False, default=_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=_now, onupdate=_now)

    __table_args__ = (
        db.UniqueConstraint('buyer_id', 'product_id', name='uq_cart_buyer_product'),
    )

    buyer = db.relationship('BuyerProfile', backref=db.backref('cart_items', lazy='dynamic'))

    def to_dict(self):
        p = self.product
        imgs = p.images.order_by(ProductImage.sort_order).all() if p else []
        primary = next((i for i in imgs if i.is_primary), None)
        image_url = primary.image_url if primary else (imgs[0].image_url if imgs else None)
        return {
            'id': self.id,
            'product_id': self.product_id,
            'title': p.title if p else None,
            'artist': p.artist.brand_name if p and p.artist else None,
            'price': float(p.price) if p else None,
            'image': image_url,
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat(),
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyer_profiles.id'), nullable=False)
    artist_id = db.Column(db.String(36), db.ForeignKey('artist_profiles.id'), nullable=False)
    status = db.Column(
        db.Enum('pending', 'processing', 'shipped', 'delivered', 'cancelled',
                name='order_status_enum'),
        nullable=False, default='pending'
    )
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_cost = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    # JSON snapshot of address and payment at the moment of purchase
    shipping_address_snapshot = db.Column(db.JSON, nullable=False)
    payment_snapshot = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=_now, onupdate=_now)

    # Relationships
    buyer = db.relationship('BuyerProfile', backref=db.backref('orders', lazy='dynamic'))
    artist = db.relationship('ArtistProfile', backref=db.backref('received_orders', lazy='dynamic'))
    items = db.relationship(
        'OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan'
    )
    tracking_events = db.relationship(
        'OrderTrackingEvent', backref='order', lazy='dynamic',
        cascade='all, delete-orphan',
        order_by='OrderTrackingEvent.created_at'
    )

    @property
    def display_id(self):
        # Produces a human-readable prefix like ORD-A3F8C21B
        return f"ORD-{self.id[:8].upper()}"

    def to_dict(self, include_items=False, include_tracking=False):
        data = {
            'id': self.id,
            'display_id': self.display_id,
            'buyer_id': self.buyer_id,
            'artist_id': self.artist_id,
            'buyer_name': self.buyer.full_name if self.buyer else None,
            'artist_name': self.artist.brand_name if self.artist else None,
            'status': self.status,
            'subtotal': float(self.subtotal),
            'shipping_cost': float(self.shipping_cost),
            'total': float(self.total),
            'shipping_address_snapshot': self.shipping_address_snapshot,
            'payment_snapshot': self.payment_snapshot,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_items:
            data['items'] = [i.to_dict() for i in self.items.all()]
        if include_tracking:
            data['tracking_events'] = [e.to_dict() for e in self.tracking_events.all()]
        return data


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    # Nullable so that records survive even if the product is later soft-deleted
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=True)
    product_title_snapshot = db.Column(db.String(200), nullable=False)
    product_image_snapshot = db.Column(db.String(500), nullable=True)
    artist_name_snapshot = db.Column(db.String(150), nullable=False)
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'title': self.product_title_snapshot,
            'image': self.product_image_snapshot,
            'artist': self.artist_name_snapshot,
            'price': float(self.price_at_purchase),
            'quantity': self.quantity,
            'line_total': float(self.price_at_purchase * self.quantity),
        }


class OrderTrackingEvent(db.Model):
    __tablename__ = 'order_tracking_events'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    event = db.Column(
        db.Enum(
            'confirmed', 'dispatched', 'out_for_delivery', 'delivered', 'cancelled',
            name='tracking_event_enum'
        ),
        nullable=False
    )
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_now)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'event': self.event,
            'note': self.note,
            'created_at': self.created_at.isoformat(),
        }
