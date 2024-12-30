from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.services.invest import invest_funds
from app.schemas.donation import (
    DonationCreate, DonationResponseUser, DonationResponseSuperuser,
)
from app.models import User

router = APIRouter()


@router.post(
    '/',
    response_model=DonationResponseUser,
    dependencies=[Depends(current_user)],
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создать пожертвование от текущего пользователя."""
    new_donation = await donation_crud.create(
        obj_in=donation,
        session=session,
        user=user,
    )
    await invest_funds(session)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationResponseUser],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список всех пожертвований текущего пользователя."""
    return await donation_crud.get_all_user_donations(session, user)


@router.get(
    '/',
    response_model=List[DonationResponseSuperuser],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """ Получить список всех пожертвований."""
    return await donation_crud.get_multi(session=session)
