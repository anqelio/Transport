from sqlmodel import SQLModel
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    '''
    Инициализация БД при запуске приложения
    '''
    SQLModel.metadata.create_all(engine)

def get_engine():
    '''
    Получение engine для миграций
    :return: engine
    '''
    return engine

def close_db():
    '''
    Освобождение ресурсов
    '''
    engine.dispose()