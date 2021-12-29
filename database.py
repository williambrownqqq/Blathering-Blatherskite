import mysql.connector
from databaseConfig import host, user, password, dataBaseName

""" 
connection to pentagon database 
"""

connector = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=dataBaseName,
)
cursor = connector.cursor()


def check_user(username):
    """
    Function to check user existence in database
    """
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
    """
    function to find random user to sex
    """
    query = f'SELECT * FROM botuser WHERE UserSex = "{sex}" and id != {chat_id}' \
               f' and Active = 1 order by rand() LIMIT 1;'
    cursor.execute(query)
    return cursor.fetchone()


def set_active(state, chat_id):
    """
    set user status to active
    """
    query = f"UPDATE botuser SET Active = %s WHERE ID = %s "
    data = (state, chat_id)
    cursor.execute(query, data)
    connector.commit()


def save_all(telegram_user):
    """
    put user data to database after registration or editing profile
    """
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
