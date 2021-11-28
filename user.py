""" user profile """
class User:
    counter = 0
    def __init__(self, idd, name):
        self.idd = idd
        self.name = name
        self.age = None
        self.sex = None
        User.counter +=1
    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, age):
        print(type(age))
        # int(age)
        # if not isinstance(age, int):
        #     raise TypeError("Must be int!")
        # if not 14<age<100:
        #     raise ValueError("Must be higher than 14 and lower than 100")
        print(type(age))
        self.__age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Must be str")
        self.__name = name

    def __str__(self):
        return f"\tUser №{User.counter}\n" \
               f"ID:    {self.idd}\n" \
               f"name:  {self.name}\n" \
               f"age:   {self.age}\n" \
               f"sex:   {self.sex}\n"