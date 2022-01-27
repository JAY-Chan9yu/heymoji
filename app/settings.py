from dataclasses import dataclass
from conf import config


##################################################################
#                   Database Setting
##################################################################
@dataclass
class DataBaseSettings:
    HOST = config.settings.HOST
    PORT = config.settings.PORT
    DATABASE = config.settings.DATABASE
    USERNAME = config.settings.USERNAME
    PASSWORD = config.settings.PASSWORD


##################################################################
#                       Reaction Setting
##################################################################
DAY_MAX_REACTION = config.settings.DAY_MAX_REACTION  # 하루 최대 사용할 수 있는 reaction 개수
REACTION_LIST = config.settings.REACTION_LIST  # 리액션 허용 이모지 type(name)
SLACK_TOKEN = config.settings.SLACK_TOKEN
SLACK_CHANNEL = config.settings.SLACK_CHANNEL
