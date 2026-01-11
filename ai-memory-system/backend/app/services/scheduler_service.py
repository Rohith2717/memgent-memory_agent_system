import asyncio
from app.scheduler.callback_manager import CallbackManager

class SchedulerService:
    def __init__(self):
        self.manager = CallbackManager()

    def schedule_callback(self, task_id: str, payload: dict, delay_seconds: int):
        asyncio.create_task(
            self.manager.schedule(task_id, payload, delay_seconds)
        )
