from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import uuid

from ..database import Base

class UserGoogleDetails(Base):
    __tablename__ = "user_google_details"
    __table_args__ = {'comment': 'Stores additional details for users authenticated with Google'}

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, comment='Reference to the user account')
    external_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, comment='Google user ID (sub claim in ID Token)')
    email_verified: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, comment='Whether the email has been verified by Google')
    picture: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment='User profile picture URL')
    hd: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment='Hosted domain for Google Workspace users')
    tenant_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment='Optional tenant ID for Google Workspace')

    user = relationship("User", back_populates="google_details")
