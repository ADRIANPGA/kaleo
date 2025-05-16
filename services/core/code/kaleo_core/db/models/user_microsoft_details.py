from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import uuid

from ..database import Base

class UserMicrosoftDetails(Base):
    __tablename__ = "user_microsoft_details"
    __table_args__ = {'comment': 'Stores additional details for users authenticated with Microsoft'}

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    external_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    tenant_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    upn: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    given_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    family_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationship back to user
    user = relationship("User", back_populates="microsoft_details")
