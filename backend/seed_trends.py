import os
import sys
from datetime import datetime, timezone

# Ensure we are in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

from app import db, create_app
from app.models.analytics import ArtistRevenueTrend, PlatformRevenueTrend, AnalyticsSnapshot
from app.models.user import ArtistProfile

app = create_app()

def seed_trends():
    with app.app_context():
        print("Seeding trends...")
        
        artists = ArtistProfile.query.all()
        if not artists:
            print("No artists found. Please register some artists first.")
            return

        months = ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03"]
        
        # Seed Artist Trends
        for artist in artists:
            base_rev = 10000
            base_views = 500
            for i, month in enumerate(months):
                rev = base_rev + (i * 2500)
                views = base_views + (i * 150)
                
                trend = ArtistRevenueTrend.query.filter_by(artist_id=artist.id, month=month).first()
                if not trend:
                    trend = ArtistRevenueTrend(
                        artist_id=artist.id,
                        month=month,
                        revenue=rev,
                        orders=int(rev/2000),
                        catalogue_views=views,
                        story_engagement_rate=0.05 + (i * 0.01)
                    )
                    db.session.add(trend)
        
        # Seed Platform Trends
        for i, month in enumerate(months):
            rev = (i + 1) * 50000
            orders = int(rev/1500)
            
            trend = PlatformRevenueTrend.query.filter_by(month=month).first()
            if not trend:
                trend = PlatformRevenueTrend(
                    month=month,
                    revenue=rev,
                    new_signups=10 + (i * 5),
                    total_orders=orders,
                    avg_order_value=rev/orders if orders else 0
                )
                db.session.add(trend)

        # Seed an AI Snapshot for the platform
        platform_snapshot = AnalyticsSnapshot.query.filter_by(entity_type='platform', period='2026-03').first()
        if not platform_snapshot:
            platform_snapshot = AnalyticsSnapshot(
                entity_type='platform',
                period='2026-03',
                metrics={"revenue": 300000, "growth": "15%"},
                ai_summary="The platform is seeing strong growth in the Ceramics and Handloom categories. New artist signups are up 20% this month.",
                generated_at=datetime.now(timezone.utc)
            )
            db.session.add(platform_snapshot)

        db.session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    seed_trends()
