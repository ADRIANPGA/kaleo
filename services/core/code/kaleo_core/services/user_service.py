from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Dict
from datetime import datetime, timezone

from ..db.models.user import User
from ..db.models.auth_provider_type_enum import AuthProviderType
from ..db.models.user_google_details import UserGoogleDetails
from ..db.models.user_microsoft_details import UserMicrosoftDetails
from fastapi import HTTPException, status

class UserService:
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, db: AsyncSession, user_id: str) -> Optional[User]:
        # Assuming user_id is a UUID string and User.id is the primary key
        # If User.id is not directly queryable by db.get with a string, adjust as needed
        # For example, if User.id needs to be cast to UUID:
        # from uuid import UUID
        # user = await db.get(User, UUID(user_id))
        # However, usually SQLAlchemy handles the type conversion if the column type is UUID.
        # Let's assume db.get works directly or use select for clarity if User.id is not the PK name for get.
        # For now, using select to be explicit, similar to get_user_by_email
        stmt = select(User).where(User.id == user_id) # type: ignore[attr-defined] # SQLAlchemy dynamically adds attributes like id
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        db: AsyncSession,
        email: str,
        password_hash: Optional[str] = None,
        name: Optional[str] = None,
        auth_provider: AuthProviderType = AuthProviderType.local,
    ) -> User:
        now = datetime.now(timezone.utc)
        user = User(
            email=email,
            name=name,
            password_hash=password_hash,
            auth_provider=auth_provider,
            created_at=now,
            updated_at=now
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update_user_name(self, db: AsyncSession, user: User, name: str) -> User:
        if user.name != name:
            user.name = name
            await db.commit()
            await db.refresh(user)
        return user

    async def find_or_create_google_user(
        self, 
        db: AsyncSession, 
        email: str, 
        provider_user_id: str, 
        name: Optional[str] = None,
        email_verified: Optional[bool] = None,
        picture: Optional[str] = None,
        hd: Optional[str] = None,
        # google_tenant_id: Optional[str] = None # If you plan to use tenant_id in UserGoogleDetails
    ) -> User:
        user = await self.get_user_by_email(db, email)
        if user:
            if user.auth_provider != AuthProviderType.google:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User with email {email} already exists with {user.auth_provider.value} authentication."
                )
            # User exists, update details if necessary
            if user.name != name and name is not None:
                user.name = name # type: ignore
            
            if not user.google_details:
                # This case should ideally not happen if user.auth_provider is GOOGLE
                # but as a safeguard, create details
                user.google_details = UserGoogleDetails(
                    external_id=provider_user_id,
                    email_verified=email_verified,
                    picture=picture,
                    hd=hd
                )
            else:
                updated = False
                if user.google_details.external_id != provider_user_id: # Should not change, but good to check
                    user.google_details.external_id = provider_user_id
                    updated = True
                if user.google_details.email_verified != email_verified and email_verified is not None:
                    user.google_details.email_verified = email_verified
                    updated = True
                if user.google_details.picture != picture and picture is not None:
                    user.google_details.picture = picture
                    updated = True
                if user.google_details.hd != hd and hd is not None:
                    user.google_details.hd = hd
                    updated = True
                # if updated: await db.commit(); await db.refresh(user.google_details)
            if db.is_modified(user) or (user.google_details and db.is_modified(user.google_details)):
                 await db.commit()
                 await db.refresh(user) # Refresh user to get potentially updated google_details too

        else:
            # Create new user with Google details
            user = User(
                email=email,
                name=name,
                auth_provider=AuthProviderType.google,
                google_details=UserGoogleDetails(
                    external_id=provider_user_id,
                    email_verified=email_verified,
                    picture=picture,
                    hd=hd
                )
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

    async def find_or_create_microsoft_user(
        self, 
        db: AsyncSession, 
        email: str, 
        provider_user_id: str, # This is 'oid' from Microsoft
        name: Optional[str] = None,
        microsoft_tenant_id: Optional[str] = None,
        upn: Optional[str] = None,
        given_name: Optional[str] = None, # For UserMicrosoftDetails
        family_name: Optional[str] = None, # For UserMicrosoftDetails
    ) -> User:
        user = await self.get_user_by_email(db, email)
        if user:
            if user.auth_provider != AuthProviderType.microsoft:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User with email {email} already exists with {user.auth_provider.value} authentication."
                )
            if user.name != name and name is not None:
                user.name = name # type: ignore

            if not user.microsoft_details:
                user.microsoft_details = UserMicrosoftDetails(
                    external_id=provider_user_id,
                    tenant_id=microsoft_tenant_id,
                    upn=upn,
                    given_name=given_name,
                    family_name=family_name
                )
            else:
                # Update existing Microsoft details if changed
                if user.microsoft_details.external_id != provider_user_id: # Should ideally not change
                    user.microsoft_details.external_id = provider_user_id
                if user.microsoft_details.tenant_id != microsoft_tenant_id:
                    user.microsoft_details.tenant_id = microsoft_tenant_id
                if user.microsoft_details.upn != upn:
                    user.microsoft_details.upn = upn
                if user.microsoft_details.given_name != given_name:
                    user.microsoft_details.given_name = given_name
                if user.microsoft_details.family_name != family_name:
                    user.microsoft_details.family_name = family_name
            
            if db.is_modified(user) or (user.microsoft_details and db.is_modified(user.microsoft_details)):
                await db.commit()
                await db.refresh(user)
        else:
            user = User(
                email=email,
                name=name,
                auth_provider=AuthProviderType.microsoft,
                microsoft_details=UserMicrosoftDetails(
                    external_id=provider_user_id,
                    tenant_id=microsoft_tenant_id,
                    upn=upn,
                    given_name=given_name,
                    family_name=family_name
                )
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

# To be used as a dependency in API routes if preferred, or instantiated directly
def get_user_service() -> UserService:
    """Get a UserService instance. This is synchronous because creating the service
    doesn't involve any async operations. The service methods themselves are async."""
    return UserService()

print("kaleo_core.services.user_service created.") 