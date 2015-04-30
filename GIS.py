__author__ = 'Tony'

from City import City
from Edge import Edge
import re
import networkx as nx
import matplotlib.pyplot as plt


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
        domain_callbacks = {
            'name': lambda city: not (len(re.findall(regex_pattern, callbacks[attribute](city))) == 0),
            'state': lambda city: city.state == lowerBound,
            'numeric': lambda city: (lowerBound <= callbacks[attribute](city) <= upperBound)
        }

        domain_func = domain_callbacks.get(attribute, domain_callbacks['numeric'])

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
        graph = nx.Graph()

        cityLabels = {}
        edgeLabels = {}
        for city in self.city_selections:
            graph.add_node(city)
            cityLabels[city] = city.name

        for edge in self.edge_selections:
            if (edge.city1 in self.city_selections) and (edge.city2 in self.city_selections):
                graph.add_edge(edge.city1, edge.city2)
                edgeLabels[(edge.city1, edge.city2)] = edge.distance

        pos = nx.shell_layout(graph)

        nx.draw(graph, pos)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edgeLabels, font_size=10)
        nx.draw_networkx_labels(graph, pos, labels=cityLabels, font_size=10,)
        plt.show()

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
        repeat = True
        while repeat is not False:
            print('type in the source and destination in the format: sourceCity, sourceState->destCity, destState')
            user_input = input()
            tokens = re.findall('[\w, ]+[\w]+|[\->< ]+', user_input)

            if len(tokens) == 0:
                repeat = False
                continue
            elif len(tokens) != 3:
                print('invalid input')
                continue

            if '->' in tokens[1]:
                sourceName = tokens[0]
                destName = tokens[2]
            else:
                sourceName = tokens[2]
                destName = tokens[0]

            destCity = None
            sourceCity = None
            for city in self.city_selections:
                if sourceName in city.name:
                    sourceCity = city
                if destName in city.name:
                    destCity = city

            if sourceCity is None:
                print('source city does not exist in city selections')
                continue
            if destCity is None:
                print('destination city does not exist in city selections')
                continue

            self.__dijkstrasAlgorithm(sourceCity, destCity)

    def __dijkstrasAlgorithm(self, sourceCity, destCity):

        not_visited = self.city_selections.copy()
        city_dist = {}
        city_last = {}

        for city in self.city_selections:
            city_dist[city] = float('inf')
        city_dist[sourceCity] = 0

        current_city = None
        while current_city is not destCity:
            current_city = min(not_visited, key=lambda city: city_dist[city])
            if city_dist[current_city] == float('inf'):
                print('Destination is impossible with the edges and cities currently selected')
                return
            adjacent_edges = self.__findAdjacentSelectedEdges(current_city, not_visited)
            if len(adjacent_edges) is not 0:
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

        path = []
        city = destCity
        while city is not None:
            prev_city = city_last.get(city)
            if prev_city is not None:
                path.insert(0, (prev_city, city, city_dist[city] - city_dist[prev_city]))
            city = prev_city

        for tup in path:
            print(tup[0].name + ' --> ' + tup[1].name + ': dis: ' + str(tup[2]))
        print('total distance: ' + str(city_dist[destCity]))
        return

    def __findAdjacentSelectedEdges(self, city, notVisited):
        adjacent = []
        for edge in self.edge_selections:
            if edge.city1 is city and edge.city2 in notVisited:
                adjacent.append(edge)
            elif edge.city2 is city and edge.city1 in notVisited:
                adjacent.append(edge)
        return adjacent

    def tour(self, start):
        pass

x = Gis()
x.selectAllCities()
x.selectAllEdges()
x.testMinMaxConsDistance()

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