from app.memory.memory_store import MemoryStore
from app.rl.rl_agent import RLAgent

class MemoryService:
    def __init__(self):
        self.store = MemoryStore()
        self.rl = RLAgent()

    def get_sessions(self) -> list[str]:
        return self.store.get_all_task_ids()

    def get_chat_history(self, task_id: str) -> list[dict]:
        memories = self.store.get_memories(task_id)
        # We could parse here, but let's send raw and let frontend handle parsing for now
        # to ensure we don't break things.
        return memories

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

        # Return full objects so caller can use IDs for feedback
        return selected

    def apply_feedback(self, memory_ids: list[str], positive: bool):
        """Update scores based on feedback."""
        delta = 1.0 if positive else -1.0
        self.rl.update_scores(memory_ids, delta)

