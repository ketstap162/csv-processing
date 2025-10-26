from fastapi import FastAPI
import uvicorn

from api.routes import router as api_router
from core.settings import settings

app = FastAPI(
    title="CSV Processing API",
    description="API for processing CSV data and storing results",
    version="1.0.0",
)

# Include API routes
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,  # Enable auto-reload during development
    )
