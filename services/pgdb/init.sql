-- Connect to kaleo database
\c kaleo;

-- Activate the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ENUM auth_provider_type
CREATE TYPE auth_provider_type AS ENUM ('local', 'google', 'microsoft');

-- Generic users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    auth_provider auth_provider_type NOT NULL,
    password_hash TEXT, -- Only for local authentication
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Add comments to users table and columns
COMMENT ON TABLE users IS 'Stores user account information';
COMMENT ON COLUMN users.id IS 'Unique identifier for the user';
COMMENT ON COLUMN users.email IS 'User email address (unique)';
COMMENT ON COLUMN users.name IS 'User display name';
COMMENT ON COLUMN users.auth_provider IS 'Authentication provider (local, google, or microsoft)';
COMMENT ON COLUMN users.password_hash IS 'Hashed password (only for local authentication)';
COMMENT ON COLUMN users.created_at IS 'Timestamp when the user was created';
COMMENT ON COLUMN users.updated_at IS 'Timestamp when the user was last updated';

-- Google authentication details table
CREATE TABLE user_google_details (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    external_id TEXT UNIQUE NOT NULL,  -- sub in Google ID Token
    email_verified BOOLEAN,
    picture TEXT,
    hd TEXT,  -- tenant domain (if Google Workspace)
    tenant_id TEXT  -- optional, for Workspace
);

-- Add comments to user_google_details table and columns
COMMENT ON TABLE user_google_details IS 'Stores additional details for users authenticated with Google';
COMMENT ON COLUMN user_google_details.user_id IS 'Reference to the user account';
COMMENT ON COLUMN user_google_details.external_id IS 'Google user ID (sub claim in ID Token)';
COMMENT ON COLUMN user_google_details.email_verified IS 'Whether the email has been verified by Google';
COMMENT ON COLUMN user_google_details.picture IS 'User profile picture URL';
COMMENT ON COLUMN user_google_details.hd IS 'Hosted domain for Google Workspace users';
COMMENT ON COLUMN user_google_details.tenant_id IS 'Optional tenant ID for Google Workspace';

-- Microsoft authentication details table
CREATE TABLE user_microsoft_details (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    external_id TEXT UNIQUE NOT NULL,  -- oid in ID Token or user_id
    tenant_id TEXT,  -- Azure tenant ID
    upn TEXT,        -- user principal name (email-like)
    given_name TEXT,
    family_name TEXT
);

-- Add comments to user_microsoft_details table and columns
COMMENT ON TABLE user_microsoft_details IS 'Stores additional details for users authenticated with Microsoft';
COMMENT ON COLUMN user_microsoft_details.user_id IS 'Reference to the user account';
COMMENT ON COLUMN user_microsoft_details.external_id IS 'Microsoft user ID (oid claim in ID Token)';
COMMENT ON COLUMN user_microsoft_details.tenant_id IS 'Azure tenant ID (important for multi-tenant)';
COMMENT ON COLUMN user_microsoft_details.upn IS 'User Principal Name (typically email)';
COMMENT ON COLUMN user_microsoft_details.given_name IS 'User first name';
COMMENT ON COLUMN user_microsoft_details.family_name IS 'User last name';

-- Optional tenants table for multi-tenant support
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    external_id TEXT UNIQUE,  -- external tenant ID (Google Workspace domain, Azure Tenant ID)
    provider auth_provider_type NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Add comments to tenants table and columns
COMMENT ON TABLE tenants IS 'Stores tenant information for multi-tenant support';
COMMENT ON COLUMN tenants.id IS 'Unique identifier for the tenant';
COMMENT ON COLUMN tenants.name IS 'Display name of the tenant';
COMMENT ON COLUMN tenants.external_id IS 'External tenant identifier (Google Workspace domain or Azure Tenant ID)';
COMMENT ON COLUMN tenants.provider IS 'Authentication provider for this tenant';
COMMENT ON COLUMN tenants.created_at IS 'Timestamp when the tenant was created';

-- Optional user-tenant relationship table for indirect multi-tenancy
CREATE TABLE user_tenants (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, tenant_id)
);

-- Add comments to user_tenants table and columns
COMMENT ON TABLE user_tenants IS 'Maps users to their associated tenants for multi-tenant support';
COMMENT ON COLUMN user_tenants.user_id IS 'Reference to the user account';
COMMENT ON COLUMN user_tenants.tenant_id IS 'Reference to the tenant';


