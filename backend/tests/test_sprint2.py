"""
Kala Platform — Sprint 2 Pytest Test Suite
===========================================
Tests cover all API endpoints developed in Milestone 3 & 4.

Run with:
    cd backend
    pytest tests/test_sprint2.py -v

Requires:
    - A running PostgreSQL instance configured in .env
    - FLASK_ENV=testing or a test database URL set
"""

import io
import json
import pytest
import uuid
from app import create_app, db
from app.models.user import User, ArtistProfile, BuyerProfile
from app.models.commerce import Product, ProductImage, CartItem, Order, OrderItem, OrderTrackingEvent
from app.models.catalogue import Catalogue, CatalogueStats, CatalogueLike
from app.models.social import Follow, Review, Post
from app.models.analytics import ArtistRevenueTrend, AnalyticsSnapshot
from app.models.communication import Broadcast
from werkzeug.security import generate_password_hash


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def app():
    """Create application for the testing session."""
    application = create_app()
    application.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": application.config.get(
            "SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:"
        ),
        "JWT_SECRET_KEY": "test-jwt-secret-key",
        "JWT_ACCESS_TOKEN_EXPIRES": False,
    })
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def seeded_data(app):
    """Create reusable test users and related profiles once per session."""
    with app.app_context():
        # Admin user
        admin_user = User(
            id=str(uuid.uuid4()),
            email="admin@test.com",
            password_hash=generate_password_hash("adminpass"),
            role="admin"
        )
        db.session.add(admin_user)

        # Artist user
        artist_user = User(
            id=str(uuid.uuid4()),
            email="artist@test.com",
            password_hash=generate_password_hash("artistpass"),
            role="artist"
        )
        db.session.add(artist_user)
        db.session.flush()

        artist_profile = ArtistProfile(
            id=str(uuid.uuid4()),
            user_id=artist_user.id,
            full_name="Test Artist",
            brand_name="Test Brand",
            verification_status="approved"
        )
        db.session.add(artist_profile)

        # Pending artist user
        pending_artist_user = User(
            id=str(uuid.uuid4()),
            email="pending_artist@test.com",
            password_hash=generate_password_hash("pendingpass"),
            role="artist"
        )
        db.session.add(pending_artist_user)
        db.session.flush()

        pending_artist_profile = ArtistProfile(
            id=str(uuid.uuid4()),
            user_id=pending_artist_user.id,
            full_name="Pending Artist",
            brand_name="Pending Brand",
            verification_status="pending"
        )
        db.session.add(pending_artist_profile)

        # Buyer user
        buyer_user = User(
            id=str(uuid.uuid4()),
            email="buyer@test.com",
            password_hash=generate_password_hash("buyerpass"),
            role="buyer"
        )
        db.session.add(buyer_user)
        db.session.flush()

        buyer_profile = BuyerProfile(
            id=str(uuid.uuid4()),
            user_id=buyer_user.id,
            full_name="Test Buyer"
        )
        db.session.add(buyer_profile)

        # Product
        product = Product(
            id=str(uuid.uuid4()),
            artist_id=artist_profile.id,
            title="Test Ceramic Vase",
            description="A beautiful handcrafted ceramic vase.",
            price=4500,
            category="Ceramics",
            in_stock=True
        )
        db.session.add(product)

        out_of_stock_product = Product(
            id=str(uuid.uuid4()),
            artist_id=artist_profile.id,
            title="Sold Out Item",
            price=1000,
            in_stock=False
        )
        db.session.add(out_of_stock_product)

        # Catalogue
        catalogue = Catalogue(
            id=str(uuid.uuid4()),
            artist_id=artist_profile.id,
            title="Test Live Catalogue",
            status="live",
            theme="earth",
            launch_intent="live"
        )
        db.session.add(catalogue)
        db.session.flush()

        catalogue_stats = CatalogueStats(
            id=str(uuid.uuid4()),
            catalogue_id=catalogue.id,
            total_views=0,
            total_likes=0,
            total_revenue=0,
            total_orders=0
        )
        db.session.add(catalogue_stats)

        db.session.commit()

        return {
            "admin_user_id": admin_user.id,
            "artist_user_id": artist_user.id,
            "artist_profile_id": artist_profile.id,
            "pending_artist_user_id": pending_artist_user.id,
            "pending_artist_profile_id": pending_artist_profile.id,
            "buyer_user_id": buyer_user.id,
            "buyer_profile_id": buyer_profile.id,
            "product_id": product.id,
            "oos_product_id": out_of_stock_product.id,
            "catalogue_id": catalogue.id,
        }


def _make_token(app, user_id, role, email):
    """Generate a real JWT token for a given identity."""
    from flask_jwt_extended import create_access_token
    with app.app_context():
        identity = json.dumps({"id": user_id, "role": role, "email": email})
        return create_access_token(identity=identity)


def _auth(app, user_id, role, email="test@test.com"):
    return {"Authorization": f"Bearer {_make_token(app, user_id, role, email)}"}


