from fastapi import APIRouter, Depends

from menu_restaurant.database.schemas import Dishes

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
                 status_code=200,
                 response_model=list[Dishes],
                 tags=['Dish']
                 )
async def get_list_dishes(all_dish=Depends(get_all_dish_service)):
    return all_dish


@dish_router.post('',
                  name='Создает блюдо',
                  status_code=201,
                  response_model=Dishes,
                  tags=['Dish'])
async def create_dishe(dish=Depends(create_dish_service)):
    return dish


@dish_router.get('/{target_dish_id}',
                 name='Просматривает определенное блюдо',
                 status_code=200,
                 response_model=Dishes,
                 tags=['Dish']
                 )
async def get_dish(dish=Depends(get_dish_service)):
    return dish


@dish_router.patch('/{target_dish_id}',
                   name='Обновляет блюдо',
                   response_model=Dishes,
                   tags=['Dish']
                   )
async def update_dish(dish=Depends(update_dish_service)):
    return dish


@dish_router.delete('/{target_dish_id}',
                    name='Удаляет блюдо',
                    tags=['Dish']
                    )
async def delete_dish(dish=Depends(delete_dish_service)):
    return dish
