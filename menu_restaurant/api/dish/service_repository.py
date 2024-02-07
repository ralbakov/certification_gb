from fastapi import HTTPException
from sqlalchemy.orm import Session

from menu_restaurant.api.dish import crud
from menu_restaurant.database.redis_tools import RedisCache
from menu_restaurant.database.schemas import DishesCreate, DishesUpdate


def create_dish_service(target_menu_id: str,
                        target_submenu_id: str,
                        dish: DishesCreate,
                        db: Session):
    """Создает блюдо"""

    create_dish = crud.create_dish(db=db,
                                   menus_id=target_menu_id,
                                   submenu_id=target_submenu_id,
                                   dish=dish
                                   )
    RedisCache.set_dish(target_menu_id=target_menu_id,
                        target_submenu_id=target_submenu_id,
                        id=str(create_dish.id),
                        dish=create_dish
                        )
    return create_dish


def get_all_dish_service(target_menu_id: str, target_submenu_id: str, db: Session):
    """Получает все блюда"""

    get_all_dish_cache = RedisCache.get_all_dish(target_submenu_id=target_submenu_id)
    if get_all_dish_cache is not None or get_all_dish_cache == []:
        return get_all_dish_cache
    db_all_dish = crud.get_dishes(db=db,
                                  menus_id=target_menu_id,
                                  submenu_id=target_submenu_id
                                  )
    return db_all_dish


def get_dish_service(target_menu_id: str,
                     target_submenu_id: str,
                     target_dish_id: str,
                     db: Session):
    """Получает блюдо"""

    if target_dish_id not in RedisCache.get_all_keys_dishes(target_submenu_id=target_submenu_id):
        db_dish = crud.get_dish(db=db,
                                menus_id=target_menu_id,
                                submenu_id=target_submenu_id,
                                dishes_id=target_dish_id
                                )
        if db_dish is None:
            raise HTTPException(status_code=404, detail='dish not found')
        RedisCache.set_dish(target_menu_id=target_menu_id,
                            target_submenu_id=target_submenu_id,
                            id=target_dish_id,
                            dish=db_dish)
        return db_dish

    get_dish_cache = RedisCache.get_dish(target_submenu_id=target_submenu_id,
                                         id=target_dish_id)
    return get_dish_cache


def update_dish_service(target_menu_id: str,
                        target_submenu_id: str,
                        target_dish_id: str,
                        dish: DishesUpdate,
                        db: Session):
    """Обновляет блюдо"""

    db_dish = crud.update_dish(db=db,
                               menus_id=target_menu_id,
                               submenu_id=target_submenu_id,
                               dishes_id=target_dish_id,
                               dish=dish
                               )
    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    RedisCache.update_dish(target_submenu_id=target_submenu_id,
                           id=target_dish_id,
                           dish=db_dish
                           )
    return db_dish


def delete_dish_service(target_menu_id: str,
                        target_submenu_id: str,
                        target_dish_id: str,
                        db: Session):
    """Удаляет блюдо"""

    crud.delete_dish(db=db,
                     menus_id=target_menu_id,
                     submenu_id=target_submenu_id,
                     dishes_id=target_dish_id
                     )
    RedisCache.delete_dish(target_menu_id=target_menu_id,
                           target_submenu_id=target_submenu_id,
                           id=target_dish_id)
    return {'message': 'dish delete'}
