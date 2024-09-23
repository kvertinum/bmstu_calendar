from src.database.db import Base, session_pool

from sqlalchemy import ColumnExpressionArgument, select, update


class BaseRepository:
    def __init__(self, model: Base):
        self._model = model

    async def _new(
        self, **kwargs
    ):
        async with session_pool() as session:
            model_obj = self._model(**kwargs)
            session.add(model_obj)
            await session.commit()

    async def _update(self, where_field: ColumnExpressionArgument[bool], **kwargs):
        async with session_pool() as session:
            await session.execute(
                update(self._model)
                .where(where_field)
                .values(**kwargs)
            )
            await session.commit()

    async def _get(self, where_field: ColumnExpressionArgument[bool]):
        async with session_pool() as session:
            ex_res = await session.execute(
                select(self._model)
                .where(where_field)
            )
            get_result = ex_res.scalar()
            return get_result
        
    async def _select(self, where_field: ColumnExpressionArgument[bool]):
        async with session_pool() as session:
            ex_res = await session.execute(
                select(self._model)
                .where(where_field)
            )
            get_result = ex_res.all()
            return get_result
