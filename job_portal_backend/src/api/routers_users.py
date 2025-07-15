"""Routers for user listing and retrieval (to be expanded for DB)."""

from fastapi import APIRouter, HTTPException
from .models import UserRead
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# In-memory sample data for demo only
users = [
    {"id": 1, "username": "alice", "email": "alice@email.com", "role": "candidate"},
    {"id": 2, "username": "employerX", "email": "employer@email.com", "role": "employer"},
    {"id": 3, "username": "bob", "email": "bob@email.com", "role": "candidate"},
    {"id": 4, "username": "hiringpro", "email": "hiringpro@email.com", "role": "employer"},
]

# PUBLIC_INTERFACE
@router.get("/", response_model=List[UserRead], summary="List all users")
def list_users():
    """Retrieve all users (admin/dev use; not in production)."""
    return users

# PUBLIC_INTERFACE
@router.get("/{user_id}", response_model=UserRead, summary="Get user by ID")
def get_user(user_id: int):
    """Retrieve a single user by ID."""
    for u in users:
        if u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")
