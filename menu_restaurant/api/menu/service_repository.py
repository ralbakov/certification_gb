from fastapi import HTTPException
from sqlalchemy.orm import Session

from menu_restaurant.api.menu import crud
from menu_restaurant.database.redis_tools import RedisCache
from menu_restaurant.database.schemas import MenusCreate, MenusUpdate


def create_menu_service(menu: MenusCreate, db: Session):
    """Создает меню"""

    db_menu = crud.create_menu(db=db, menu=menu)
    RedisCache.set_menu(id=str(db_menu.id), menu=db_menu)
    return db_menu


def get_all_menu_service(db: Session):
    """Получает все меню"""

    get_all_menu_cache = RedisCache.get_all_menu()
    if get_all_menu_cache is not None or get_all_menu_cache == []:
        return get_all_menu_cache

    get_all_menu_db = crud.get_menus(db)
    return get_all_menu_db


def get_menu_service(target_menu_id: str,
                     db: Session):
    """Получает меню"""

    if target_menu_id not in RedisCache.get_all_keys_menu():
        get_menu_db = crud.get_menu(menus_id=target_menu_id, db=db)
        if get_menu_db is None:
            raise HTTPException(status_code=404, detail='menu not found')
        RedisCache.set_menu(id=target_menu_id, menu=get_menu_db)
        return get_menu_db

    get_menu_cache = RedisCache.get_menu(id=target_menu_id)
    return get_menu_cache


def update_menu_service(target_menu_id: str,
                        menu: MenusUpdate,
                        db: Session):
    """Обновляет меню"""

    update_menu = crud.update_menu(menus_id=target_menu_id, menu=menu, db=db)
    if update_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    RedisCache.update_menu(id=target_menu_id, menu=update_menu)
    return update_menu


def delete_menu_service(target_menu_id: str, db: Session):
    """Удаляет меню"""

    crud.delete_menu(menus_id=target_menu_id, db=db)
    RedisCache.delete_menu(id=target_menu_id)
    return None
