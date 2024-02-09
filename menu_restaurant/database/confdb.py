import os

from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.util import deprecations

load_dotenv('.env.work')

deprecations.SILENCE_UBER_WARNING = True

SQLALCHEMY_DATABASE_URL = os.environ['DB_URL']

Base = declarative_base()
