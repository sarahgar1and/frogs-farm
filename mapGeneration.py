from cmu_graphics import *
import random

app.forestSize = 9

def forest_createMap(app): 
    #diamond square algorithm source: 
    #https://learn.64bitdragon.com/articles/computer-science/procedural-generation/the-diamond-square-algorithm 
    app.forestMap = [[0]*app.forestSize for i in range(app.forestSize)]
    randomness = 10
    #step 1. set corners to same random value
    randomValue = random.randint(1, 10)
    app.forestMap[0][0] = randomValue
    app.forestMap[0][app.forestSize-1] = randomValue
    app.forestMap[app.forestSize-1][0] = randomValue
    app.forestMap[app.forestSize-1][app.forestSize-1] = randomValue
    return forest_createMapHelper(app, randomness, app.forestSize-1, 0, 0)

def forest_createMapHelper(app, randomness, subMapWidth, topLeftX, topLeftY):
    if subMapWidth < 1: return
    else:
        randomDisplacement = random.randint(1, randomness)
        currMapEdge = topLeftX + subMapWidth
        #step 2. set center index to average of conrners +
        #  a random displacement
        centerIndex = (currMapEdge)//2
        sumOfCorners = ((((app.forestMap[topLeftX][topLeftY] + 
                           app.forestMap[topLeftX][currMapEdge] + 
                          app.forestMap[currMapEdge][topLeftY] + 
                          app.forestMap[currMapEdge][currMapEdge])//4)))
        
        app.forestMap[centerIndex][centerIndex] = sumOfCorners + randomDisplacement
        
        #step 3. set midpoints of edges to average of corners +
        #a random displacement
        rand = random.randint(1, randomness)
        #left mid point: top left corner + bottom left corner
        app.forestMap[topLeftX][centerIndex] = ((((app.forestMap[topLeftX][topLeftY] + 
                                            app.forestMap[topLeftX][currMapEdge])//2 + 
                                            rand)))
        
        #right mid point: top right corner + bottom right corner 
        app.forestMap[currMapEdge][centerIndex] = ((((app.forestMap[topLeftX][currMapEdge] + 
                                            app.forestMap[currMapEdge][currMapEdge])//2 + 
                                            rand)))
        
        rand = random.randint(1, randomness)
        #top mid point: top left corner + top right corner
        app.forestMap[centerIndex][topLeftY] = ((((app.forestMap[topLeftX][topLeftY] + 
                                            app.forestMap[currMapEdge][topLeftX])//2 + 
                                            rand)))

        #bottom mid point: bottom left corner + bottom right corner
        app.forestMap[centerIndex][currMapEdge] = ((((app.forestMap[topLeftX][currMapEdge] + 
                                            app.forestMap[currMapEdge][currMapEdge])//2 + 
                                            rand)))
    
        #step 4. recurse and decrease randomDisplacement
        #Quarter the current portion we're looking at: new width = centerIndex

        newTopLefts = [(0, 0), (0, centerIndex), (centerIndex, 0), 
                       (centerIndex, centerIndex)]
        for x, y in newTopLefts:
            forest_createMapHelper(app, randomness//2 +1, subMapWidth//2, x, y)

forest_createMap(app)
for L in app.forestMap: print(L)