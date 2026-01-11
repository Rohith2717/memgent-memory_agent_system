from app.services.memory_service import MemoryService
from app.services.scheduler_service import SchedulerService
from app.llm.llm_client import LLMClient
from app.chat.intent_router import detect_domain

class AgentService:
    def __init__(self):
        self.memory = MemoryService()
        self.scheduler = SchedulerService()
        self.llm = LLMClient()

    async def handle_message(self, task_id: str, message: str) -> str:
        domain = detect_domain(message)
        # retrieve memory using message as query
        context = self.memory.retrieve_context(task_id, message)

        prompt = f"""
You are an AI agent handling a long-running task.

Task ID: {task_id}
Domain: {domain}

Relevant past context:
{chr(10).join(context)}

User message:
{message}

Continue the task naturally.
"""

        # generate response
        response = await self.llm.generate(message, context)

        # store response
        self.memory.store_context(task_id, message, response)

        return response
