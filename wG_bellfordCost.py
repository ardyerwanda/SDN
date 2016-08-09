from pyretic.lib.query import *
from pyretic.core import *
from pyretic.lib.corelib import *
from pyretic.lib.std import *

def abileneCostList(G):
    huge=1e30000
    routeTable={}
    route={}
    for RT in {1,2,3,4,5,6,7,8,9,10,11}:
        routeTable[RT]={}
        for u in {1,2,3,4,5,6,7,8,9,10,11}:
            routeTable[RT][u]={}
            route[u]={}
            for v in {1,2,3,4,5,6,7,8,9,10,11}:
                if u==RT:
                    route[u][v] = huge
                    route[u][u] = 0
                elif u==v and v==RT:
                    route[u][v]=0
                else:
                    route[u][v]=huge
                routeTable[RT][u][v]=route[u][v]

    #print routeTable[1][1][2]

#cost switch 1:
    #routeTable[][1] = {}
    #ke switch 2:
    routeTable[1][1][2] = 1
    #ke switch 4:
    routeTable[1][1][4] = 1

#cost switch 2:
    #routeTable[][2] = {}
    #ke switch 1:
    routeTable[2][2][1] = routeTable[1][1][2]
    #ke switch 3:
    routeTable[2][2][3] = 1
    #ke switch 4:
    routeTable[2][2][4] = 1

#cost switch 3:
    #routeTable[][3] = {}
    #ke switch 2:
    routeTable[3][3][2] = routeTable[2][2][3]
    #ke switch 6:
    routeTable[3][3][6] = 1

#cost switch 4:
    #routeTable[][4] = {}
    #ke switch 1:
    routeTable[4][4][1] = routeTable[1][1][4]
    #ke switch 2:
    routeTable[4][4][2] = routeTable[2][2][4]
    #ke switch 5:
    routeTable[4][4][5] = 1

#cost switch 5:
    #routeTable[5][5] = {}
    #ke switch 4:
    routeTable[5][5][4] = routeTable[4][4][5]
    #ke switch 6:
    routeTable[5][5][6] = 1
    #ke switch 7:
    routeTable[5][5][7] = 1

#cost switch 6:
    #routeTable[][6] = {}
    #ke switch 3:
    routeTable[6][6][3] = routeTable[3][3][6]
    #ke switch 5:
    routeTable[6][6][5] = routeTable[5][5][6]
    #ke switch 11:
    routeTable[6][6][11] = 1

#cost switch 7:
    #routeTable[][7] = {}
    #ke switch 5:
    routeTable[7][7][5] = routeTable[5][5][7]
    #ke switch 8:
    routeTable[7][7][8] = 1
    #ke switch 11:
    routeTable[7][7][11] = 1

#cost switch 8:
    #routeTable[][8] = {}
    #ke switch 7:
    routeTable[8][8][7] = routeTable[7][7][8]
    #ke switch 9:
    routeTable[8][8][9] = 1

#cost switch 9:
    #routeTable[][9] = {}
    #ke switch 8:
    routeTable[9][9][8] = routeTable[8][8][9]
    #ke switch 10:
    routeTable[9][9][10] = 1

#cost switch 10:
    #routeTable[][10] = {}
    #ke switch 9:
    routeTable[10][10][9] = routeTable[9][9][10]
    #ke switch 11:
    routeTable[10][10][11] = 1

#cost switch 11:
    #routeTable[][11] = {}
    #ke switch 6:
    routeTable[11][11][6] = routeTable[6][6][11]
    #ke switch 7:
    routeTable[11][11][7] = routeTable[7][7][11]
    #ke switch 11:
    routeTable[11][11][10] = routeTable[10][10][11]

    return routeTable