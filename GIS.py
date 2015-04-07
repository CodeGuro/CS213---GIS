__author__ = 'Tony'

from City import City
import re


class Gis:

    def __init__(self):
        self.cities = []  # This is the list of all the available cities
        with open('gis.dat', 'r') as gisfile:
            gisfile.seek(110)
            tokens = re.split(", |[\s+\[\],]", gisfile.read())
            i = 0  # iterator
            while i < len(tokens):
                delim = ""
                name = ""
                while not tokens[i+1].isnumeric():
                    name += delim + tokens[i+0]
                    delim = " "
                    i += 1
                state = tokens[i+0]
                lat = tokens[i+1]
                lon = tokens[i+2]
                pop = tokens[i+3]
                i += 4
                current_city = City(name, state, lat, lon, pop)
                for city in self.cities:
                    distance = int(tokens[i])
                    current_city.appendDistanceTo(city.name, distance)
                    city.appendDistanceTo(name, distance)
                    i += 1
                current_city.appendDistanceTo(name, 0)
                self.cities.append(current_city)
        print('success!')

    def selectCities(self, attribute, lowerBound, upperBound):
        pass

    def selectAllCities(self):
        pass

    def selectEdges(self, lowerBound, upperBound):
        pass

    def selectAllEdges(self):
        pass

    def makeGraph(self):
        pass

    def printCities(self, attribute, choice):
        pass

    def printEdges(self):
        pass

    def testMinMaxConsDistance(self):
        pass

    def tour(self, start):
        pass

    def minCut(self):
        pass

x = Gis()
print("success!")