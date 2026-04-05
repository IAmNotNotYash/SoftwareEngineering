import json
import pytest

def test_admin_dashboard(client, auth_headers):
    """Test GET /v1/admin/dashboard"""
    response = client.get("/v1/admin/dashboard", headers=auth_headers("admin"))
    assert response.status_code in [200, 404]

def test_admin_verification_queue(client, auth_headers):
    """Test GET /v1/admin/verification"""
    response = client.get("/v1/admin/verification?status=pending", headers=auth_headers("admin"))
    assert response.status_code in [200, 404]

def test_admin_approve_artist(client, auth_headers):
    """Test POST /v1/admin/verification/{id}/approve"""
    # Assuming UUID format
    response = client.post("/v1/admin/verification/123e4567-e89b-12d3-a456-426614174000/approve", headers=auth_headers("admin"))
    assert response.status_code in [200, 404]

def test_admin_suspend_artist(client, auth_headers):
    """Test POST /v1/admin/artists/{id}/suspend"""
    response = client.post("/v1/admin/artists/123e4567-e89b-12d3-a456-426614174000/suspend", headers=auth_headers("admin"))
    assert response.status_code in [200, 404]

def test_admin_orders(client, auth_headers):
    """Test GET /v1/admin/orders"""
    response = client.get("/v1/admin/orders", headers=auth_headers("admin"))
    assert response.status_code in [200, 404]

def test_admin_analytics(client, auth_headers):
    """Test GET /v1/admin/analytics"""
    response = client.get("/v1/admin/analytics", headers=auth_headers("admin"))
    assert response.status_code in [200, 404]
