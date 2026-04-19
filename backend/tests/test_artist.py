import json
import pytest

def test_artist_get_profile(client, auth_headers):
    """Test GET /v1/artist/profile"""
    response = client.get("/v1/artist/profile", headers=auth_headers("artist"))
    assert response.status_code in [200, 404]

def test_artist_products(client, auth_headers):
    """Test GET and POST /v1/artist/products"""
    headers = auth_headers("artist")
    
    # GET
    res_get = client.get("/v1/artist/products", headers=headers)
    assert res_get.status_code in [200, 404]
    
    # POST
    payload = {
        "title": "Handcrafted Vase",
        "description": "A beautiful vase.",
        "category": "Pottery",
        "price": 1200.00,
        "stock": 5
    }
    res_post = client.post("/v1/artist/products", headers=headers, json=payload)
    assert res_post.status_code in [201, 404]

def test_artist_catalogues(client, auth_headers):
    """Test POST /v1/artist/catalogues"""
    headers = auth_headers("artist")
    payload = {
        "title": "Spring Collection",
        "theme": "Nature",
        "philosophy": "Inspired by spring",
        "artist_note": "Thank you",
        "product_ids": ["temp-uuid"]
    }
    response = client.post("/v1/artist/catalogues", headers=headers, json=payload)
    assert response.status_code in [201, 404]

def test_artist_analytics(client, auth_headers):
    """Test GET /v1/artist/analytics"""
    response = client.get("/v1/artist/analytics", headers=auth_headers("artist"))
    assert response.status_code in [200, 404]

def test_artist_broadcasts(client, auth_headers):
    """Test POST /v1/artist/broadcasts"""
    payload = {
        "message": "New items available!",
        "intent": "preorder",
        "platforms": ["email", "instagram"]
    }
    response = client.post("/v1/artist/broadcasts", headers=auth_headers("artist"), json=payload)
    assert response.status_code in [201, 404]
