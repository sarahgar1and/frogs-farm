from cmu_graphics import *
from classes import *

#data csv file lines -- initial vals:
    #1. day -- 0
    #2. frog hunger -- 20
    #3. frog sleep -- 20
    #4. money -- 20
    #5. inventory list -- ''
    #6. num in inventory -- ''
    #7. dirt cells -- ''
    #8. plants -- ''
    #9. plants days alive -- ''
    #10. plants location -- ''

#------------------------------------------LOAD
def loadStartFile(app):
    dataList = []
    with open('data.csv', 'r') as file:
        data = file.read()
    for line in data.splitlines():
         dataList.append([line])
#integers:
    app.day = int(dataList[0][0])
    app.frog.hunger = int(dataList[1][0])
    app.frog.sleep = int(dataList[2][0])
    app.money = int(dataList[3][0])
#inventory:
    if dataList[4][0] != '':
        loadInventory(app, dataList[4][0], dataList[5][0])
#dirt cells:
    if dataList[6][0] != '':
        loadDirt(app, dataList[6][0])
#plants:
    if dataList[7][0] != '':
        loadPlants(app, dataList[7][0], dataList[8][0], dataList[9][0])

def loadInventory(app, itemString, numString):
    #itemString looks like: 'tomato blueberrySeed strawberry'
    #numString looks like: '1 1 2'
    numList = []
    for num in numString.split(' '):
        numList.append(int(num))

    i=0 #keep track of place in string, index into numList
    for item in itemString.split(' '):
        if 'Seed' in item:
            item = item[:-4] #get rid of 'Seed'
            seed = Seed(item)
            seed.num = numList[i]
            addToInventory(app, seed)
        else: 
            crop = Crop(item)
            crop.num = numList[i]
            addToInventory(app, crop)
        i += 1

def loadDirt(app, cellString):
    #cellString looks like: '100,300 400,500 600,200'
    for line in cellString.split(' '):
        cellLeft, cellTop = line.split(',')
        app.dirtCells.add((int(cellLeft), int(cellTop)))

        x, y = int(cellLeft)+app.cellWidth/2, int(cellTop)+app.cellHeight/2
        app.plants[(x, y)] = 'dirt' #can put something here

def loadPlants(app, plantString, dayString, locationString):
    # plantString looks like: 'tomato strawberry wheat'
    # dayString looks like: '1 2 4'
    # locationString looks like: '150.0,128.0 400.0,500.0'
    dayList = []
    for day in dayString.split(' '):
        dayList.append(int(day))

    plantList = []
    i = 0
    for item in plantString.split(' '):
        plant = Plant(item)
        plant.days = dayList[i]
        plantList.append[plant]
        i += 1

    i = 0
    for coords in locationString.split(' '):
        x, y = coords.split(',')
        app.plants[(int(x), int(y))] = plantList[i]
        i += 1

#------------------------------------------SAVE     
def saveData(app):
    #in order of lines:
    inventoryItems = getInventoryItems(app)
    numInventoryItems = getInventoryNums(app)
    dirtCells = getDirtCells(app)
    plants = getPlants(app)
    plantsDays = getPlantDays(app)
    plantsLocations = getPlantLocations(app)
    with open('data.csv', 'w') as file:
        file.write(f"{app.day}\n{app.frog.hunger}\n{app.frog.sleep}\n{app.money}\n{inventoryItems}\n{numInventoryItems}\n{dirtCells}\n{plants}\n{plantsDays}\n{plantsLocations}")

def getInventoryItems(app):
    itemString = ''
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            if app.inventory[row][col] != None:
                if type(app.inventory[row][col]) == Seed:
                    itemString += f' {app.inventory[row][col].type}Seed'
                else: itemString += f' {app.inventory[row][col].type}'
    return itemString.strip()

def getInventoryNums(app):
    numString = ''
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            if app.inventory[row][col] != None:
                numString += f' {app.inventory[row][col].num}'
    return numString.strip()

def getDirtCells(app):
    cells = ''
    for x, y in app.dirtCells:
        cells += f' {x},{y}'
    return cells.strip()

def getPlants(app):    
    plants = ''
    for cell in app.plants:
        if app.plants[cell] != 'dirt':
            plants += f' {app.plants[cell].species}'
    return plants.strip()

def getPlantDays(app):
    days = ''
    for cell in app.plants:
        if app.plants[cell] != 'dirt':
            days += f' {app.plants[cell].days}'
    return days.strip()

def getPlantLocations(app):
    locations = ''
    for cell in app.plants:
        if app.plants[cell] != 'dirt':
            x, y = cell
            locations += f' {x},{y}'
    return locations.strip()

#------------------------------------------Inventory stuff from main
def addToInventory(app, item):
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            if item == app.inventory[row][col]:
                app.inventory[row][col].num += 1
                return
    # otherwise, add new
    row, col = getNextEmptySlot(app)
    app.inventory[row][col] = item

def getNextEmptySlot(app):
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            if app.inventory[row][col] == None:
                return row, col