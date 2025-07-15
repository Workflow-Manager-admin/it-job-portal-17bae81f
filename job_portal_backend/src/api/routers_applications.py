"""Routers for job application and candidate application tracking."""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from .models import ApplicationRead
from .auth_utils import oauth2_scheme, decode_access_token
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/applications",
    tags=["applications"]
)

applications = []

# PUBLIC_INTERFACE
@router.post("/", response_model=ApplicationRead, summary="Apply to a job")
async def apply_to_job(
    job_id: int = Form(...),
    user_id: int = Form(...),
    resume: UploadFile = File(None),
    token: str = Depends(oauth2_scheme)
):
    """Candidate applies to a job. File upload supported for resume."""
    payload = decode_access_token(token)
    if payload.get("role") != "candidate":
        raise HTTPException(status_code=401, detail="Only candidates can apply for jobs")
    resume_url = None
    if resume:
        # For demo, just use fixed-placeholding behavior.
        resume_url = f"/resumes/{resume.filename}"
    app_id = len(applications) + 1
    record = {
        "id": app_id, "job_id": job_id, "user_id": user_id,
        "status": "pending", "resume_url": resume_url, "applied_at": datetime.utcnow()
    }
    applications.append(record)
    return record

# PUBLIC_INTERFACE
@router.get("/", response_model=List[ApplicationRead], summary="List job applications")
def get_applications(job_id: int = None, user_id: int = None, token: str = Depends(oauth2_scheme)):
    """Return list of applications, filtered by job or user if provided."""
    result = applications
    if job_id:
        result = [a for a in result if a["job_id"] == job_id]
    if user_id:
        result = [a for a in result if a["user_id"] == user_id]
    return result
