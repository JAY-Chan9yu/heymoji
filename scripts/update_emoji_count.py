import os
import sys
import pymysql

# 모듈 경로를 못찾는 경우가 있어서 sys.path 에 경로 추가 (IDE를 사용하면 잘 찾음)
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(script_dir) not in sys.path:
    sys.path.insert(0, os.path.dirname(script_dir))

from app.settings import DataBaseSettings as Settings, DAY_MAX_REACTION

settings = Settings()
connection = pymysql.connect(host=settings.HOST, user=settings.USERNAME, password=settings.PASSWORD, db=settings.DATABASE)


with connection:
    with connection.cursor() as cursor:
        sql = f"UPDATE users SET my_reaction = {DAY_MAX_REACTION}"
        cursor.execute(sql)

    connection.commit()
