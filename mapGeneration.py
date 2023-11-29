import copy, random

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
    return forest_createMapHelper(app, app.forestMap, randomness)

def forest_createMapHelper(app, currMap, randomness):
    if len(currMap[0])<3: return
    else:
        # for L in currMap: print(L)
        # print('Before mod \n')
        randomDisplacement = random.randint(1, randomness)
        currMapEdge = len(currMap[0])-1
        #step 2. set center index to average of conrners +
        #  a random displacement
        centerIndex = (currMapEdge)//2
        sumOfCorners = ((((currMap[0][0] + currMap[0][currMapEdge] + 
                          currMap[currMapEdge][0] + 
                          currMap[currMapEdge][currMapEdge])//4)))
        
        currMap[centerIndex][centerIndex] = sumOfCorners + randomDisplacement

        #step 3. set midpoints of edges to average of corners +
        #a random displacement
        rand = random.randint(0, 10)
        #top point:
        currMap[0][centerIndex] = ((((currMap[0][0] + 
                                            currMap[0][currMapEdge])//2 + 
                                            rand)))
        #bottom point: 
        currMap[currMapEdge][centerIndex] = ((((currMap[0][currMapEdge] + 
                                            currMap[currMapEdge][currMapEdge])//2 + 
                                            rand)))
        rand = random.randint(0, 10)
        #left point:
        currMap[centerIndex][0] = ((((currMap[0][0] + 
                                            currMap[currMapEdge][0])//2 + 
                                            rand)))
        #right point: 
        currMap[centerIndex][currMapEdge] = ((((currMap[currMapEdge][0] + 
                                            currMap[currMapEdge][currMapEdge])//2 + 
                                            rand)))


        # for L in currMap: print(L)
        # print('After mod \n')
        #ADD THIS TO INTO app.forestMap AT CORRECT IDENCIES

        #step 4. recurse and decrease randomDisplacement
        #to recurse: we need to chop current map into 4 smaller maps

        newTopLefts = [(0, 0), (0, centerIndex), (centerIndex, 0), 
                       (centerIndex, centerIndex)]
        newDim = (len(currMap)+1)//2
        currMapCopy = copy.deepcopy(currMap)
        for x, y in newTopLefts:
            newMap = [[0]*newDim for i in range(newDim)]
            for row in range(newDim):
                for col in range(newDim):
                    newMap[row][col] = currMapCopy[row+x][col+y]
            forest_createMapHelper(app, newMap, randomness//2 +1)
            addToCurrMap(app, currMap, newMap, x, y)

def addToCurrMap(app, currMap, subMap, topLeftX, topLeftY):
    subMapEdge = len(subMap) -1
    oldCenter = subMapEdge//2
    newCenter = (topLeftX + topLeftX + subMapEdge)//2 #topLeft + topRight //2
    #topLeftX and topLeftY are original position in map we quartered
    newBottomX = topLeftX + subMapEdge
    newBottomY = topLeftY + subMapEdge

    currMap[topLeftX][newCenter] = subMap[0][oldCenter]
    currMap[newCenter][topLeftY] = subMap[oldCenter][0]
    currMap[newCenter][newBottomX] = subMap[oldCenter][subMapEdge]
    currMap[newBottomY][newCenter] = subMap[subMapEdge][oldCenter]

