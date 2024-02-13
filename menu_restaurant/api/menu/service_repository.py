from fastapi import Depends, HTTPException

from menu_restaurant.api.menu.crud import (
    create_menu,
    delete_menu,
    get_menu,
    get_menus,
    update_menu,
)
from menu_restaurant.database.models import Menus
from menu_restaurant.database.redis_tools import RedisCache


def create_menu_service(menu=Depends(create_menu)) -> Menus:
    """Создает меню"""
    RedisCache.set_menu_cache(target_menu_id=menu['target_menu_id'], menu=menu['menu'])
    return menu['menu']


def get_all_menu_service(menu=Depends(get_menus)) -> list[Menus] | list[None]:
    """Получает все меню"""

    get_all_menu_cache = RedisCache.get_all_menu_cache()
    if get_all_menu_cache is not None or get_all_menu_cache == []:
        return get_all_menu_cache
    return menu


def get_menu_service(target_menu_id: str,
                     menu=Depends(get_menu)) -> Menus | HTTPException:
    """Получает меню"""

    if target_menu_id in RedisCache.get_all_keys_menu():
        get_menu_cache = RedisCache.get_menu_cache(target_menu_id=target_menu_id)
        return get_menu_cache
    if menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    RedisCache.set_menu_cache(target_menu_id=target_menu_id, menu=menu)
    return menu


def update_menu_service(target_menu_id: str,
                        menu=Depends(update_menu)) -> Menus | HTTPException:
    """Обновляет меню"""

    if menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    elif menu is ValueError:
        raise HTTPException(status_code=409, detail='menu with title alredy exist')
    RedisCache.update_menu_cache(target_menu_id=target_menu_id, menu=menu)
    return menu


def delete_menu_service(target_menu_id: str,
                        menu=Depends(delete_menu)) -> None:
    """Удаляет меню"""

    RedisCache.delete_menu_cache(target_menu_id=target_menu_id)
    return menu
