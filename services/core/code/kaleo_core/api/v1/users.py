from datetime import timedelta
from fastapi import HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from kaleo_core_api_server.apis.default_api_base import BaseDefaultApi
from kaleo_core_api_server.models.user_profile import UserProfile
from kaleo_core_api_server.models.login_request import LoginRequest
from kaleo_core_api_server.models.login_response_body import LoginResponseBody
from kaleo_core_api_server.models.o_auth_token_request import OAuthTokenRequest

# Imports from your auth middleware
from ...middleware.auth import (
    verify_password,
    get_password_hash, 
)
from ...db.database import get_db
from ...db.models.user import User
from ...db.models.auth_provider_type_enum import AuthProviderType

# Import services and their dependency getters
from ...services.user_service import UserService, get_user_service
from ...services.jwt_service import JWTService, get_jwt_service
from ...services.oauth_service import OAuthService, get_oauth_service

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login" # Or your actual token URL
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

class UsersApiImpl(BaseDefaultApi):
    async def users_me_get(self, current_user: User = Security(get_current_user_from_token_dependency)) -> UserProfile:
        print(f"Executing custom users_me_get for user: {current_user.email}")
        return UserProfile(
            id=str(current_user.id),
            email=current_user.email,
            name=current_user.name if current_user.name else ""
        )

    async def auth_login_post(
        self, 
        login_request: LoginRequest, 
        db: AsyncSession = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service)
    ) -> LoginResponseBody:
        print(f"Executing custom auth_login_post for user: {login_request.username}")
        
        user = await user_service.get_user_by_email(db, login_request.username)
        
        if not user or user.auth_provider != AuthProviderType.LOCAL or not user.password_hash or not verify_password(login_request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = {"sub": user.email, "user_id": str(user.id)}
        access_token = jwt_service.create_access_token(data=token_data)
        
        return LoginResponseBody(
            token=access_token, 
            user=UserProfile(id=str(user.id), email=user.email, name=user.name if user.name else "")
        )

    async def _handle_oauth_login(
        self,
        provider_name: str,
        oauth_user_info: dict,
        db: AsyncSession,
        user_service: UserService,
        jwt_service: JWTService,
        auth_provider_enum: AuthProviderType
    ) -> LoginResponseBody:
        user_email = oauth_user_info["email"]
        user_name = oauth_user_info.get("name")
        provider_user_id = oauth_user_info["provider_user_id"]

        user: Optional[User] = None
        if auth_provider_enum == AuthProviderType.GOOGLE:
            if not oauth_user_info.get("email_verified", False):
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google email not verified")
            user = await user_service.find_or_create_google_user(
                db=db,
                email=user_email,
                name=user_name,
                provider_user_id=provider_user_id,
                email_verified=oauth_user_info.get("email_verified"),
                picture=oauth_user_info.get("picture"),
                hd=oauth_user_info.get("hd")
            )
            print(f"User processed via Google OAuth: {user_email}")
        elif auth_provider_enum == AuthProviderType.MICROSOFT:
            user = await user_service.find_or_create_microsoft_user(
                db=db,
                email=user_email,
                name=user_name,
                provider_user_id=provider_user_id,
                microsoft_tenant_id=oauth_user_info.get("microsoft_tenant_id"),
                upn=oauth_user_info.get("upn"),
                given_name=oauth_user_info.get("given_name"),
                family_name=oauth_user_info.get("family_name")
            )
            print(f"User processed via Microsoft OAuth: {user_email}")
        else:
            # Should not happen if called correctly
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unsupported OAuth provider in _handle_oauth_login")

        if not user: # Should be handled by service raising an error or returning a user
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User object not returned from service.")

        token_data = {"sub": user.email, "user_id": str(user.id), "provider": provider_name.lower()}
        access_token = jwt_service.create_access_token(data=token_data)
        
        return LoginResponseBody(
            token=access_token, 
            user=UserProfile(id=str(user.id), email=user.email, name=user.name if user.name else "")
        )

    async def auth_oauth_google_post(
        self, 
        o_auth_token_request: OAuthTokenRequest, 
        db: AsyncSession = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        oauth_service: OAuthService = Depends(get_oauth_service)
    ) -> LoginResponseBody:
        print(f"Executing custom auth_oauth_google_post with token: {o_auth_token_request.token[:20]}...")
        google_user_info = await oauth_service.verify_google_token(o_auth_token_request.token)
        return await self._handle_oauth_login(
            "Google", google_user_info, db, user_service, jwt_service, AuthProviderType.GOOGLE
        )

    async def auth_oauth_microsoft_post(
        self, 
        o_auth_token_request: OAuthTokenRequest, 
        db: AsyncSession = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        oauth_service: OAuthService = Depends(get_oauth_service)
    ) -> LoginResponseBody:
        print(f"Executing custom auth_oauth_microsoft_post with token: {o_auth_token_request.token[:20]}...")
        microsoft_user_info = await oauth_service.verify_microsoft_token(o_auth_token_request.token)
        return await self._handle_oauth_login(
            "Microsoft", microsoft_user_info, db, user_service, jwt_service, AuthProviderType.MICROSOFT
        )

print("kaleo_core.api.v1.users refactored to use UserService, JWTService, and OAuthService.") 