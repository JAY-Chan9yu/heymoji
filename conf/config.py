import os

from pydantic import BaseSettings


# 로컬에 동일한 이름의 환경변수가 적용되어있으면, 그걸로 덮어지게됨 (printenv 로 확인 필요)
class Settings(BaseSettings):
    HOST: str
    PORT: int
    DATABASE: str
    USERNAME: str
    PASSWORD: str

    class Config:
        env_file = os.path.expanduser('~/.env')
        env_file_encoding = 'utf-8'
