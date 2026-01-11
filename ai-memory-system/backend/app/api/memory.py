from fastapi import APIRouter

router = APIRouter()

@router.get("/memory/health")
def memory_health():
    return {"status": "ok"}
