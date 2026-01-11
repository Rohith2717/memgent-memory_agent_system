import json
import os

class RLAgent:
    def __init__(self):
        self.path = "data/rewards.json"
        self.rewards = self._load()

    def rank(self, memories):
        return sorted(memories, key=lambda m: m["score"], reverse=True)

    def reward(self, memories):
        for m in memories:
            m["score"] += 1
        self._save()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.rewards, f)
