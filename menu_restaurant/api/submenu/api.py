from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.database.schemas import Submenus

from ..submenu.service_repository import (
    create_submenu_service,
    delete_submenu_service,
    get_all_submenu_service,
    get_submenu_service,
    update_submenu_service,
)

submenu_router = APIRouter(prefix=('/api/v1/menus'
                                   '/{target_menu_id}/submenus'))


@submenu_router.get('',
                    name='Просматривает список подменю',
                    status_code=200,
                    response_model=list[Submenus],
                    tags=['Submenu']
                    )
async def get_list_submenus(all_submenu: AsyncSession = Depends(get_all_submenu_service)):
    return all_submenu


@submenu_router.post('',
                     name='Создает подменю',
                     status_code=201,
                     response_model=Submenus,
                     tags=['Submenu'])
async def create_submenu(submenu: AsyncSession = Depends(create_submenu_service)):
    return submenu


@submenu_router.get('/{target_submenu_id}',
                    name='Просматривает определенное подменю',
                    status_code=200,
                    response_model=Submenus,
                    tags=['Submenu'])
async def get_submenu(submenu: AsyncSession = Depends(get_submenu_service)):
    return submenu


@submenu_router.patch('/{target_submenu_id}',
                      name='Обновляет подменю',
                      response_model=Submenus,
                      tags=['Submenu'])
async def update_submenu(submenu: AsyncSession = Depends(update_submenu_service)):
    return submenu


@submenu_router.delete('/{target_submenu_id}',
                       name='Удаляет подменю', tags=['Submenu'])
async def delete_submenu(submenu: AsyncSession = Depends(delete_submenu_service)):
    return submenu
