__author__ = 'Tony'


# This class is a data structure used to generalize cities for the Gis class
class City:

    def __init__(self, name, latitude, longitude, population):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.population = population
        self.cities = {}

    def appendDistanceTo(self, name, distance):
        self.cities[name] = distance