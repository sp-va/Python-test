from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
from src.config import settings

# Создание сессии
SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Подключение базы (с автоматической генерацией моделей)
Base = declarative_base()

def get_session():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()
        