"""
Integration Tests for Orders API
Lab 4 Complete: Testing API endpoints end-to-end.
"""

import pytest


class TestCreateOrderAPI:
    """Tests for POST /api/v1/orders."""
    
    @pytest.mark.asyncio
    async def test_create_order_success(self, client):
        """Should create order and return 201."""
        response = await client.post("/api/v1/orders", json={
            "user_id": 1,
            "shipping_address": "123 Test St",
            "items": [
                {"product_id": 1, "quantity": 2}
            ]
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == 1
        assert data["status"] == "pending"
        assert "id" in data
        assert len(data["items"]) == 1
    
    @pytest.mark.asyncio
    async def test_create_order_without_items_fails(self, client):
        """Should return 422 when items are missing."""
        response = await client.post("/api/v1/orders", json={
            "user_id": 1,
            "shipping_address": "123 Test St",
            "items": []
        })
        
        assert response.status_code == 422


class TestGetOrderAPI:
    """Tests for GET /api/v1/orders/{id}."""
    
    @pytest.mark.asyncio
    async def test_get_order_success(self, client, sample_order):
        """Should return order details."""
        response = await client.get(f"/api/v1/orders/{sample_order.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_order.id
        assert data["user_id"] == sample_order.user_id
        assert "items" in data
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_order_returns_404(self, client):
        """Should return 404 for invalid ID."""
        response = await client.get("/api/v1/orders/99999")
        
        assert response.status_code == 404


class TestListOrdersAPI:
    """Tests for GET /api/v1/orders."""
    
    @pytest.mark.asyncio
    async def test_list_orders_with_pagination(self, client, multiple_orders):
        """Should return paginated orders."""
        response = await client.get("/api/v1/orders", params={"page": 1, "page_size": 2})
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 2
    
    @pytest.mark.asyncio
    async def test_list_orders_filter_by_user(self, client, multiple_orders):
        """Should filter by user_id."""
        response = await client.get("/api/v1/orders", params={"user_id": 1})
        
        assert response.status_code == 200
        data = response.json()
        assert all(o["user_id"] == 1 for o in data["items"])


class TestUpdateOrderAPI:
    """Tests for PATCH /api/v1/orders/{id}."""
    
    @pytest.mark.asyncio
    async def test_update_status_success(self, client, sample_order):
        """Should update order status."""
        response = await client.patch(
            f"/api/v1/orders/{sample_order.id}",
            json={"status": "confirmed"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "confirmed"
    
    @pytest.mark.asyncio
    async def test_invalid_status_transition_returns_400(self, client, sample_order):
        """Should return 400 for invalid transition."""
        response = await client.patch(
            f"/api/v1/orders/{sample_order.id}",
            json={"status": "delivered"}  # Can't skip from pending to delivered
        )
        
        assert response.status_code == 400


class TestCancelOrderAPI:
    """Tests for POST /api/v1/orders/{id}/cancel."""
    
    @pytest.mark.asyncio
    async def test_cancel_order_success(self, client, sample_order):
        """Should cancel order."""
        response = await client.post(f"/api/v1/orders/{sample_order.id}/cancel")
        
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"
    
    @pytest.mark.asyncio
    async def test_cancel_nonexistent_order_returns_404(self, client):
        """Should return 404 for invalid ID."""
        response = await client.post("/api/v1/orders/99999/cancel")
        
        assert response.status_code == 404


class TestUserOrdersAPI:
    """Tests for GET /api/v1/users/{id}/orders."""
    
    @pytest.mark.asyncio
    async def test_get_user_orders(self, client, multiple_orders):
        """Should return all orders for a user."""
        response = await client.get("/api/v1/users/1/orders")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(o["user_id"] == 1 for o in data)


class TestHealthAPI:
    """Tests for GET /api/v1/health."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Should return healthy status."""
        response = await client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "order-service"
