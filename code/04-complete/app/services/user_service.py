"""
User Service - Business Logic Layer
"""

from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate
from app.core.exceptions import UserNotFoundError, UserAlreadyExistsError


class UserService:
    """Service layer for user business logic."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, data: UserCreate) -> User:
        """Create a new user."""
        # Check if email already exists
        existing = await self.repository.get_by_email(data.email)
        if existing:
            raise UserAlreadyExistsError(data.email)

        user = User(
            email=data.email,
            name=data.name
        )
        return await self.repository.create(user)

    async def get_user(self, user_id: int) -> User:
        """Get user by ID."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user
