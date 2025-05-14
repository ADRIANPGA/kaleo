from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class UserTenant(Base):
    __tablename__ = 'user_tenants'
    __table_args__ = {'comment': 'Maps users to their associated tenants for multi-tenant support'}

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, comment='Reference to the user account')
    tenant_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, comment='Reference to the tenant')

    user = relationship("User", back_populates="tenants", passive_deletes=True)
    tenant = relationship("Tenant", back_populates="users", passive_deletes=True)
