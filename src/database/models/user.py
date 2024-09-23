from src.database.db import Base

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    BigInteger
)

from datetime import datetime


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, unique=True)
    telegram_name = Column(String(255))
    group = Column(String(255))
    share = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'<User: {self.id}>'
