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
            'population': lambda city: city.population,
            'name': lambda city: city.name,
            'latitude': lambda city: city.latitude,
            'longitude': lambda city: city.longitude,
            'state': lambda city: city.state,
            }

        if attribute not in callbacks:
            print('invalid attribute')
            return

        regex_pattern = '^[' + str(lowerBound) + '-' + str(upperBound) + ']'
        numeric_domain = lambda city: (lowerBound <= callbacks[attribute](city) <= upperBound)
        name_domain = lambda city: not (len(re.findall(regex_pattern, callbacks[attribute](city))) == 0)
        state_domain = lambda city: city.state == lowerBound

        if attribute == 'name':
            domain_func = name_domain
        elif attribute == 'state':
            domain_func = state_domain
        else:
            domain_func = numeric_domain

        for city in self.city_selections.copy():
            if not domain_func(city):
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

        lambda_procs = {
            'name': lambda city: city.name,
            'state': lambda city: city.state,
            'population': lambda city: city.population,
            'latitude': lambda city: city.latitude,
            'longitude': lambda city: city.longitude,
        }

        printCB = {
            'F': self.__fullCityPrint,
            'S': self.__shortCityPrint
        }

        if (attribute not in lambda_procs) or (choice not in printCB):
            print('invalid attribute or choice')
            return

        sorted_cities = sorted(self.city_selections, key=lambda_procs.get(attribute))

        for city in sorted_cities:
            printCB[choice](city)

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
print("\n")
x.printCities('longitude')
print("\n")
x.selectAllCities()
x.printCities('population', 'F')
exit()