import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from menu_restaurant.database.dependency import get_db
from menu_restaurant.database.models import Dishes, Submenus
from menu_restaurant.database.schemas import DishesCreate, DishesUpdate


def get_dishes(target_menu_id: str,
               target_submenu_id: str,
               db: Session = Depends(get_db)
               ) -> list[Dishes] | list[None]:
    return (
        db.query(Dishes)
        .join(Submenus)
        .filter(Submenus.id == target_submenu_id,
                Submenus.target_menu_id == target_menu_id
                )
        .all()
    )


def create_dish(target_menu_id: str,
                target_submenu_id: str,
                dish_schema: DishesCreate,
                db: Session = Depends(get_db)) -> dict | ValueError:
    db_create_dish = (db.query(Dishes)
                      .join(Submenus)
                      .filter(Submenus.id == target_submenu_id,
                              Submenus.target_menu_id == target_menu_id,
                              Dishes.title == dish_schema.title
                              )
                      .one_or_none()
                      )
    if db_create_dish is not None:
        raise ValueError
    db_create_dish = Dishes(id=str(uuid.uuid4()),
                            target_submenu_id=target_submenu_id,
                            title=dish_schema.title,
                            description=dish_schema.description,
                            price=dish_schema.price
                            )
    db.add(db_create_dish)
    db.commit()
    db.refresh(db_create_dish)
    return {'target_dish_id': str(db_create_dish.id), 'dish': db_create_dish}


def get_dish(target_menu_id: str,
             target_submenu_id: str,
             target_dish_id: str,
             db: Session = Depends(get_db)) -> Dishes | None:
    db_dish = (db.query(Dishes)
               .join(Submenus)
               .filter(
        Submenus.id == target_submenu_id,
        Submenus.target_menu_id == target_menu_id,
        Dishes.id == target_dish_id,
    )
        .one_or_none()
    )
    return db_dish


def update_dish(target_menu_id: str,
                target_submenu_id: str,
                target_dish_id: str,
                dish_schema: DishesUpdate,
                db: Session = Depends(get_db)) -> Dishes | None | ValueError:
    db_update_dish = (db.query(Dishes)
                      .join(Submenus)
                      .filter(Dishes.id == target_dish_id,
                              Submenus.id == target_submenu_id,
                              Submenus.target_menu_id == target_menu_id
                              )
                      .one_or_none()
                      )
    if db_update_dish is None:
        return None
    if db_update_dish.title == dish_schema.title:
        raise ValueError
    db_update_dish.title = dish_schema.title
    db_update_dish.description = dish_schema.description
    db_update_dish.price = dish_schema.price
    db.add(db_update_dish)
    db.commit()
    db.refresh(db_update_dish)
    return db_update_dish


def delete_dish(target_menu_id: str,
                target_submenu_id: str,
                target_dish_id: str,
                db: Session = Depends(get_db)) -> None:
    (
        db.query(Dishes)
        .filter(
            Submenus.id == target_submenu_id,
            Submenus.target_menu_id == target_menu_id,
            Dishes.id == target_dish_id,
        )
        .delete(synchronize_session=False)
    )
    db.commit()
    return None
