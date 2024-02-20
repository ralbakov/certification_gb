from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from menu_restaurant.api.submenu.crud import (
    create_submenu,
    delete_submenu,
    get_submenu,
    get_submenus,
    update_submenu,
)
from menu_restaurant.database.models import Submenus
from menu_restaurant.database.redis_tools import RedisCache


async def create_submenu_service(target_menu_id: str,
                                 submenu: AsyncSession = Depends(create_submenu)) -> Submenus | HTTPException:
    """Создает подменю"""
    if submenu is ValueError:
        raise HTTPException(status_code=409, detail='submenu with title alredy exist')
    await RedisCache.set_submenu_cache(target_menu_id=target_menu_id,
                                       target_submenu_id=submenu['target_submenu_id'],
                                       submenu=submenu['submenu']
                                       )
    return submenu['submenu']


async def get_all_submenu_service(target_menu_id: str,
                                  submenu: AsyncSession = Depends(get_submenus)) -> list[Submenus] | list[None]:
    """Получает все подменю"""
    get_all_submenu_cache = await RedisCache.get_all_submenu_cache(target_menu_id=target_menu_id)
    if get_all_submenu_cache is not None or get_all_submenu_cache == []:
        return get_all_submenu_cache
    return submenu


async def get_submenu_service(target_menu_id: str,
                              target_submenu_id: str,
                              submenu: AsyncSession = Depends(get_submenu)) -> Submenus | HTTPException:
    """Получает подменю"""

    if target_submenu_id in await RedisCache.get_all_keys_submenu(target_menu_id=target_menu_id):
        get_submenu_cache = await RedisCache.get_submenu_cache(target_menu_id=target_menu_id,
                                                               target_submenu_id=target_submenu_id
                                                               )
        return get_submenu_cache
    if submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    await RedisCache.set_submenu_cache(target_menu_id=target_menu_id,
                                       target_submenu_id=target_submenu_id,
                                       submenu=submenu
                                       )
    return submenu


async def update_submenu_service(target_menu_id: str,
                                 target_submenu_id: str,
                                 submenu: AsyncSession = Depends(update_submenu)) -> Submenus | HTTPException:
    """Обновляет подменю"""

    if submenu is None:
        return HTTPException(status_code=404, detail='submenu not found')
    elif submenu is ValueError:
        return HTTPException(status_code=409, detail='submenu with title alredy exist')
    await RedisCache.update_submenu_cache(target_menu_id=target_menu_id,
                                          target_submenu_id=target_submenu_id,
                                          submenu=submenu
                                          )
    return submenu


async def delete_submenu_service(target_menu_id: str,
                                 target_submenu_id: str,
                                 submenu: AsyncSession = Depends(delete_submenu)) -> None:
    """Удаляет подменю"""

    await RedisCache.delete_submenu_cache(target_menu_id=target_menu_id,
                                          target_submenu_id=target_submenu_id
                                          )
    return submenu
