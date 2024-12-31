from typing import Optional, Union

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CharityProjectCRUD(CRUDBase):

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[dict[str, Union[str, float]]]:
        closed_projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.description,
                func.round(
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date),
                    2
                ).label('duration_days')
            ).where(
                CharityProject.fully_invested
            ).order_by(
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date)
            )
        )

        projects = closed_projects.all()

        return [
            {
                'name': project.name,
                'description': project.description,
                'duration_days': project.duration_days
            }
            for project in projects
        ]

    async def get_project_id_by_name(
            self,
            name: str,
            session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == name
            )
        )
        return db_project_id.scalars().first()


charity_project_crud = CharityProjectCRUD(CharityProject)
