import logging
from fastapi import HTTPException, status, Depends, Security, Request
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request as StarletteRequest
import contextvars

from kaleo_core_api_server.apis.users_api_base import BaseUsersApi
from kaleo_core_api_server.models.user_profile import UserProfile
from kaleo_core_api_server.security_api import get_token_BearerAuth
from kaleo_core_api_server.models.extra_models import TokenModel

# Imports for get_current_user_from_token_dependency
from ...db.database import get_db
from ...db.models.user import User
from ...services.user_service import UserService, get_user_service
from ...services.jwt_service import JWTService, get_jwt_service
from ...db.models.auth_provider_type_enum import AuthProviderType

logger = logging.getLogger(__name__)

# Dependency to get current user from token
async def get_current_user_from_token_dependency(
    token: str = Security(get_token_BearerAuth),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service)
) -> User:
    try:
        user_id = await jwt_service.get_user_id_from_token(token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - user_id missing or invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        return user
    except Exception as e:
        logger.error(f"Error in get_current_user_from_token_dependency: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

class UsersApiImpl(BaseUsersApi):
    def __init__(self):
        self.user_service = get_user_service()

    async def api_v1_users_me_get(self, token_BearerAuth: TokenModel) -> UserProfile:
        # Get JWT service to validate the token and extract user_id
        jwt_service = await get_jwt_service()
        user_id = await jwt_service.get_user_id_from_token(token_BearerAuth.sub)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get the user from the database
        async for db in get_db():
            user = await self.user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            logger.info(f"Successfully retrieved user profile for: {user.email}")
            return UserProfile(
                id=str(user.id),
                email=user.email,
                name=user.name if user.name else "",
                auth_provider=user.auth_provider.value
            )

# OAuth2PasswordBearer for token dependency
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login" 
)

print("kaleo_core.api.v1.users refactored to focus on user-specific endpoints.") 