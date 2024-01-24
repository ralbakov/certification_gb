from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/v1/menus",
          status_code=201,
          name="Создает меню",
          )
async def create_menu(menu: schemas.MenusCreate, db: Session = Depends(get_db)):
   return crud.create_menu(db=db, menu=menu)
   

@app.get("/api/v1/menus", 
         name="Просматривает список меню"
         )
async def get_menus(db: Session = Depends(get_db)):
   return crud.get_menus(db)

@app.get("/api/v1/menus/{target_menu_id}", 
         name="Просматривает определенное меню"
         )
async def get_menu(target_menu_id: str, db: Session = Depends(get_db)):
   db_menu = crud.get_menu(db, menus_id=target_menu_id)
   if db_menu == None:
      raise HTTPException(status_code=404, detail='menu not found')
   return db_menu

@app.patch("/api/v1/menus/{target_menu_id}", 
           name="Обновляет меню"
           )
async def update_menu(target_menu_id: str, menu: schemas.MenusCreate, db: Session = Depends(get_db)):
   db_menu = crud.update_menu(db, menus_id=target_menu_id, menu=menu)
   if db_menu == None:
      raise HTTPException(status_code=404, detail="menu not found")
   return db_menu

@app.delete("/api/v1/menus/{target_menu_id}", name="Удаляет меню")
async def delete_menu(target_menu_id: str, db: Session = Depends(get_db)):  
   db_menu = crud.delete_menu(db, menus_id=target_menu_id)
   return db_menu


@app.get("/api/v1/menus/{target_menu_id}/submenus", 
         name="Просматривает список подменю"
         )
async def get_list_submenus(target_menu_id: str, db: Session = Depends(get_db)):
   return crud.get_submenus(db=db, menus_id=target_menu_id)

@app.post("/api/v1/menus/{target_menu_id}/submenus", 
          name="Создает подменю",
          status_code=201)
async def create_submenu(target_menu_id: str, submenu: schemas.SubmenusCreate, db: Session = Depends(get_db)):
   return crud.create_submenu(db=db, menus_id=target_menu_id, submenu=submenu)


@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}", 
         name="Просматривает определенное подменю")
async def get_submenu(target_menu_id: str, target_submenu_id: str, db: Session = Depends(get_db)):
   db_submenu = crud.get_submenu(db=db, menus_id=target_menu_id, submenu_id=target_submenu_id)
   if db_submenu == None:
      raise HTTPException(status_code=404, detail='submenu not found')
   return db_submenu

@app.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}", 
           name="Обновляет подменю")
async def update_submenu(target_menu_id: str, target_submenu_id: str, submenu: schemas.SubmenusCreate, db: Session = Depends(get_db)):
   db_submenu = crud.update_submenu(db=db, menus_id=target_menu_id, submenu_id=target_submenu_id, submenu=submenu)
   if db_submenu == None:
      raise HTTPException(status_code=404, detail="submenu not found")
   return db_submenu

@app.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}", name="Удаляет подменю")
async def delete_submenu(target_menu_id: str, target_submenu_id: str, db: Session = Depends(get_db)): 
   crud.delete_submenu(db, menus_id=target_menu_id, submenu_id=target_submenu_id)
   return

@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes", 
         name="Просматривает список блюд"
         )
async def get_list_dishes(target_menu_id: str, target_submenu_id: str, db: Session = Depends(get_db)):
   return crud.get_dishes(db=db, menus_id=target_menu_id, submenu_id=target_submenu_id)

@app.post("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes", 
         name="Создает блюдо",
         status_code=201)
async def create_dishe(target_menu_id: str, target_submenu_id: str, dish: schemas.DishesCreate, db: Session = Depends(get_db)):
   db_dish = crud.create_dish(db=db, menus_id=target_menu_id, submenu_id=target_submenu_id, dish=dish)
   return db_dish


@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}", 
         name="Просматривает определенное блюдо"
         )
async def get_list_dishes(target_menu_id: str, target_submenu_id: str, target_dish_id: str, db: Session = Depends(get_db)):
   db_dish = crud.get_dish(db=db, menus_id=target_menu_id, submenu_id=target_submenu_id, dishes_id=target_dish_id)
   if db_dish == None:
      raise HTTPException(status_code=404, detail="dish not found")
   return crud.get_dish(db=db, menus_id=target_menu_id, submenu_id=target_submenu_id, dishes_id=target_dish_id)


@app.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}", 
         name="Обновляет блюдо"
         )
async def update_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str, dish: schemas.DishesCreate, db: Session = Depends(get_db)):
   db_dish = crud.update_dish(db=db, menus_id=target_menu_id, submenu_id=target_submenu_id, dishes_id=target_dish_id, dish=dish)
   if db_dish == None:
      raise HTTPException(status_code=404, detail="dish not found")
   return db_dish

@app.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
         name="Удаляет блюдо"
         )
async def delete_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str, db: Session = Depends(get_db)): 
   crud.delete_dish(db=db, menus_id=target_menu_id, submenu_id=target_submenu_id, dishes_id=target_dish_id)
   return