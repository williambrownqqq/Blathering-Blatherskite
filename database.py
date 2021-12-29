
import mysql.connector
from databaseConfig import host, user, password, dataBaseName

""" connection to pentagon database """

connector = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=dataBaseName,
)
cursor = connector.cursor()


def check_user(username):
    try:
        query = f"SELECT UserName FROM botuser WHERE UserChatUsername = %s"
        cursor.execute(query, (username,))

        rows = cursor.fetchall()
        if rows:
            return True
        else:
            return False
    except Exception as ex:
        print("Connection refused!")
        print(ex)


def find_user(sex, chat_id):
    query = f'SELECT * FROM botuser WHERE UserSex = "{sex}" and id != {chat_id}' \
               f' and Active = 1 order by rand() LIMIT 1;'
    cursor.execute(query)
    return cursor.fetchone()


def set_active(state, chat_id):
    query = f"UPDATE botuser SET Active = %s WHERE ID = %s "
    data = (state, chat_id)
    cursor.execute(query, data)
    connector.commit()


def save_all(telegram_user):
    try:
        nickname = telegram_user.name
        id = telegram_user.idd
        age = telegram_user.age
        sex = telegram_user.sex
        university = telegram_user.university
        description = telegram_user.description
        chat_username = telegram_user.username
        path = 'DownloadedPhotos/' + telegram_user.photo
        with open(path, 'rb') as file:
            binary_data = file.read()
        if check_user(chat_username):
            query = f"UPDATE botuser SET UserName = %s, UserAge = %s, UserSex =  %s, UserCity =  %s, UserPhoto = %s, UserDescription = %s WHERE ID = %s "
            data = (nickname, age, sex, university, binary_data, description, id)
        else:
            query = f"INSERT INTO botuser(ID, UserName, UserAge, UserSex, UserCity, UserPhoto, UserDescription, UserChatUsername) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
            data = (id, nickname, age, sex, university, binary_data, description, chat_username)
        cursor.execute(query, data)

        connector.commit()
        print("Successfully connect!")
    except Exception as ex:
        print("Connection refused!")
        print(ex)


def take_photo(id):
    try:
        print("bye", id)
        query = "SELECT * FROM botuser WHERE id = '{0}'"
        cursor.execute(query.format(str(id)))
        result = cursor.fetchone()[4]
        print(type(result))
        store = "ImageOutputs/img{0}.jpg".format(str(id))
        # print(result)
        with open(store, "wb") as file:
            print(type(result))
            file.write(result)  # works with bytes
            file.close()
    except Exception as error:
        print("Failed to grab the photo from table", error)
