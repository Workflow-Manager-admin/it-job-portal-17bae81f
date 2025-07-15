"""
Database setup and utility functions using SQLAlchemy for the IT Job Portal backend.

- Sets up the SQLite database connection.
- Defines the async session creator.
- Provides basic utility for database initialization.
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

DATABASE_URL = "sqlite+aiosqlite:///./job_portal.db"

# Create the async engine
engine: AsyncEngine = create_async_engine(
    DATABASE_URL, echo=True, future=True, poolclass=NullPool
)

# Base class for ORM models
Base = declarative_base()

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# PUBLIC_INTERFACE
async def get_async_session() -> AsyncSession:
    """Yields an async SQLAlchemy session."""
    async with AsyncSessionLocal() as session:
        yield session

# PUBLIC_INTERFACE
async def init_db():
    """Initialize database tables. Should be called at startup for migrations (dev) or use Alembic for prod."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
