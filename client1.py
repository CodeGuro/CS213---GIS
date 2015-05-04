from GIS import *

def main():
    gsystem = Gis()
    gsystem.selectAllCities()
    gsystem.selectAllEdges()

    delimiter = '\n*************************************\n'

    #### EXPERIMENT 1 ####
    gsystem.selectCities('state', 'AZ')
    gsystem.printCities("longitude", 'S')
    
    gsystem.selectAllCities()
    gsystem.selectCities('state', 'VA')
    gsystem.selectCities('name','R','V')
    gsystem.printCities()
    print (delimiter)

    # print full display
    gsystem.printCities('population', 'F')
    print (delimiter)

    gsystem.selectCities('state', 'GA')
    gsystem.printCities()    

    #### EXPERIMENT 2 ####

    # select all cities with latitudes between 40N and 50N
    # and longitudes between 85W and 130W.
    
    gsystem.selectAllCities()
    gsystem.selectAllEdges()
    gsystem.selectCities('latitude',40,50)
    gsystem.selectCities('longitude',85,130)

    print ('Population distribution of cities with latitudes between\n \
    40N and 50N and longitudes between 85W and 130W.\n')
    
    gsystem.printPopulationDistr()

    print (delimiter)

    # print population distribution of cities in CA
    gsystem.selectAllCities()
    gsystem.selectCities('state','NY')

    print ('Population distribution of cities in California.\n')
    gsystem.printPopulationDistr(2000)    

    print (delimiter)
    
    #### EXPERIMENT 3 ####

    # print 'num' most populated states in non-increasing 
    # order of their population.

    gsystem.selectCities('population', 100000, 2000000)
    
    num = 3
    gsystem.printPopulatedStates(num)
    print (delimiter)

    gsystem.selectCities('population', 10000, 100000)
    
    num = 2
    gsystem.printPopulatedStates(num)
    print (delimiter)
    
    gsystem.selectCities('population', 10000, 10000)
    
    num = 1
    gsystem.printPopulatedStates(num)
    print (delimiter)

    

main()
