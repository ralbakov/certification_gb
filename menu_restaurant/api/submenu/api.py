from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from menu_restaurant.database.dependency import get_db
from menu_restaurant.database.schemas import Submenus, SubmenusCreate, SubmenusUpdate

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
                    response_model=list[Submenus],
                    tags=['Submenu']
                    )
async def get_list_submenus(target_menu_id: str,
                            db: Session = Depends(get_db)):
    return get_all_submenu_service(target_menu_id=target_menu_id, db=db)


@submenu_router.post('',
                     name='Создает подменю',
                     status_code=201,
                     response_model=Submenus,
                     tags=['Submenu'])
async def create_submenu(target_menu_id: str,
                         submenu: SubmenusCreate,
                         db: Session = Depends(get_db)):
    return create_submenu_service(target_menu_id=target_menu_id, submenu=submenu, db=db)


@submenu_router.get('/{target_submenu_id}',
                    name='Просматривает определенное подменю',
                    response_model=Submenus,
                    tags=['Submenu'])
async def get_submenu(target_menu_id: str,
                      target_submenu_id: str,
                      db: Session = Depends(get_db)):
    return get_submenu_service(target_menu_id=target_menu_id,
                               target_submenu_id=target_submenu_id,
                               db=db)


@submenu_router.patch('/{target_submenu_id}',
                      name='Обновляет подменю',
                      response_model=Submenus,
                      tags=['Submenu'])
async def update_submenu(target_menu_id: str,
                         target_submenu_id: str,
                         submenu: SubmenusUpdate,
                         db: Session = Depends(get_db)):
    return update_submenu_service(target_menu_id=target_menu_id,
                                  target_submenu_id=target_submenu_id,
                                  submenu=submenu,
                                  db=db)


@submenu_router.delete('/{target_submenu_id}',
                       name='Удаляет подменю', tags=['Submenu'])
async def delete_submenu(target_menu_id: str,
                         target_submenu_id: str,
                         db: Session = Depends(get_db)):
    return delete_submenu_service(target_menu_id=target_menu_id,
                                  target_submenu_id=target_submenu_id,
                                  db=db)
