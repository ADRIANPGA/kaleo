from datetime import timedelta
from fastapi import HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from kaleo_core_api_server.apis.login_api_base import BaseLoginApi
from kaleo_core_api_server.models.login_request import LoginRequest
from kaleo_core_api_server.models.login_response_body import LoginResponseBody
from kaleo_core_api_server.models.o_auth_token_request import OAuthTokenRequest
from kaleo_core_api_server.models.user_profile import UserProfile

# Imports from your auth middleware
from ...middleware.auth import verify_password
from ...db.database import get_db
from ...db.models.user import User
from ...db.models.auth_provider_type_enum import AuthProviderType
from ...config import settings

# Import services and their dependency getters
from ...services.user_service import UserService, get_user_service
from ...services.jwt_service import JWTService, get_jwt_service
from ...services.oauth_service import OAuthService, get_oauth_service

logger = logging.getLogger(__name__)

# This might be more general or defined elsewhere, but for now, placing it here
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

class LoginApiImpl(BaseLoginApi):
    def __init__(self):
        self.user_service = get_user_service()
        self.get_db = get_db

    async def api_v1_auth_login_post(
        self,
        login_request: LoginRequest,
    ) -> LoginResponseBody:
        try:
            jwt_service = await get_jwt_service()
            async for db in self.get_db():
                logger.info(f"Executing auth_login_post for user: {login_request.email}")
                user = await self.user_service.get_user_by_email(db, login_request.email)
                if not user or user.auth_provider != AuthProviderType.local or not user.password_hash or not verify_password(login_request.password.get_secret_value(), user.password_hash):
                    logger.warning(f"Failed login attempt for user: {login_request.email}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect email or password",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                token_data = {"sub": user.email, "user_id": str(user.id)}
                access_token, refresh_token = jwt_service.create_token_pair(token_data)
                logger.info(f"Successful login for user: {login_request.email}")
                return LoginResponseBody(
                    access_token=access_token,
                    token_type="bearer",
                    expires_in=settings.access_token_expire_minutes * 60,
                    refresh_token=refresh_token,
                    user=UserProfile(
                        id=str(user.id),
                        email=user.email,
                        name=user.name if user.name else "",
                        auth_provider=user.auth_provider.value
                    )
                )
        except HTTPException:
            raise
        except Exception as ex:
            logger.error(f"Unexpected error in login: {str(ex)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during login"
            )

    async def api_v1_auth_oauth_google_post(
        self,
        o_auth_token_request: OAuthTokenRequest,
        db: AsyncSession = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        oauth_service: OAuthService = Depends(get_oauth_service)
    ) -> LoginResponseBody:
        try:
            logger.info("Processing Google OAuth token request")
            google_user_info = await oauth_service.verify_google_token(o_auth_token_request.token)
            return await self._handle_oauth_login(
                "Google", google_user_info, db, user_service, jwt_service, AuthProviderType.google
            )
        except Exception as ex:
            logger.error(f"Error in Google OAuth: {str(ex)}", exc_info=True)
            raise

    async def api_v1_auth_oauth_microsoft_post(
        self, 
        o_auth_token_request: OAuthTokenRequest,
        db: AsyncSession = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        oauth_service: OAuthService = Depends(get_oauth_service)
    ) -> LoginResponseBody:
        try:
            logger.info("Processing Microsoft OAuth token request")
            microsoft_user_info = await oauth_service.verify_microsoft_token(o_auth_token_request.token)
            return await self._handle_oauth_login(
                "Microsoft", microsoft_user_info, db, user_service, jwt_service, AuthProviderType.microsoft
            )
        except Exception as ex:
            logger.error(f"Error in Microsoft OAuth: {str(ex)}", exc_info=True)
            raise

    async def _handle_oauth_login(
        self,
        provider_name: str,
        oauth_user_info: dict,
        db: AsyncSession,
        user_service: UserService,
        jwt_service: JWTService,
        auth_provider_enum: AuthProviderType
    ) -> LoginResponseBody:
        try:
            user_email = oauth_user_info["email"]
            user_name = oauth_user_info.get("name")
            provider_user_id = oauth_user_info["provider_user_id"]

            logger.info(f"Processing {provider_name} OAuth login for email: {user_email}")

            user: Optional[User] = None
            if auth_provider_enum == AuthProviderType.google:
                if not oauth_user_info.get("email_verified", False):
                    logger.warning(f"Unverified Google email attempt: {user_email}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Google email not verified"
                    )
                user = await user_service.find_or_create_google_user(
                    db=db,
                    email=user_email,
                    name=user_name,
                    provider_user_id=provider_user_id,
                    email_verified=oauth_user_info.get("email_verified"),
                    picture=oauth_user_info.get("picture"),
                    hd=oauth_user_info.get("hd")
                )
                logger.info(f"User processed via Google OAuth: {user_email}")
            elif auth_provider_enum == AuthProviderType.microsoft:
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
                logger.info(f"User processed via Microsoft OAuth: {user_email}")
            else:
                logger.error(f"Unsupported OAuth provider: {provider_name}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unsupported OAuth provider in _handle_oauth_login"
                )

            if not user:
                logger.error(f"User object not returned from service for {provider_name} OAuth")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="User object not returned from service"
                )

            token_data = {"sub": user.email, "user_id": str(user.id), "provider": provider_name.lower()}
            access_token, refresh_token = jwt_service.create_token_pair(token_data)
            
            return LoginResponseBody(
                access_token=access_token,
                token_type="bearer",
                expires_in=settings.access_token_expire_minutes * 60,
                refresh_token=refresh_token,
                user=UserProfile(
                    id=str(user.id),
                    email=user.email,
                    name=user.name if user.name else "",
                    auth_provider=user.auth_provider.value
                )
            )
        except HTTPException:
            raise
        except KeyError as ke:
            logger.error(f"Missing required OAuth field: {str(ke)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required OAuth field: {str(ke)}"
            )
        except Exception as ex:
            logger.error(f"Unexpected error in OAuth login: {str(ex)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during OAuth login"
            )

print("kaleo_core.api.v1.login created and populated.") 