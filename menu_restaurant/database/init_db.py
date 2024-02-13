from menu_restaurant.database import models
from menu_restaurant.database.confdb import engine


def init_db():
    models.Base.metadata.create_all(bind=engine)
