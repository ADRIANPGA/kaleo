from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

class AuthProviderType(str, Enum):
    # Values must match exactly what's in the database
    local = "local"
    google = "google"
    microsoft = "microsoft"

# Create the SQLAlchemy type that matches the database enum
AuthProviderTypeEnum = SQLAlchemyEnum(
    AuthProviderType,
    name="auth_provider_type",  # This must match the enum name in the database
    create_constraint=True,
    validate_strings=True,
    native_enum=True  # This tells SQLAlchemy to use native PostgreSQL enum
)
