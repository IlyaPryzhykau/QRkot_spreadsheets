from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime

from app.core.db import Base


DEFAULT_INVESTED_AMOUNT = 0


class AbstractDonationOrProject(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, nullable=True)
