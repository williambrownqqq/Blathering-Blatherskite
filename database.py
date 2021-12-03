import random
from getpass import getpass
import pymysql
# from mysql.connector import connect
import mysql.connector
from databaseConfig import host, user, password, dataBaseName
from PIL import Image
import sqlite3
import cv2
import io

""" connection to pentagon database """

connectort = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=dataBaseName,
)
MyCursor = connectort.cursor()


# def writing(myUser):
#     print(myUser)
#     try:
#         with connect(
#                 host=host,
#                 user=user,
#                 password=password,
#                 database=dataBaseName,
#         ) as connection:
#             print(connection)
#             nickname = myUser.name
#             id = random.randint(0, 1000000)  # myUser.idd
#             age = myUser.age
#             sex = myUser.sex
#             city = myUser.city
#
#             img = Image.open("1451232188.jpg")
#             # try:
#             #     img = Image.open("1451232188.jpg")
#             #     binimg = convertToBinaryData(img)
#             # except IOError:
#             #     pass
#
#             #image = Image.open('DSC_0144.JPG')
#             im = cv2.imread('1451232188.jpg')
#             im_resize = cv2.resize(im, (500, 500))
#
#             is_success, im_buf_arr = cv2.imencode(".jpg", im_resize)
#             byte_im = im_buf_arr.tobytes()
#             print(type(byte_im))
#             botquery = f"INSERT INTO botuser(ID, UserName, UserAge, UserSex, UserCity) VALUES (%s, %s, %s, %s, %s) "
#             user1 = (id, nickname, age, sex, city)
#
#             imagequery = f"INSERT INTO BotUser (UserPhoto) VALUES (%s)"
#
#             with connection.cursor() as cursor:
#                 cursor.execute(botquery, user1)
#                 cursor.execute(imagequery, (byte_im,))
#             connection.commit()
#             # query = "SHOW TABLES"
#             # with connection.cursor() as cursor:
#             #     cursor.execute(query)
#             #     for db in cursor:
#             #         print(db)
#
#             # create pentagon database
#             # create_db_query = "CREATE DATABASE pentagon"
#             # with connection.cursor() as cursor:
#             #     cursor.execute(create_db_query)
#
#             # create photo
#             # create_db_query = "ALTER TABLE BotUser ADD UserPhoto LONGBLOB NOT NULL"
#             # with connection.cursor() as cursor:
#             #     cursor.execute(create_db_query)
#
#             # show our databases
#             # show_db_query = "SHOW DATABASES"
#             # with connection.cursor() as cursor:
#             #     cursor.execute(show_db_query)
#             #     for db in cursor:
#             #         print(db)
#             RetriveBlob(id)
#         print("Successfully connect!")
#     except Exception as ex:
#         print("Connection refused!")
#         print(ex)

def writing(myUser):
    try:
        # MyCursor = connectort.cursor()
        print(connectort) # our object address

        nickname = myUser.name
        id = myUser.idd # random.randint(0, 1000000)
        #print("hi", id)
        age =myUser.age
        sex = myUser.sex
        city = myUser.city
        description = myUser.describe
        chatUserame = myUser.chatUsername
        path = '1451232188.jpg'



        #botquery = f"INSERT INTO botuser(ID, UserName, UserAge, UserSex, UserCity) VALUES (%s, %s, %s, %s, %s) "
        #user1 = (id, nickname, age, sex, city)
        # imagequery = f"INSERT INTO BotUser(UserPhoto) VALUES (%s)"



        InsertPhoto(path, id, nickname, age, sex, city, description, chatUserame) # send data to database
        TakePhoto(id) #back photo from database

        # #MyCursor.execute(botquery, user1)
        # MyCursor.execute(imagequery, (byte_im,))
        connectort.commit()
        # RetriveBlob(id)
        print("Successfully connect!")
    except Exception as ex:
        print("Connection refused!")
        print(ex)



def InsertPhoto(FilePath, id, nickname, age, sex, city, description, chatUsername):
    try:
        with open(FilePath, 'rb') as File:
            BinaryData = File.read()
        print(type(BinaryData))

        botquery = f"INSERT INTO botuser(ID, UserName, UserAge, UserSex, UserCity, UserPhoto, UserDescription, UserChatUsername) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
        data = (id, nickname, age, sex, city, BinaryData, description, chatUsername)
        MyCursor.execute(botquery, data)

        # sqlQuery = f"INSERT INTO BotUser(UserPhoto) VALUES (%s) "
        # MyCursor.execute(sqlQuery, (BinaryData, ))
        connectort.commit()
    except Exception as error:
        print("Failed to put a photo from table", error)

def TakePhoto(id):
    try:
        print("bye", id)
        sqlQuery = "SELECT * FROM BotUser WHERE id = '{0}'"
        MyCursor.execute(sqlQuery.format(str(id)))
        MyResult = MyCursor.fetchone()[4]
        print(type(MyResult))
        store = "ImageOutputs/img{0}.jpg".format(str(id))
        #print(MyResult)
        with open(store, "wb") as file:
            print(type(MyResult))
            file.write(MyResult) # works with bytes
            file.close()
    except Exception as error:
        print("Failed to grab the photo from table", error)


# def RetriveBlob(id):
#     # sqlquery = "SELECT * FROM BotUser"
#     # print("suc")
#     # with connection.cursor() as cursor:
#     #     cursor.execute(sqlquery)
#     #     Myres = connection.cursor.fetchall()
#     #     store = "ImageFoulder/ing{0}.jpg".format(str(id))
#     #     print(Myres)
#     # connection.commit()
#     # with open(store, "wb") as file:
#     #     file.write()
#     #     file.close()
#     try:
#         # connection = sqlite3.connect('pentagon.db')
#         # cursor = connection.cursor()
#         # print("Connected to SQLite")
#         print("hello query")
#         # sqlquery = "SELECT UserPhoto FROM BotUser WHERE id = '{0}'" - work
#         sqlquery = "SELECT * FROM BotUser WHERE id = '{0}'"
#         MyCursor.execute(sqlquery.format(str(id)))
#
#         records = MyCursor.fetchone()[5]
#         print("hello query")
#         store = "ImageOutputs/img{0}.jpg".format(str(id))
#         print(records)
#         with open(store, "wb") as file:
#             file.write(records)
#             file.close()
#
#         with open(store, "rb") as file:
#             file.read(records)
#             file.close()
#
#         # MyCursor.close()
#     except Exception as error:
#         print("Failed to read data from table", error)


#writing(user)
