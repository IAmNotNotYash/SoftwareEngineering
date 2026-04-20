from datetime import datetime
from app import db
from app.models.analytics import ArtistRevenueTrend, PlatformRevenueTrend
from app.models.catalogue import CatalogueStats

def update_revenue_analytics(order):
    """
    Updates ArtistRevenueTrend, PlatformRevenueTrend and CatalogueStats when an order is delivered.
    """
    month = datetime.now().strftime("%Y-%m")
    
    # 1. Update Artist Revenue Trend
    artist_trend = ArtistRevenueTrend.query.filter_by(
        artist_id=order.artist_id, 
        month=month
    ).first()
    
    if not artist_trend:
        artist_trend = ArtistRevenueTrend(
            artist_id=order.artist_id,
            month=month,
            revenue=0,
            orders=0
        )
        db.session.add(artist_trend)
    
    artist_trend.revenue = float(artist_trend.revenue) + float(order.subtotal)
    artist_trend.orders += 1
    
    # 2. Update Platform Revenue Trend
    platform_trend = PlatformRevenueTrend.query.filter_by(month=month).first()
    
    if not platform_trend:
        platform_trend = PlatformRevenueTrend(
            month=month,
            revenue=0,
            total_orders=0,
            avg_order_value=0
        )
        db.session.add(platform_trend)
    
    platform_trend.revenue = float(platform_trend.revenue) + float(order.total)
    platform_trend.total_orders += 1
    
    # Recalculate average order value
    if platform_trend.total_orders > 0:
        platform_trend.avg_order_value = float(platform_trend.revenue) / platform_trend.total_orders

    # 3. Update Catalogue Stats for each product in the order
    for item in order.items:
        if item.product and item.product.catalogue_id:
            cat_stats = CatalogueStats.query.filter_by(catalogue_id=item.product.catalogue_id).first()
            if not cat_stats:
                cat_stats = CatalogueStats(catalogue_id=item.product.catalogue_id)
                db.session.add(cat_stats)
            
            cat_stats.total_revenue = float(cat_stats.total_revenue) + float(item.price_at_purchase * item.quantity)
            cat_stats.total_orders += 1
