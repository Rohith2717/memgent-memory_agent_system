from fastapi import APIRouter
from app.agent.agent_core import AgentCore
from app.models.schemas import ChatRequest

router = APIRouter()
agent = AgentCore()

@router.post("/chat")
async def chat(request: ChatRequest):
    response = await agent.process(request.task_id, request.message)

    # GUARANTEE response
    if not response:
        return {"response": "[SYSTEM ERROR] Empty response"}

    return {"response": response}
