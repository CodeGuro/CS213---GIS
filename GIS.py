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
                lati = int(tokens[i+1])
                long = int(tokens[i+2])
                popu = int(tokens[i+3])
                stat = re.findall('[\w]+$', name)[0]
                i += 4
                current_city = City(name, stat, lati, long, popu)
                for city in self.cities:
                    distance = int(tokens[i])
                    current_city.appendDistanceTo(city.name, distance)
                    city.appendDistanceTo(name, distance)
                    i += 1
                current_city.appendDistanceTo(name, 0)
                self.cities.append(current_city)

    def selectCities(self, attribute, lowerBound, upperBound=None):
        callbacks = {
            'population': self.__selectCitiesByPopulation,
            'name': self.__selectCitiesByName,
            'latitude': self.__selectCitiesByLatitude,
            'longitude': self.__selectCitiesByLongitude,
            'state': self.__selectCitiesByState,
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

    def __selectCitiesByLatitude(self, lowerBound, upperBound):
        print('called __selectCitiesByLatitude, lb: ' + str(lowerBound) + ', ub:' + str(upperBound))
        for city in self.city_selections.copy():
            if not lowerBound <= city.latitude <= upperBound:
                self.city_selections.remove(city)

    def __selectCitiesByLongitude(self, lowerBound, upperBound):
        print('called __selectCitiesByLongitude, lb: ' + str(lowerBound) + ', ub:' + str(upperBound))
        for city in self.city_selections.copy():
            if not lowerBound <= city.longitude <= upperBound:
                self.city_selections.remove(city)

    def __selectCitiesByState(self, state, placeholder):
        print('called __selectCitiesByState, state: ' + state)
        for city in self.city_selections.copy():
            if city.state != state:
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

        callbacks = {
            'name': self.__printCitiesByName,
            'population': self.__printCitiesByPopulation
        }
        printCB = {
            'F': self.__fullCityPrint,
            'S': self.__shortCityPrint
        }

        callbacks[attribute](printCB[choice])

    def __printCitiesByName(self, printCB):
        for city in self.city_selections:
            printCB(city)

    def __printCitiesByPopulation(self, printCB):
        city_dict = dict()
        for city in self.city_selections:
            city_dict[city.population] = city

        sortedCities = sorted(city_dict.items())

        for it in sortedCities:
            city = it[1]
            printCB(city)

    def __fullCityPrint(self, city):
        print(city.name + ' [' + str(city.latitude) + ',' + str(city.longitude) + '], ' + str(city.population))

    def __shortCityPrint(self, city):
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
x.printCities('name')
print("\n")
x.selectCities('population', 1000, 15000)
x.printCities()
print("\n")
x.selectCities('name', 'R', 'T')
x.printCities()
print("\n")
x.selectCities('latitude', 3000, 4000)
x.printCities()
print("\n")
x.selectAllCities()
x.selectCities('state', 'OH')
x.printCities()
print("\n")
x.printCities('population')
exit()