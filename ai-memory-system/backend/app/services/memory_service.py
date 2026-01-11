from app.memory.memory_store import MemoryStore
from app.rl.rl_agent import RLAgent

class MemoryService:
    def __init__(self):
        self.store = MemoryStore()
        self.rl = RLAgent()

    def store_context(self, task_id: str, user_message: str, assistant_response: str):
        combined = (
            f"User intent: {user_message}\n"
            f"Assistant response: {assistant_response}"
        )
        self.store.add(task_id, combined, {})


    def retrieve_context(self, task_id: str, query: str):
        memories = self.store.search(task_id, query)

        if not memories:
            return []

        ranked = self.rl.rank(memories)
        selected = ranked[:3]

        # reward only selected memories
        self.rl.reward(selected)

        return [m["content"] for m in selected]

