from datetime import datetime, timezone
import uuid
from sqlalchemy.dialects.postgresql import JSON
from app import db

class ArtistRevenueTrend(db.Model):
    __tablename__ = 'artist_revenue_trend'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artist_id = db.Column(db.String(36), db.ForeignKey('artist_profiles.id'), nullable=False)
    month = db.Column(db.String(7), nullable=False) # "YYYY-MM"
    revenue = db.Column(db.Numeric(12, 2), default=0)
    orders = db.Column(db.Integer, default=0)
    catalogue_views = db.Column(db.Integer, default=0)
    story_engagement_rate = db.Column(db.Float) # Percentage
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('artist_id', 'month', name='_artist_month_trend_uc'),)

    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'month': self.month,
            'revenue': float(self.revenue),
            'orders': self.orders,
            'catalogue_views': self.catalogue_views,
            'story_engagement_rate': self.story_engagement_rate,
            'recorded_at': self.recorded_at.isoformat()
        }

class PlatformRevenueTrend(db.Model):
    __tablename__ = 'platform_revenue_trend'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    month = db.Column(db.String(7), unique=True, nullable=False) # "YYYY-MM"
    revenue = db.Column(db.Numeric(14, 2), default=0)
    new_signups = db.Column(db.Integer, default=0)
    total_orders = db.Column(db.Integer, default=0)
    avg_order_value = db.Column(db.Numeric(10, 2), default=0)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'month': self.month,
            'revenue': float(self.revenue),
            'new_signups': self.new_signups,
            'total_orders': self.total_orders,
            'avg_order_value': float(self.avg_order_value),
            'recorded_at': self.recorded_at.isoformat()
        }

class AnalyticsSnapshot(db.Model):
    __tablename__ = 'analytics_snapshots'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type = db.Column(db.Enum('artist', 'platform', name='analytics_entity_type'), nullable=False)
    entity_id = db.Column(db.String(36), nullable=True) # Artist ID or Null
    period = db.Column(db.String(20), nullable=False) # "2026-03", "all-time"
    metrics = db.Column(JSON, nullable=False)
    ai_summary = db.Column(db.Text)
    sentiment_summary = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id if self.entity_id else None,
            'period': self.period,
            'metrics': self.metrics,
            'ai_summary': self.ai_summary,
            'sentiment_summary': self.sentiment_summary,
            'generated_at': self.generated_at.isoformat()
        }
