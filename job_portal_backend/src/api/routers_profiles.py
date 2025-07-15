"""Routers for user profile retrieval, update, and file (resume) upload."""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from .models import ProfileRead
from .auth_utils import oauth2_scheme, decode_access_token
from typing import Optional

router = APIRouter(
    prefix="/profile",
    tags=["profiles"]
)

profiles = []

# PUBLIC_INTERFACE
@router.get("/", response_model=ProfileRead, summary="Get logged-in user's profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    """Get the profile for the authenticated user."""
    payload = decode_access_token(token)
    user_id = int(payload["sub"])
    for p in profiles:
        if p["user_id"] == user_id:
            return p
    raise HTTPException(status_code=404, detail="Profile not found")

# PUBLIC_INTERFACE
@router.post("/", response_model=ProfileRead, summary="Create or update user profile")
async def create_or_update_profile(
    bio: Optional[str] = Form(None),
    company_info: Optional[str] = Form(None),
    resume: UploadFile = File(None),
    token: str = Depends(oauth2_scheme)
):
    """Create or update profile for authenticated user; supports file upload."""
    payload = decode_access_token(token)
    user_id = int(payload["sub"])
    # Replace or insert profile
    resume_url = None
    if resume:
        resume_url = f"/resumes/{resume.filename}"
    profile_data = {"id": user_id, "user_id": user_id, "bio": bio, "company_info": company_info, "resume_url": resume_url}
    global profiles
    profiles = [p for p in profiles if p["user_id"] != user_id]
    profiles.append(profile_data)
    return profile_data
