from src.database.db import Base

from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    BigInteger,
    ForeignKey,
)
from datetime import datetime


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(BigInteger, ForeignKey("user.id"), primary_key=True, unique=True)
    everyday_schedule_alert = Column(Boolean, default=False)
    free_after_classes_alert = Column(Boolean, default=False)
    share = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'<UserSettings: {self.id}>'
