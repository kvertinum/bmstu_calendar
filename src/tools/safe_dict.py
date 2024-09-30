import asyncio
from typing import TypeVar, Generic, Dict


K = TypeVar("K")
V = TypeVar("V")


class SafeDict(Generic[K, V]):
    def __init__(self, default={}):
        self._dict: Dict[K, V] = default
        self._lock = asyncio.Lock()

    async def set(self, key: K, value: V):
        async with self._lock:
            self._dict[key] = value

    async def get(self, key: K):
        async with self._lock:
            return self._dict.get(key)

    async def delete(self, key: K):
        async with self._lock:
            if key in self._dict:
                del self._dict[key]
