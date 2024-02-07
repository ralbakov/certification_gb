from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from menu_restaurant.database.dependency import get_db
from menu_restaurant.database.schemas import Menus, MenusCreate, MenusUpdate

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
                  tags=['Menu']
                  )
async def create_menu(menu: MenusCreate,
                      db: Session = Depends(get_db)):
    return create_menu_service(db=db, menu=menu)


@menu_router.get('',
                 name='Просматривает список меню',
                 response_model=list[Menus],
                 status_code=200,
                 tags=['Menu']
                 )
async def get_all_menu(db: Session = Depends(get_db)):
    return get_all_menu_service(db=db)


@menu_router.get('/{target_menu_id}',
                 name='Просматривает определенное меню',
                 response_model=Menus,
                 status_code=200,
                 tags=['Menu']
                 )
async def get_menu(target_menu_id: str,
                   db: Session = Depends(get_db)):
    return get_menu_service(target_menu_id=target_menu_id, db=db)


@menu_router.patch('/{target_menu_id}',
                   name='Обновляет меню',
                   response_model=Menus,
                   status_code=200,
                   tags=['Menu']
                   )
async def update_menu(target_menu_id: str,
                      menu: MenusUpdate,
                      db: Session = Depends(get_db)):
    return update_menu_service(target_menu_id=target_menu_id, menu=menu, db=db)


@menu_router.delete('/{target_menu_id}', name='Удаляет меню', tags=['Menu'])
async def delete_menu(target_menu_id: str,
                      db: Session = Depends(get_db)):
    return delete_menu_service(target_menu_id=target_menu_id, db=db)
