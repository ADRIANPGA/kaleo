from fastapi import HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from kaleo_core_api_server.apis.users_api_base import BaseUsersApi
from kaleo_core_api_server.models.user_profile import UserProfile

# Imports for get_current_user_from_token_dependency
from ...db.database import get_db
from ...db.models.user import User
from ...services.user_service import UserService, get_user_service
from ...services.jwt_service import JWTService, get_jwt_service

# OAuth2PasswordBearer for token dependency
# The tokenUrl here should ideally point to your actual login/token endpoint.
# If it's now /api/v1_generated/auth/login (due to default_api_router prefix)
# or something else, it should be updated. For now, keeping it as it was,
# but this is a common point of configuration.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login" 
)

# Updated dependency for getting the current user
async def get_current_user_from_token_dependency(
    token: str = Depends(reusable_oauth2),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service)
) -> User:
    user_id = await jwt_service.get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - user_id missing or invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

class UsersApiImpl(BaseUsersApi):
    async def users_me_get(self, current_user: User = Security(get_current_user_from_token_dependency)) -> UserProfile:
        print(f"Executing custom users_me_get for user: {current_user.email}")
        return UserProfile(
            id=str(current_user.id),
            email=current_user.email,
            name=current_user.name if current_user.name else ""
        )

print("kaleo_core.api.v1.users refactored to focus on user-specific endpoints.") 