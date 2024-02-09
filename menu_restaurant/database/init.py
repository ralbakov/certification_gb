from menu_restaurant.database import models
from menu_restaurant.database.engine import engine


def init_db():
    models.Base.metadata.create_all(bind=engine)
