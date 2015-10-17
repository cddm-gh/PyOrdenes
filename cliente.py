__author__ = 'developer'
class Cliente(object):
    def __init__(self):
        self.__name = ""
        self.__id = ""

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id

    def set_name(self, name):
        self.__name = name

    def set_id(self, id):
        self.__id = id