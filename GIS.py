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
                name = tokens[i+0]
                state = tokens[i+1]
                lat = tokens[i+2]
                lon = tokens[i+3]
                pop = tokens[i+4]
                i += 5
                if i == 205:
                    print('Stop here!')
                current_city = City(name, state, lat, lon, pop)
                for city in self.cities:
                    city.appendDistanceTo(name, int(tokens[i]))
                    i += 1
                current_city.appendDistanceTo(name, 0)
                self.cities.append(current_city)

            pass
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