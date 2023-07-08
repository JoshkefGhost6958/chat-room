from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,session
from config import settings

SQLALCHEMY_URL = f"{settings.DATABASE_DRIVER}://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
engine = create_engine(SQLALCHEMY_URL)

SESSION_LOCAL = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
  try:
    db = SESSION_LOCAL()
    yield db
  finally:
    db.close()

