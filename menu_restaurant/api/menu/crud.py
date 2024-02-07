import uuid

from sqlalchemy.orm import Session

from menu_restaurant.database import models
from menu_restaurant.database.schemas import MenusCreate, MenusUpdate


def get_menus(db: Session) -> list[models.Menus] | list[None]:
    return db.query(models.Menus).all()


def get_menu(menus_id: str, db: Session) -> models.Menus | None:
    return (
        db.query(models.Menus)
        .filter(models.Menus.id == menus_id).one_or_none()
    )


def create_menu(menu: MenusCreate, db: Session) -> models.Menus:
    if (db.query(models.Menus)
            .filter(models.Menus.title == menu.title)
            .one_or_none()) is not None:
        raise ValueError('Menu with title alredy exist')
    db_menu = models.Menus(id=str(uuid.uuid4()),
                           title=menu.title,
                           description=menu.description
                           )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(menus_id: str,
                menu: MenusUpdate,
                db: Session,
                ) -> models.Menus | None:
    db_menu = (db.query(models.Menus)
               .filter(models.Menus.id == menus_id)
               .one_or_none()
               )
    if db_menu.title == menu.title:
        raise ValueError('Menu with title alredy exist')
    db_menu.title = menu.title
    db_menu.description = menu.description
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def delete_menu(menus_id: str, db: Session) -> None:
    (
        db.query(models.Menus)
        .filter(models.Menus.id == menus_id)
        .delete(synchronize_session=False)
    )
    db.commit()
    return None
