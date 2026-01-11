from pydantic import BaseModel

class ChatRequest(BaseModel):
    task_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
