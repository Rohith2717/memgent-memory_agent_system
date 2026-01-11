from typing import Callable, Dict, Any, Awaitable

class TaskRegistry:
    _registry: Dict[str, Callable[[str, Dict[str, Any]], Awaitable[None]]] = {}

    @classmethod
    def register(cls, key: str, handler: Callable[[str, Dict[str, Any]], Awaitable[None]]):
        """Register a handler function for a specific task type key."""
        cls._registry[key] = handler

    @classmethod
    def get_handler(cls, key: str) -> Callable[[str, Dict[str, Any]], Awaitable[None]]:
        """Retrieve a handler function by key."""
        return cls._registry.get(key)
