"""
Product Repository - Data Access Layer
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product


class ProductRepository:
    """Repository for Product database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product: Product) -> Product:
        """Create a new product."""
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        query = select(Product).where(Product.id == product_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Product], int]:
        """Get products with optional filtering and pagination."""
        conditions = []
        if category:
            conditions.append(Product.category == category)

        # Count total
        count_query = select(func.count(Product.id))
        if conditions:
            count_query = count_query.where(*conditions)
        total = await self.session.execute(count_query)
        total = total.scalar() or 0

        # Get paginated results
        offset = (page - 1) * page_size
        query = (
            select(Product)
            .order_by(Product.name)
            .offset(offset)
            .limit(page_size)
        )
        if conditions:
            query = query.where(*conditions)

        result = await self.session.execute(query)
        products = list(result.scalars().all())

        return products, total

    async def get_low_stock(self, threshold: int = 10) -> list[Product]:
        """Get products with low stock."""
        query = (
            select(Product)
            .where(Product.stock < threshold)
            .order_by(Product.stock)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_stock(self, product_id: int, new_stock: int) -> Product | None:
        """Update product stock."""
        product = await self.get_by_id(product_id)
        if product:
            product.stock = new_stock
            await self.session.commit()
            await self.session.refresh(product)
        return product

    async def add_stock(self, product_id: int, quantity: int) -> Product | None:
        """Add to product stock."""
        product = await self.get_by_id(product_id)
        if product:
            product.stock += quantity
            await self.session.commit()
            await self.session.refresh(product)
        return product

    async def update(self, product: Product) -> Product:
        """Update a product."""
        await self.session.commit()
        await self.session.refresh(product)
        return product
