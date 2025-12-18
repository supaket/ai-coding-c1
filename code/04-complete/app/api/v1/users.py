"""
Users API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import UserNotFoundError, UserAlreadyExistsError
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas import UserCreate, UserResponse, ErrorResponse

router = APIRouter()


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    """Dependency to get UserService instance."""
    repository = UserRepository(session)
    return UserService(repository)


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    responses={409: {"model": ErrorResponse}}
)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    try:
        user = await service.create_user(data)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={404: {"model": ErrorResponse}}
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Get user by ID."""
    try:
        user = await service.get_user(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
