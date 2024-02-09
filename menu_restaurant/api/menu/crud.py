import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from menu_restaurant.api.dependency import get_db
from menu_restaurant.database.models import Menus
from menu_restaurant.database.schemas import MenusCreate, MenusUpdate


def get_menus(db: Session = Depends(get_db)) -> list[Menus] | list[None]:
    return db.query(Menus).all()


def get_menu(target_menu_id: str,
             db: Session = Depends(get_db)) -> Menus | None:
    menu = (
        db.query(Menus)
        .filter(Menus.id == target_menu_id).one_or_none()
    )
    return menu


def create_menu(menu_schema: MenusCreate,
                db: Session = Depends(get_db)
                ) -> dict | ValueError:
    if (db.query(Menus)
            .filter(Menus.title == menu_schema.title)
            .one_or_none()) is not None:
        raise ValueError
    menu = Menus(id=str(uuid.uuid4()),
                 title=menu_schema.title,
                 description=menu_schema.description
                 )
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return {'target_menu_id': str(menu.id), 'menu': menu}


def update_menu(target_menu_id: str,
                menu_schema: MenusUpdate,
                db: Session = Depends(get_db),
                ) -> Menus | None | ValueError:
    menu = (db.query(Menus)
            .filter(Menus.id == target_menu_id)
            .one_or_none()
            )
    if menu is None:
        return None
    if menu.title == menu_schema.title:
        raise ValueError
    menu.title = menu_schema.title
    menu.description = menu_schema.description
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def delete_menu(target_menu_id: str, db: Session = Depends(get_db)) -> None:
    (
        db.query(Menus)
        .filter(Menus.id == target_menu_id)
        .delete(synchronize_session=False)
    )
    db.commit()
    return None
