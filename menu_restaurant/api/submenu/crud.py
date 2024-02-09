import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from menu_restaurant.api.dependency import get_db
from menu_restaurant.database.models import Submenus
from menu_restaurant.database.schemas import SubmenusCreate, SubmenusUpdate


def get_submenus(target_menu_id: str,
                 db: Session = Depends(get_db)
                 ) -> list[Submenus] | list[None]:
    return (
        db.query(Submenus)
        .filter(Submenus.target_menu_id == target_menu_id).all()
    )


def create_submenu(target_menu_id: str,
                   submenu: SubmenusCreate,
                   db: Session = Depends(get_db),
                   ) -> dict | ValueError:
    if (db.query(Submenus)
            .filter(Submenus.target_menu_id == target_menu_id,
                    Submenus.title == submenu.title)
            .one_or_none()) is not None:
        raise ValueError
    db_submenu = (Submenus(target_menu_id=target_menu_id,
                           id=str(uuid.uuid4()),
                           title=submenu.title,
                           description=submenu.description
                           )
                  )
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return {'target_submenu_id': str(db_submenu.id), 'submenu': db_submenu}


def get_submenu(target_menu_id: str,
                target_submenu_id: str,
                db: Session = Depends(get_db)
                ) -> Submenus | None:
    db_submenu = (db.query(Submenus)
                  .filter(Submenus.target_menu_id == target_menu_id,
                          Submenus.id == target_submenu_id)
                  .one_or_none()
                  )
    return db_submenu


def update_submenu(target_menu_id: str,
                   target_submenu_id: str,
                   submenu: SubmenusUpdate,
                   db: Session = Depends(get_db)) -> Submenus | None | ValueError:
    db_update_submenu = (
        db.query(Submenus)
        .filter(Submenus.target_menu_id == target_menu_id,
                Submenus.id == target_submenu_id
                )
        .one_or_none()
    )
    if db_update_submenu is None:
        return None
    if db_update_submenu.title == submenu.title:
        raise ValueError
    db_update_submenu.title = submenu.title
    db_update_submenu.description = submenu.description
    db.add(db_update_submenu)
    db.commit()
    db.refresh(db_update_submenu)
    return db_update_submenu


def delete_submenu(target_menu_id: str,
                   target_submenu_id: str,
                   db: Session = Depends(get_db)) -> None:
    (
        db.query(Submenus)
        .filter(Submenus.target_menu_id == target_menu_id,
                Submenus.id == target_submenu_id
                )
        .delete(synchronize_session=False)
    )
    db.commit()
    return None
