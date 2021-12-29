""" user profile """


class User:
    """
    User class
    attributes:
    idd: id of telegram acc
    photo_id: id of the photo
    age: but this is age
    name: name of new user
    sex: arrr, all good only male or female
    username: telegram username of new user
    university: place of study, KPI forever
    description: description of new acc in bot
    """
    def __init__(self, idd):
        self.idd = idd

    @property
    def photo_id(self):
        return self.__photo_id

    @photo_id.setter
    def photo_id(self, photo_id):
        if not isinstance(photo_id, str):
            raise TypeError("Must be str!")
        if photo_id is None:
            raise ValueError("Mustn't be empty!")
        self.__photo_id = photo_id

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if not isinstance(age, int):
            raise TypeError("Must be int!")
        if not 14 < age < 100:
            raise ValueError("Must be higher than 14 and lower than 100")
        self.__age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name:
            if not isinstance(name, str):
                raise TypeError("Must be string")
            elif not name.isalpha():
                raise ValueError("Must be letters")
        self.__name = name

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, sex):
        if not isinstance(sex, str):
            raise TypeError("Sex must be str!")
        self.__sex = sex

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        if not isinstance(username, str):
            raise TypeError("username must be str!")
        self.__username = username

    @property
    def university(self):
        return self.__city

    @university.setter
    def university(self, university):
        if not isinstance(university, str):
            raise TypeError("university must be str!")
        elif not 0 < len(university) < 255:
            raise ValueError("university must be between 0 and 255 symbols long")
        self.__city = university

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError("Description must be str!")
        self.__description = description

    @property
    def photo(self):
        return self.__photo

    @photo.setter
    def photo(self, path):
        if not isinstance(path, str):
            raise TypeError("Must be string")
        self.__photo = path

    def __str__(self):
        return f"ID:    {self.idd}\n" \
               f"name:  {self.name}\n" \
               f"age:   {self.age}\n" \
               f"sex:   {self.sex}\n" \
               f"university   {self.university}\n" \
               f"description: {self.description}\n"
