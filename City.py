__author__ = 'Tony'

# This class is a data structure used to generalize cities for the Gis class
class City:

    def __init__(self, name, state, latitude, longitude, population):
        self.name = name
        self.state = state
        self.latitude = latitude
        self.longitude = longitude
        self.population = population
        self.cities = {}  # city name to distance dictionary

    def appendDistanceTo(self, name, distance):
        self.cities[name] = distance