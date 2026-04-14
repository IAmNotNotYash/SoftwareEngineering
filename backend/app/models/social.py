from datetime import datetime, timezone
import uuid
from app import db

class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyer_profiles.id'), nullable=False)
    artist_id = db.Column(db.String(36), db.ForeignKey('artist_profiles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('buyer_id', 'artist_id', name='_buyer_artist_follow_uc'),)

    def to_dict(self):
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'artist_id': self.artist_id,
            'created_at': self.created_at.isoformat()
        }

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artist_id = db.Column(db.String(36), db.ForeignKey('artist_profiles.id'), nullable=False)
    type = db.Column(db.Enum('story', 'insight', name='post_type'), nullable=False)
    catalogue_id = db.Column(db.String(36), db.ForeignKey('catalogues.id'), nullable=True)
    title = db.Column(db.String(300), nullable=True)
    body = db.Column(db.Text, nullable=False)
    cover_image_url = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    artist = db.relationship('ArtistProfile', backref=db.backref('posts', lazy='dynamic'))
    catalogue = db.relationship('Catalogue', backref=db.backref('posts', lazy='dynamic'))
    likes = db.relationship('PostLike', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'artist_name': self.artist.brand_name if self.artist else '',
            'catalogue_id': self.catalogue_id,
            'type': self.type,
            'title': self.title,
            'body': self.body,
            'cover_image_url': self.cover_image_url,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat(),
            'likes_count': self.likes.count()
        }

class PostLike(db.Model):
    __tablename__ = 'post_likes'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False)
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyer_profiles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('post_id', 'buyer_id', name='_post_buyer_like_uc'),)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'buyer_id': self.buyer_id,
            'created_at': self.created_at.isoformat()
        }

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = db.Column(db.String(36), db.ForeignKey('buyer_profiles.id'), nullable=False)
    target_type = db.Column(db.Enum('product', 'catalogue', name='review_target_type'), nullable=False)
    target_id = db.Column(db.String(36), nullable=False) # Polymorphic
    rating = db.Column(db.Integer) # 1-5
    body = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    buyer = db.relationship('BuyerProfile', backref=db.backref('reviews', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'buyer_name': self.buyer.full_name if self.buyer else '',
            'target_type': self.target_type,
            'target_id': self.target_id,
            'rating': self.rating,
            'body': self.body,
            'created_at': self.created_at.isoformat()
        }
