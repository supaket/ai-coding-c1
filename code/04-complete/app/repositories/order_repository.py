"""
Order Repository - Data Access Layer
Lab 3 Complete: Clean separation of database operations.
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Order, OrderItem


class OrderRepository:
    """Repository for Order database operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, order: Order) -> Order:
        """Create a new order."""
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
    
    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """Get order by ID with items eagerly loaded."""
        query = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        user_id: Optional[int] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Order], int]:
        """
        Get orders with filtering and pagination.
        Returns (orders, total_count).
        """
        # Build conditions
        conditions = []
        if user_id is not None:
            conditions.append(Order.user_id == user_id)
        if status is not None:
            conditions.append(Order.status == status)
        
        # Count total
        count_query = select(func.count(Order.id))
        if conditions:
            count_query = count_query.where(*conditions)
        total = (await self.session.execute(count_query)).scalar() or 0
        
        # Get paginated results
        offset = (page - 1) * page_size
        query = (
            select(Order)
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        if conditions:
            query = query.where(*conditions)
        
        result = await self.session.execute(query)
        orders = list(result.scalars().all())
        
        return orders, total
    
    async def get_by_user_id(self, user_id: int) -> list[Order]:
        """Get all orders for a user with items loaded."""
        query = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def update(self, order: Order) -> Order:
        """Update an existing order."""
        await self.session.commit()
        await self.session.refresh(order)
        return order
    
    async def delete(self, order: Order) -> None:
        """Delete an order."""
        await self.session.delete(order)
        await self.session.commit()
