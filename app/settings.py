from functools import lru_cache
from typing import Dict, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = Field(..., env='DB_HOST')
    DB_PORT: str = Field(..., env='DB_PORT')
    DB_DRIVER: str = Field(..., env='DB_DRIVER')
    DB_NAME: str = Field(..., env='DB_NAME')
    DB_USER: str = Field(..., env='DB_USER')
    DB_PASSWORD: str = Field(..., env='DB_PASSWORD')

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True, always=True)
    def build_sqlalchemy_url(cls, v: object, values: Dict[str, object]) -> str:  # pylint: disable=no-self-argument
        return (
            f'{values["DB_DRIVER"]}://{values["DB_USER"]}:{values["DB_PASSWORD"]}'
            f'@{values["DB_HOST"]}:{values["DB_PORT"]}/{values["DB_NAME"]}'
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
