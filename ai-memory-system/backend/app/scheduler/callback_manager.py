import asyncio
import json
import os
import time
from typing import List, Dict
from app.scheduler.task_registry import TaskRegistry

STATE_FILE = "data/scheduler_state.json"

class CallbackManager:
    def __init__(self):
        self.tasks: List[Dict] = []
        self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
             try:
                 with open(STATE_FILE, 'r') as f:
                     self.tasks = json.load(f)
             except json.JSONDecodeError:
                 self.tasks = []

    def _save_state(self):
        # Ensure data dir exists
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    async def execute(self, task: Dict):
        print(f"[CALLBACK] Executing task {task.get('task_id')}")
        
        # Remove from state
        # (Compare by execute_at and task_id to act as simple unique ID for now)
        self.tasks = [t for t in self.tasks if t != task]
        self._save_state()

        handler = TaskRegistry.get_handler(task.get("type", "default"))
        if handler:
            await handler(task["task_id"], task.get("payload", {}))
        else:
            print(f"[CALLBACK] No handler for type {task.get('type')}")

    async def schedule(self, task_id: str, payload: dict, delay_seconds: int, type: str = "default"):
        execute_at = time.time() + delay_seconds
        task = {
            "task_id": task_id,
            "payload": payload,
            "execute_at": execute_at,
            "type": type
        }
        self.tasks.append(task)
        self._save_state()
        
        asyncio.create_task(self._wait_and_execute(task))

    async def _wait_and_execute(self, task: Dict):
        now = time.time()
        delay = task["execute_at"] - now
        if delay > 0:
            await asyncio.sleep(delay)
        await self.execute(task)

    async def recover_tasks(self):
        """Called on startup to reschedule pending tasks"""
        print(f"[SCHEDULER] Recovering {len(self.tasks)} tasks...")
        for task in list(self.tasks): 
             asyncio.create_task(self._wait_and_execute(task))

    def get_pending_task(self, task_id: str, type: str = "default") -> Dict | None:
        """Find a pending task for the ID and type."""
        for task in self.tasks:
            if task["task_id"] == task_id and task["type"] == type:
                return task
        return None

    def cancel_task(self, task_id: str, type: str = "default"):
         """Remove a task from the schedule."""
         original_len = len(self.tasks)
         self.tasks = [t for t in self.tasks if not (t["task_id"] == task_id and t["type"] == type)]
         if len(self.tasks) < original_len:
             self._save_state()
             print(f"[SCHEDULER] Cancelled task {task_id} type {type}")
