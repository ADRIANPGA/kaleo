from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class UserMicrosoftDetails(Base):
    __tablename__ = 'user_microsoft_details'
    __table_args__ = {'comment': 'Stores additional details for users authenticated with Microsoft'}

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, comment='Reference to the user account')
    external_id: Mapped[str] = mapped_column(unique=True, nullable=False, comment='Microsoft user ID (oid claim in ID Token)')
    tenant_id: Mapped[str | None] = mapped_column(comment='Azure tenant ID (important for multi-tenant)')
    upn: Mapped[str | None] = mapped_column(comment='User Principal Name (typically email)')
    given_name: Mapped[str | None] = mapped_column(comment='User first name')
    family_name: Mapped[str | None] = mapped_column(comment='User last name')

    user = relationship("User", back_populates="microsoft_details", passive_deletes=True)
