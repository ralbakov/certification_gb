from fastapi import FastAPI

from menu_restaurant.api.dish.api import dish_router
from menu_restaurant.api.menu.api import menu_router
from menu_restaurant.api.submenu.api import submenu_router
from menu_restaurant.database import models
from menu_restaurant.database.session import engine

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


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
