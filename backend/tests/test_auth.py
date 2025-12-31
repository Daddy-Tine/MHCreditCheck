"""
Tests for authentication endpoints
"""
import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "testpassword123",
            "full_name": "New User",
            "role": "CONSUMER"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["success"] is True
    assert response.json()["data"]["email"] == "newuser@test.com"


def test_login_success(client, admin_user):
    """Test successful login"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@test.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert "access_token" in response.json()["data"]
    assert "refresh_token" in response.json()["data"]


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrong@test.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, admin_user):
    """Test getting current user info"""
    # First login to get token
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@test.com",
            "password": "testpassword"
        }
    )
    token = login_response.json()["data"]["access_token"]
    
    # Get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["email"] == "admin@test.com"

