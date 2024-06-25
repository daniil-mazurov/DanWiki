import os
from typing import Annotated

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import mapped_column

from .path import PATH

intpk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, 256]


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        """URL для подключения к базе (asyncpg)

        Returns:
            str: postgresql+asyncpg://username:password@localhost:port/base
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        """URL для подключения к базе (psycopg)

        Returns:
            str: postgresql+psycopg://username:password@localhost:port/base
        """
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(PATH), ".env")
    )


settings = Settings()
