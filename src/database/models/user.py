from src.database.db import Base
from src.database import models

from sqlalchemy import (
    Column,
    String,
    DateTime,
    BigInteger,
)
from sqlalchemy.orm import Mapped, relationship

from datetime import datetime, timezone


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, unique=True)
    telegram_name = Column(String(255))
    group = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())

    settings: Mapped["models.UserSettings"] = relationship("UserSettings", back_populates="user", uselist=False)

    def __repr__(self):
        return f'<User: {self.id}>'
