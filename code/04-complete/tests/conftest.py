"""
Test Configuration - Pytest Fixtures
Lab 4 Complete: Test setup with async database.
"""

import pytest
import pytest_asyncio
from decimal import Decimal
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.database import Base, get_async_session
from app.models import Order, OrderItem, OrderStatus


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine):
    """Create test database session."""
    async_session = async_sessionmaker(
        test_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(test_session):
    """Create test client with overridden database."""
    
    async def override_get_session():
        yield test_session
    
    app.dependency_overrides[get_async_session] = override_get_session
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_order(test_session) -> Order:
    """Create a sample order for testing."""
    order = Order(
        user_id=1,
        status=OrderStatus.PENDING.value,
        total=Decimal("149.98"),
        shipping_address="123 Test St"
    )
    order.items.append(OrderItem(
        product_id=1,
        product_name="Test Product",
        quantity=2,
        unit_price=Decimal("74.99")
    ))
    
    test_session.add(order)
    await test_session.commit()
    await test_session.refresh(order)
    
    return order


@pytest_asyncio.fixture
async def multiple_orders(test_session) -> list[Order]:
    """Create multiple orders for pagination testing."""
    orders = []
    
    for i in range(5):
        order = Order(
            user_id=1 if i < 3 else 2,
            status=OrderStatus.PENDING.value if i < 2 else OrderStatus.CONFIRMED.value,
            total=Decimal(f"{100 + i * 50}.00"),
            shipping_address=f"Address {i+1}"
        )
        order.items.append(OrderItem(
            product_id=i + 1,
            product_name=f"Product {i+1}",
            quantity=1,
            unit_price=Decimal(f"{100 + i * 50}.00")
        ))
        orders.append(order)
    
    test_session.add_all(orders)
    await test_session.commit()
    
    for order in orders:
        await test_session.refresh(order)
    
    return orders
