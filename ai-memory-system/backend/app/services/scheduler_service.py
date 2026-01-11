import asyncio
from app.scheduler.callback_manager import CallbackManager

class SchedulerService:
    def __init__(self):
        self.manager = CallbackManager()

    def schedule_callback(self, task_id: str, payload: dict, delay_seconds: int, type: str = "default"):
         # We can await this since we changed schedule to be async but it spawns a task internally
         # However, since this method is sync in the original code (implied by lack of async def, though it calls asyncio.create_task),
         # we should probably keep it sync or make it async.
         # Original: def schedule_callback... -> asyncio.create_task(...)
         # My new CallbackManager.schedule is async.
         asyncio.create_task(
            self.manager.schedule(task_id, payload, delay_seconds, type)
         )

    async def recover(self):
        await self.manager.recover_tasks()

    def get_pending_task(self, task_id: str, type: str = "default") -> dict | None:
        return self.manager.get_pending_task(task_id, type)

    def cancel_task(self, task_id: str, type: str = "default"):
        self.manager.cancel_task(task_id, type)
