import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@finder.app",
            "password": "strongpassword123",
            "full_name": "John Smith",
            "role": "FIRST_RESPONDER"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@finder.app"
    assert "id" in data
    assert data["role"] == "FIRST_RESPONDER"

@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, test_user):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "medic@finder.app",
            "password": "securepass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_login_failure(async_client: AsyncClient, test_user):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "medic@finder.app",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
