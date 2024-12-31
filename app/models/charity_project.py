from sqlalchemy import Column, Text, String

from .base import AbstractDonationOrProject


MAX_NAME_LENGTH = 100


class CharityProject(AbstractDonationOrProject):
    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
