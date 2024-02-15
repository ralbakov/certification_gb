from fastapi import APIRouter, Depends

from menu_restaurant.database.schemas import Menus

from ..menu.service_repository import (
    create_menu_service,
    delete_menu_service,
    get_all_menu_service,
    get_menu_service,
    update_menu_service,
)

menu_router = APIRouter(prefix='/api/v1/menus')


@menu_router.post('',
                  status_code=201,
                  name='Создает меню',
                  response_model=Menus,
                  tags=['Menu'],
                  )
async def create_menu(menu=Depends(create_menu_service)) -> Menus:
    return menu


@menu_router.get('',
                 name='Просматривает список меню',
                 response_model=list[Menus],
                 status_code=200,
                 tags=['Menu']
                 )
async def get_all_menu(menu=Depends(get_all_menu_service)) -> list[Menus] | list[None]:
    return menu


@menu_router.get('/{target_menu_id}',
                 name='Просматривает определенное меню',
                 response_model=Menus,
                 status_code=200,
                 tags=['Menu']
                 )
async def get_menu(menu=Depends(get_menu_service)) -> Menus:
    return menu


@menu_router.patch('/{target_menu_id}',
                   name='Обновляет меню',
                   response_model=Menus,
                   status_code=200,
                   tags=['Menu']
                   )
async def update_menu(menu=Depends(update_menu_service)) -> Menus:
    return menu


@menu_router.delete('/{target_menu_id}',
                    name='Удаляет меню',
                    response_model=None,
                    status_code=200,
                    tags=['Menu'])
async def delete_menu(menu=Depends(delete_menu_service)) -> None:
    return menu
