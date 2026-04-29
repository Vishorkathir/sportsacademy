"""Tests for health check endpoint."""

from httpx import AsyncClient


class TestHealth:
    """Test health check endpoint."""

    async def test_health_check(self, client: AsyncClient):
        """Test health endpoint returns ok status."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
