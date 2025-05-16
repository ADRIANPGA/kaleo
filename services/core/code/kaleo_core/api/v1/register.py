from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from sqlalchemy.exc import IntegrityError

from kaleo_core_api_server.apis.register_api_base import BaseRegisterApi
from kaleo_core_api_server.models.register_request import RegisterRequest
from kaleo_core_api_server.models.user_profile import UserProfile
from kaleo_core_api_server.models.login_response_body import LoginResponseBody

# Imports from your auth middleware (if needed for hashing, etc.)
from ...middleware.auth import get_password_hash
from ...db.models.user import User
from ...db.models.auth_provider_type_enum import AuthProviderType
from ...db.database import get_db
from ...config import settings

# Import services
from ...services.user_service import UserService, get_user_service
from ...services.jwt_service import JWTService, get_jwt_service

logger = logging.getLogger(__name__)

class RegisterApiImpl(BaseRegisterApi):
    def __init__(self):
        self.user_service = get_user_service()
        # Store the dependency functions for later use
        self.get_db = get_db

    async def api_v1_auth_register_post(
        self,
        register_request: RegisterRequest,
    ) -> LoginResponseBody:
        try:
            # Get JWT service
            jwt_service = await get_jwt_service()
            
            # Get a database session using context manager
            async for db in self.get_db():
                logger.info(f"Processing registration request for email: {register_request.email}")

                # Validate request data
                if not register_request.email or not register_request.password:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email and password are required"
                    )

                existing_user = await self.user_service.get_user_by_email(db, register_request.email)
                if existing_user:
                    logger.warning(f"Registration attempt for existing email: {register_request.email}")
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Email already registered"
                    )

                # Hash password and create user
                try:
                    hashed_password = get_password_hash(register_request.password.get_secret_value())
                except Exception as hash_ex:
                    logger.error(f"Password hashing failed: {str(hash_ex)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Error processing password"
                    )
                
                try:
                    new_user = await self.user_service.create_user(
                        db=db,
                        email=register_request.email,
                        password_hash=hashed_password,
                        name=register_request.name if hasattr(register_request, 'name') else None,
                        auth_provider=AuthProviderType.local
                    )
                except IntegrityError as ie:
                    logger.error(f"Database integrity error during user creation: {str(ie)}")
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Could not create user due to data conflict"
                    )

                if not new_user:
                    logger.error("User creation failed without raising an exception")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Could not create user"
                    )

                # Generate JWT token
                try:
                    token_data = {"sub": new_user.email, "user_id": str(new_user.id)}
                    access_token, refresh_token = jwt_service.create_token_pair(token_data)
                except Exception as token_ex:
                    logger.error(f"Token generation failed: {str(token_ex)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Error generating authentication token"
                    )

                # Create response
                user_profile = UserProfile(
                    id=str(new_user.id),
                    email=new_user.email,
                    name=new_user.name if new_user.name else "",
                    auth_provider=AuthProviderType.local.value
                )

                logger.info(f"Successfully registered user: {register_request.email}")
                return LoginResponseBody(
                    access_token=access_token,
                    token_type="bearer",
                    expires_in=settings.access_token_expire_minutes * 60,  # Convert minutes to seconds
                    refresh_token=refresh_token,
                    user=user_profile
                )

        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as ex:
            logger.error(f"Unexpected error in registration implementation: {str(ex)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during registration"
            )

print("kaleo_core.api.v1.register created and populated with RegisterApiImpl.") 