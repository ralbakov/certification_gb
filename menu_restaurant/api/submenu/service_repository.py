from fastapi import HTTPException
from sqlalchemy.orm import Session

from menu_restaurant.api.submenu import crud
from menu_restaurant.database.redis_tools import RedisCache
from menu_restaurant.database.schemas import SubmenusCreate, SubmenusUpdate


def create_submenu_service(target_menu_id: str, submenu: SubmenusCreate, db: Session):
    """Создает подменю"""
    create_submenu = crud.create_submenu(db=db, menus_id=target_menu_id, submenu=submenu)
    RedisCache.set_submenu(target_menu_id=target_menu_id,
                           id=str(create_submenu.id),
                           submenu=create_submenu
                           )
    return create_submenu


def get_all_submenu_service(target_menu_id: str, db: Session):
    """Получает все подменю"""

    get_all_submenu_cache = RedisCache.get_all_submenu(target_menu_id=target_menu_id)
    if get_all_submenu_cache is not None or get_all_submenu_cache == []:
        return get_all_submenu_cache

    db_all_submenu = crud.get_submenus(db=db, menus_id=target_menu_id)
    return db_all_submenu


def get_submenu_service(target_menu_id: str,
                        target_submenu_id: str,
                        db: Session):
    """Получает подменю"""

    if target_submenu_id not in RedisCache.get_all_keys_submenu(target_menu_id=target_menu_id):
        db_submenu = crud.get_submenu(db=db,
                                      menus_id=target_menu_id,
                                      submenu_id=target_submenu_id
                                      )
        if db_submenu is None:
            raise HTTPException(status_code=404, detail='submenu not found')
        RedisCache.set_submenu(target_menu_id=target_menu_id,
                               id=target_submenu_id,
                               submenu=db_submenu
                               )
        return db_submenu

    get_submenu_cache = RedisCache.get_submenu(target_menu_id=target_menu_id,
                                               id=target_submenu_id
                                               )
    return get_submenu_cache


def update_submenu_service(target_menu_id: str,
                           target_submenu_id: str,
                           submenu: SubmenusUpdate,
                           db: Session):
    """Обновляет подменю"""

    db_submenu = crud.update_submenu(db=db,
                                     menus_id=target_menu_id,
                                     submenu_id=target_submenu_id,
                                     submenu=submenu
                                     )
    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    RedisCache.update_submenu(target_menu_id=target_menu_id,
                              id=target_submenu_id,
                              submenu=db_submenu
                              )
    return db_submenu


def delete_submenu_service(target_menu_id: str,
                           target_submenu_id: str,
                           db: Session):
    """Удаляет подменю"""

    crud.delete_submenu(db=db,
                        menus_id=target_menu_id,
                        submenu_id=target_submenu_id)
    RedisCache.delete_submenu(target_menu_id=target_menu_id,
                              id=target_submenu_id
                              )
    return None
