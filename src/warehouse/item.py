class Item:
    def __init__(self, name, description, price, num_of_available_items, id=None):
        if "" in (name, price, num_of_available_items):
            raise ValueError("Data is null")
        self.__name = name
        self.__description = description
        self.__price = float(price)
        self.__num_of_available_items = int(num_of_available_items)
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if name == "":
            raise ValueError("Name is null")
        self.__name = name

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if price == "":
            raise ValueError("Price is null")
        self.__price = round(float(price), 2)

    def get_num_of_available_items(self):
        return self.__num_of_available_items

    def set_num_of_available_items(self, num):
        if num == "":
            raise ValueError("Available amount is null")
        num = int(num)
        if num < 0:
            raise ValueError("Available amount can't be less then zero")
        self.__num_of_available_items = int(num)

    def get_id(self):
        return self.__id
