import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_trigger_sos(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/emergencies/sos",
        json={
            "location_lat": 34.0522,
            "location_lon": -118.2437,
            "is_anonymous": True,
            "severity": 5
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ACTIVE"
