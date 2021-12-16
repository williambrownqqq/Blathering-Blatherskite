""" user profile """


class User:
    counter = 0

    def __init__(self, idd):
        self.idd = idd
        User.counter += 1

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if not isinstance(age, int):
             raise TypeError("Must be int!")
        if not 14<age<100:
             raise ValueError("Must be higher than 14 and lower than 100")
        self.__age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Must be string")
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
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        if not isinstance(city, str):
            raise TypeError("City must be str!")
        self.__city = city

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
    def photo(self, name):
        if not isinstance(name, str):
            raise TypeError("Must be string")
        self.__photo = name

    def __str__(self):
        return f"\tUser №{User.counter}\n" \
               f"ID:    {self.idd}\n" \
               f"name:  {self.name}\n" \
               f"age:   {self.age}\n" \
               f"sex:   {self.sex}\n" \
               f"city   {self.city}\n" \
               f"description: {self.description}\n"