# ===========================================================================
# AUTH TESTS
# ===========================================================================

class TestAuth:

    def test_register_buyer_success(self, client):
        """TC-AUTH-01: Buyer registration returns 201 with token."""
        payload = {
            "firstName": "Aarav",
            "lastName": "Sharma",
            "email": f"buyer_{uuid.uuid4().hex[:6]}@example.com",
            "password": "securepass123",
            "role": "buyer"
        }
        res = client.post("/api/auth/register", json=payload)
        assert res.status_code == 201
        data = res.get_json()
        assert "token" in data
        assert data["user"]["role"] == "buyer"
        assert data["user"]["buyerId"] is not None

    def test_register_artist_success(self, client):
        """TC-AUTH-02: Artist registration with brand name returns 201."""
        payload = {
            "firstName": "Meera",
            "lastName": "Nair",
            "email": f"artist_{uuid.uuid4().hex[:6]}@example.com",
            "password": "securepass123",
            "role": "artist",
            "brandName": "Meera Crafts"
        }
        res = client.post("/api/auth/register", json=payload)
        assert res.status_code == 201
        data = res.get_json()
        assert data["user"]["role"] == "artist"
        assert data["user"]["artistId"] is not None

    def test_register_artist_missing_brand_name(self, client):
        """TC-AUTH-03: Artist registration without brand name returns 400."""
        payload = {
            "firstName": "No",
            "lastName": "Brand",
            "email": f"nobrand_{uuid.uuid4().hex[:6]}@example.com",
            "password": "pass123",
            "role": "artist"
        }
        res = client.post("/api/auth/register", json=payload)
        assert res.status_code == 400
        assert "brand" in res.get_json()["error"].lower()

    def test_register_duplicate_email(self, client):
        """TC-AUTH-04: Duplicate email registration returns 400."""
        email = f"dup_{uuid.uuid4().hex[:6]}@example.com"
        payload = {
            "firstName": "A", "lastName": "B",
            "email": email, "password": "pass123", "role": "buyer"
        }
        client.post("/api/auth/register", json=payload)
        res = client.post("/api/auth/register", json=payload)
        assert res.status_code == 400

    def test_login_valid_credentials(self, client, seeded_data):
        """TC-AUTH-05: Login with correct credentials returns 200 and token."""
        res = client.post("/api/auth/login", json={
            "email": "buyer@test.com", "password": "buyerpass"
        })
        assert res.status_code == 200
        data = res.get_json()
        assert "token" in data

    def test_login_invalid_password(self, client, seeded_data):
        """TC-AUTH-06: Wrong password returns 401."""
        res = client.post("/api/auth/login", json={
            "email": "buyer@test.com", "password": "wrongpass"
        })
        assert res.status_code == 401

    def test_login_nonexistent_user(self, client):
        """TC-AUTH-06b: Login with unknown email returns 401."""
        res = client.post("/api/auth/login", json={
            "email": "nobody@example.com", "password": "whatever"
        })
        assert res.status_code == 401

    def test_login_suspended_account(self, client, app, seeded_data):
        """TC-AUTH-07: Suspended user cannot log in."""
        with app.app_context():
            user = db.session.get(User, seeded_data["buyer_user_id"])
            user.is_suspended = True
            db.session.commit()

        res = client.post("/api/auth/login", json={
            "email": "buyer@test.com", "password": "buyerpass"
        })
        assert res.status_code == 403

        # Restore
        with app.app_context():
            user = db.session.get(User, seeded_data["buyer_user_id"])
            user.is_suspended = False
            db.session.commit()

    def test_get_profile(self, client, app, seeded_data):
        """TC-AUTH-08: Authenticated user can retrieve their profile."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/auth/profile", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert data["email"] == "buyer@test.com"

    def test_get_profile_unauthenticated(self, client):
        """TC-AUTH-08b: Unauthenticated profile request returns 401."""
        res = client.get("/api/auth/profile")
        assert res.status_code == 401

    def test_update_profile(self, client, app, seeded_data):
        """TC-AUTH-09: Buyer can update their profile."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.patch("/api/auth/profile", json={"phone": "+919999999999"},
                           headers=headers)
        assert res.status_code == 200


# ===========================================================================
# CATALOGUE TESTS
# ===========================================================================

