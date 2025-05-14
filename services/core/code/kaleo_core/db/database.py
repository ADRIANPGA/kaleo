from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from ..config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_tenant_from_db(session: AsyncSession, tenant_id: str):
    query = """
        SELECT tenant_id::text, display_name, default_domain, verified_domains, backend_url, ui_url
        FROM public.tenants
        WHERE tenant_id = :tenant_id
    """
    result = await session.execute(query, {"tenant_id": tenant_id})
    row = result.first()
    
    if row:
        return {
            "id": row.tenant_id,
            "name": row.display_name,
            "default_domain": row.default_domain,
            "verified_domains": row.verified_domains,
            "backend_url": row.backend_url,
            "ui_url": row.ui_url,
        }
    return None 