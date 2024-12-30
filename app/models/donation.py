from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from .base import AbstractDonationOrProject


class Donation(AbstractDonationOrProject):
    user_id = Column(
        Integer, ForeignKey('user.id'), name='fk_donation_user_id_user'
    )
    comment = Column(Text, nullable=True)
    user = relationship('User', back_populates='donations')
