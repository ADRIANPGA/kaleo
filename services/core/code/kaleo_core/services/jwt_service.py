from datetime import timedelta # Keep for timedelta if create_access_token logic moves here
from typing import Dict, Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status

from ..config import settings # For SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
# Assuming create_access_token is in middleware.auth as previously discussed.
# If we centralize all JWT logic here, we would move its implementation here.
from ..middleware.auth import create_access_token as auth_create_access_token 

class JWTService:
    def __init__(self, secret_key: str = settings.jwt_secret_key, algorithm: str = settings.jwt_algorithm):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        # This method can either reimplement token creation or call the existing one.
        # For now, let's assume it calls the existing one from middleware for consistency
        # until a full refactor of that middleware piece.
        # If expires_delta is not None, it would be passed to auth_create_access_token if it supports it,
        # or the logic in auth_create_access_token uses settings.ACCESS_TOKEN_EXPIRE_MINUTES.
        return auth_create_access_token(data=data, expires_delta=expires_delta)

    async def decode_access_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            # Specific errors like ExpiredSignatureError, JWTClaimsError can be caught too
            # For now, a general JWTError is caught.
            # The calling code should handle the None return and raise appropriate HTTPExceptions.
            return None
    
    async def get_user_id_from_token(self, token: str) -> Optional[str]:
        payload = await self.decode_access_token(token)
        if payload:
            return payload.get("user_id") # Assumes 'user_id' is in the token payload
        return None

# Dependency to get JWTService instance
async def get_jwt_service():
    return JWTService(secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

print("kaleo_core.services.jwt_service created.") 