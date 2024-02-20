from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.api.menu.crud import (
    create_menu,
    delete_menu,
    get_menu,
    get_menus,
    update_menu,
)
from menu_restaurant.database.models import Menus
from menu_restaurant.database.redis_tools import RedisCache


async def create_menu_service(menu: AsyncSession = Depends(create_menu)) -> Menus | HTTPException:
    """Создает меню"""
    if menu is ValueError:
        raise HTTPException(status_code=409, detail='menu with title alredy exist')
    await RedisCache.set_menu_cache(target_menu_id=menu['target_menu_id'], menu=menu['menu'])
    return menu['menu']


async def get_all_menu_service(menu: AsyncSession = Depends(get_menus)) -> list[Menus] | list[None]:
    """Получает все меню"""

    get_all_menu_cache = await RedisCache.get_all_menu_cache()
    if get_all_menu_cache is not None or get_all_menu_cache == []:
        return get_all_menu_cache
    return menu


async def get_menu_service(target_menu_id: str,
                           menu: AsyncSession = Depends(get_menu)) -> Menus | HTTPException:
    """Получает меню"""

    if target_menu_id in await RedisCache.get_all_keys_menu():
        get_menu_cache = await RedisCache.get_menu_cache(target_menu_id=target_menu_id)
        return get_menu_cache
    if menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    await RedisCache.set_menu_cache(target_menu_id=target_menu_id, menu=menu)
    return menu


async def update_menu_service(target_menu_id: str,
                              menu: AsyncSession = Depends(update_menu)) -> Menus | HTTPException:
    """Обновляет меню"""

    if menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    elif menu is ValueError:
        raise HTTPException(status_code=409, detail='menu with title alredy exist')
    await RedisCache.update_menu_cache(target_menu_id=target_menu_id, menu=menu)
    return menu


async def delete_menu_service(target_menu_id: str,
                              menu: AsyncSession = Depends(delete_menu)) -> None:
    """Удаляет меню"""

    await RedisCache.delete_menu_cache(target_menu_id=target_menu_id)
    return menu
