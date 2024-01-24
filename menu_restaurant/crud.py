from sqlalchemy.orm import Session
import uuid


from . import models, schemas

def get_menus(db: Session):
    return db.query(models.Menus).all()


def get_menu(db: Session, menus_id: str):
    return db.query(models.Menus).filter(models.Menus.id == menus_id).one_or_none()


def create_menu(db: Session, menu: schemas.MenusCreate): # создает меню
    db_menu = models.Menus(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menus_id: str, menu: schemas.MenusCreate):
    db_menu = db.query(models.Menus) \
        .filter(models.Menus.id == menus_id).one_or_none()
    if db_menu.title != menu.title and db_menu.description != menu.description:
        db_menu.title = menu.title
        db_menu.description = menu.description
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu
    raise

def delete_menu(db: Session, menus_id: str):
    db.query(models.Menus) \
        .filter(models.Menus.id == menus_id) \
        .delete(synchronize_session=False)
    db.commit()
    return {"message": "menu deleted"}


def get_submenus(db: Session, menus_id: str):
    return db.query(models.Submenus).filter(models.Submenus.target_menu_id == menus_id).all()

def create_submenu(db: Session, menus_id: str, submenu: schemas.SubmenusCreate):
    db_menu_submenu = db.query(models.Submenus).filter(models.Submenus.target_menu_id == menus_id).one_or_none()
    db_menu_submenu = models.Submenus(target_menu_id = menus_id, title=submenu.title, description=submenu.description)
    db.add(db_menu_submenu)
    db.commit()
    db.refresh(db_menu_submenu)
    return db_menu_submenu

def get_submenu(db: Session, menus_id: str, submenu_id: str):
    return db.query(models.Submenus) \
            .filter(models.Submenus.target_menu_id == menus_id, models.Submenus.id == submenu_id).one_or_none()

def update_submenu(db: Session, menus_id: str, submenu_id: str, submenu: schemas.SubmenusCreate):
    db_update_submenu = db.query(models.Submenus) \
            .filter(models.Submenus.target_menu_id == menus_id, models.Submenus.id == submenu_id).one_or_none()
    db_update_submenu.title = submenu.title
    db_update_submenu.description = submenu.description
    db.add(db_update_submenu)
    db.commit()
    db.refresh(db_update_submenu)
    return db_update_submenu

def delete_submenu(db: Session, menus_id: str, submenu_id: str):
    db.query(models.Submenus) \
            .filter(models.Submenus.target_menu_id == menus_id, models.Submenus.id == submenu_id) \
            .delete(synchronize_session=False)
    db.commit()
    return {"message": "submenu deleted"}


def get_dishes(db: Session, menus_id: str, submenu_id: str):
    return db.query(models.Dishes) \
            .filter(models.Dishes.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id).all()

def create_dish(db: Session, menus_id: str, submenu_id: str, dish: schemas.DishesCreate):
    db_create_dish = db.query(models.Dishes).filter(models.Submenus.id == submenu_id, models.Submenus.target_menu_id == menus_id).one_or_none()
    db_create_dish = models.Dishes(id=str(uuid.uuid4()), target_submenu_id=submenu_id, title=dish.title, description=dish.description, price=dish.price)
    db.add(db_create_dish)
    db.commit()
    db.refresh(db_create_dish)
    return db_create_dish

def get_dish(db: Session, menus_id: str, submenu_id: str, dishes_id):
    return db.query(models.Dishes) \
            .filter(models.Dishes.id == dishes_id, models.Dishes.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id).one_or_none()

def update_dish(db: Session, menus_id: str, submenu_id: str, dishes_id: str, dish: schemas.DishesCreate):
    db_update_dish = db.query(models.Dishes) \
            .filter(models.Dishes.id == dishes_id, models.Dishes.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id).one_or_none()
    db_update_dish.title = dish.title
    db_update_dish.description = dish.description
    db_update_dish.price = dish.price
    db.add(db_update_dish)
    db.commit()
    db.refresh(db_update_dish)
    return db_update_dish

def delete_dish(db: Session, menus_id: str, submenu_id: str, dishes_id: str):
    db.query(models.Dishes) \
            .filter(models.Dishes.id == dishes_id, models.Dishes.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id) \
            .delete(synchronize_session=False)
    db.commit()
    return {"message": "dish deleted"}