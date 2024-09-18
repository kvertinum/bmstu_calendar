import asyncio
from typing import Hashable, Any


class SafeDict:
    def __init__(self, default={}):
        self._dict = default
        self._lock = asyncio.Lock()

    async def set(self, key: Hashable, value: Any):
        async with self._lock:
            self._dict[key] = value

    async def get(self, key: Hashable):
        async with self._lock:
            return self._dict.get(key)

    async def delete(self, key: Hashable):
        async with self._lock:
            if key in self._dict:
                del self._dict[key]
