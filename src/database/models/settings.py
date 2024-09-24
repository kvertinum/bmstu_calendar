from src.database.db import Base
from src.database import models

from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, relationship

from datetime import datetime, timezone


class UserSettings(Base):
    __tablename__ = "user_settings"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, ForeignKey("user.id"), primary_key=True, unique=True)
    everyday_schedule_alert = Column(Boolean, default=False)
    free_after_classes_alert = Column(Boolean, default=False)
    share = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    user: Mapped["models.User"] = relationship("User", back_populates="settings")

    def __repr__(self):
        return f'<User: {self.id}>'
