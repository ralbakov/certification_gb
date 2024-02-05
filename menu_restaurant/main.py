from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from menu_restaurant.database import SessionLocal, engine
from menu_restaurant.redis_cache.tools import RedisCache

from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title='Restaurante API',
              description=('Приложение для работы с меню ресторана, '
                           'включая работу с подменю и блюдами'),
              version='3.0',
              openapi_tags=[
                  {
                      'name': 'Menu',
                      'description': 'Работа с меню',
                  },
                  {
                      'name': 'Submenu',
                      'description': 'Работа с подменю',
                  },
                  {
                      'name': 'Dish',
                      'description': 'Работа с блюдами',
                  },
              ],
              )


menu_router = APIRouter(prefix='/api/v1/menus')

submenu_router = APIRouter(prefix=('/api/v1/menus'
                                   '/{target_menu_id}/submenus'))

dish_router = APIRouter(prefix=('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@menu_router.post('',
                  status_code=201,
                  name='Создает меню',
                  response_model=schemas.Menus,
                  tags=['Menu']
                  )
async def create_menu(menu: schemas.MenusCreate,
                      db: Session = Depends(get_db)):
    menu = crud.create_menu(db=db, menu=menu)
    RedisCache.set_menu(id=str(menu.id), menu=menu)
    return menu


@menu_router.get('',
                 name='Просматривает список меню',
                 response_model=list[schemas.Menus],
                 tags=['Menu']
                 )
async def get_menus(db: Session = Depends(get_db)):
    get_all_menu_cache = RedisCache.get_all_menu()
    if get_all_menu_cache is not None or get_all_menu_cache == []:
        return get_all_menu_cache

    db_all_menu = crud.get_menus(db)
    return db_all_menu


@menu_router.get('/{target_menu_id}',
                 name='Просматривает определенное меню',
                 response_model=schemas.Menus,
                 tags=['Menu']
                 )
async def get_menu(target_menu_id: str,
                   db: Session = Depends(get_db)):
    if target_menu_id not in RedisCache.get_all_keys_menu():
        db_menu = crud.get_menu(db, menus_id=target_menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail='menu not found')
        RedisCache.set_menu(id=target_menu_id, menu=db_menu)
        return db_menu

    get_menu_cache = RedisCache.get_menu(id=target_menu_id)
    return get_menu_cache


@app.patch('/api/v1/menus/{target_menu_id}',
           name='Обновляет меню',
           response_model=schemas.Menus,
           tags=['Menu']
           )
async def update_menu(target_menu_id: str,
                      menu: schemas.MenusUpdate,
                      db: Session = Depends(get_db)):
    db_menu = crud.update_menu(db, menus_id=target_menu_id, menu=menu)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')

    RedisCache.update_menu(id=target_menu_id, menu=db_menu)
    return db_menu


@menu_router.delete('/{target_menu_id}', name='Удаляет меню', tags=['Menu'])
async def delete_menu(target_menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.delete_menu(db, menus_id=target_menu_id)
    RedisCache.delete_menu(id=target_menu_id)
    return db_menu


@submenu_router.get('',
                    name='Просматривает список подменю',
                    response_model=list[schemas.Submenus],
                    tags=['Submenu']
                    )
async def get_list_submenus(target_menu_id: str,
                            db: Session = Depends(get_db)):
    get_all_submenu_cache = RedisCache.get_all_submenu(target_menu_id=target_menu_id)
    if get_all_submenu_cache is not None or get_all_submenu_cache == []:
        return get_all_submenu_cache

    db_all_submenu = crud.get_submenus(db=db, menus_id=target_menu_id)
    return db_all_submenu


@submenu_router.post('',
                     name='Создает подменю',
                     status_code=201,
                     response_model=schemas.Submenus,
                     tags=['Submenu'])
async def create_submenu(target_menu_id: str,
                         submenu: schemas.SubmenusCreate,
                         db: Session = Depends(get_db)):
    submenu = crud.create_submenu(db=db, menus_id=target_menu_id, submenu=submenu)
    RedisCache.set_submenu(target_menu_id=target_menu_id,
                           id=str(submenu.id),
                           submenu=submenu
                           )

    return submenu


@submenu_router.get('/{target_submenu_id}',
                    name='Просматривает определенное подменю',
                    response_model=schemas.Submenus,
                    tags=['Submenu'])
async def get_submenu(target_menu_id: str,
                      target_submenu_id: str,
                      db: Session = Depends(get_db)):
    if target_submenu_id not in RedisCache.get_all_keys_submenu(target_menu_id=target_menu_id):
        db_submenu = crud.get_submenu(db=db,
                                      menus_id=target_menu_id,
                                      submenu_id=target_submenu_id
                                      )
        if db_submenu is None:
            raise HTTPException(status_code=404, detail='submenu not found')
        RedisCache.set_submenu(target_menu_id=target_menu_id,
                               id=target_submenu_id,
                               submenu=db_submenu
                               )
        return db_submenu

    get_submenu_cache = RedisCache.get_submenu(target_menu_id=target_menu_id,
                                               id=target_submenu_id
                                               )
    return get_submenu_cache


@submenu_router.patch('/{target_submenu_id}',
                      name='Обновляет подменю',
                      response_model=schemas.Submenus,
                      tags=['Submenu'])
async def update_submenu(target_menu_id: str,
                         target_submenu_id: str,
                         submenu: schemas.SubmenusUpdate,
                         db: Session = Depends(get_db)):
    db_submenu = crud.update_submenu(db=db,
                                     menus_id=target_menu_id,
                                     submenu_id=target_submenu_id,
                                     submenu=submenu
                                     )
    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    RedisCache.update_submenu(target_menu_id=target_menu_id,
                              id=target_submenu_id,
                              submenu=db_submenu
                              )
    return db_submenu


@submenu_router.delete('/{target_submenu_id}',
                       name='Удаляет подменю', tags=['Submenu'])
async def delete_submenu(target_menu_id: str,
                         target_submenu_id: str,
                         db: Session = Depends(get_db)):
    db_submenu = crud.delete_submenu(db,
                                     menus_id=target_menu_id,
                                     submenu_id=target_submenu_id)
    RedisCache.delete_submenu(target_menu_id=target_menu_id,
                              id=target_submenu_id
                              )
    return db_submenu


@dish_router.get('',
                 name='Просматривает список блюд',
                 response_model=list[schemas.Dishes],
                 tags=['Dish']
                 )
async def get_list_dishes(target_menu_id: str,
                          target_submenu_id: str,
                          db: Session = Depends(get_db)):
    get_all_dish_cache = RedisCache.get_all_dish(target_submenu_id=target_submenu_id)
    if get_all_dish_cache is not None or get_all_dish_cache == []:
        return get_all_dish_cache
    db_all_dish = crud.get_dishes(db=db,
                                  menus_id=target_menu_id,
                                  submenu_id=target_submenu_id
                                  )
    return db_all_dish


@dish_router.post('',
                  name='Создает блюдо',
                  status_code=201,
                  response_model=schemas.Dishes,
                  tags=['Dish'])
async def create_dishe(target_menu_id: str,
                       target_submenu_id: str,
                       dish: schemas.DishesCreate,
                       db: Session = Depends(get_db)):
    dish = crud.create_dish(db=db,
                            menus_id=target_menu_id,
                            submenu_id=target_submenu_id,
                            dish=dish
                            )
    RedisCache.set_dish(target_menu_id=target_menu_id,
                        target_submenu_id=target_submenu_id,
                        id=str(dish.id),
                        dish=dish
                        )
    return dish


@dish_router.get('/{target_dish_id}',
                 name='Просматривает определенное блюдо',
                 response_model=schemas.Dishes,
                 tags=['Dish']
                 )
async def get_dish(target_menu_id: str,
                   target_submenu_id: str,
                   target_dish_id: str,
                   db: Session = Depends(get_db)):
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


@dish_router.patch('/{target_dish_id}',
                   name='Обновляет блюдо',
                   response_model=schemas.Dishes,
                   tags=['Dish']
                   )
async def update_dish(target_menu_id: str,
                      target_submenu_id: str,
                      target_dish_id: str,
                      dish: schemas.DishesUpdate,
                      db: Session = Depends(get_db)):
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


@dish_router.delete('/{target_dish_id}',
                    name='Удаляет блюдо',
                    tags=['Dish']
                    )
async def delete_dish(target_menu_id: str,
                      target_submenu_id: str,
                      target_dish_id: str,
                      db: Session = Depends(get_db)):
    db_dish = crud.delete_dish(db=db,
                               menus_id=target_menu_id,
                               submenu_id=target_submenu_id,
                               dishes_id=target_dish_id
                               )
    RedisCache.delete_dish(target_menu_id=target_menu_id,
                           target_submenu_id=target_submenu_id,
                           id=target_dish_id)
    return db_dish

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
