
import mysql.connector
from databaseConfig import host, user, password, dataBaseName

""" connection to pentagon database """

Myconnector = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=dataBaseName,
)
MyCursor = Myconnector.cursor()

def checkuser(username):
    try:
        query = f"SELECT UserName FROM botuser WHERE UserChatUsername = %s"
        MyCursor.execute(query, (username,))

        rows = MyCursor.fetchall()
        if rows:
            return True
        else:
            return False
    except Exception as ex:
        print("Connection refused!")
        print(ex)



def writing(myUser):
    try:
        nickname = myUser.name
        id = myUser.idd
        age = myUser.age
        sex = myUser.sex
        university = myUser.university
        description = myUser.description
        chatusername = myUser.username
        path = 'DownloadedPhotos/' + myUser.photo
        with open(path, 'rb') as File:
            BinaryData = File.read()
        if checkuser(chatusername):
            botquery = f"UPDATE botuser SET UserName = %s, UserAge = %s, UserSex =  %s, UserCity =  %s, UserPhoto = %s, UserDescription = %s WHERE ID = %s "
            data = (nickname, age, sex, university, BinaryData, description, id)
        else:
            botquery = f"INSERT INTO botuser(ID, UserName, UserAge, UserSex, UserCity, UserPhoto, UserDescription, UserChatUsername) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
            data = (id, nickname, age, sex, university, BinaryData, description, chatusername)
        MyCursor.execute(botquery, data)

        Myconnector.commit()
        print("Successfully connect!")
    except Exception as ex:
        print("Connection refused!")
        print(ex)

def TakePhoto(id):
    try:
        print("bye", id)
        sqlQuery = "SELECT * FROM botuser WHERE id = '{0}'"
        MyCursor.execute(sqlQuery.format(str(id)))
        MyResult = MyCursor.fetchone()[4]
        print(type(MyResult))
        store = "ImageOutputs/img{0}.jpg".format(str(id))
        # print(MyResult)
        with open(store, "wb") as file:
            print(type(MyResult))
            file.write(MyResult)  # works with bytes
            file.close()
    except Exception as error:
        print("Failed to grab the photo from table", error)



