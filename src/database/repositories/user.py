from src.database.models import User, UserSettings
from src.database.db import session_pool
from src.keyboards.inline import callbacks as cbq

from typing import Optional, List
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload


class UserRepository:
    def __init__(self, user: Optional[User] = None):
        self.user = user

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
        
    async def update_notifications(self, notification_name: str):
        async with session_pool() as session:
            settings = self.user.settings

            match notification_name:
                case cbq.EverydayScheduleCallback.__prefix__:
                    settings.everyday_schedule_alert = not settings.everyday_schedule_alert
                case cbq.AfterClassesCallback.__prefix__:
                    settings.free_after_classes_alert = not settings.free_after_classes_alert

            await session.merge(self.user)
            await session.commit()

            return settings
        
    async def update_settings(self, settings_name: str):
        async with session_pool() as session:
            settings = self.user.settings

            match settings_name:
                case cbq.UpdateShareCallback.__prefix__:
                    settings.share = not settings.share

            await session.merge(self.user)
            await session.commit()

            return settings

    @staticmethod
    async def get(user_id: int) -> Optional[User]:
        async with session_pool() as session:
            user = await session.get(
                User, user_id,
                options=[joinedload(User.settings)]
            )
            return user
    
    @staticmethod
    async def get_all_share() -> List[User]:
        async with session_pool() as session:
            ex_res = await session.execute(
                select(User)
                .join(User.settings)
                .where(UserSettings.share)
                .options(joinedload(User.settings))
            )

            result = ex_res.scalars().all()
            return result
        
    @staticmethod
    async def get_share_by_ids(user_ids: List[int]) -> List[User]:
        async with session_pool() as session:
            ex_res = await session.execute(
                select(User)
                .join(User.settings)
                .where(User.id.in_(user_ids), UserSettings.share)
                .options(joinedload(User.settings))
            )

            result = ex_res.scalars().all()
            return result
        
    @staticmethod
    async def get_all_notifications() -> List[User]:
        async with session_pool() as session:
            ex_res = await session.execute(
                select(User)
                .join(User.settings)
                .where(or_(
                    UserSettings.everyday_schedule_alert,
                    UserSettings.free_after_classes_alert,
                ))
                .options(joinedload(User.settings))
            )

            result = ex_res.scalars().all()
            return result
