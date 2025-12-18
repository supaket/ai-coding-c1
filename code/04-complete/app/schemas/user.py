"""
Pydantic Schemas for User API
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Request schema for creating a user."""
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=100, description="User name")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "name": "John Doe"
            }
        }
    )


class UserResponse(BaseModel):
    """Response schema for user."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    created_at: datetime
