from sqlalchemy import create_engine

from menu_restaurant.database.confdb import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
