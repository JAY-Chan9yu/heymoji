import pymysql
from conf import settings


connection = pymysql.connect(
    host=settings.config.HOST,
    user=settings.config.USERNAME,
    password=settings.config.PASSWORD,
    db=settings.config.DATABASE
)


with connection:
    with connection.cursor() as cursor:
        sql = f"UPDATE users SET my_reaction = {settings.config.DAY_MAX_REACTION}"
        cursor.execute(sql)
