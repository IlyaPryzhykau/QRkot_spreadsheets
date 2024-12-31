from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings


DEFAULT_ROW_COUNT = 100
DEFAULT_COLUMN_COUNT = 11
DEFAULT_SHEET_ID = 0
DEFAULT_SHEET_TITLE = 'Лист1'
FORMAT = "%Y/%m/%d %H:%M:%S"
LOCALE_RU = 'ru_RU'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {now_date_time}',
                       'locale': LOCALE_RU},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': DEFAULT_SHEET_ID,
                                   'title': DEFAULT_SHEET_TITLE,
                                   'gridProperties':
                                       {'rowCount': DEFAULT_ROW_COUNT,
                                        'columnCount': DEFAULT_COLUMN_COUNT}}}]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for project in projects:
        new_row = [str(project['name']),
                   float(project['duration_days']),
                   str(project['description'])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
