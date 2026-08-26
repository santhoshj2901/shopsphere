from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth import router as auth_router
from app.db.database import get_db
from app.api.routes.users import router as users_router


app = FastAPI(
    title="ShopSphere API",
    description="Multi-vendor e-commerce marketplace for small businesses",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to ShopSphere API"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
async def database_test(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }