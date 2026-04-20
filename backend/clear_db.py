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

app = create_app()

def clear_db():
    with app.app_context():
        print("Clearing all data from the database...")

        try:
            # Delete in order of dependencies to avoid foreign key constraints issues
            
            print("Deleting social interactions (Follows, Likes, Reviews, Posts)...")
            Follow.query.delete()
            PostLike.query.delete()
            Review.query.delete()
            Post.query.delete()
            
            print("Deleting tracking events, items and cart...")
            OrderTrackingEvent.query.delete()
            OrderItem.query.delete()
            CartItem.query.delete()
            
            print("Deleting orders...")
            Order.query.delete()
            
            print("Deleting catalogue interactions and stats...")
            CatalogueLike.query.delete()
            CatalogueView.query.delete()
            CatalogueProduct.query.delete()
            CatalogueStats.query.delete()
            
            print("Deleting products and images...")
            ProductImage.query.delete()
            Product.query.delete()
            
            print("Deleting catalogues...")
            Catalogue.query.delete()
            
            print("Deleting user profiles, addresses and payment methods...")
            ArtistProfile.query.delete()
            BuyerProfile.query.delete()
            Address.query.delete()
            PaymentMethod.query.delete()
            
            print("Deleting users...")
            User.query.delete()
            
            db.session.commit()
            print("Database cleared successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing database: {str(e)}")

if __name__ == "__main__":
    clear_db()
