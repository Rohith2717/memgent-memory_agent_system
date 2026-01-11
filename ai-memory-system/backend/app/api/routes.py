from fastapi import APIRouter
from app.api.chat import router as chat_router
from app.api.memory import router as memory_router
from app.api.scheduler import router as scheduler_router

router = APIRouter()
router.include_router(chat_router)
router.include_router(memory_router)
router.include_router(scheduler_router)
