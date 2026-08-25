from fastapi import FastAPI


app = FastAPI(
    title="ShopSphere API",
    description="Multi-vendor e-commerce marketplace for small businesses",
    version="1.0.0",
)


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