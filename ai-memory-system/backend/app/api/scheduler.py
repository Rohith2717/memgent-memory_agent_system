from fastapi import APIRouter

router = APIRouter()

@router.get("/scheduler/health")
def scheduler_health():
    return {"status": "ok"}
