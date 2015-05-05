__author__ = 'Tony'

from City import City
from Edge import Edge
import re
import networkx as nx
import matplotlib.pyplot as plt
from math import floor


class Gis:

    # Define the default constructor
    def __init__(self):
        # This code is responsible for reading from the GisFile
        self.cities = []  # This is the list of all the available cities
        self.edges = []
        self.city_selections = set()
        self.edge_selections = set()
        with open('gis.dat', 'r') as gisfile:
            # Parse from the file and generate tokens
            tokens = re.findall('[A-Za-z\- ]+, [A-Za-z\- ]*|[0-9]+', gisfile.read())
            i = 0  # iterator
            while i < len(tokens):
                name = tokens[i+0]
                lati = float(tokens[i+1]) / 100.0
                long = float(tokens[i+2]) / 100.0
                popu = int(tokens[i+3])
                stat = re.findall('[\w]+$', name)[0]
                i += 4
                current_city = City(name, stat, lati, long, popu)
                for city in self.cities:
                    distance = int(tokens[i])
                    self.edges.append(Edge(current_city, city, distance))
                    i += 1
                self.cities.append(current_city)

    # add a single city to the selected list
    def selectSingleCity(self, name):
        for city in self.cities:
            if name == city.name:
                if city in self.city_selections:
                    print(name + ' is already selected')
                else:
                    print('city found: ' + city.getFullStr())
                    self.city_selections.add(city)
                return
        print(name + ' is not in the database')

    # remove a single city by name from selected list
    def removeSingleCity(self, name):
        for city in self.city_selections.copy():
            if city.name == name:
                self.city_selections.remove(city)
                break

    # Create a new constraint on the currently selected cities
    def selectCities(self, attribute, lowerBound, upperBound=None):
        # callbacks reflects the attribute
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
        # Regex pattern for state, must be one letter
        regex_pattern = '^[' + str(lowerBound) + '-' + str(upperBound) + ']'
        domain_callbacks = {
            'name': lambda city: not (len(re.findall(regex_pattern, callbacks[attribute](city))) == 0),
            'state': lambda city: city.state == lowerBound,
            'numeric': lambda city: (lowerBound <= callbacks[attribute](city) <= upperBound)
        }

        # default numeric domain (for safety)
        domain_func = domain_callbacks.get(attribute, domain_callbacks['numeric'])

        for city in self.city_selections.copy():
            if not domain_func(city):
                self.city_selections.remove(city)

    # Select all available cities
    def selectAllCities(self):
        for city in self.cities:
            self.city_selections.add(city)

    # Clear the city selections
    def unselectAllCities(self):
        self.city_selections.clear()

    # Create a new constraint on the currently selected Edges
    def selectEdges(self, lowerBound, upperBound):
        for edge in self.edge_selections.copy():
            if not lowerBound <= edge.distance <= upperBound:
                self.edge_selections.remove(edge)

    # Select a single edge between two cities
    def selectSingleEdge(self, cityNameState1, cityNameState2):
        city1 = None
        city2 = None
        for city in self.cities:
            if city.name == cityNameState1:
                city1 = city
            if city.name == cityNameState2:
                city2 = city

        check = lambda edge: (edge.city1 is city1 and edge.city2 is city2) or (edge.city1 is city2 and edge.city2 is city1)
        for edge in self.edges:
            if check(edge):
                if edge in self.edge_selections:
                    print('edge already selected')
                else:
                    print('edge found: ' + edge.getStr())
                    self.edge_selections.add(edge)
                return
        # One of the cities do not exist
        missing = cityNameState1 if city1 is None else cityNameState2
        print(missing + ' is not a city in the database')

    # Remove a single edge
    def removeSingleEdge(self, cityNameState1, cityNameState2):
        city1 = None
        city2 = None
        for city in self.cities:
            if city.name == cityNameState1:
                city1 = city
            if city.name == cityNameState2:
                city2 = city

        check = lambda edge: (edge.city1 is city1 and edge.city2 is city2) or (edge.city1 is city2 and edge.city2 is city1)
        for edge in self.edges:
            if check(edge):
                if edge in self.edge_selections:
                    print('edge found: ' + edge.getStr())
                    self.edge_selections.remove(edge)
                else:
                    print('edge \'' + edge.getStr() + '\' not selected')
                return
        # One of the cities do not exist
        missing = cityNameState1 if city1 is None else cityNameState2
        print(missing + ' is not a city in the database')

    # Select all available edges
    def selectAllEdges(self):
        for edge in self.edges:
            self.edge_selections.add(edge)

    # Clear the edge selections
    def unselectAllEdges(self):
        self.edge_selections.clear()

    # Draw the graph (warning: will not look pretty if too many vertices are selected)
    def makeGraph(self):
        graph = nx.Graph()

        # Label the cities
        cityLabels = {}
        edgeLabels = {}
        for city in self.city_selections:
            graph.add_node(city)
            cityLabels[city] = city.name

        # Label the edges
        for edge in self.edge_selections:
            if (edge.city1 in self.city_selections) and (edge.city2 in self.city_selections):
                graph.add_edge(edge.city1, edge.city2)
                edgeLabels[(edge.city1, edge.city2)] = edge.distance

        # Do the drawing
        pos = nx.shell_layout(graph)
        nx.draw(graph, pos)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edgeLabels, font_size=10)
        nx.draw_networkx_labels(graph, pos, labels=cityLabels, font_size=10,)
        plt.show()

    # Print the currently selected cities: choice=(F:full, S:short)
    def printCities(self, attribute=None, choice=None):
        if attribute is None:
            attribute = 'name'
        if choice is None:
            choice = 'F'

        # lambda_procs reflects the attribute
        lambda_procs = {
            'name': lambda city: city.name,
            'state': lambda city: city.state,
            'population': lambda city: city.population,
            'latitude': lambda city: city.latitude,
            'longitude': lambda city: city.longitude,
        }

        printCB = {
            'F': City.fullPrint,
            'S': City.shortPrint
        }

        if (attribute not in lambda_procs) or (choice not in printCB):
            print('invalid attribute or choice')
            return

        # Elegantly sort by the attribute
        sorted_cities = sorted(self.city_selections, key=lambda_procs.get(attribute))

        for city in sorted_cities:
            printCB[choice](city)

    # Print the currently selected edges
    def printEdges(self):
        for edge in self.edge_selections:
            print(edge.getStr())

    # Minimize the maximum distance between two cities
    def testMinMaxConsDistance(self):
        # Repeatedly ask user for input until they quit (by giving no input)
        repeat = True
        while repeat is not False:
            print('type in the source and destination in the format: sourceCity, sourceState->destCity, destState')

            # Parse the user input into tokens
            user_input = input()
            tokens = re.findall('[\w, ]+[\w]+|[\->< ]+', user_input)

            if len(tokens) == 0:  # No input, quit
                repeat = False
                continue
            elif len(tokens) != 3:  # Not enough input, repeat
                print('invalid input')
                continue

            if '->' in tokens[1]:  # source -> destination
                sourceName = tokens[0]
                destName = tokens[2]
            elif '<-' in tokens[1]:  # destination <- source
                sourceName = tokens[2]
                destName = tokens[0]
            else:
                print('invalid input')
                continue

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

            # The fun starts here
            self.__dijkstrasAlgorithm(sourceCity, destCity)

    # Dijkstra's Algorithm used to find shortest possible path between a pair of vertices
    def __dijkstrasAlgorithm(self, sourceCity, destCity):

        not_visited = self.city_selections.copy()
        city_dist = {}
        city_last = {}

        # Assign infinity to every city, except the starting city
        for city in self.city_selections:
            city_dist[city] = float('inf')
        city_dist[sourceCity] = 0

        # Begin the loop, start with the smallest city possible, remove it from 'not_visited' list, update vals, repeat
        # Until the destination has been found. Dijkstra's algorithm guarantees it will be the shortest path possible
        current_city = None
        while current_city is not destCity:
            current_city = min(not_visited, key=lambda city: city_dist[city])
            if city_dist[current_city] == float('inf'): # if true, sourceCity must be in a disconnected component
                print('Destination is impossible with the edges and cities currently selected')
                return
            adjacent_edges = self.__findAdjacentSelectedEdges(current_city, not_visited)
            if len(adjacent_edges) is not 0:
                for edge in adjacent_edges:
                    # Replace path to adjacent city with current path, if it is shorter
                    if edge.city1 is current_city:
                        if city_dist[edge.city2] > city_dist[current_city] + edge.distance:
                            city_dist[edge.city2] = city_dist[current_city] + edge.distance
                            city_last[edge.city2] = current_city
                    else:
                        if city_dist[edge.city1] > city_dist[current_city] + edge.distance:
                            city_dist[edge.city1] = city_dist[current_city] + edge.distance
                            city_last[edge.city1] = current_city
            not_visited.remove(current_city)  # update the not_visited cities

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

    # Print n most populated cities
    def printPopulatedStates(self, numStates=50):

        # sort the cities by population
        popStates = {}

        # add the cities to the list in order of n most populated, decreasing order of population
        for city in self.city_selections:
            if city.state not in popStates:
                popStates[city.state] = 0
            popStates[city.state] += city.population

        mostPopStates = sorted(popStates, key=lambda str: popStates[str], reverse=True)

        iterator = 0
        for state in mostPopStates:
            iterator += 1
            if iterator > numStates:
                break
            print(state + ' ' + str(popStates[state]))

    # print population distribution with the given stride (default: 20000)
    def printPopulationDistr(self, stride=20000):

        distribs = []
        for city in self.city_selections:
            idx = floor(city.population / stride)
            while len(distribs) < idx + 2:
                distribs.append(0)
            distribs[idx] += 1
            if city.population % stride == 0:
                distribs[idx+1] += 1

        it = 0
        for numCities in distribs:
            print('[' + str(stride * it) + ', ' + str(stride * (it+1)) + ']: ' + str(numCities))
            it += 1

    # Utility function used to find adjacent edges between single city and non-visited vertices using selected edges
    def __findAdjacentSelectedEdges(self, city, notVisited):
        adjacent = []
        for edge in self.edge_selections:
            if edge.city1 is city and edge.city2 in notVisited:
                adjacent.append(edge)
            elif edge.city2 is city and edge.city1 in notVisited:
                adjacent.append(edge)
        return adjacent

    # Uses Nearest Neighbor algorithm to compute output for the traveling salesman problem
    def tour(self, start):
        # Make sur ethe start city actually exists in the selections
        start_city = None
        for city in self.city_selections:
            if start == city.name:
                start_city = city
        if start_city not in self.city_selections:
            print(start + ' is not selected')
            return

        # Begin the hamiltonian circuit starting from the source: start_city
        path = [(start_city, 0)]
        not_visited = self.city_selections.copy()
        current_city = start_city
        while len(not_visited) > 0:
            adjacent_edges = self.__findAdjacentSelectedEdges(current_city, not_visited)
            not_visited.remove(current_city)
            if len(adjacent_edges) == 0:
                break
            next_city = None
            next_dist = float("inf")
            for edge in adjacent_edges:
                if edge.distance < next_dist:
                    next_city = edge.city1 if current_city is not edge.city1 else edge.city2
                    next_dist = edge.distance
            path.append((next_city, next_dist))
            current_city = next_city

        # All cities have been visited, find an edge between current city and start city
        last_edge_l = self.__findAdjacentSelectedEdges(current_city, {start_city})
        if (len(not_visited) > 0) or (len(last_edge_l) == 0):
            print('tour not possible from ' + start)
            return
        path.append((start_city, last_edge_l[0].distance))  # path becomes a circuit here

        # Begin printing the circuit trace
        total_distance = 0
        iterator = 0
        string = ''
        delim = ''
        for tup in path:
            iterator += 1
            total_distance += tup[1]
            string += delim + tup[0].name
            if iterator % 4 == 0:
                delim = '-->\n'
            else:
                delim = '-->'
        print(string)
        print('total distance: ' + str(total_distance))