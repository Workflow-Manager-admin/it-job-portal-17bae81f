"""
SQLAlchemy ORM models for the IT Job Portal.

Defines:
- User
- Job
- Application
- Profile
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    Table,
)
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .db import Base

class UserRoleEnum(enum.Enum):
    candidate = "candidate"
    employer = "employer"

class ApplicationStatusEnum(enum.Enum):
    pending = "pending"
    reviewed = "reviewed"
    accepted = "accepted"
    rejected = "rejected"

# ASSOCIATIONS

job_skills = Table(
    "job_skills",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id"), primary_key=True),
    Column("skill", String, primary_key=True),
)

# USER ORM model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(Enum(UserRoleEnum), nullable=False)
    hashed_password = Column(String(300), nullable=False)

    profile = relationship("Profile", uselist=False, back_populates="user")
    jobs = relationship("Job", back_populates="employer")
    applications = relationship("Application", back_populates="user")


# JOB ORM model
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    posted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_posted = Column(DateTime, default=datetime.utcnow, nullable=False)

    skills = relationship(
        "JobSkill", back_populates="job", cascade="all, delete-orphan"
    )
    employer = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


# JOB SKILL as separate table for 1-n relationship,
class JobSkill(Base):
    __tablename__ = "job_skills_assoc"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    skill = Column(String(64), nullable=False)
    job = relationship("Job", back_populates="skills")


# APPLICATION ORM model
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ApplicationStatusEnum), default=ApplicationStatusEnum.pending, nullable=False)
    resume_url = Column(String(1024), nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")


# PROFILE ORM model
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    resume_url = Column(String(1024), nullable=True)
    company_info = Column(Text, nullable=True)

    user = relationship("User", back_populates="profile")
