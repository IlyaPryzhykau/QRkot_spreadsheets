from sqlalchemy import Column, Text, String

from .base import AbstractDonationOrProject


class CharityProject(AbstractDonationOrProject):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
