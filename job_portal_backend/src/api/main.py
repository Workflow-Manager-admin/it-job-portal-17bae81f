from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers_users import router as users_router
from .routers_jobs import router as jobs_router
from .routers_auth import router as auth_router
from .routers_applications import router as applications_router
from .routers_profiles import router as profiles_router

tags_metadata = [
    {"name": "auth", "description": "User registration and login"},
    {"name": "users", "description": "User info and management"},
    {"name": "jobs", "description": "Job search and employer posting"},
    {"name": "applications", "description": "Apply to jobs and view applications"},
    {"name": "profiles", "description": "Manage profiles and upload resumes"},
]

app = FastAPI(
    title="IT Job Portal Backend",
    description="RESTful API server for IT job seekers and employers – modular routers, JWT, docs, and ready for DB integration",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users_router)
app.include_router(jobs_router)
app.include_router(auth_router)
app.include_router(applications_router)
app.include_router(profiles_router)

@app.get("/", tags=["root"])
def health_check():
    """Health check route."""
    return {"message": "Healthy"}

# Error handler for HTTPException
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )
