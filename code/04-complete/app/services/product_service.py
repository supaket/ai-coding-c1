"""
Product Service - Business Logic Layer
"""

from typing import List, Tuple, Optional
from decimal import Decimal

from app.models import Product
from app.repositories.product_repository import ProductRepository
from app.schemas import ProductCreate, BulkRestockRequest
from app.core.exceptions import ProductNotFoundError


class ProductService:
    """Service layer for product business logic."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, data: ProductCreate) -> Product:
        """Create a new product."""
        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            stock=data.stock,
            category=data.category
        )
        return await self.repository.create(product)

    async def get_product(self, product_id: int) -> Product:
        """Get product by ID."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    async def list_products(
        self,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Product], int]:
        """List products with optional filtering."""
        return await self.repository.get_all(
            category=category,
            page=page,
            page_size=page_size
        )

    async def get_low_stock_items(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock."""
        return await self.repository.get_low_stock(threshold)

    async def update_stock(self, product_id: int, new_stock: int) -> Product:
        """Update product stock."""
        product = await self.repository.update_stock(product_id, new_stock)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    async def bulk_restock(self, data: BulkRestockRequest) -> List[Product]:
        """Bulk restock multiple products."""
        updated_products = []
        for item in data.items:
            product = await self.repository.add_stock(item.product_id, item.quantity)
            if not product:
                raise ProductNotFoundError(item.product_id)
            updated_products.append(product)
        return updated_products
