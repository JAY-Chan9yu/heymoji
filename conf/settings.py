from enum import Enum

from pydantic import BaseSettings, Field


class EmojiRankEnv(Enum):
    PROD = 'prod'
    STAGE = 'stage'
    DEV = 'dev'


class BaseConfig(BaseSettings):
    ENV: str = Field(env="ENV", default=EmojiRankEnv.DEV.value)

    HOST: str = Field(env="HOST", default="127.0.0.1")
    PORT: int = Field(env="PORT", default="3306")
    DATABASE: str = Field(env="DATABASE", default="emojirank_db")
    USERNAME: str = Field(env="USERNAME")
    PASSWORD: str = Field(env="PASSWORD")

    DAY_MAX_REACTION: int = Field(env="DAY_MAX_REACTION", default=1000)
    REACTION_LIST: list = Field(env="REACTION_LIST", default=['heart'])
    SLACK_TOKEN: str = Field(env="SLACK_TOKEN")
    ERROR_CHANNEL: str = Field(env="ERROR_CHANNEL")
    BOT_NAME: str = Field(env="BOT_NAME")
    ALLOWED_EMOJI_TYPES: list = Field(env="ALLOWED_EMOJI_TYPES", default=[])

    RANK_URL: str = Field(env="RANK_URL", default="")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


config = BaseConfig(_env_file=f'./.env')
