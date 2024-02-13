from fastapi import Depends, HTTPException

from menu_restaurant.api.dish.crud import (
    create_dish,
    delete_dish,
    get_dish,
    get_dishes,
    update_dish,
)
from menu_restaurant.database.models import Dishes
from menu_restaurant.database.redis_tools import RedisCache


def create_dish_service(target_menu_id: str,
                        target_submenu_id: str,
                        dish=Depends(create_dish)) -> Dishes | HTTPException:
    """Создает блюдо"""
    if dish is ValueError:
        raise HTTPException(status_code=409, detail='dish with title alredy exist')
    RedisCache.set_dish_cache(target_menu_id=target_menu_id,
                              target_submenu_id=target_submenu_id,
                              target_dish_id=dish['target_dish_id'],
                              dish=dish['dish']
                              )
    return dish['dish']


def get_all_dish_service(target_submenu_id: str,
                         dish=Depends(get_dishes)) -> list[Dishes] | list[None]:
    """Получает все блюда"""

    get_all_dish_cache = RedisCache.get_all_dish_cache(target_submenu_id=target_submenu_id)
    if get_all_dish_cache is not None or get_all_dish_cache == []:
        return get_all_dish_cache
    return dish


def get_dish_service(target_menu_id: str,
                     target_submenu_id: str,
                     target_dish_id: str,
                     dish=Depends(get_dish)) -> Dishes | HTTPException:
    """Получает блюдо"""

    if target_dish_id in RedisCache.get_all_keys_dishes(target_submenu_id=target_submenu_id):
        get_dish_cache = RedisCache.get_dish_cache(target_submenu_id=target_submenu_id,
                                                   target_dish_id=target_dish_id)
        return get_dish_cache
    if dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    RedisCache.set_dish_cache(target_menu_id=target_menu_id,
                              target_submenu_id=target_submenu_id,
                              target_dish_id=target_dish_id,
                              dish=dish)
    return dish


def update_dish_service(target_submenu_id: str,
                        target_dish_id: str,
                        dish=Depends(update_dish)) -> Dishes | HTTPException:
    """Обновляет блюдо"""
    if dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    if dish is ValueError:
        raise HTTPException(status_code=409, detail='dish with title alredy exist')
    RedisCache.update_dish_cache(target_submenu_id=target_submenu_id,
                                 target_dish_id=target_dish_id,
                                 dish=dish
                                 )
    return dish


def delete_dish_service(target_menu_id: str,
                        target_submenu_id: str,
                        target_dish_id: str,
                        dish=Depends(delete_dish)) -> None:
    """Удаляет блюдо"""

    RedisCache.delete_dish_cache(target_menu_id=target_menu_id,
                                 target_submenu_id=target_submenu_id,
                                 target_dish_id=target_dish_id)
    return dish
