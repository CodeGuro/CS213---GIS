__author__ = 'Tony'

from City import City
from Edge import Edge
import re


class Gis:

    def __init__(self):
        self.cities = []  # This is the list of all the available cities
        self.edges = []
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
                    self.edges.append(Edge(current_city, city, distance))
                    i += 1
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
        for edge in self.edge_selections.copy():
            if not lowerBound <= edge.distance <= upperBound:
                self.edge_selections.remove(edge)

    def selectAllEdges(self):
        for edge in self.edges:
            self.edge_selections.add(edge)

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
        for edge in self.edge_selections:
            print(edge.city1.name + '<-->' + edge.city2.name + ': ' + str(edge.distance))

    def testMinMaxConsDistance(self):
        # We want to Dijkstra's algorithm to find the shortest path between source and destination
        print('type in the source and destination in the format: sourceCity, sourceState->destCity, destState')
        user_input = input()
        tokens = re.findall('[\w]*, [\w]*|[\->< ]+', user_input)

        if len(tokens) == 0:
            return True
        elif len(tokens) != 3:
            print('invalid input')
            return False

        if '->' in tokens[1]:
            sourceName = tokens[0]
            destName = tokens[2]
        else:
            sourceName = tokens[2]
            destName = tokens[1]

        destCity = None
        sourceCity = None
        for city in self.city_selections:
            if sourceName in city.name:
                sourceCity = city
            if destName in city.name:
                destCity = city

        if sourceCity is None:
            print('source city does not exist in city selections')
            return False
        if destCity is None:
            print('destination city does not exist in city selections')
            return False

        not_visited = self.city_selections.copy()
        city_dist = {}
        city_last = {}

        for city in self.city_selections:
            city_dist[city] = float('inf')
        city_dist[sourceCity] = 0

        current_city = None
        while current_city is not destCity:
            current_city = min(not_visited, key=lambda city: city_dist[city])
            adjacent_edges = self.__findAdjacentSelectedEdges(current_city, not_visited)
            if len(adjacent_edges) is 0:
                print('Destination is impossible with the edges and cities currently selected')
                return False
            for edge in adjacent_edges:
                if edge.city1 is current_city:
                    if city_dist[edge.city2] > city_dist[current_city] + edge.distance:
                        city_dist[edge.city2] = city_dist[current_city] + edge.distance
                        city_last[edge.city2] = current_city
                else:
                    if city_dist[edge.city1] > city_dist[current_city] + edge.distance:
                        city_dist[edge.city1] = city_dist[current_city] + edge.distance
                        city_last[edge.city1] = current_city
            not_visited.remove(current_city)

        print('printing city trace...')

        city = destCity
        while city is not None:
            print(city.name)
            city = city_last.get(city)
        print('total distance: ' + str(city_dist[destCity]))
        return False

    def testMinMaxConDistanceLoop(self):
        while not self.testMinMaxConsDistance():
            pass

    def __findAdjacentSelectedEdges(self, city, notVisited):
        neighbors = []
        for edge in self.edge_selections:
            if edge.city1 is city and edge.city2 in notVisited:
                neighbors.append(edge)
            elif edge.city2 is city and edge.city1 in notVisited:
                neighbors.append(edge)
        return neighbors

    def tour(self, start):
        pass

    def minCut(self):
        pass



x = Gis()
x.selectAllCities()
x.selectAllEdges()

x.testMinMaxConDistanceLoop()

x.printEdges()
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