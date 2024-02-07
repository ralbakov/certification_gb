import uuid

from sqlalchemy.orm import Session

from menu_restaurant.database import models
from menu_restaurant.database.schemas import SubmenusCreate, SubmenusUpdate


def get_submenus(menus_id: str, db: Session) -> models.Submenus | list[None]:
    return (
        db.query(models.Submenus)
        .filter(models.Submenus.target_menu_id == menus_id).all()
    )


def create_submenu(menus_id: str,
                   db: Session,
                   submenu: SubmenusCreate) -> models.Submenus:
    db_submenu = (db.query(models.Submenus)
                  .filter(models.Submenus.target_menu_id == menus_id)
                  .one_or_none()
                  )
    if (db.query(models.Submenus)
            .filter(models.Submenus.target_menu_id == menus_id,
                    models.Submenus.title == submenu.title)
            .one_or_none()) is not None:
        raise ValueError('Submenu with title alredy exist')
    db_submenu = (models.Submenus(target_menu_id=menus_id,
                                  id=str(uuid.uuid4()),
                                  title=submenu.title,
                                  description=submenu.description
                                  )
                  )
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def get_submenu(menus_id: str,
                submenu_id: str,
                db: Session
                ) -> models.Submenus | None:
    return (
        db.query(models.Submenus)
        .filter(models.Submenus.target_menu_id == menus_id,
                models.Submenus.id == submenu_id
                )
        .one_or_none()
    )


def update_submenu(db: Session, menus_id: str,
                   submenu_id: str,
                   submenu: SubmenusUpdate) -> models.Submenus | None:
    db_update_submenu = (
        db.query(models.Submenus)
        .filter(models.Submenus.target_menu_id == menus_id,
                models.Submenus.id == submenu_id
                )
        .one_or_none()
    )
    if db_update_submenu.title == submenu.title:
        raise ValueError('Submenu with title alredy exist')
    db_update_submenu.title = submenu.title
    db_update_submenu.description = submenu.description
    db.add(db_update_submenu)
    db.commit()
    db.refresh(db_update_submenu)
    return db_update_submenu


def delete_submenu(menus_id: str, submenu_id: str, db: Session) -> None:
    (
        db.query(models.Submenus)
        .filter(models.Submenus.target_menu_id == menus_id,
                models.Submenus.id == submenu_id
                )
        .delete(synchronize_session=False)
    )
    db.commit()
    return None
