import faiss
import os
import shutil
import pickle
import uuid
import numpy as np
from app.memory.embeddings import embed
from app.core.config import settings

class MemoryStore:
    def __init__(self):
        self.dim = 64
        self.index_path = f"{settings.VECTOR_DB_PATH}/index.faiss"
        self.meta_path = f"{settings.VECTOR_DB_PATH}/meta.pkl"

        if os.path.exists(settings.VECTOR_DB_PATH):
            if not os.path.isdir(settings.VECTOR_DB_PATH):
                os.remove(settings.VECTOR_DB_PATH)

        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.metadata = []

    def add(self, task_id: str, content: str, metadata: dict):
        vec = np.array([embed(content)], dtype="float32")
        self.index.add(vec)
        
        mem_id = metadata.get("id") or str(uuid.uuid4())
        
        self.metadata.append({
            "id": mem_id,
            "task_id": task_id,
            "content": content,
            "metadata": metadata,
            "score": 0.0 # Initial score
        })
        self._persist()

    def search(self, task_id: str, query: str, k: int = 5):
        if len(self.metadata) == 0:
            return []

        vec = np.array([embed(query)], dtype="float32")
        distances, indices = self.index.search(vec, k)  
        results = []
        for i in indices[0]:
            if 0 <= i < len(self.metadata):
                mem = self.metadata[i]
                if mem["task_id"] == task_id:
                    results.append(mem) 
        return results


    def _persist(self):
        if not os.path.exists(settings.VECTOR_DB_PATH):
            os.makedirs(settings.VECTOR_DB_PATH)
            
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def get_all_task_ids(self) -> list[str]:
        return list(set(m["task_id"] for m in self.metadata))

    def get_memories(self, task_id: str) -> list[dict]:
        return [m for m in self.metadata if m["task_id"] == task_id]
