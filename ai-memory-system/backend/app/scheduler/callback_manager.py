from datetime import datetime
import asyncio

class CallbackManager:
    async def execute(self, task_id: str, payload: dict):
        print(f"[CALLBACK] Executing task {task_id} with payload {payload}")

    async def schedule(self, task_id: str, payload: dict, delay_seconds: int):
        await asyncio.sleep(delay_seconds)
        await self.execute(task_id, payload)
