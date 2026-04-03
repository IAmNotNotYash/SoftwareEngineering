from datetime import datetime, timezone
import uuid
from sqlalchemy.dialects.postgresql import JSON
from app import db

class Broadcast(db.Model):
    __tablename__ = 'broadcasts'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artist_id = db.Column(db.String(36), db.ForeignKey('artist_profiles.id'), nullable=False)
    catalogue_id = db.Column(db.String(36), db.ForeignKey('catalogues.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    intent = db.Column(db.Enum('launch', 'preorder', 'flash_sale', 'exclusive_reveal', name='broadcast_intent'), nullable=False)
    platforms = db.Column(JSON, nullable=False, default=list) # ["email", "telegram"]
    status = db.Column(db.Enum('draft', 'sent', 'failed', name='broadcast_status'), default='draft')
    scheduled_at = db.Column(db.DateTime)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    artist = db.relationship('ArtistProfile', backref=db.backref('broadcasts', lazy='dynamic'))
    catalogue = db.relationship('Catalogue', backref=db.backref('broadcasts', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'artist_name': self.artist.brand_name if self.artist else '',
            'catalogue_id': self.catalogue_id if self.catalogue_id else None,
            'catalogue_title': self.catalogue.title if self.catalogue else None,
            'message': self.message,
            'intent': self.intent,
            'platforms': self.platforms,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat()
        }
