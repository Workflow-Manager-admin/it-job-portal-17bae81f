"""Routers for job search, filter, and employer job posting."""

from fastapi import APIRouter, HTTPException, Depends
from .models import JobCreate, JobRead, ErrorResponse
from .auth_utils import oauth2_scheme, decode_access_token
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

# Sample in-memory job list for demo (replace with DB)
jobs = [
    {
        "id": 1, "title": "Backend Developer", "description": "Python/FastAPI backend", "location": "Remote",
        "company": "TechSoft", "posted_by": 2, "skills": ["Python", "FastAPI"], "date_posted": datetime.utcnow(),
    }
]

# PUBLIC_INTERFACE
@router.get("/", response_model=List[JobRead], summary="Search and list jobs", responses={200: {"description": "List of jobs"}})
def search_jobs(location: str = None, skill: str = None):
    """Search for jobs, optionally by location or skill."""
    filtered = jobs
    if location:
        filtered = [j for j in filtered if j["location"].lower() == location.lower()]
    if skill:
        filtered = [j for j in filtered if skill.lower() in [s.lower() for s in j["skills"]]]
    return filtered

# PUBLIC_INTERFACE
@router.post("/", response_model=JobRead, summary="Post a new job (employer only)", responses={201: {"description": "Created job"}, 401: {"model": ErrorResponse}})
def post_job(job: JobCreate, token: str = Depends(oauth2_scheme)):
    """Employers post new jobs. JWT required, must have 'employer' role."""
    payload = decode_access_token(token)
    if payload.get("role") != "employer":
        raise HTTPException(status_code=401, detail="Only employers can post jobs")
    new_job = job.dict()
    new_job["id"] = len(jobs) + 1
    new_job["date_posted"] = datetime.utcnow()
    jobs.append(new_job)
    return new_job
