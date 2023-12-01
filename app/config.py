from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TG_API_TOKEN: str

    @property
    def DATABASE_URL(self):
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.DB_USER,
            self.DB_PASS,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()
