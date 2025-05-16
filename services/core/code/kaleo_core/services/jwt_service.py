from datetime import timedelta, datetime, timezone
from typing import Dict, Optional, Tuple

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
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: Dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_token_pair(self, data: Dict) -> Tuple[str, str]:
        """Create both access and refresh tokens"""
        access_token = self.create_access_token(data)
        refresh_token = self.create_refresh_token(data)
        return access_token, refresh_token

    async def decode_token(self, token: str, verify_type: Optional[str] = None) -> Optional[Dict]:
        """Decode and verify a token, optionally checking its type"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if verify_type and payload.get("type") != verify_type:
                return None
            return payload
        except JWTError:
            return None

    async def verify_refresh_token(self, token: str) -> Optional[Dict]:
        """Specifically verify a refresh token"""
        return await self.decode_token(token, verify_type="refresh")

    async def get_user_id_from_token(self, token: str) -> Optional[str]:
        payload = await self.decode_token(token)
        if payload:
            return payload.get("user_id")
        return None

# Dependency to get JWTService instance
async def get_jwt_service():
    return JWTService(secret_key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

print("kaleo_core.services.jwt_service created.") 