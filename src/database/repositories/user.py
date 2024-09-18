from src.database.models import User
from src.database.repositories.base_repository import BaseRepository

from typing import Optional


class UserRepository(BaseRepository):
    def __init__(self, user_id: int):
        self.user_id = user_id

        super().__init__(User)

    async def new(self, group: str):
        user = self.get()
        if not user:
            await self._new(id=self.user_id, group=group)
        else:
            await self.update(group=group)

    async def update(self, **kwargs):
        await self._update(User.id == self.user_id, **kwargs)

    async def get(self) -> Optional[User]:
        user = await self._get(User.id == self.user_id)
        return user
