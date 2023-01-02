import pymysql
from conf import settings


connection = pymysql.connect(
    host=settings.config.DB_HOST,
    user=settings.config.DB_USERNAME,
    password=settings.config.DB_PASSWORD,
    db=settings.config.DATABASE
)


with connection:
    with connection.cursor() as cursor:
        sql = f"UPDATE users SET my_reaction = {settings.config.DAY_MAX_REACTION}"
        cursor.execute(sql)
