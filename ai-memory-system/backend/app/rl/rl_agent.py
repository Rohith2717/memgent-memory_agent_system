import json
import os
from typing import List, Dict

class RLAgent:
    def __init__(self):
        self.path = "data/rewards.json"
        self.rewards = self._load()

    def rank(self, memories: List[Dict]) -> List[Dict]:
        """Apply scores to memories and sort them."""
        for m in memories:
            m_id = m.get("id")
            if m_id:
                m["score"] = self.rewards.get(m_id, 0.0)
        
        return sorted(memories, key=lambda m: m.get("score", 0), reverse=True)

    def update_scores(self, mem_ids: List[str], delta: float):
        """Update scores for specific memories."""
        updated = False
        for mid in mem_ids:
            if mid:
                current = self.rewards.get(mid, 0.0)
                self.rewards[mid] = current + delta
                updated = True
        
        if updated:
            self._save()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save(self):
        # Ensure data dir
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.rewards, f, indent=2)
