from src.database.models import User
from src.database.repositories.base_repository import BaseRepository

from typing import Optional, List
from sqlalchemy import ColumnExpressionArgument


class UserRepository(BaseRepository):
    def __init__(self, user_id: Optional[int] = None):
        self.user_id = user_id

        super().__init__(User)

    async def new(self, group: str, tg_name: str):
        user = await self.get()
        if not user:
            await self._new(id=self.user_id, group=group, telegram_name=tg_name)
        else:
            await self.update(group=group, telegram_name=tg_name)

    async def update(self, **kwargs):
        await self._update(User.id == self.user_id, **kwargs)

    async def get(self) -> Optional[User]:
        user = await self._get(User.id == self.user_id)
        return user
    
    async def select(self, where_field: ColumnExpressionArgument[bool]) -> List[User]:
        result = await self._select(where_field)
        f_elements = [i[0] for i in result if i]
        return f_elements
