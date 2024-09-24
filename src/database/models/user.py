from src.database.db import Base

from sqlalchemy import (
    Column,
    String,
    DateTime,
    BigInteger,
)
from sqlalchemy.orm import Mapped, relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models import UserSettings


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, unique=True)
    telegram_name = Column(String(255))
    group = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())

    settings: Mapped["UserSettings"] = relationship(backref="user")

    def __repr__(self):
        return f'<User: {self.id}>'
