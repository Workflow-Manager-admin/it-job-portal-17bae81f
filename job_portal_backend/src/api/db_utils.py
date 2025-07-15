"""
Provides CRUD utility functions for User, Job, Application, and Profile using SQLAlchemy ORM.
Designed for use in FastAPI dependency-injection handlers.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .db_models import User, Job, Application, Profile, JobSkill, UserRoleEnum, ApplicationStatusEnum

# -------------------- USERS --------------------

# PUBLIC_INTERFACE
async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Return a User by id."""
    q = await db.execute(select(User).where(User.id == user_id))
    return q.scalar_one_or_none()

# PUBLIC_INTERFACE
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Return User by username."""
    q = await db.execute(select(User).where(User.username == username))
    return q.scalar_one_or_none()

# PUBLIC_INTERFACE
async def list_users(db: AsyncSession) -> List[User]:
    """Return all users."""
    q = await db.execute(select(User))
    return q.scalars().all()

# PUBLIC_INTERFACE
async def create_user(db: AsyncSession, username: str, email: str, hashed_password: str, role: UserRoleEnum) -> User:
    """Create and return new User."""
    user = User(username=username, email=email, hashed_password=hashed_password, role=role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# ---------------- JOBS ----------------

# PUBLIC_INTERFACE
async def list_jobs(db: AsyncSession, location: Optional[str] = None, skill: Optional[str] = None) -> List[Job]:
    """List jobs, filter by location and/or skill."""
    stmt = select(Job).options(selectinload(Job.skills))
    if location:
        stmt = stmt.where(Job.location == location)
    jobs = (await db.execute(stmt)).scalars().all()
    if skill:
        jobs = [j for j in jobs if any(js.skill.lower() == skill.lower() for js in j.skills)]
    return jobs

# PUBLIC_INTERFACE
async def get_job_by_id(db: AsyncSession, job_id: int) -> Optional[Job]:
    """Get job by ID."""
    q = await db.execute(select(Job).options(selectinload(Job.skills)).where(Job.id == job_id))
    return q.scalar_one_or_none()

# PUBLIC_INTERFACE
async def create_job(db: AsyncSession, title: str, description: str, location: str, company: str, posted_by: int, skills: List[str]) -> Job:
    """Create new job and return Job object."""
    job = Job(title=title, description=description, location=location, company=company, posted_by=posted_by)
    db.add(job)
    await db.flush()
    # Add job skills (after flush, so job.id exists)
    for s in skills:
        db.add(JobSkill(job_id=job.id, skill=s))
    await db.commit()
    await db.refresh(job)
    return job

# ---------------- APPLICATIONS ----------------

# PUBLIC_INTERFACE
async def create_application(db: AsyncSession, user_id: int, job_id: int, resume_url: Optional[str], status: ApplicationStatusEnum = ApplicationStatusEnum.pending) -> Application:
    """Create an application and return."""
    app = Application(user_id=user_id, job_id=job_id, resume_url=resume_url, status=status)
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return app

# PUBLIC_INTERFACE
async def list_applications(db: AsyncSession, job_id: Optional[int] = None, user_id: Optional[int] = None) -> List[Application]:
    """Return applications filtered by job or user."""
    stmt = select(Application)
    if job_id:
        stmt = stmt.where(Application.job_id == job_id)
    if user_id:
        stmt = stmt.where(Application.user_id == user_id)
    q = await db.execute(stmt)
    return q.scalars().all()

# PUBLIC_INTERFACE
async def get_application_by_id(db: AsyncSession, app_id: int) -> Optional[Application]:
    """Get single application by ID."""
    q = await db.execute(select(Application).where(Application.id == app_id))
    return q.scalar_one_or_none()

# ---------------- PROFILE ----------------

# PUBLIC_INTERFACE
async def get_profile_by_user_id(db: AsyncSession, user_id: int) -> Optional[Profile]:
    """Get profile by user ID."""
    q = await db.execute(select(Profile).where(Profile.user_id == user_id))
    return q.scalar_one_or_none()

# PUBLIC_INTERFACE
async def upsert_profile(db: AsyncSession, user_id: int, bio: Optional[str], resume_url: Optional[str], company_info: Optional[str]) -> Profile:
    """Create or update the profile associated with a user."""
    q = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = q.scalar_one_or_none()
    if profile:
        profile.bio = bio
        profile.resume_url = resume_url
        profile.company_info = company_info
    else:
        profile = Profile(user_id=user_id, bio=bio, resume_url=resume_url, company_info=company_info)
        db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile
