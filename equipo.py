__author__ = 'gorydev'


class Equipo(object):
    def __init__(self):
        self.__fecha = ""
        self.__marca = ""
        self.__modelo = ""
        self.__imei = ""
        self.__falla = ""
        self.__status = ""
#   Getters--------------------

    def getfecha(self):
        return self.__fecha

    def getmarca(self):
        return self.__marca

    def getmodelo(self):
        return self.__modelo

    def getimei(self):
        return self.__imei

    def getfalla(self):
        return self.__falla

    def getstatus(self):
        return self.__status


#   Setters-------------------

    def setfecha(self,fecha):
        self.__fecha = fecha

    def setmarca(self,marca):
        self.__marca = marca

    def setmodelo(self,modelo):
        self.__modelo = modelo

    def setimei(self,imei):
        self.__imei = imei

    def setfalla(self,falla):
        self.__falla = falla

    def setstatus(self,status):
        self.__status = status







