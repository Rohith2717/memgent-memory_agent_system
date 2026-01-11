from app.services.agent_service import AgentService

class AgentCore:
    def __init__(self):
        self.service = AgentService()

    async def process(self, task_id: str, message: str) -> str:
        return await self.service.handle_message(task_id, message)