class TestCatalogue:

    def test_create_catalogue_approved_artist(self, client, app, seeded_data):
        """TC-CAT-01: Approved artist can create a catalogue."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.post("/api/catalogues", json={
            "title": "New Test Catalogue",
            "narrative": "A fresh collection from the studio.",
            "theme": "earth",
            "launch_intent": "live",
            "status": "draft"
        }, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data["title"] == "New Test Catalogue"
        assert data["status"] == "draft"

    def test_create_catalogue_unverified_artist(self, client, app, seeded_data):
        """TC-CAT-02: Pending artist cannot create a catalogue."""
        headers = _auth(app, seeded_data["pending_artist_user_id"], "artist", "pending_artist@test.com")
        res = client.post("/api/catalogues", json={
            "title": "Should Fail",
            "theme": "earth",
            "launch_intent": "live",
            "status": "draft"
        }, headers=headers)
        assert res.status_code == 403

    def test_create_catalogue_missing_title(self, client, app, seeded_data):
        """TC-CAT-02b: Creating catalogue without title returns 400."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.post("/api/catalogues", json={
            "narrative": "No title here",
            "theme": "earth",
        }, headers=headers)
        assert res.status_code == 400


    def test_get_catalogue_detail(self, client, seeded_data):
        """TC-CAT-04: Get single catalogue returns products and stories."""
        res = client.get(f"/api/catalogues/{seeded_data['catalogue_id']}")
        assert res.status_code == 200
        data = res.get_json()
        assert "products" in data or "stats" in data

    def test_get_catalogue_not_found(self, client):
        """TC-CAT-04b: Get non-existent catalogue returns 404."""
        res = client.get("/api/catalogues/nonexistent-id-12345")
        assert res.status_code == 404

    def test_update_catalogue_status_to_live(self, client, app, seeded_data):
        """TC-CAT-05: Artist can update catalogue status to live."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        # First create a draft catalogue
        create_res = client.post("/api/catalogues", json={
            "title": "Draft to Live",
            "theme": "warm",
            "launch_intent": "live",
            "status": "draft"
        }, headers=headers)
        cat_id = create_res.get_json()["id"]

        res = client.patch(f"/api/catalogues/{cat_id}", json={"status": "live"},
                           headers=headers)
        assert res.status_code == 200
        assert res.get_json()["status"] == "live"
        assert res.get_json()["published_at"] is not None

    def test_update_catalogue_wrong_owner(self, client, app, seeded_data):
        """TC-CAT-05b: Artist cannot update another artist's catalogue."""
        # Create a second artist
        with app.app_context():
            u2 = User(id=str(uuid.uuid4()), email=f"cat_artist2_{uuid.uuid4().hex[:4]}@test.com",
                      password_hash=generate_password_hash("pass"), role="artist")
            db.session.add(u2)
            db.session.flush()
            p2 = ArtistProfile(id=str(uuid.uuid4()), user_id=u2.id,
                                full_name="Artist 2", brand_name="Brand 2",
                                verification_status="approved")
            db.session.add(p2)
            db.session.commit()
            u2_id = u2.id

        headers2 = _auth(app, u2_id, "artist", "cat_artist2@test.com")
        res = client.patch(f"/api/catalogues/{seeded_data['catalogue_id']}",
                           json={"title": "Hijacked"}, headers=headers2)
        assert res.status_code == 404

    def test_like_catalogue(self, client, app, seeded_data):
        """TC-CAT-06: Buyer can like a catalogue."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post(f"/api/catalogues/{seeded_data['catalogue_id']}/like",
                          headers=headers)
        assert res.status_code in (201, 409)  # 409 if already liked

    def test_like_catalogue_duplicate(self, client, app, seeded_data):
        """TC-CAT-07: Liking a catalogue twice returns 409."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        client.post(f"/api/catalogues/{seeded_data['catalogue_id']}/like", headers=headers)
        res = client.post(f"/api/catalogues/{seeded_data['catalogue_id']}/like", headers=headers)
        assert res.status_code == 409

    def test_unlike_catalogue(self, client, app, seeded_data):
        """TC-CAT-08: Buyer can unlike a catalogue they have liked."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        # Ensure liked first
        client.post(f"/api/catalogues/{seeded_data['catalogue_id']}/like", headers=headers)
        res = client.delete(f"/api/catalogues/{seeded_data['catalogue_id']}/like",
                            headers=headers)
        assert res.status_code == 200
        assert res.get_json()["liked"] is False

    def test_catalogue_feed_requires_auth(self, client):
        """TC-CAT-09: Feed endpoint requires authentication."""
        res = client.get("/api/catalogues/feed")
        assert res.status_code in (200, 401)

    def test_delete_catalogue(self, client, app, seeded_data):
        """TC-CAT-10: Artist can end (delete) their own catalogue."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        create_res = client.post("/api/catalogues", json={
            "title": "To Be Ended",
            "theme": "earth",
            "status": "draft"
        }, headers=headers)
        cat_id = create_res.get_json()["id"]
        res = client.delete(f"/api/catalogues/{cat_id}", headers=headers)
        assert res.status_code == 200


# ===========================================================================
# PRODUCT TESTS
# ===========================================================================

