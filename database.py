from getpass import getpass
import pymysql
from mysql.connector import connect, Error
from databaseConfig import host, user, password, dataBaseName


def writing(myUser):
    print(myUser)
    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=dataBaseName,
        ) as connection:
            print(connection)
            nickname = myUser.name
            id = 7 #myUser.idd
            age = myUser.age
            sex = myUser.sex
            botquery = f"INSERT INTO botuser(ID, UserName, UserAge, UserSex) VALUES (%s, %s, %s, %s) "
            user1 = (id, nickname, age, sex)
            with connection.cursor() as cursor:
                cursor.execute(botquery, user1)
            connection.commit()
            # query = "SHOW TABLES"
            # with connection.cursor() as cursor:
            #     cursor.execute(query)
            #     for db in cursor:
            #         print(db)

            # create pentagon database
            # create_db_query = "CREATE DATABASE pentagon"
            # with connection.cursor() as cursor:
            #     cursor.execute(create_db_query)

            # show our databases
            # show_db_query = "SHOW DATABASES"
            # with connection.cursor() as cursor:
            #     cursor.execute(show_db_query)
            #     for db in cursor:
            #         print(db)
        print("Successfully connect!")
    except Exception as ex:
        print("Connection refused!")
        print(ex)
