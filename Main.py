__author__ = 'Tony'

from GIS import Gis

class Main:
    def main(self):
        g_system = Gis()
        g_system.selectAllCities()
        g_system.selectAllEdges()

        delim = '\n*************************************'
        print('#### EXPERIMENT 1 ####')
        print('g_system.printCities(\'name\', \'S\')')
        g_system.printCities('name', 'S')

        print(delim)
        print('# print full display')
        print('g_system.printCities(\'population\', \'F\')')
        g_system.printCities('population', 'F')

        print(delim)
        print('#### EXPERIMENT 2 ####')
        print('# select all cities with latitudes between 40N and 50N'
              '\n# and longitudes between 85W and 130W.')
        g_system.selectCities('latitude', 40, 50)
        g_system.selectCities('longitude', 85, 130)
        print('Population distribution of cities with latitudes between 40N and 50N'
              '\nand longitudes between 85W and 130W')
        g_system.printCities('population', 'F')

        print(delim)
        print('#### EXPERIMENT 3 ####')
        print('# print the most populated states in increasing'
              '\norder of population')
        g_system.printCities('population', 'F')

        print(delim)
        print('#### EXPERIMENT 4 ####')
        print('g_system.testMinMaxConsDistance')
        g_system.testMinMaxConsDistance()

        print(delim)
        print('#### EXPERIMENT 5 ####')
        print('# print TSP tour starting from Yakima, WA, with'
              '\n# exactly 4 cities on each line except possibly the'
              '\n# last line.')
        print('g_system.selectAllCities()')
        print('g_system.selectAllEdges()')
        print('g_system.tour(\'Yakima, WA\')')
        g_system.selectAllCities()
        g_system.selectAllEdges()
        g_system.tour('Yakima, WA')
        print(delim)
        print('g_system.unselectAllEdges()')
        print('g_system.tour(\'Yakima, WA\')')
        g_system.unselectAllEdges()
        g_system.tour('Yakima, WA')

        print(delim)
        print('This concludes all of the experiments')

main = Main()
main.main()