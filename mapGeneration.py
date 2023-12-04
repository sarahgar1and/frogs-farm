import random

def forest_createMap(app): 
    app.forestSize = 21
    #diamond square algorithm source: 
    #https://learn.64bitdragon.com/articles/computer-science/procedural-generation/the-diamond-square-algorithm 
    app.forestMap = [[0]*app.forestSize for i in range(app.forestSize)]
    randomness = 10
    #step 1. set corners to same random value
    app.randomValue = random.randint(1, 10)
    app.forestMap[0][0] = app.randomValue
    app.forestMap[0][app.forestSize-1] = app.randomValue
    app.forestMap[app.forestSize-1][0] = app.randomValue
    app.forestMap[app.forestSize-1][app.forestSize-1] = app.randomValue

    forest_createMapHelper(app, randomness, app.forestSize-1, 0, 0)

def forest_createMapHelper(app, randomness, subMapWidth, topLeftX, topLeftY):
    if subMapWidth < 1: return
    else:
        randomDisplacement = random.randint(1, randomness)
        currMapEdgeX = topLeftX + subMapWidth
        currMapEdgeY = topLeftY + subMapWidth
        #step 2. set center index to average of conrners +
        #  a random displacement
        centerIndexX = (currMapEdgeX+topLeftX)//2
        centerIndexY = (currMapEdgeY+topLeftY)//2
        sumOfCorners = ((((app.forestMap[topLeftX][topLeftY] + 
                           app.forestMap[topLeftX][currMapEdgeY] + 
                          app.forestMap[currMapEdgeX][topLeftY] + 
                          app.forestMap[currMapEdgeX][currMapEdgeY])//4)))
        
        app.forestMap[centerIndexX][centerIndexY] = sumOfCorners + randomDisplacement
        
        #step 3. set midpoints of edges to average of corners +
        #a random displacement
        rand = random.randint(1, randomness)
        #left mid point: top left corner + bottom left corner
        app.forestMap[topLeftX][centerIndexY] = ((((app.forestMap[topLeftX][topLeftY] + 
                                            app.forestMap[topLeftX][currMapEdgeY])//2 + 
                                            rand)))
        
        #right mid point: top right corner + bottom right corner 
        app.forestMap[currMapEdgeX][centerIndexY] = ((((app.forestMap[currMapEdgeX][topLeftY] + 
                                            app.forestMap[currMapEdgeY][currMapEdgeY])//2 + 
                                            rand)))
        
        rand = random.randint(1, randomness)
        #top mid point: top left corner + top right corner
        app.forestMap[centerIndexX][topLeftY] = ((((app.forestMap[topLeftX][topLeftY] + 
                                            app.forestMap[currMapEdgeX][topLeftY])//2 + 
                                            rand)))

        #bottom mid point: bottom left corner + bottom right corner
        app.forestMap[centerIndexX][currMapEdgeY] = ((((app.forestMap[topLeftX][currMapEdgeY] + 
                                            app.forestMap[currMapEdgeX][currMapEdgeY])//2 + 
                                            rand)))
    
        #step 4. recurse and decrease randomDisplacement
        #Quarter the current portion we're looking at: new width = centerIndex

        newTopLefts = [(topLeftX, topLeftY), (topLeftX, centerIndexY), 
                       (centerIndexX, topLeftY), (centerIndexX, centerIndexY)]
        for x, y in newTopLefts:
            forest_createMapHelper(app, randomness//2 +1, subMapWidth//2, x, y)

# forest_createMap(app)
# for L in app.forestMap: print(L)

