import uuid
from datetime import datetime, timezone
from app import db


def _now():
    return datetime.now(timezone.utc)


class Catalogue(db.Model):
    __tablename__ = 'catalogues'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artist_id = db.Column(db.String(36), db.ForeignKey('artist_profiles.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    narrative = db.Column(db.Text, nullable=True)
    cover_photo_url = db.Column(db.String(500), nullable=True)
    theme = db.Column(
        db.Enum('warm', 'earth', 'cool', 'dark', name='catalogue_theme_enum'),
        nullable=False, default='earth'
    )
    launch_intent = db.Column(
        db.Enum('live', 'preview', 'preorder', name='catalogue_launch_intent_enum'),
        nullable=False, default='live'
    )
    status = db.Column(
        db.Enum('draft', 'live', 'ended', name='catalogue_status_enum'),
        nullable=False, default='draft'
    )
    philosophy = db.Column(db.Text, nullable=True)
    artist_note = db.Column(db.Text, nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=_now, onupdate=_now)

    # Relationships
    artist = db.relationship('ArtistProfile', backref=db.backref('catalogues', lazy='dynamic'))
    catalogue_products = db.relationship(
        'CatalogueProduct', backref='catalogue', lazy='dynamic',
        cascade='all, delete-orphan', order_by='CatalogueProduct.sort_order'
    )
    stats = db.relationship('CatalogueStats', backref='catalogue', uselist=False, cascade='all, delete-orphan')
    views = db.relationship('CatalogueView', backref='catalogue', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('CatalogueLike', backref='catalogue', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_products=False):
        data = {
            'id': self.id,
            'artist_id': self.artist_id,
            'artist_name': self.artist.brand_name if self.artist else None,
            'artist_profile_image': self.artist.profile_image_url if self.artist else None,
            'title': self.title,
            'narrative': self.narrative,
            'cover_photo_url': self.cover_photo_url,
            'theme': self.theme,
            'launch_intent': self.launch_intent,
            'status': self.status,
            'philosophy': self.philosophy,
            'artist_note': self.artist_note,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'stats': self.stats.to_dict() if self.stats else None,
        }
        if include_products:
            from app.models.commerce import Product
            cp_list = self.catalogue_products.all()
            products = []
            for cp in cp_list:
                product = db.session.get(Product, cp.product_id)
                if product and not product.is_deleted:
                    products.append(product.to_dict())
            data['products'] = products
        return data


class CatalogueProduct(db.Model):
    __tablename__ = 'catalogue_products'
    __table_args__ = (
        db.UniqueConstraint('catalogue_id', 'product_id', name='uq_catalogue_product'),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    catalogue_id = db.Column(db.String(36), db.ForeignKey('catalogues.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)

    product = db.relationship('Product')


class CatalogueStats(db.Model):
    __tablename__ = 'catalogue_stats'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    catalogue_id = db.Column(db.String(36), db.ForeignKey('catalogues.id'), unique=True, nullable=False)
    total_views = db.Column(db.Integer, default=0, nullable=False)
    total_likes = db.Column(db.Integer, default=0, nullable=False)
    total_revenue = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    total_orders = db.Column(db.Integer, default=0, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=_now, onupdate=_now)

    def to_dict(self):
        return {
            'total_views': self.total_views,
            'total_likes': self.total_likes,
            'total_revenue': float(self.total_revenue),
            'total_orders': self.total_orders,
            'last_updated': self.last_updated.isoformat(),
        }


class CatalogueView(db.Model):
    __tablename__ = 'catalogue_views'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    catalogue_id = db.Column(db.String(36), db.ForeignKey('catalogues.id'), nullable=False)
    # Nullable — allows anonymous (unauthenticated) views
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyer_profiles.id'), nullable=True)
    viewed_at = db.Column(db.DateTime, nullable=False, default=_now)

    buyer = db.relationship('BuyerProfile', backref=db.backref('catalogue_views', lazy='dynamic'))


class CatalogueLike(db.Model):
    __tablename__ = 'catalogue_likes'
    __table_args__ = (
        db.UniqueConstraint('catalogue_id', 'buyer_id', name='uq_catalogue_like'),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    catalogue_id = db.Column(db.String(36), db.ForeignKey('catalogues.id'), nullable=False)
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyer_profiles.id'), nullable=False)
    liked_at = db.Column(db.DateTime, nullable=False, default=_now)

    buyer = db.relationship('BuyerProfile', backref=db.backref('catalogue_likes', lazy='dynamic'))
