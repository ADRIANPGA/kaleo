import enum

class AuthProviderType(enum.Enum):
    local = 'local'
    google = 'google'
    microsoft = 'microsoft'
