import uuid
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('buyer', 'artist', 'admin', name='user_roles'), nullable=False)
    is_suspended = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    artist_profile = db.relationship('ArtistProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    buyer_profile = db.relationship('BuyerProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    addresses = db.relationship('Address', backref='user', lazy=True, cascade='all, delete-orphan')
    payment_methods = db.relationship('PaymentMethod', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ArtistProfile(db.Model):
    __tablename__ = 'artist_profiles'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    brand_name = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_image_url = db.Column(db.String(500), nullable=True)
    cover_image_url = db.Column(db.String(500), nullable=True)
    verification_status = db.Column(db.Enum('pending', 'approved', 'rejected', name='verification_status_enum'), nullable=False, default='approved')
    rejection_reason = db.Column(db.String(500), nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user = db.relationship('User', foreign_keys=[user_id], back_populates='artist_profile')

    def to_dict(self):
        from app.models.social import Follow
        follower_count = Follow.query.filter_by(artist_id=self.id).count()
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email': self.user.email if self.user else None,
            'brand_name': self.brand_name,
            'full_name': self.full_name,
            'location': self.location,
            'bio': self.bio,
            'profile_image_url': self.profile_image_url,
            'cover_image_url': self.cover_image_url,
            'follower_count': follower_count,
            'verification_status': self.verification_status,
            'created_at': self.created_at.isoformat(),
        }



class BuyerProfile(db.Model):
    __tablename__ = 'buyer_profiles'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='buyer_profile')

    def to_dict(self):
        from app.models.social import Follow
        from app.models.commerce import Order
        followed_count = Follow.query.filter_by(buyer_id=self.id).count()
        order_count = Order.query.filter_by(buyer_id=self.id).count()
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email': self.user.email if self.user else None,
            'full_name': self.full_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'stats': {
                'followed_artists': followed_count,
                'orders': order_count,
            },
            'addresses': [a.to_dict() for a in self.user.addresses] if self.user else [],
            'payment_methods': [p.to_dict() for p in self.user.payment_methods] if self.user else [],
        }

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    label = db.Column(db.String(50), nullable=True)
    full_address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False, default='India')
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'full_address': self.full_address,
            'city': self.city,
            'state': self.state,
            'pin_code': self.pin_code,
            'country': self.country,
            'is_default': self.is_default
        }

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    last_4 = db.Column(db.String(4), nullable=False)
    expiry_month = db.Column(db.String(2), nullable=False)
    expiry_year = db.Column(db.String(4), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'card_type': self.card_type,
            'last_4': self.last_4,
            'expiry_month': self.expiry_month,
            'expiry_year': self.expiry_year,
            'is_default': self.is_default
        }
