from sqlalchemy.orm import sessionmaker

from menu_restaurant.database.engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
