import pymysql

# TODO: 모듈을 제대로 불러오지 못하는 경우가 생김. root 디렉토리나, 모듈을 찾을 수 있게 해줘야 할 것 같은데.. 흠..
# from conf.config import Settings
# settings = Settings(_env_file='prod.env')
# connection = pymysql.connect(host=settings.HOST, user=settings.USERNAME,
#                              password=settings.PASSWORD, db=settings.DATABASE)

HOST = 'HOST'
DATABASE = 'DATABASE'
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'

connection = pymysql.connect(host=HOST, user=USERNAME, password=PASSWORD, db=DATABASE)


with connection:
    with connection.cursor() as cursor:
        sql = "UPDATE users SET my_reaction = 5"
        cursor.execute(sql)

    connection.commit()
