from fastapi import APIRouter
from app.services.memory_service import MemoryService

router = APIRouter()
memory_service = MemoryService()

@router.get("/memory/health")
def memory_health():
    return {"status": "ok"}

@router.get("/memory/history")
async def get_history():
    sessions = memory_service.get_sessions()
    # Mock data structure for UI
    return {
        "history": [
            {"id": sid, "last_active": "Just now"} 
            for sid in sessions
        ]
    }

@router.get("/memory/session/{task_id}")
async def get_session_history(task_id: str):
    history = memory_service.get_chat_history(task_id)
    return {"messages": history}
