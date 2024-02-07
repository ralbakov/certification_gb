from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from menu_restaurant.database.dependency import get_db
from menu_restaurant.database.schemas import Dishes, DishesCreate, DishesUpdate

from ..dish.service_repository import (
    create_dish_service,
    delete_dish_service,
    get_all_dish_service,
    get_dish_service,
    update_dish_service,
)

dish_router = APIRouter(prefix=('/api/v1/menus'
                                '/{target_menu_id}'
                                '/submenus/{target_submenu_id}/dishes'))


@dish_router.get('',
                 name='Просматривает список блюд',
                 response_model=list[Dishes],
                 tags=['Dish']
                 )
async def get_list_dishes(target_menu_id: str,
                          target_submenu_id: str,
                          db: Session = Depends(get_db)):
    return get_all_dish_service(target_menu_id=target_menu_id,
                                target_submenu_id=target_submenu_id,
                                db=db)


@dish_router.post('',
                  name='Создает блюдо',
                  status_code=201,
                  response_model=Dishes,
                  tags=['Dish'])
async def create_dishe(target_menu_id: str,
                       target_submenu_id: str,
                       dish: DishesCreate,
                       db: Session = Depends(get_db)):
    return create_dish_service(target_menu_id=target_menu_id,
                               target_submenu_id=target_submenu_id,
                               dish=dish,
                               db=db)


@dish_router.get('/{target_dish_id}',
                 name='Просматривает определенное блюдо',
                 response_model=Dishes,
                 tags=['Dish']
                 )
async def get_dish(target_menu_id: str,
                   target_submenu_id: str,
                   target_dish_id: str,
                   db: Session = Depends(get_db)):
    return get_dish_service(target_menu_id=target_menu_id,
                            target_submenu_id=target_submenu_id,
                            target_dish_id=target_dish_id,
                            db=db)


@dish_router.patch('/{target_dish_id}',
                   name='Обновляет блюдо',
                   response_model=Dishes,
                   tags=['Dish']
                   )
async def update_dish(target_menu_id: str,
                      target_submenu_id: str,
                      target_dish_id: str,
                      dish: DishesUpdate,
                      db: Session = Depends(get_db)):
    return update_dish_service(target_menu_id=target_menu_id,
                               target_submenu_id=target_submenu_id,
                               target_dish_id=target_dish_id,
                               dish=dish,
                               db=db)


@dish_router.delete('/{target_dish_id}',
                    name='Удаляет блюдо',
                    tags=['Dish']
                    )
async def delete_dish(target_menu_id: str,
                      target_submenu_id: str,
                      target_dish_id: str,
                      db: Session = Depends(get_db)):
    return delete_dish_service(target_menu_id=target_menu_id,
                               target_submenu_id=target_submenu_id,
                               target_dish_id=target_dish_id,
                               db=db)
