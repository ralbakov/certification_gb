from sqlalchemy.orm import Session
import uuid


from . import models, schemas

def get_menus(db: Session):
    return db.query(models.Menus).all()


def get_menu(db: Session, menus_id: str):
    return db.query(models.Menus).filter(models.Menus.target_menu_id == menus_id).all()


def create_menu(db: Session, menu: schemas.MenusCreate): # создает меню
    db_menu = models.Menus(target_menu_title=menu.title, target_menu_description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menus_id: str, menu: schemas.MenusCreate):
    db_menu = db.query(models.Menus) \
        .filter(models.Menus.target_menu_id == menus_id).first()
    if db_menu.target_menu_title != menu.title and db_menu.target_menu_description != menu.description:
        db_menu.target_menu_title = menu.title
        db_menu.target_menu_description = menu.description
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu
    raise

def delete_menu(db: Session, menus_id: str):
    db.query(models.Menus) \
        .filter(models.Menus.target_menu_id == menus_id) \
        .delete(synchronize_session=False)
    db.commit()
    return {"message": "menu deleted"}


def get_submenus(db: Session, menus_id: str):
    return db.query(models.Submenus).filter(models.Submenus.target_menu_id == menus_id).all()

def create_submenu(db: Session, menus_id: str, submenu: schemas.SubmenusCreate):
    db_menu_submenu = db.query(models.Submenus).filter(models.Submenus.target_menu_id == menus_id).first()
    db_menu_submenu = models.Submenus(target_menu_id = menus_id, target_submenu_title=submenu.title, target_submenu_description=submenu.description)
    db.add(db_menu_submenu)
    db.commit()
    db.refresh(db_menu_submenu)
    return db_menu_submenu

def get_submenu(db: Session, menus_id: str, submenu_id: str):
    return db.query(models.Submenus) \
            .filter(models.Submenus.target_menu_id == menus_id, models.Submenus.target_submenu_id == submenu_id).all()

def update_submenu(db: Session, menus_id: str, submenu_id: str, submenu: schemas.SubmenusCreate):
    db_update_submenu = db.query(models.Submenus) \
            .filter(models.Submenus.target_menu_id == menus_id, models.Submenus.target_submenu_id == submenu_id).first()
    db_update_submenu.target_submenu_title = submenu.title
    db_update_submenu.target_submenu_description = submenu.description
    db.add(db_update_submenu)
    db.commit()
    db.refresh(db_update_submenu)
    return db_update_submenu

def delete_submenu(db: Session, menus_id: str, submenu_id: str):
    db.query(models.Submenus) \
            .filter(models.Submenus.target_menu_id == menus_id, models.Submenus.target_submenu_id == submenu_id) \
            .delete(synchronize_session=False)
    db.commit()
    return {"message": "submenu deleted"}


def get_dishes(db: Session, menus_id: str, submenu_id: str):
    return db.query(models.Dishes) \
            .filter(models.Dishes.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id).all()


def create_dish(db: Session, menus_id: str, submenu_id: str, dish: schemas.DishesCreate):
    db_create_dish = db.query(models.Dishes).filter(models.Submenus.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id).first()
    db_create_dish = models.Dishes(target_dish_id=str(uuid.uuid4()), target_submenu_id=submenu_id, target_dish_title=dish.title, target_dish_description=dish.description, target_dish_price=dish.price)
    db.add(db_create_dish)
    db.commit()
    db.refresh(db_create_dish)
    return db_create_dish


def get_dish(db: Session, menus_id: str, submenu_id: str, dishes_id):
    return db.query(models.Dishes) \
            .filter(models.Dishes.target_dish_id == dishes_id, models.Dishes.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id).all()

def update_dish(db: Session, menus_id: str, submenu_id: str, dishes_id: str, dish: schemas.DishesCreate):
    db_update_dish = db.query(models.Dishes) \
            .filter(models.Dishes.target_dish_id == dishes_id, models.Dishes.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id).first()
    db_update_dish.target_dish_title = dish.title
    db_update_dish.target_dish_description = dish.description
    db_update_dish.target_dish_price = dish.price
    db.add(db_update_dish)
    db.commit()
    db.refresh(db_update_dish)
    return db_update_dish

def delete_dish(db: Session, menus_id: str, submenu_id: str, dishes_id: str):
    db.query(models.Dishes) \
            .filter(models.Dishes.target_dish_id == dishes_id, models.Dishes.target_submenu_id == submenu_id, models.Submenus.target_menu_id == menus_id) \
            .delete(synchronize_session=False)
    db.commit()
    return {"message": "dish deleted"}



