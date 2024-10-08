from src.database.db import Base

from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
)


class Chats(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, primary_key=True)

    def __repr__(self):
        return f'<Chat: {self.id}>'
