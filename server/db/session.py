from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://dailydash:yourpass@localhost/betterment"
SQLALCHEMY_DATABASE_URL = os.get_env('DD_DB_HOST')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
