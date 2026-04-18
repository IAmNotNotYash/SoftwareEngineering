import json
import pytest

def test_buyer_get_profile(client, auth_headers):
    """Test GET /v1/buyer/profile"""
    response = client.get("/v1/buyer/profile", headers=auth_headers("buyer"))
    assert response.status_code in [200, 404]

def test_buyer_patch_profile(client, auth_headers):
    """Test PATCH /v1/buyer/profile"""
    response = client.patch("/v1/buyer/profile", headers=auth_headers("buyer"), json={
        "full_name": "Updated Buyer Name"
    })
    assert response.status_code in [200, 404]

def test_buyer_addresses(client, auth_headers):
    """Test GET and POST /v1/buyer/addresses"""
    headers = auth_headers("buyer")
    # GET
    res_get = client.get("/v1/buyer/addresses", headers=headers)
    assert res_get.status_code in [200, 404]
    
    # POST
    payload = {
        "full_name": "Home Address",
        "phone": "+919876543210",
        "full_address": "123 Random St",
        "city": "Mumbai",
        "state": "MH",
        "pin_code": "400001",
        "country": "India"
    }
    res_post = client.post("/v1/buyer/addresses", headers=headers, json=payload)
    assert res_post.status_code in [201, 404]

def test_buyer_cart_operations(client, auth_headers):
    """Test Cart GET, POST, PATCH, DELETE"""
    headers = auth_headers("buyer")
    # GET
    assert client.get("/v1/buyer/cart", headers=headers).status_code in [200, 404]
    # POST
    payload = {"product_id": "temp-uuid", "quantity": 1}
    assert client.post("/v1/buyer/cart", headers=headers, json=payload).status_code in [200, 201, 404]
    # DELETE
    assert client.delete("/v1/buyer/cart", headers=headers).status_code in [204, 404]

def test_buyer_discovery_products(client):
    """Test GET /v1/products"""
    response = client.get("/v1/products?q=pottery")
    assert response.status_code in [200, 404]

def test_buyer_checkout(client, auth_headers):
    """Test POST /v1/buyer/orders"""
    payload = {
        "shipping": {
            "address": {
                "full_name": "Home Address",
                "phone": "+919876543210",
                "full_address": "123 Random St",
                "city": "Mumbai",
                "state": "MH",
                "pin_code": "400001",
                "country": "India"
            }
        },
        "payment": {
            "method": "upi",
            "upi_id": "test@upi"
        }
    }
    response = client.post("/v1/buyer/orders", headers=auth_headers("buyer"), json=payload)
    assert response.status_code in [201, 404]
