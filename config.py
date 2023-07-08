import pydantic_settings as ps

class Settings(ps.BaseSettings):
  SECRET_KEY:str
  DATABASE_NAME:str
  DATABASE_USER:str
  DATABASE_PASSWORD:str
  DATABASE_HOST:str
  DATABASE_PORT:int
  DATABASE_DRIVER:str
  SUB_DRIVER:str

  class Config:
    env_file = '.env'


settings = Settings()