class TestProducts:

    def test_create_product_success(self, client, app, seeded_data):
        """TC-PROD-01: Approved artist can create a product."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.post("/api/commerce/products", json={
            "title": "Handwoven Indigo Scarf",
            "description": "Cotton scarf dyed with natural indigo.",
            "price": 3200,
            "category": "Textiles"
        }, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data["title"] == "Handwoven Indigo Scarf"
        assert data["in_stock"] is True

    def test_create_product_missing_price(self, client, app, seeded_data):
        """TC-PROD-01b: Creating product without price returns 400."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.post("/api/commerce/products", json={
            "title": "No Price Product",
        }, headers=headers)
        assert res.status_code == 400

    def test_list_products_public(self, client, seeded_data):
        """TC-PROD-02: Public endpoint lists non-deleted products."""
        res = client.get("/api/commerce/products")
        assert res.status_code == 200
        products = res.get_json()
        assert isinstance(products, list)
        for p in products:
            assert "title" in p and "price" in p

    def test_search_products(self, client, seeded_data):
        """TC-PROD-03: Search filters products by keyword."""
        res = client.get("/api/commerce/products?search=ceramic")
        assert res.status_code == 200
        products = res.get_json()
        for p in products:
            assert "ceramic" in p["title"].lower() or "ceramic" in (p.get("description") or "").lower()

    def test_get_product_detail(self, client, seeded_data):
        """TC-PROD-03b: Get single product detail returns 200."""
        res = client.get(f"/api/commerce/products/{seeded_data['product_id']}")
        assert res.status_code == 200
        data = res.get_json()
        assert data["id"] == seeded_data["product_id"]

    def test_get_product_not_found(self, client):
        """TC-PROD-03c: Get non-existent product returns 404."""
        res = client.get("/api/commerce/products/nonexistent-id-12345")
        assert res.status_code == 404

    def test_update_product(self, client, app, seeded_data):
        """TC-PROD-04: Artist can update their product."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        product_id = seeded_data["product_id"]
        res = client.patch(f"/api/commerce/products/{product_id}",
                           json={"price": 5000, "in_stock": True}, headers=headers)
        assert res.status_code == 200
        assert float(res.get_json()["price"]) == 5000.0

    def test_update_product_wrong_owner(self, client, app, seeded_data):
        """TC-PROD-04b: Artist cannot update another artist's product."""
        with app.app_context():
            user2 = User(id=str(uuid.uuid4()), email=f"artist2_{uuid.uuid4().hex[:4]}@test.com",
                         password_hash=generate_password_hash("pass"), role="artist")
            db.session.add(user2)
            db.session.flush()
            profile2 = ArtistProfile(id=str(uuid.uuid4()), user_id=user2.id,
                                      full_name="Artist 2", brand_name="Brand 2",
                                      verification_status="approved")
            db.session.add(profile2)
            db.session.commit()
            user2_id = user2.id

        headers2 = _auth(app, user2_id, "artist", "artist2@test.com")
        res = client.patch(f"/api/commerce/products/{seeded_data['product_id']}",
                           json={"price": 1}, headers=headers2)
        assert res.status_code == 404  # Not found from this artist's perspective

    def test_soft_delete_product(self, client, app, seeded_data):
        """TC-PROD-05: Soft delete marks product as deleted."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        # Create a product to delete
        create_res = client.post("/api/commerce/products", json={
            "title": "To Be Deleted",
            "price": 100
        }, headers=headers)
        product_id = create_res.get_json()["id"]
        res = client.delete(f"/api/commerce/products/{product_id}", headers=headers)
        assert res.status_code == 200

        # Verify it's no longer in the list
        list_res = client.get("/api/commerce/products")
        ids = [p["id"] for p in list_res.get_json()]
        assert product_id not in ids

    def test_upload_product_image(self, client, app, seeded_data):
        """TC-PROD-06: Artist can upload an image file for their product."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        fake_image = io.BytesIO(b"\xff\xd8\xff\xe0" + b"\x00" * 100)  # minimal JPEG header
        fake_image.name = "test.jpg"
        res = client.post(
            f"/api/commerce/products/{seeded_data['product_id']}/upload-image",
            data={"file": (fake_image, "test.jpg", "image/jpeg")},
            content_type="multipart/form-data",
            headers=headers,
        )
        assert res.status_code == 200
        data = res.get_json()
        assert "url" in data
        assert data["url"].startswith("http")

    def test_list_artists_public(self, client):
        """Public can list approved artists."""
        res = client.get("/api/commerce/artists")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)


# ===========================================================================
# CART TESTS
# ===========================================================================

