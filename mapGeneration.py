from cmu_graphics import *
import copy, random

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
    return forest_createMapHelper(app, randomness, 
                                  app.forestSize-1, 0, 0)

def forest_createMapHelper(app, randomness, subMapWidth, x, y):
    if subMapWidth < 3: return
    else:
        randomDisplacement = random.randint(1, randomness)
        currMapEdge = x + subMapWidth
        #step 2. set center index to average of conrners +
        #  a random displacement
        centerIndex = (currMapEdge)//2
        sumOfCorners = ((((app.forestMap[0][0] + app.forestMap[0][currMapEdge] + 
                          app.forestMap[currMapEdge][0] + 
                          app.forestMap[currMapEdge][currMapEdge])//4)))
        
        app.forestMap[centerIndex][centerIndex] = sumOfCorners + randomDisplacement

        #step 3. set midpoints of edges to average of corners +
        #a random displacement
        rand = random.randint(1, randomness)
        #top point:
        app.forestMap[0][centerIndex] = ((((app.forestMap[0][0] + 
                                            app.forestMap[0][currMapEdge])//2 + 
                                            rand)))
        #bottom point: 
        app.forestMap[currMapEdge][centerIndex] = ((((app.forestMap[0][currMapEdge] + 
                                            app.forestMap[currMapEdge][currMapEdge])//2 + 
                                            rand)))
        rand = random.randint(1, randomness)
        #left point:
        app.forestMap[centerIndex][0] = ((((app.forestMap[0][0] + 
                                            app.forestMap[currMapEdge][0])//2 + 
                                            rand)))
        #right point: 
        app.forestMap[centerIndex][currMapEdge] = ((((app.forestMap[currMapEdge][0] + 
                                            app.forestMap[currMapEdge][currMapEdge])//2 + 
                                            rand)))

        #step 4. recurse and decrease randomDisplacement
        #Quarter the current portion we're looking at: new width = centerIndex

        newTopLefts = [(0, 0), (0, centerIndex), (centerIndex, 0), 
                       (centerIndex, centerIndex)]
        for x, y in newTopLefts:
            forest_createMapHelper(app, randomness//2+1, centerIndex, x, y)

# def addToCurrMap(app, currMap, subMap, topLeftX, topLeftY):
#     subMapEdge = len(subMap) -1
#     oldCenter = subMapEdge//2
#     newCenter = (topLeftX + topLeftX + subMapEdge)//2 #topLeft + topRight //2
#     #topLeftX and topLeftY are original position in map we quartered
#     newBottomX = topLeftX + subMapEdge
#     newBottomY = topLeftY + subMapEdge

#     currMap[topLeftX][newCenter] = subMap[0][oldCenter]
#     currMap[newCenter][topLeftY] = subMap[oldCenter][0]
#     currMap[newCenter][newBottomX] = subMap[oldCenter][subMapEdge]
#     currMap[newBottomY][newCenter] = subMap[subMapEdge][oldCenter]

forest_createMap(app)
for L in app.forestMap: print(L)