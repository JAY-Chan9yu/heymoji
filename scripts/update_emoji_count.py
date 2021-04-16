import pymysql

from conf.config import Settings

settings = Settings(_env_file='prod.env')
connection = pymysql.connect(host=settings.HOST, user=settings.USERNAME,
                             password=settings.PASSWORD, db=settings.DATABASE)

with connection:
    with connection.cursor() as cursor:
        sql = "UPDATE slack_user SET my_reaction = 5"
        cursor.execute(sql)

    connection.commit()
