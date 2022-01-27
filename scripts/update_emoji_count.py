import pymysql

from conf import settings


# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

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

    connection.commit()
