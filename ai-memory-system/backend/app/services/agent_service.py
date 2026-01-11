from app.services.memory_service import MemoryService
from app.services.scheduler_service import SchedulerService
from app.llm.llm_client import LLMClient
from app.chat.intent_router import detect_domain
from app.scheduler.task_registry import TaskRegistry

class AgentService:
    def __init__(self):
        self.memory = MemoryService()
        self.scheduler = SchedulerService()
        self.llm = LLMClient()
        
        # Register callback
        TaskRegistry.register("resume", self.resume_task)

    async def handle_message(self, task_id: str, message: str) -> str:
        # Check for resume intent
        if "resume" in message.lower():
            # 1. Check for pending tasks
            pending = self.scheduler.get_pending_task(task_id, "resume")
            if pending:
                print(f"[AGENT] Found pending resume task. Executing manually.")
                self.scheduler.cancel_task(task_id, "resume")
                payload = pending["payload"]
            else:
                print(f"[AGENT] No pending resume task. Forcing resume.")
                payload = {"context_hint": "resume task status"}
            
            # 2. Trigger resume logic
            # This returns nothing in current signature, but we need to return string.
            # resume_task prints and stores, but let's change it to return string too? 
            # Or just hack it here. 
            # resume_task calls llm.generate -> store. 
            # Let's refactor resume_task to return the response.
            response = await self.resume_task(task_id, payload)
            return response

        domain = detect_domain(message)
        # retrieve memory using message as query
        context_objs = self.memory.retrieve_context(task_id, message)
        
        # Extract content
        context_str = chr(10).join([m["content"] for m in context_objs])

        prompt = f"""
You are an AI agent handling a long-running task.

Task ID: {task_id}
Domain: {domain}

Relevant past context:
{context_str}

User message:
{message}

Continue the task naturally.
"""

        # generate response
        # Context passed to LLM client should probably be just text or list of text
        # Assuming llm.generate takes list of strings for context or just prompt?
        # Re-reading original: response = await self.llm.generate(message, context)
        # So I should pass the list of strings.
        response = await self.llm.generate(message, [m["content"] for m in context_objs])

        # store response
        self.memory.store_context(task_id, message, response)

        return response

    async def resume_task(self, task_id: str, payload: dict):
        """Callback to resume a paused task."""
        print(f"[AGENT] Resuming task {task_id}")
        
        # 1. Retrieve context (what happened before?)
        # Use a generic query for resumption context or payload hint
        query = payload.get("context_hint", "resume task status")
        context_objs = self.memory.retrieve_context(task_id, query)
        context_str = chr(10).join([m["content"] for m in context_objs])
        
        # 2. Construct Prompt
        prompt = f"""
SYSTEM: You are resuming a paused task (ID: {task_id}).
CONTEXT:
{context_str}

INSTRUCTION: Review the context and continue the workflow. 
If there were pending actions, execute them or describe the next steps.
"""
        # 3. Generate content (Action/Thought) - bypassing user input since it's a callback
        response = await self.llm.generate(query, [m["content"] for m in context_objs]) 
        
        print(f"[AGENT] Resumption output: {response}")
        
        # 4. Store the resumption event
        self.memory.store_context(task_id, f"SYSTEM: Resumed task with hint '{query}'", response)
        
        return response
