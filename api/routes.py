from fastapi import APIRouter
from .modules.processing.controllers import router as processing_router


router = APIRouter()

router.include_router(
    prefix="/processing",
    router=processing_router,
)
