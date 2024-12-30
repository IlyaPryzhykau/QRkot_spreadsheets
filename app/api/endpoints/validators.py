from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models import CharityProject
from app.crud.charity_project import charity_project_crud


async def get_project_or_404(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверить существование проекта."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def validate_project_not_fully_invested(
        project: CharityProject
) -> None:
    """Проверить, что проект не закрыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя редактировать или удалять закрытый проект!'
        )


async def validate_min_investment_amount(
        project: CharityProject,
        new_amount: int
) -> None:
    """Проверить, что новая сумма больше или равна внесенной."""
    if project.invested_amount > new_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Новая сумма не может быть меньше внесенной!'
        )


async def validate_project_can_be_deleted(
        project: CharityProject
) -> None:
    """Проверить, что проект можно удалить."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя удалить проект, в который уже внесли средства!'
        )


async def validate_name_not_duplicate(
        name: str,
        session: AsyncSession
) -> None:
    """Проверить, что имя проекта уникально."""
    project_id = await charity_project_crud.get_project_id_by_name(
        name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким названием уже существует!'
        )


async def validate_name_and_description(
        name: Optional[str],
        description: Optional[str]
) -> None:
    """Проверить, что имя и описание не пустые и не содержат только пробелы."""
    if name is not None and not name.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Имя проекта не может состоять только из пробелов!'
        )

    if description is not None and not description.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Описание проекта не может состоять только из пробелов!'
        )
