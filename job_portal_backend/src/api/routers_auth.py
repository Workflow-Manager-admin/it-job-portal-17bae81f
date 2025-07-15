"""Routers for user registration, login, and JWT token handling."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .models import UserCreate, UserRead, Token
from .auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# In-memory user store for demonstration
users = [
    {"id": 1, "username": "alice", "email": "alice@email.com", "role": "candidate", "password": hash_password("password")},
    {"id": 2, "username": "employerX", "email": "employer@email.com", "role": "employer", "password": hash_password("password")},
]

def find_user_by_username(username: str):
    for u in users:
        if u["username"] == username:
            return u
    return None

# PUBLIC_INTERFACE
@router.post("/register", response_model=UserRead, summary="Register a new user", status_code=201)
def register(user: UserCreate):
    """Registers a new user; returns created user data."""
    if find_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    id_new = len(users) + 1
    new_user = user.dict()
    new_user["id"] = id_new
    new_user["password"] = hash_password(user.password)
    users.append(new_user)
    return {k: v for k, v in new_user.items() if k in ("id", "username", "email", "role")}

# PUBLIC_INTERFACE
@router.post("/login", response_model=Token, summary="Login and receive JWT token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with username/password. Returns JWT on success."""
    user = find_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user["id"]), "username": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}
