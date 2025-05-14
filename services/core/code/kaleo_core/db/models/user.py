from sqlalchemy import text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .auth_provider_type_enum import AuthProviderType
from .base import Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Stores user account information'}

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'), comment='Unique identifier for the user')
    email: Mapped[str] = mapped_column(unique=True, nullable=False, comment='User email address (unique)')
    name: Mapped[str | None] = mapped_column(comment='User display name')
    auth_provider: Mapped[AuthProviderType] = mapped_column(Enum(AuthProviderType, name='auth_provider_type'), nullable=False, comment='Authentication provider (local, google, or microsoft)')
    password_hash: Mapped[str | None] = mapped_column(comment='Hashed password (only for local authentication)')
    created_at: Mapped[datetime] = mapped_column(server_default=text('now()'), comment='Timestamp when the user was created')
    updated_at: Mapped[datetime] = mapped_column(server_default=text('now()'), comment='Timestamp when the user was last updated')

    google_details = relationship("UserGoogleDetails", back_populates="user", cascade="all, delete-orphan", uselist=False)
    microsoft_details = relationship("UserMicrosoftDetails", back_populates="user", cascade="all, delete-orphan", uselist=False)
    tenants = relationship("UserTenant", back_populates="user", cascade="all, delete-orphan")
