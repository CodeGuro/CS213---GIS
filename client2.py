from gis import *

def main():
    gsystem = Gis()
    gsystem.selectAllCities()
    gsystem.selectAllEdges()

    delimiter = '\n*************************************\n'

    #### EXPERIMENT 4 ####
    gsystem.selectAllCities()
    gsystem.testMinMaxConsDistance()
    # source: Williston, ND and target: Wilmington, DE
    # source: Trinidad, CO, Rochester, NY
    print (delimiter)

    gsystem.selectCities('population', 50000, 100000)
    gsystem.testMinMaxConsDistance()
    # source: Waterbury, CT and target: Victoria, TX
    # source: Waterbury, CT and target: Washington, DC
    

main()
