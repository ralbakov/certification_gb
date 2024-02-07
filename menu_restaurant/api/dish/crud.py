import uuid

from sqlalchemy.orm import Session

from menu_restaurant.database import models
from menu_restaurant.database.schemas import DishesCreate, DishesUpdate


def get_dishes(db: Session,
               menus_id: str,
               submenu_id: str) -> list[models.Dishes] | list[None]:
    return (
        db.query(models.Dishes)
        .filter(models.Dishes.target_submenu_id == submenu_id,
                models.Submenus.target_menu_id == menus_id
                )
        .all()
    )


def create_dish(db: Session,
                menus_id: str,
                submenu_id: str,
                dish: DishesCreate) -> models.Dishes:
    db_create_dish = (db.query(models.Dishes)
                      .filter(models.Submenus.id == submenu_id,
                              models.Submenus.target_menu_id == menus_id
                              )
                      .one_or_none()
                      )
    if (db.query(models.Dishes)
            .filter(models.Dishes.target_submenu_id == submenu_id,
                    models.Dishes.title == dish.title,
                    models.Submenus.target_menu_id == menus_id
                    )
            .one_or_none()) is not None:
        raise ValueError('Dish with title alredy exist')
    db_create_dish = models.Dishes(id=str(uuid.uuid4()),
                                   target_submenu_id=submenu_id,
                                   title=dish.title,
                                   description=dish.description,
                                   price=dish.price
                                   )
    db.add(db_create_dish)
    db.commit()
    db.refresh(db_create_dish)
    return db_create_dish


def get_dish(db: Session,
             menus_id: str,
             submenu_id: str,
             dishes_id) -> models.Dishes | None:
    return (
        db.query(models.Dishes)
        .filter(models.Dishes.id == dishes_id,
                models.Dishes.target_submenu_id == submenu_id,
                models.Submenus.target_menu_id == menus_id
                )
        .one_or_none()
    )


def update_dish(db: Session,
                menus_id: str,
                submenu_id: str,
                dishes_id: str,
                dish: DishesUpdate) -> models.Dishes | None:
    db_update_dish = (db.query(models.Dishes)
                      .filter(models.Dishes.id == dishes_id,
                              models.Dishes.target_submenu_id == submenu_id,
                              models.Submenus.target_menu_id == menus_id
                              )
                      .one_or_none()
                      )
    if db_update_dish.title == dish.title:
        raise ValueError('Dish with title alredy exist')
    db_update_dish.title = dish.title
    db_update_dish.description = dish.description
    db_update_dish.price = dish.price
    db.add(db_update_dish)
    db.commit()
    db.refresh(db_update_dish)
    return db_update_dish


def delete_dish(db: Session,
                menus_id: str,
                submenu_id: str,
                dishes_id: str) -> None:
    (
        db.query(models.Dishes)
        .filter(models.Dishes.id == dishes_id,
                models.Dishes.target_submenu_id == submenu_id,
                models.Submenus.target_menu_id == menus_id
                )
        .delete(synchronize_session=False)
    )
    db.commit()
    return None
