from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv

env_dict = dotenv.dotenv_values('.env')

# Создание сессии
SQLALCHEMY_DATABASE_URI = f'postgresql://{env_dict["DATABASE_USER"]}:{env_dict["DATABASE_PASSWORD"]}@{env_dict["DATABASE_HOST"]}:{env_dict["DATABASE_PORT"]}/{env_dict["DATABASE_NAME"]}'
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
        