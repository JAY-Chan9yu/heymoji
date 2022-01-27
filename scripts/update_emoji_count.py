import pymysql

from conf import config

connection = pymysql.connect(
    host=config.settings.HOST,
    user=config.settings.USERNAME,
    password=config.settings.PASSWORD,
    db=config.settings.DATABASE
)


with connection:
    with connection.cursor() as cursor:
        sql = f"UPDATE users SET my_reaction = {config.settings.DAY_MAX_REACTION}"
        cursor.execute(sql)

    connection.commit()
