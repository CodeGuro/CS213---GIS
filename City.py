__author__ = 'Tony'


# This class is a data structure used to generalize cities for the Gis class
class City:

    def __init__(self, name, state, latitude, longitude, population):
        self.name = name
        self.state = state
        self.latitude = latitude
        self.longitude = longitude
        self.population = population

    def fullPrint(self):
        print(self.getFullStr())

    def shortPrint(self):
        print(self.name)

    def getFullStr(self):
        return self.name + ' [' + str(self.latitude) + ',' + str(self.longitude) + '], ' + str(self.population)