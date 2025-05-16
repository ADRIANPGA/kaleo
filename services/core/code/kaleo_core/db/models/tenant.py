from sqlalchemy import String, DateTime, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List
import uuid

from ..database import Base
from .auth_provider_type_enum import AuthProviderType, AuthProviderTypeEnum

# Association table for user-tenant relationship
user_tenants = Table(
    "user_tenants",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("tenant_id", ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True)
)

class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    provider: Mapped[AuthProviderType] = mapped_column(AuthProviderTypeEnum, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship to users through the association table
    users = relationship("User", secondary=user_tenants, back_populates="tenants")
