import os
from os.path import dirname

from dotenv import load_dotenv

env_path = os.path.join(dirname(dirname(os.path.abspath(__file__))), '.env')

load_dotenv(dotenv_path=env_path)


class Setting:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")
        self.DB_NAME = os.getenv("DB_NAME")

        self.TG_API_TOKEN = os.getenv("TG_API_TOKEN")

    @property
    def DATABASE_URL(self):
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.DB_USER,
            self.DB_PASS,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )


settings = Setting()
