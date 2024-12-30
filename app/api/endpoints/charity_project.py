from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.services.invest import invest_funds
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate, CharityProjectResponse)
from app.api.endpoints.validators import (
    get_project_or_404, validate_project_can_be_deleted,
    validate_project_not_fully_invested, validate_name_not_duplicate,
    validate_name_and_description, validate_min_investment_amount)
from app.core.user import current_superuser


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectResponse]
)
async def get_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать новый проект."""
    await validate_name_not_duplicate(project.name, session)
    project = await charity_project_crud.create(project, session)
    await invest_funds(session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить проект."""
    project = await get_project_or_404(project_id, session)

    await validate_name_and_description(
        project_in.name, project_in.description)
    await validate_project_not_fully_invested(project)

    if project_in.name and project_in.name != project.name:
        await validate_name_not_duplicate(project_in.name, session)

    if project_in.full_amount:
        await validate_min_investment_amount(project, project_in.full_amount)

    return await charity_project_crud.update(project, project_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удалить проект."""
    project = await get_project_or_404(project_id, session)
    await validate_project_can_be_deleted(project)
    await charity_project_crud.remove(project, session)
    return project
