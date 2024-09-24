from src.database.models import User, UserSettings
from src.database.db import session_pool
from src.database.repositories.base_repository import BaseRepository

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class UserRepository(BaseRepository):
    def __init__(self, user: Optional[User] = None):
        self.user = user

        super().__init__(User)

    async def new(self, user_id: int, group: str, tg_name: str):
        async with session_pool() as session:
            if self.user:
                self.user.group = group
                self.user.telegram_name = tg_name

                await session.merge(self.user)

            else:
                user_obj = User(
                    id=user_id,
                    group=group,
                    telegram_name=tg_name,
                    settings=UserSettings(),
                )

                session.add(user_obj)
            
            await session.commit()

    async def update_share_status(self):
        async with session_pool() as session:
            new_share_status = not self.user.settings.share
            self.user.settings.share = new_share_status

            await session.merge(self.user)
            await session.commit()

            return new_share_status

    @staticmethod
    async def get(user_id: int) -> Optional[User]:
        async with session_pool() as session:
            ex_res = await session.execute(
                select(User)
                .where(User.id == user_id)
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
