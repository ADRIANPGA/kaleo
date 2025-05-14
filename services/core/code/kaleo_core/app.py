from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .logging import logger

# Import your API implementation modules to ensure subclass registration
from .api.v1 import login, register, users 

# Import the auto-generated base classes and router
from kaleo_core_api_server.apis.login_api import router as LoginApiRouter
from kaleo_core_api_server.apis.register_api import router as RegisterApiRouter
from kaleo_core_api_server.apis.users_api import router as UsersApiRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Kaleo Core service")
    yield
    logger.info("Shutting down Kaleo Core service")

app = FastAPI(
    title="Kaleo Core",
    description="Core service for Kaleo platform",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(LoginApiRouter)
app.include_router(RegisterApiRouter)
app.include_router(UsersApiRouter)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(",") if settings.cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Kaleo Core FastAPI app configured with refactored API structure.") 