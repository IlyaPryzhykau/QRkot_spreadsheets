from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, root_validator


MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 100
MIN_DESCRIPTION_LENGTH = 1


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    description: str = Field(
        ...,
        min_length=MIN_DESCRIPTION_LENGTH
    )
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @root_validator(pre=True)
    def check_unexpected_fields(cls, values):
        allowed_fields = {'name', 'description', 'full_amount'}
        for field in values:
            if field not in allowed_fields:
                raise ValueError(f'Поле {field} нельзя редактировать!')
        return values


class CharityProjectResponse(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
