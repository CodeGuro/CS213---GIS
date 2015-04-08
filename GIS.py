__author__ = 'Tony'

from City import City
import re


class Gis:

    def __init__(self):
        self.cities = []  # This is the list of all the available cities
        self.city_selections = set()
        self.edge_selections = set()
        with open('gis.dat', 'r') as gisfile:
            tokens = re.findall('[A-Za-z\- ]+, [A-Za-z\- ]*|[0-9]+', gisfile.read())
            i = 0  # iterator
            while i < len(tokens):
                name = tokens[i+0]
                lat = int(tokens[i+1])
                lon = int(tokens[i+2])
                pop = int(tokens[i+3])
                i += 4
                current_city = City(name, lat, lon, pop)
                for city in self.cities:
                    distance = int(tokens[i])
                    current_city.appendDistanceTo(city.name, distance)
                    city.appendDistanceTo(name, distance)
                    i += 1
                current_city.appendDistanceTo(name, 0)
                self.cities.append(current_city)

    def selectCities(self, attribute, lowerBound, upperBound):
        callbacks = {
            'population': self.__selectCitiesByPopulation,
            'name': self.__selectCitiesByName
        }

        callbacks[attribute](lowerBound, upperBound)

    def __selectCitiesByPopulation(self, lowerBound, upperBound):
        print('called __selectCitiesByPopulation, lb: ' + str(lowerBound) + ', upperBound: ' + str(upperBound))
        for city in self.city_selections.copy():
            if not lowerBound <= city.population <= upperBound:
                self.city_selections.remove(city)

    def __selectCitiesByName(self, lowerBound, upperBound):
        print('called __selectCitiesByName, lb: ' + lowerBound + ', upperBound: ' + upperBound)
        for city in self.city_selections.copy():
            regex_pattern = '^[' + lowerBound + '-' + upperBound + ']'
            if len(re.findall(regex_pattern, city.name)) == 0:
                self.city_selections.remove(city)

    def selectAllCities(self):
        for city in self.cities:
            self.city_selections.add(city)

    def unselectAllCities(self):
        self.city_selections.clear()

    def selectEdges(self, lowerBound, upperBound):
        pass

    def selectAllEdges(self):
        pass

    def unselectAllEdges(self):
        self.edge_selections.clear()

    def makeGraph(self):
        pass

    def printCities(self, attribute=None, choice=None):
        if attribute is None:
            attribute = 'name'
        if choice is None:
            choice = 'F'
        for city in self.city_selections:
            print(city.name)

    def printEdges(self):
        pass

    def testMinMaxConsDistance(self):
        pass

    def tour(self, start):
        pass

    def minCut(self):
        pass

x = Gis()
x.selectAllCities()
x.printCities()
print("\n")
x.selectCities('population', 1000, 15000)
x.printCities()
print("\n")
x.selectCities('name', 'V', 'V')
x.printCities()
print('success!')
exit()