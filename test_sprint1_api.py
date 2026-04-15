import pytest

from app import create_app, db
from app.models.commerce import CartItem, Order, Product
from app.models.user import ArtistProfile, User


@pytest.fixture()
def app():
    application = create_app()
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
    )

    with application.app_context():
        db.drop_all()
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def seeded_accounts(app, client):
    buyer_payload = {
        'email': 'buyer@example.com',
        'password': 'buyerpass123',
        'role': 'buyer',
        'firstName': 'Bala',
        'lastName': 'Buyer',
    }
    artist_payload = {
        'email': 'artist@example.com',
        'password': 'artistpass123',
        'role': 'artist',
        'firstName': 'Anya',
        'lastName': 'Artist',
        'brandName': 'Anya Crafts',
    }

    buyer_register = client.post('/api/auth/register', json=buyer_payload)
    artist_register = client.post('/api/auth/register', json=artist_payload)

    assert buyer_register.status_code == 201
    assert artist_register.status_code == 201

    with app.app_context():
        artist_user = User.query.filter_by(email='artist@example.com').first()
        artist_user.artist_profile.verification_status = 'approved'

        admin_user = User(email='admin@example.com', role='admin')
        admin_user.set_password('adminpass123')
        db.session.add(admin_user)
        db.session.commit()

        artist_profile = ArtistProfile.query.filter_by(user_id=artist_user.id).first()

    buyer_login = client.post(
        '/api/auth/login',
        json={'email': 'buyer@example.com', 'password': 'buyerpass123'},
    )
    artist_login = client.post(
        '/api/auth/login',
        json={'email': 'artist@example.com', 'password': 'artistpass123'},
    )
    admin_login = client.post(
        '/api/auth/login',
        json={'email': 'admin@example.com', 'password': 'adminpass123'},
    )

    assert buyer_login.status_code == 200
    assert artist_login.status_code == 200
    assert admin_login.status_code == 200

    return {
        'buyer_token': buyer_login.get_json()['token'],
        'artist_token': artist_login.get_json()['token'],
        'admin_token': admin_login.get_json()['token'],
        'artist_profile_id': artist_profile.id,
    }


def auth_header(token):
    return {'Authorization': f'Bearer {token}'}


def test_health_endpoint_returns_ok(client):
    response = client.get('/health')

    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok'}


def test_register_buyer_returns_token_and_profile(client):
    payload = {
        'email': 'freshbuyer@example.com',
        'password': 'securepass123',
        'role': 'buyer',
        'firstName': 'Fresh',
        'lastName': 'Buyer',
    }

    response = client.post('/api/auth/register', json=payload)
    body = response.get_json()

    assert response.status_code == 201
    assert body['message'] == 'Account created successfully'
    assert body['user']['email'] == payload['email']
    assert body['user']['role'] == 'buyer'
    assert body['token']


def test_register_payload_from_old_yaml_shape_is_rejected(client):
    payload = {
        'email': 'legacydoc@example.com',
        'password': 'securepass123',
        'role': 'artist',
        'full_name': 'Legacy Artist',
        'brand_name': 'Legacy Brand',
    }

    response = client.post('/api/auth/register', json=payload)

    assert response.status_code == 400
    assert response.get_json() == {'error': 'Missing required fields'}


def test_artist_can_create_product_after_approval(client, seeded_accounts):
    payload = {
        'title': 'Terracotta Vase',
        'description': 'Handmade vase fired in a wood kiln.',
        'price': 1499,
        'category': 'Home Decor',
        'images': ['https://example.com/vase.jpg'],
    }

    response = client.post(
        '/api/commerce/products',
        json=payload,
        headers=auth_header(seeded_accounts['artist_token']),
    )
    body = response.get_json()

    assert response.status_code == 201
    assert body['title'] == payload['title']
    assert body['price'] == 1499.0
    assert body['artist_name'] == 'Anya Crafts'


def test_buyer_can_add_product_to_cart(client, app, seeded_accounts):
    with app.app_context():
        product = Product.query.first()
        if product is None:
            artist = db.session.get(ArtistProfile, seeded_accounts['artist_profile_id'])
            product = Product(
                artist_id=artist.id,
                title='Handwoven Basket',
                price=899,
                category='Storage',
            )
            db.session.add(product)
            db.session.commit()
        product_id = product.id

    response = client.post(
        '/api/commerce/cart',
        json={'product_id': product_id, 'quantity': 2},
        headers=auth_header(seeded_accounts['buyer_token']),
    )
    body = response.get_json()

    assert response.status_code == 201
    assert body['product_id'] == product_id
    assert body['quantity'] == 2


def test_buyer_can_place_order_from_cart(client, app, seeded_accounts):
    with app.app_context():
        product = Product.query.first()
        if product is None:
            artist = db.session.get(ArtistProfile, seeded_accounts['artist_profile_id'])
            product = Product(
                artist_id=artist.id,
                title='Clay Lamp',
                price=650,
                category='Lighting',
            )
            db.session.add(product)
            db.session.commit()
        product_id = product.id

    add_response = client.post(
        '/api/commerce/cart',
        json={'product_id': product_id, 'quantity': 1},
        headers=auth_header(seeded_accounts['buyer_token']),
    )
    assert add_response.status_code in (200, 201)

    payload = {
        'shipping_address': {
            'label': 'Home',
            'full_address': '12 Market Street',
            'city': 'Chennai',
            'state': 'Tamil Nadu',
            'pin_code': '600001',
            'country': 'India',
        },
        'payment': {
            'method': 'card',
            'card_type': 'Visa',
            'last_4': '4242',
            'expiry_month': '12',
            'expiry_year': '2030',
        },
    }

    response = client.post(
        '/api/commerce/orders',
        json=payload,
        headers=auth_header(seeded_accounts['buyer_token']),
    )
    body = response.get_json()

    assert response.status_code == 201
    assert body['status'] == 'pending'
    assert body['shipping_cost'] == 500.0
    assert len(body['items']) == 1
    assert body['tracking_events'][0]['event'] == 'confirmed'

    with app.app_context():
        assert Order.query.count() == 1
        assert CartItem.query.count() == 0


def test_admin_stats_endpoint_returns_counts(client, seeded_accounts):
    response = client.get(
        '/api/admin/stats',
        headers=auth_header(seeded_accounts['admin_token']),
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body['registeredArtists'] == 1
    assert body['registeredBuyers'] == 1
    assert body['pendingVerifications'] == 0