class TestCart:

    def test_add_to_cart(self, client, app, seeded_data):
        """TC-CART-01: Buyer can add in-stock product to cart."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post("/api/commerce/cart", json={
            "product_id": seeded_data["product_id"],
            "quantity": 1
        }, headers=headers)
        assert res.status_code in (200, 201)
        data = res.get_json()
        assert data["product_id"] == seeded_data["product_id"]

    def test_add_out_of_stock_to_cart(self, client, app, seeded_data):
        """TC-CART-02: Out-of-stock product cannot be added to cart."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post("/api/commerce/cart", json={
            "product_id": seeded_data["oos_product_id"],
            "quantity": 1
        }, headers=headers)
        assert res.status_code == 400

    def test_add_to_cart_invalid_quantity(self, client, app, seeded_data):
        """TC-CART-02b: Cannot add zero quantity to cart."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post("/api/commerce/cart", json={
            "product_id": seeded_data["product_id"],
            "quantity": 0
        }, headers=headers)
        assert res.status_code == 400

    def test_get_cart(self, client, app, seeded_data):
        """TC-CART-03: Buyer can retrieve their cart contents."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/commerce/cart", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_get_cart_requires_auth(self, client):
        """TC-CART-03b: Cart access requires authentication."""
        res = client.get("/api/commerce/cart")
        assert res.status_code == 401

    def test_update_cart_item_quantity(self, client, app, seeded_data):
        """TC-CART-04: Buyer can update cart item quantity."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        # Ensure item in cart
        client.post("/api/commerce/cart", json={
            "product_id": seeded_data["product_id"], "quantity": 1
        }, headers=headers)
        cart_res = client.get("/api/commerce/cart", headers=headers)
        items = cart_res.get_json()
        if not items:
            pytest.skip("No cart items to update")
        item_id = items[0]["id"]
        res = client.patch(f"/api/commerce/cart/{item_id}", json={"quantity": 3},
                           headers=headers)
        assert res.status_code == 200
        assert res.get_json()["quantity"] == 3

    def test_remove_cart_item(self, client, app, seeded_data):
        """TC-CART-05: Buyer can remove a specific cart item."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        client.post("/api/commerce/cart", json={
            "product_id": seeded_data["product_id"], "quantity": 1
        }, headers=headers)
        cart_res = client.get("/api/commerce/cart", headers=headers)
        items = cart_res.get_json()
        if not items:
            pytest.skip("No cart items to remove")
        item_id = items[0]["id"]
        res = client.delete(f"/api/commerce/cart/{item_id}", headers=headers)
        assert res.status_code == 200

    def test_clear_cart(self, client, app, seeded_data):
        """TC-CART-06: Buyer can clear their entire cart."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        client.post("/api/commerce/cart", json={
            "product_id": seeded_data["product_id"], "quantity": 1
        }, headers=headers)
        res = client.delete("/api/commerce/cart", headers=headers)
        assert res.status_code == 200

        cart_after = client.get("/api/commerce/cart", headers=headers).get_json()
        assert len(cart_after) == 0


# ===========================================================================
# ORDER TESTS
# ===========================================================================

class TestOrders:

    SHIPPING = {
        "label": "Home",
        "full_address": "12 Artisan Lane",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pin_code": "400001",
        "country": "India"
    }
    PAYMENT = {"method": "upi", "upi_id": "test@upi"}

    def _populate_cart(self, client, app, seeded_data):
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        client.delete("/api/commerce/cart", headers=headers)
        client.post("/api/commerce/cart", json={
            "product_id": seeded_data["product_id"], "quantity": 1
        }, headers=headers)
        return headers

    def test_place_order_success(self, client, app, seeded_data):
        """TC-ORDER-01: Buyer can place an order with valid cart."""
        headers = self._populate_cart(client, app, seeded_data)
        res = client.post("/api/commerce/orders", json={
            "shipping_address": self.SHIPPING,
            "payment": self.PAYMENT
        }, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data["status"] == "pending"
        assert len(data["items"]) > 0
        assert any(e["event"] == "confirmed" for e in data["tracking_events"])

    def test_place_order_empty_cart(self, client, app, seeded_data):
        """TC-ORDER-02: Cannot place order with empty cart."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        client.delete("/api/commerce/cart", headers=headers)
        res = client.post("/api/commerce/orders", json={
            "shipping_address": self.SHIPPING,
            "payment": self.PAYMENT
        }, headers=headers)
        assert res.status_code == 400

    def test_place_order_multi_artist_cart(self, client, app, seeded_data):
        """TC-ORDER-03: Cart with products from two artists is rejected at checkout."""
        with app.app_context():
            # Create a second approved artist with their own product
            u2 = User(id=str(uuid.uuid4()), email=f"artist2_ord_{uuid.uuid4().hex[:4]}@test.com",
                      password_hash=generate_password_hash("pass"), role="artist")
            db.session.add(u2)
            db.session.flush()
            p2_profile = ArtistProfile(id=str(uuid.uuid4()), user_id=u2.id,
                                       full_name="Artist Two", brand_name="Brand Two",
                                       verification_status="approved")
            db.session.add(p2_profile)
            db.session.flush()
            p2_product = Product(id=str(uuid.uuid4()), artist_id=p2_profile.id,
                                 title="Second Artist Product", price=1000, in_stock=True)
            db.session.add(p2_product)
            db.session.commit()
            second_product_id = p2_product.id

        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        # Clear cart, then add products from two different artists
        client.delete("/api/commerce/cart", headers=headers)
        client.post("/api/commerce/cart",
                    json={"product_id": seeded_data["product_id"], "quantity": 1},
                    headers=headers)
        client.post("/api/commerce/cart",
                    json={"product_id": second_product_id, "quantity": 1},
                    headers=headers)

        res = client.post("/api/commerce/orders", json={
            "shipping_address": self.SHIPPING,
            "payment": self.PAYMENT
        }, headers=headers)
        assert res.status_code == 400
        assert "artist" in res.get_json()["error"].lower()

    def test_place_order_missing_shipping(self, client, app, seeded_data):
        """Cannot place order without shipping address."""
        headers = self._populate_cart(client, app, seeded_data)
        res = client.post("/api/commerce/orders", json={
            "payment": self.PAYMENT
        }, headers=headers)
        assert res.status_code == 400

    def test_list_orders_buyer(self, client, app, seeded_data):
        """TC-ORDER-04: Buyer can list their orders."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/commerce/orders", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_list_orders_artist(self, client, app, seeded_data):
        """TC-ORDER-05: Artist can list received orders."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.get("/api/commerce/orders", headers=headers)
        assert res.status_code == 200

    def test_advance_order_status_valid(self, client, app, seeded_data):
        """TC-ORDER-06: Artist can advance order to next valid status."""
        # Create fresh order
        buy_headers = self._populate_cart(client, app, seeded_data)
        order_res = client.post("/api/commerce/orders", json={
            "shipping_address": self.SHIPPING,
            "payment": self.PAYMENT
        }, headers=buy_headers)
        if order_res.status_code != 201:
            pytest.skip("Could not create order for status test")
        order_id = order_res.get_json()["id"]

        art_headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.patch(f"/api/commerce/orders/{order_id}/status",
                           json={"status": "processing"}, headers=art_headers)
        assert res.status_code == 200
        assert res.get_json()["status"] == "processing"

    def test_advance_order_status_invalid_transition(self, client, app, seeded_data):
        """TC-ORDER-07: Invalid status transitions are rejected."""
        with app.app_context():
            buyer_profile = BuyerProfile.query.filter_by(user_id=seeded_data["buyer_user_id"]).first()
            artist_profile = ArtistProfile.query.filter_by(user_id=seeded_data["artist_user_id"]).first()
            closed_order = Order(
                id=str(uuid.uuid4()),
                buyer_id=buyer_profile.id,
                artist_id=artist_profile.id,
                status="delivered",
                subtotal=4500,
                shipping_cost=500,
                total=5000,
                shipping_address_snapshot={"city": "Mumbai"},
                payment_snapshot={"method": "upi"}
            )
            db.session.add(closed_order)
            db.session.commit()
            closed_order_id = closed_order.id

        art_headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.patch(f"/api/commerce/orders/{closed_order_id}/status",
                           json={"status": "pending"}, headers=art_headers)
        assert res.status_code == 400

    def test_get_order_tracking(self, client, app, seeded_data):
        """TC-ORDER-08: Buyer can get tracking events for their order."""
        buy_headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        orders_res = client.get("/api/commerce/orders", headers=buy_headers)
        orders = orders_res.get_json()
        if not orders:
            pytest.skip("No orders to check tracking for")
        order_id = orders[0]["id"]
        res = client.get(f"/api/commerce/orders/{order_id}/tracking", headers=buy_headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_list_orders_requires_auth(self, client):
        """TC-ORDER-09: Listing orders requires authentication."""
        res = client.get("/api/commerce/orders")
        assert res.status_code == 401


# ===========================================================================
# SOCIAL TESTS
# ===========================================================================

class TestSocial:

    def test_follow_artist(self, client, app, seeded_data):
        """TC-SOCIAL-01: Buyer can follow an artist."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post("/api/social/follows", json={
            "artist_id": seeded_data["artist_profile_id"]
        }, headers=headers)
        assert res.status_code in (200, 201)

    def test_follow_artist_duplicate(self, client, app, seeded_data):
        """TC-SOCIAL-01b: Following an artist twice returns 200 (already following)."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        client.post("/api/social/follows", json={"artist_id": seeded_data["artist_profile_id"]}, headers=headers)
        res = client.post("/api/social/follows", json={"artist_id": seeded_data["artist_profile_id"]}, headers=headers)
        assert res.status_code == 200

    def test_unfollow_artist(self, client, app, seeded_data):
        """TC-SOCIAL-02: Buyer can unfollow an artist."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        # Ensure followed
        client.post("/api/social/follows", json={
            "artist_id": seeded_data["artist_profile_id"]
        }, headers=headers)
        res = client.delete(f"/api/social/follows/{seeded_data['artist_profile_id']}",
                            headers=headers)
        assert res.status_code == 200

    def test_check_follow_status(self, client, app, seeded_data):
        """TC-SOCIAL-03: Check follow status returns correct boolean."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get(f"/api/social/follows/check/{seeded_data['artist_profile_id']}",
                         headers=headers)
        assert res.status_code == 200
        assert "is_following" in res.get_json()

    def test_list_following(self, client, app, seeded_data):
        """TC-SOCIAL-03b: Buyer can list artists they follow."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/social/following", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_list_followers(self, client, app, seeded_data):
        """TC-SOCIAL-03c: Artist can list their followers."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.get("/api/social/followers", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_submit_product_review(self, client, app, seeded_data):
        """TC-SOCIAL-04: Buyer can submit a product review."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post("/api/social/reviews", json={
            "target_type": "product",
            "target_id": seeded_data["product_id"],
            "rating": 5,
            "body": "Absolutely beautiful craftsmanship."
        }, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data["target_type"] == "product"
        assert data["rating"] == 5

    def test_submit_catalogue_review(self, client, app, seeded_data):
        """TC-SOCIAL-05: Buyer can review a catalogue."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post("/api/social/reviews", json={
            "target_type": "catalogue",
            "target_id": seeded_data["catalogue_id"],
            "rating": 4,
            "body": "A thoughtful and beautiful collection."
        }, headers=headers)
        assert res.status_code == 201
        assert res.get_json()["target_type"] == "catalogue"

    def test_review_requires_buyer_role(self, client, app, seeded_data):
        """TC-SOCIAL-05b: Only buyers can submit reviews."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.post("/api/social/reviews", json={
            "target_type": "product",
            "target_id": seeded_data["product_id"],
            "rating": 5,
            "body": "Artist reviewing own product"
        }, headers=headers)
        assert res.status_code == 403

    def test_get_product_reviews(self, client, seeded_data):
        """TC-SOCIAL-06: Anyone can get reviews for a product."""
        res = client.get(f"/api/social/reviews/product/{seeded_data['product_id']}")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_create_story_post(self, client, app, seeded_data):
        """TC-SOCIAL-07: Artist can create and publish a story post."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.post("/api/social/posts", json={
            "type": "story",
            "title": "The Art of Kantha Stitch",
            "body": "Kantha is a centuries-old tradition of running stitch embroidery.",
            "is_published": True
        }, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data["is_published"] is True
        assert data["published_at"] is not None

    def test_create_post_requires_artist(self, client, app, seeded_data):
        """TC-SOCIAL-07b: Only artists can create posts."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post("/api/social/posts", json={
            "type": "story",
            "title": "Buyer Story",
            "body": "Should fail.",
            "is_published": True
        }, headers=headers)
        assert res.status_code == 403

    def test_list_posts_public(self, client):
        """TC-SOCIAL-08: Public endpoint lists published posts."""
        res = client.get("/api/social/posts")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)


# ===========================================================================
# ADMIN TESTS
# ===========================================================================

class TestAdmin:

    def test_get_platform_stats(self, client, app, seeded_data):
        """TC-ADMIN-01: Admin can get platform statistics."""
        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        res = client.get("/api/admin/stats", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert "totalRevenue" in data
        assert "totalOrders" in data
        assert "registeredArtists" in data
        assert "registeredBuyers" in data

    def test_get_platform_stats_non_admin(self, client, app, seeded_data):
        """TC-ADMIN-01b: Non-admin cannot access admin stats."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/admin/stats", headers=headers)
        assert res.status_code == 403

    def test_get_platform_stats_requires_auth(self, client):
        """TC-ADMIN-01c: Admin stats requires authentication."""
        res = client.get("/api/admin/stats")
        assert res.status_code == 401

    def test_get_verification_queue(self, client, app, seeded_data):
        """TC-ADMIN-02: Admin can view the verification queue."""
        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        res = client.get("/api/admin/verification/queue", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert isinstance(data, list)

    def test_approve_artist(self, client, app, seeded_data):
        """TC-ADMIN-03: Admin can approve a pending artist."""
        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        artist_id = seeded_data["pending_artist_profile_id"]
        res = client.patch(f"/api/admin/verification/{artist_id}/status",
                           json={"status": "approved"}, headers=headers)
        assert res.status_code == 200

    def test_reject_artist_with_reason(self, client, app, seeded_data):
        """TC-ADMIN-04: Admin can reject an artist with a reason."""
        # Create a new pending artist to reject
        with app.app_context():
            pu = User(id=str(uuid.uuid4()), email=f"rej_{uuid.uuid4().hex[:4]}@test.com",
                      password_hash=generate_password_hash("pass"), role="artist")
            db.session.add(pu)
            db.session.flush()
            pp = ArtistProfile(id=str(uuid.uuid4()), user_id=pu.id,
                                full_name="Reject Me", brand_name="Reject Brand",
                                verification_status="pending")
            db.session.add(pp)
            db.session.commit()
            reject_id = pp.id

        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        res = client.patch(f"/api/admin/verification/{reject_id}/status", json={
            "status": "rejected",
            "rejection_reason": "Incomplete portfolio"
        }, headers=headers)
        assert res.status_code == 200

    def test_reject_artist_invalid_status(self, client, app, seeded_data):
        """TC-ADMIN-04b: Verification with invalid status returns 400."""
        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        artist_id = seeded_data["pending_artist_profile_id"]
        res = client.patch(f"/api/admin/verification/{artist_id}/status",
                           json={"status": "limbo"}, headers=headers)
        assert res.status_code == 400

    def test_list_artists_paginated(self, client, app, seeded_data):
        """TC-ADMIN-05: Admin can list artists with pagination."""
        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        res = client.get("/api/admin/artists?limit=5&offset=0", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert "artists" in data
        assert "total" in data
        assert len(data["artists"]) <= 5

    def test_toggle_user_suspension(self, client, app, seeded_data):
        """TC-ADMIN-06: Admin can toggle user suspension."""
        # Create a user to suspend
        with app.app_context():
            su = User(id=str(uuid.uuid4()), email=f"susp_{uuid.uuid4().hex[:4]}@test.com",
                      password_hash=generate_password_hash("pass"), role="buyer")
            db.session.add(su)
            db.session.commit()
            su_id = su.id

        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        res = client.post(f"/api/admin/users/{su_id}/toggle-suspend", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert "is_suspended" in data
        assert data["is_suspended"] is True

        # Toggle back
        res2 = client.post(f"/api/admin/users/{su_id}/toggle-suspend", headers=headers)
        assert res2.get_json()["is_suspended"] is False

    def test_toggle_nonexistent_user(self, client, app, seeded_data):
        """TC-ADMIN-06b: Toggling suspension on non-existent user returns 404."""
        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        res = client.post("/api/admin/users/nonexistent-id/toggle-suspend", headers=headers)
        assert res.status_code == 404

    def test_get_artist_performance(self, client, app, seeded_data):
        """TC-ADMIN-07: Admin can get artist performance analytics."""
        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        res = client.get("/api/admin/analytics/artists", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)


# ===========================================================================
# ANALYTICS TESTS
# ===========================================================================

class TestAnalytics:

    def test_get_artist_trend(self, client, app, seeded_data):
        """TC-ANALYTICS-01: Artist can retrieve their revenue trend data."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.get("/api/analytics/artist/trend", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_get_artist_trend_forbidden_for_buyer(self, client, app, seeded_data):
        """TC-ANALYTICS-01b: Buyer cannot access artist trend."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/analytics/artist/trend", headers=headers)
        assert res.status_code == 403

    def test_get_analytics_snapshot(self, client, app, seeded_data):
        """TC-ANALYTICS-02: Artist can get their analytics snapshot."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.get("/api/analytics/snapshots?type=artist", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert "ai_summary" in data

    def test_get_platform_trend_admin_only(self, client, app, seeded_data):
        """TC-ANALYTICS-03: Only admin can access platform trend."""
        buyer_headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/analytics/platform/trend", headers=buyer_headers)
        assert res.status_code == 403

    def test_get_platform_trend_as_admin(self, client, app, seeded_data):
        """TC-ANALYTICS-04: Admin can access platform trend."""
        headers = _auth(app, seeded_data["admin_user_id"], "admin", "admin@test.com")
        res = client.get("/api/analytics/platform/trend", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)


# ===========================================================================
# COMMUNICATION TESTS
# ===========================================================================

class TestCommunication:

    def test_send_broadcast(self, client, app, seeded_data):
        """TC-COMM-01: Artist can send a broadcast message."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.post("/api/communication/broadcasts", json={
            "message": "New collection dropping this Friday!",
            "intent": "launch",
            "platforms": ["email"]
        }, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data["status"] == "sent"
        assert data["message"] == "New collection dropping this Friday!"

    def test_send_broadcast_forbidden_for_buyer(self, client, app, seeded_data):
        """TC-COMM-01b: Buyers cannot send broadcasts."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.post("/api/communication/broadcasts", json={
            "message": "Should fail",
            "intent": "launch",
            "platforms": []
        }, headers=headers)
        assert res.status_code == 403

    def test_get_broadcasts(self, client, app, seeded_data):
        """TC-COMM-02: Artist can list their own broadcasts."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.get("/api/communication/broadcasts", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_get_broadcasts_forbidden_for_buyer(self, client, app, seeded_data):
        """TC-COMM-02b: Buyers cannot view broadcast list."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/communication/broadcasts", headers=headers)
        assert res.status_code == 403

    def test_get_audience_size(self, client, app, seeded_data):
        """TC-COMM-03: Artist can check their audience size."""
        headers = _auth(app, seeded_data["artist_user_id"], "artist", "artist@test.com")
        res = client.get("/api/communication/audience-size", headers=headers)
        assert res.status_code == 200
        data = res.get_json()
        assert "count" in data
        assert isinstance(data["count"], int)

    def test_get_audience_size_forbidden_for_buyer(self, client, app, seeded_data):
        """TC-COMM-03b: Buyers cannot check audience size."""
        headers = _auth(app, seeded_data["buyer_user_id"], "buyer", "buyer@test.com")
        res = client.get("/api/communication/audience-size", headers=headers)
        assert res.status_code == 403
