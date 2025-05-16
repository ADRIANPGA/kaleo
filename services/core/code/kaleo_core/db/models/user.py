from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List
import uuid

from ..database import Base
from .auth_provider_type_enum import AuthProviderType, AuthProviderTypeEnum
from .tenant import user_tenants, Tenant
from .user_google_details import UserGoogleDetails
from .user_microsoft_details import UserMicrosoftDetails

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    auth_provider: Mapped[AuthProviderType] = mapped_column(AuthProviderTypeEnum, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    google_details = relationship("UserGoogleDetails", back_populates="user", uselist=False, cascade="all, delete-orphan")
    microsoft_details = relationship("UserMicrosoftDetails", back_populates="user", uselist=False, cascade="all, delete-orphan")
    tenants: Mapped[List[Tenant]] = relationship(secondary=user_tenants, back_populates="users")
