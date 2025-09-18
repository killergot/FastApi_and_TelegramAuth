from app.database.psql import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session