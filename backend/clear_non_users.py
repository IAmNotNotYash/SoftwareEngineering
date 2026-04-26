import os
import sys

# Ensure we are in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

from app import db, create_app
from app.models.user import User, ArtistProfile, BuyerProfile, Address, PaymentMethod
from app.models.catalogue import Catalogue, CatalogueProduct, CatalogueStats, CatalogueLike, CatalogueView
from app.models.commerce import Product, ProductImage, CartItem, Order, OrderItem, OrderTrackingEvent
from app.models.social import Follow, Post, PostLike, Review
from app.models.analytics import ArtistRevenueTrend, PlatformRevenueTrend, AnalyticsSnapshot

app = create_app()

def clear_non_users():
    with app.app_context():
        print("Clearing all content except for Users and Profiles...")

        try:
            # Delete in order of dependencies
            
            print("Deleting social data...")
            Review.query.delete()
            PostLike.query.delete()
            Post.query.delete()
            Follow.query.delete()
            
            print("Deleting commerce data...")
            OrderTrackingEvent.query.delete()
            OrderItem.query.delete()
            Order.query.delete()
            CartItem.query.delete()
            ProductImage.query.delete()
            
            # Unlink products from catalogues before deleting catalogues to avoid FK issues
            # Or just delete catalogue products first
            CatalogueProduct.query.delete()
            Product.query.delete()
            
            print("Deleting catalogue data...")
            CatalogueLike.query.delete()
            CatalogueView.query.delete()
            CatalogueStats.query.delete()
            Catalogue.query.delete()
            
            print("Deleting analytics data...")
            ArtistRevenueTrend.query.delete()
            PlatformRevenueTrend.query.delete()
            AnalyticsSnapshot.query.delete()
            
            print("Deleting extra user data (Addresses, PaymentMethods)...")
            Address.query.delete()
            PaymentMethod.query.delete()
            
            # We keep User, ArtistProfile, and BuyerProfile
            
            db.session.commit()
            print("Data cleared successfully! (Users and Profiles preserved)")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing data: {str(e)}")

if __name__ == "__main__":
    clear_non_users()
