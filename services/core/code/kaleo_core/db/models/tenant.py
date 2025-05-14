from sqlalchemy import text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .auth_provider_type_enum import AuthProviderType
from .base import Base

class Tenant(Base):
    __tablename__ = 'tenants'
    __table_args__ = {'comment': 'Stores tenant information for multi-tenant support'}

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'), comment='Unique identifier for the tenant')
    name: Mapped[str] = mapped_column(nullable=False, comment='Display name of the tenant')
    external_id: Mapped[str | None] = mapped_column(unique=True, comment='External tenant identifier (Google Workspace domain or Azure Tenant ID)')
    provider: Mapped[AuthProviderType] = mapped_column(Enum(AuthProviderType, name='auth_provider_type'), nullable=False, comment='Authentication provider for this tenant')
    created_at: Mapped[datetime] = mapped_column(server_default=text('now()'), comment='Timestamp when the tenant was created')

    users = relationship("UserTenant", back_populates="tenant", cascade="all, delete-orphan")
