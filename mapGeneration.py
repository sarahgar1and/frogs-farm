from cmu_graphics import *
import random

def onAppStart(app):
    app.forestSize = 41
    print(forest_createMap(app))

def forest_createMap(app): 
    #diamond square algorithm source: 
    #https://learn.64bitdragon.com/articles/computer-science/procedural-generation/the-diamond-square-algorithm 
    app.forestMap = [[0]*app.forestSize for i in range(app.forestSize)]
    
    #step 1. set corners to same random value
    randomValue = random.randint(0, 200)
    app.forestMap[0][0] = randomValue
    app.forestMap[0][app.forestSize-1] = randomValue
    app.forestMap[app.forestSize - 1][0] = randomValue
    app.forestMap[app.forestSize-1][app.forestSize-1] = randomValue

    #step 2. set center index to average of conrners + a random displacement
    randomDisplacement = random.randint(0, 10)
    centerIndex = (app.forestSize-1)//2
    app.forestMap[centerIndex][centerIndex] = randomValue + randomDisplacement

    #step 3. set midpoints of edges to average of corners + a random displacement
    rand = random.randint(0, 10)
    #top point:
    app.forestMap[0][centerIndex] = ((((app.forestMap[0][0] + 
                                       app.forestMap[0][app.forestSize-1])//2 + 
                                       rand)))
    #bottom point: (same as top)
    app.forestMap[0][centerIndex] = ((((app.forestMap[0][0] + 
                                       app.forestMap[0][app.forestSize-1])//2 + 
                                       rand)))
    rand = random.randint(0, 10)
    #left point:
    app.forestMap[centerIndex][0] = ((((app.forestMap[0][0] + 
                                       app.forestMap[app.forestSize-1][0])//2 + 
                                       rand)))
    #right point: (same as left)
    app.forestMap[centerIndex][0] = ((((app.forestMap[0][0] + 
                                       app.forestMap[app.forestSize-1][0])//2 + 
                                       rand)))
    #step 4. recurse and decrease randomDisplacement
    return app.forestMap

def main():
    runApp()

main()