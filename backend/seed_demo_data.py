import os
import sys
import uuid
from datetime import datetime, timezone
import json
from decimal import Decimal

# Ensure we are in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

from app import db, create_app
from app.models.user import User, ArtistProfile, BuyerProfile
from app.models.catalogue import Catalogue, CatalogueProduct, CatalogueStats
from app.models.commerce import Product, ProductImage
from werkzeug.security import generate_password_hash

app = create_app()

def seed_demo_data():
    with app.app_context():
        print("Starting comprehensive demo data seeding...")

        # 1. Clear existing data (optional but recommended for clean slate)
        # Note: In a real app, be careful with this. We only do this for seeding.
        # CatalogueLike.query.delete()
        # CatalogueView.query.delete()
        # CatalogueProduct.query.delete()
        # CatalogueStats.query.delete()
        # ProductImage.query.delete()
        # Product.query.delete()
        # Catalogue.query.delete()
        # ArtistProfile.query.delete()
        # BuyerProfile.query.delete()
        # User.query.filter(User.email != 'admin@kala.com').delete() 
        # db.session.commit()

        # 2. Create Artists
        artists_data = [
            {
                "email": "luna@ceramics.com",
                "brand": "Luna Ceramics",
                "bio": "Creating sustainable, earth-fired ceramics using ancient local techniques.",
                "location": "Jaipur, Rajasthan",
                "category": "Ceramics",
                "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=400",
                "cover": "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=1200",
                "catalogues": [
                    {
                        "title": "The Earth Tones Collection",
                        "philosophy": "This collection explores the raw textures of unfired clay, celebrating the imperfections and natural hues found deep within the earth.",
                        "note": "Every piece in this catalogue was wheel-thrown in my home studio during the monsoon.",
                        "products": [
                            {"title": "Handcrafted Ceramic Vase", "price": 4500, "img": "https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&q=80&w=800"},
                            {"title": "Raw Clay Pitcher", "price": 3200, "img": "https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&q=80&w=800"},
                            {"title": "Earthy Serving Bowl", "price": 2100, "img": "https://images.unsplash.com/photo-1620189507195-68309c04c4d0?auto=format&fit=crop&q=80&w=800"}
                        ]
                    }
                ]
            },
            {
                "email": "aurum@studio.com",
                "brand": "Aurum Studio",
                "bio": "Minimalist jewelry inspired by the geometry of nature.",
                "location": "Ahmadabad, Gujarat",
                "category": "Jewelry",
                "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200",
                "cover": "https://images.unsplash.com/photo-1599643478524-fb524458f407?auto=format&fit=crop&q=80&w=1200",
                "catalogues": [
                    {
                        "title": "Geometric Gold",
                        "philosophy": "Clean lines and mathematical precision in 18k solid gold.",
                        "products": [
                            {"title": "Square Hoop Earrings", "price": 12500, "img": "https://images.unsplash.com/photo-1599643478524-fb524458f407?auto=format&fit=crop&q=80&w=800"},
                            {"title": "Triangle Prism Pendant", "price": 8900, "img": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&q=80&w=800"}
                        ]
                    }
                ]
            }
        ]

        for a_data in artists_data:
            user = User.query.filter_by(email=a_data["email"]).first()
            if not user:
                user = User(
                    email=a_data["email"],
                    password_hash=generate_password_hash("123"),
                    role='artist'
                )
                db.session.add(user)
                db.session.flush()

                profile = ArtistProfile(
                    user_id=user.id,
                    full_name=a_data["brand"],
                    brand_name=a_data["brand"],
                    bio=a_data["bio"],
                    location=a_data["location"],
                    profile_image_url=a_data["avatar"],
                    cover_image_url=a_data["cover"],
                    verification_status='approved'
                )
                db.session.add(profile)
                db.session.flush()
            else:
                profile = user.artist_profile

            for c_data in a_data["catalogues"]:
                cat = Catalogue.query.filter_by(artist_id=profile.id, title=c_data["title"]).first()
                if not cat:
                    cat = Catalogue(
                        artist_id=profile.id,
                        title=c_data["title"],
                        philosophy=c_data.get("philosophy"),
                        artist_note=c_data.get("note"),
                        cover_photo_url=c_data["products"][0]["img"],
                        status='live',
                        published_at=datetime.now(timezone.utc),
                        theme='earth'
                    )
                    db.session.add(cat)
                    db.session.flush()
                    
                    stats = CatalogueStats(catalogue_id=cat.id)
                    db.session.add(stats)

                for i, p_data in enumerate(c_data["products"]):
                    prod = Product.query.filter_by(artist_id=profile.id, title=p_data["title"]).first()
                    if not prod:
                        prod = Product(
                            artist_id=profile.id,
                            title=p_data["title"],
                            price=Decimal(p_data["price"]),
                            category=a_data["category"],
                            description=f"A beautiful piece from the {c_data['title']} collection."
                        )
                        db.session.add(prod)
                        db.session.flush()

                        img = ProductImage(
                            product_id=prod.id,
                            image_url=p_data["img"],
                            is_primary=True,
                            sort_order=0
                        )
                        db.session.add(img)

                    # Link product to catalogue
                    link = CatalogueProduct.query.filter_by(catalogue_id=cat.id, product_id=prod.id).first()
                    if not link:
                        link = CatalogueProduct(
                            catalogue_id=cat.id,
                            product_id=prod.id,
                            sort_order=i
                        )
                        db.session.add(link)

        db.session.commit()
        print("Demo data seeding complete!")

if __name__ == "__main__":
    seed_demo_data()
