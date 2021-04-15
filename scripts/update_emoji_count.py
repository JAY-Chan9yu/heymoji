import pymysql

HOST = 'host'
DATABASE = 'database'
USER = 'user'
PASSWORD = 'password'

#DB에 접속
connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE)

with connection:
    with connection.cursor() as cursor:
        sql = "UPDATE slack_user SET get_emoji_count = 5"
        cursor.execute(sql)

    connection.commit()
