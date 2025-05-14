from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .logging import logger

# Import your API implementation modules to ensure subclass registration
from .api.v1 import init, users 

# Import the auto-generated router
from kaleo_core_api_server.apis.default_api import router as default_api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Kaleo Core service")
    # Ensure API implementations are loaded (already done by top-level imports)
    logger.info(f"BaseDefaultApi subclasses: {users.BaseDefaultApi.subclasses}") 
    yield
    logger.info("Shutting down Kaleo Core service")

app = FastAPI(
    title="Kaleo Core",
    description="Core service for Kaleo platform",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(",") if settings.cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auto-generated default API router
# This router will use the implementations from .api.v1.users (and others)
app.include_router(default_api_router) # You might want a prefix, e.g., prefix="/api/v1_generated"

# Remove or comment out the old router inclusions if they are no longer needed:
# app.include_router(init.router, prefix="/api/v1", tags=["init"])
# app.include_router(users.router, prefix="/api/v1", tags=["users"])

logger.info("Kaleo Core FastAPI app configured.") 