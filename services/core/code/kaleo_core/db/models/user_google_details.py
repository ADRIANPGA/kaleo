from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class UserGoogleDetails(Base):
    __tablename__ = 'user_google_details'
    __table_args__ = {'comment': 'Stores additional details for users authenticated with Google'}

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, comment='Reference to the user account')
    external_id: Mapped[str] = mapped_column(unique=True, nullable=False, comment='Google user ID (sub claim in ID Token)')
    email_verified: Mapped[bool | None] = mapped_column(comment='Whether the email has been verified by Google')
    picture: Mapped[str | None] = mapped_column(comment='User profile picture URL')
    hd: Mapped[str | None] = mapped_column(comment='Hosted domain for Google Workspace users')
    tenant_id: Mapped[str | None] = mapped_column(comment='Optional tenant ID for Google Workspace')

    user = relationship("User", back_populates="google_details", passive_deletes=True)
