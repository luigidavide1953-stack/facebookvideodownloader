import json
from typing import Optional, Any
import os

class CacheService:
    def __init__(self):
        self.cache = {}
        # In a real production app, this would use Redis
        self.redis_url = os.getenv("REDIS_URL")

    async def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key)

    async def set(self, key: str, value: Any, expire: int = 3600):
        self.cache[key] = value

    async def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]

cache_service = CacheService()
