from src.database.models import User, UserSettings
from src.database.db import session_pool
from src.database.repositories.base_repository import BaseRepository

from typing import Optional, List
from sqlalchemy import ColumnExpressionArgument, select, update
from sqlalchemy.orm import joinedload


class UserRepository(BaseRepository):
    def __init__(self, user_id: Optional[int] = None):
        self.user_id = user_id

        super().__init__(User)

    async def new(self, group: str, tg_name: str):
        user = await self.get()

        async with session_pool() as session:
            if user:
                await self.update(
                    group=group,
                    telegram_name=tg_name,
                    settings=user.settings,
                )
            else:
                user_obj = User(
                    id=self.user_id,
                    group=group,
                    telegram_name=tg_name,
                )

                settings = UserSettings(id=self.user_id)
                settings.user = user_obj

                user_obj.settings = settings

                session.add(user_obj)
                await session.commit()

    async def update(self, **kwargs):
        async with session_pool() as session:
            await session.execute(
                update(User)
                .where(User.id == self.user_id)
                .values(**kwargs)
            )
            await session.commit()

    async def update_settings(self, **kwargs):
        async with session_pool() as session:
            await session.execute(
                update(UserSettings)
                .where(UserSettings.id == self.user_id)
                .values(**kwargs)
            )
            await session.commit()

    async def get(self) -> Optional[User]:
        async with session_pool() as session:
            ex_res = await session.execute(
                select(User)
                .where(User.id == self.user_id)
                .options(joinedload(User.settings))
            )
            get_result = ex_res.scalar()
            return get_result
    
    @staticmethod
    async def get_all_share() -> List[User]:
        async with session_pool() as session:
            ex_res = await session.execute(
                select(User)
                .join(User.settings)
                .where(UserSettings.share == True)
            )
            result_all = ex_res.all()
            result = [i[0] for i in result_all if i]
            return result
