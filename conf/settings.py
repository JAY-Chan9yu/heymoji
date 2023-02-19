from enum import Enum
from typing import Optional

from pydantic import BaseSettings, Field


class HeymojiEnv(Enum):
    PROD = 'prod'
    STAGE = 'stage'
    DEV = 'dev'
    TEST = 'test'


class BaseConfig(BaseSettings):
    ENV: str = Field(env="ENV", default=HeymojiEnv.DEV.value)
    ALLOW_ORIGINS: list = Field(env="ALLOW_ORIGINS", default=['*'])

    DB_HOST: str = Field(env="DB_HOST", default="127.0.0.1")
    DB_PORT: int = Field(env="DB_PORT", default="3306")
    DB_USERNAME: str = Field(env="DB_USERNAME", default="root")
    DB_PASSWORD: str = Field(env="DB_PASSWORD", default="root")
    DATABASE: str = Field(env="DATABASE", default="heymoji")

    SPECIAL_EMOJI: Optional[str] = Field(env="SPECIAL_EMOJI", default="trophy")
    LIMIT_GIVE_COUNT_OF_SPECIAL_EMOJI: int = Field(env="LIMIT_GIVE_COUNT_OF_SPECIAL_EMOJI", default=5)
    ALLOWED_REACTION_LIST: list = Field(env="ALLOWED_REACTION_LIST", default=['heart'])
    SLACK_TOKEN: str = Field(env="SLACK_TOKEN")
    ERROR_CHANNEL: str = Field(env="ERROR_CHANNEL")
    BOT_NAME: str = Field(env="BOT_NAME")
    ALLOWED_EMOJI_TYPES: list = Field(env="ALLOWED_EMOJI_TYPES", default=[])

    RANK_URL: str = Field(env="RANK_URL", default="")
    DEFAULT_AVATAR_URL: str = Field(
        env="DEFAULT_AVATAR_URL",
        default="https://github.com/JAY-Chan9yu/heymoji/blob/master/frontend/src/assets/logos/heymoji.png?raw=true"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


config = BaseConfig(_env_file=f'./.env')
