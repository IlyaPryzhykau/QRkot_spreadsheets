from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import CharityProject, Donation


async def invest_funds(session: AsyncSession):
    """Распределяет поступившие пожертвования на незавершённые проекты."""
    open_projects = await session.execute(
        select(CharityProject).filter(CharityProject.fully_invested.is_(False))
    )
    open_donations = await session.execute(
        select(Donation).filter(Donation.fully_invested.is_(False))
    )

    open_projects = open_projects.scalars().all()
    open_donations = open_donations.scalars().all()

    for project in open_projects:
        for donation in open_donations:
            project_remainder = project.full_amount - project.invested_amount
            donation_remainder = (donation.full_amount -
                                  donation.invested_amount)

            investment_amount = min(project_remainder, donation_remainder)

            project.invested_amount += investment_amount
            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.utcnow()

            donation.invested_amount += investment_amount
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.utcnow()

            if project.fully_invested:
                break

    await session.commit()

    for project in open_projects:
        await session.refresh(project)
    for donation in open_donations:
        await session.refresh(donation)
