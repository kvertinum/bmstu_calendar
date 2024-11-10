from src.database.models import Chats
from src.database.db import session_pool

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    async def get_chat_users(self):
        async with session_pool() as session:
            ex_res = await session.execute(
                select(Chats.user_id)
                .where(Chats.id == self.chat_id)
            )

            result = ex_res.scalars().all()
            return result

    async def reg_chat_user(self, user_id: int):
        async with session_pool() as session:
            user_ex = await self.user_exists(session, user_id)

            if user_ex:
                return

            chat_obj = Chats(id=self.chat_id, user_id=user_id)
            session.add(chat_obj)
            
            await session.commit()

    async def user_exists(self, session: AsyncSession, user_id: int):
        ex_res = await session.execute(
            select(Chats)
            .where(Chats.id == self.chat_id, Chats.user_id == user_id)
        )

        result = ex_res.first()
        return result is not None
