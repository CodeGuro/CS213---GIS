__author__ = 'Tony'


# This class is a data structure used to generalize edges for the Gis glass
class Edge:

    def __init__(self, city1, city2, distance):
        self.city1 = city1
        self.city2 = city2
        self.distance = distance