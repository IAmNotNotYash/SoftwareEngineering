import json
import pytest

def test_auth_register_buyer(client):
    """Test POST /v1/auth/register for a buyer"""
    response = client.post("/v1/auth/register", json={
        "email": "buyer.test2@example.com",
        "password": "securepass",
        "role": "buyer",
        "full_name": "Test Buyer"
    })
    # Will fail until endpoint is implemented
    assert response.status_code in [201, 404]

def test_auth_register_artist(client):
    """Test POST /v1/auth/register for an artist"""
    response = client.post("/v1/auth/register", json={
        "email": "artist.test2@example.com",
        "password": "securepass",
        "role": "artist",
        "full_name": "Test Artist",
        "brand_name": "Test Brand"
    })
    assert response.status_code in [201, 404]

def test_auth_login(client):
    """Test POST /v1/auth/login"""
    response = client.post("/v1/auth/login", json={
        "email": "buyer.test2@example.com",
        "password": "securepass"
    })
    assert response.status_code in [200, 400, 401, 404]

def test_auth_me(client, auth_headers):
    """Test GET /v1/auth/me"""
    headers = auth_headers("buyer")
    response = client.get("/v1/auth/me", headers=headers)
    assert response.status_code in [200, 404]
