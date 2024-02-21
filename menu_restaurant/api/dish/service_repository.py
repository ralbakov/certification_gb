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


async def create_dish_service(target_menu_id: str,
                              target_submenu_id: str,
                              dish: Dishes = Depends(create_dish)) -> Dishes | HTTPException:
    """Создает блюдо"""

    await RedisCache.set_dish_cache(target_menu_id=target_menu_id,
                                    target_submenu_id=target_submenu_id,
                                    target_dish_id=dish['target_dish_id'],
                                    dish=dish['dish']
                                    )
    return dish['dish']


async def get_all_dish_service(target_submenu_id: str,
                               dish: Dishes = Depends(get_dishes)) -> list[Dishes] | list[None]:
    """Получает все блюда"""

    get_all_dish_cache = await RedisCache.get_all_dish_cache(target_submenu_id=target_submenu_id)
    if get_all_dish_cache is not None or get_all_dish_cache == []:
        return get_all_dish_cache
    return dish


async def get_dish_service(target_menu_id: str,
                           target_submenu_id: str,
                           target_dish_id: str,
                           dish: Dishes = Depends(get_dish)) -> Dishes | HTTPException:
    """Получает блюдо"""

    if target_dish_id in await RedisCache.get_all_keys_dishes(target_submenu_id=target_submenu_id):
        get_dish_cache = await RedisCache.get_dish_cache(target_submenu_id=target_submenu_id,
                                                         target_dish_id=target_dish_id)
        return get_dish_cache
    if dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    await RedisCache.set_dish_cache(target_menu_id=target_menu_id,
                                    target_submenu_id=target_submenu_id,
                                    target_dish_id=target_dish_id,
                                    dish=dish)
    return dish


async def update_dish_service(target_submenu_id: str,
                              target_dish_id: str,
                              dish: Dishes = Depends(update_dish)) -> Dishes | HTTPException:
    """Обновляет блюдо"""
    if dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    await RedisCache.update_dish_cache(target_submenu_id=target_submenu_id,
                                       target_dish_id=target_dish_id,
                                       dish=dish
                                       )
    return dish


async def delete_dish_service(target_menu_id: str,
                              target_submenu_id: str,
                              target_dish_id: str,
                              dish: Dishes = Depends(delete_dish)) -> None:
    """Удаляет блюдо"""

    await RedisCache.delete_dish_cache(target_menu_id=target_menu_id,
                                       target_submenu_id=target_submenu_id,
                                       target_dish_id=target_dish_id)
    return None
