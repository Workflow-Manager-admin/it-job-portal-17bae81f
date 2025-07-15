"""Defines core Pydantic and (future) SQLAlchemy models for the IT Job Portal."""

from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# PUBLIC_INTERFACE
class UserBase(BaseModel):
    """Base fields for user models."""
    username: str = Field(..., description="Unique username")
    email: EmailStr = Field(..., description="User email address")
    role: Literal["candidate", "employer"] = Field(..., description="User role")

class UserCreate(UserBase):
    """Model for registering a new user."""
    password: str = Field(..., min_length=6, description="User password")

class UserRead(UserBase):
    """User info returned to frontend."""
    id: int = Field(..., description="Unique user ID")

class UserLogin(BaseModel):
    """User login credentials."""
    username: str
    password: str

# PUBLIC_INTERFACE
class JobBase(BaseModel):
    """Base job fields."""
    title: str = Field(..., description="Job title")
    description: str = Field(..., description="Full job description")
    location: str = Field(..., description="Location")
    company: str = Field(..., description="Hiring company")
    posted_by: int = Field(..., description="Employer user ID")
    skills: List[str] = Field(default=[], description="List of key skills")

class JobCreate(JobBase):
    """Job creation input."""
    pass

class JobRead(JobBase):
    """Job as seen by clients."""
    id: int = Field(..., description="Unique job ID")
    date_posted: datetime = Field(..., description="Date job was posted")

# PUBLIC_INTERFACE
class ApplicationBase(BaseModel):
    """Base application fields."""
    job_id: int
    user_id: int
    status: Literal["pending", "reviewed", "accepted", "rejected"] = "pending"

class ApplicationCreate(ApplicationBase):
    """Application input (candidates apply for jobs)."""
    resume_url: Optional[str] = None

class ApplicationRead(ApplicationBase):
    """Application as seen by frontend."""
    id: int
    resume_url: Optional[str]
    applied_at: datetime

# PUBLIC_INTERFACE
class ProfileBase(BaseModel):
    """Candidate or employer profile."""
    user_id: int = Field(..., description="Linked User ID")
    bio: Optional[str] = None
    resume_url: Optional[str] = Field(None, description="Resume file URL")
    company_info: Optional[str] = Field(None, description="Employer-specific info")

class ProfileCreate(ProfileBase):
    pass

class ProfileRead(ProfileBase):
    id: int

# Response schema for JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

# Response schema for error handling
class ErrorResponse(BaseModel):
    detail: str
