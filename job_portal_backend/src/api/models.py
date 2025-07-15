"""
Defines core Pydantic and (future) SQLAlchemy models for the IT Job Portal.

Model classes include documentation for Auto-Generated OpenAPI schema/Swagger docs.

- User (UserCreate, UserRead, UserBase): Register, read and authenticate users. "role" must be "candidate" or "employer".
- Job (JobCreate, JobRead, JobBase): Job postings with key fields/skills, linked to an employer user.
- Application (ApplicationCreate, ApplicationRead): Applications to jobs with status and resume upload.
- Profile (ProfileRead, ProfileBase): Profile info for users, with support for employer/candidate specifics.

All docstrings are included for FastAPI's /docs autodoc.
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# PUBLIC_INTERFACE
class UserBase(BaseModel):
    """Base fields for user models.

    - username: Unique username
    - email: User email address
    - role: 'candidate' or 'employer'
    """
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
    """Base job fields for job posting and searching.

    - title: Job title
    - description: Full job description
    - location: City, state, remote, etc.
    - company: Employer's company name
    - posted_by: Employer user ID
    - skills: List of required skills (strings)
    """
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
    """Base application fields.

    - job_id: ID of the job being applied to
    - user_id: ID of the candidate applying
    - status: Application status (pending, reviewed, accepted, rejected)
    """
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
    """Candidate or employer profile.

    - user_id: Linked User ID
    - bio: User's bio (optional)
    - resume_url: Link to candidate resume (optional)
    - company_info: Employer-specific info (optional)
    """
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
    """Returned on successful login.

    - access_token: JWT string
    - token_type: 'bearer'
    """
    access_token: str
    token_type: str

# Response schema for error handling
class ErrorResponse(BaseModel):
    """Returned on error responses.

    - detail: Error message
    """
    detail: str
