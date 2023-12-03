def readStartFile(app):
    i = 1
    #1 day
    #2 frog hunger
    #3 frog sleep
    #4 money
    #5 inventory list
    #6 num in inventory
    #7 dirt cells
    #8 plants
    #9 plants days alive
    #10 plants location
    with open('data.csv', 'r') as file:
        data = file.read()
    # print(data)
    for line in data.splitlines():
        if i == 1:
            app.day = int(line)
        elif i == 2:
            app.frog.hunger = int(line)
        elif i == 3:
            app.frog.sleep = int(line)
        elif i == 4:
            app.money = int(line)
        elif i == 5:
            editInventory(app, line)
        elif i == 6:
            editInventoryNums(app, line)
        elif i == 7:
            editDirtCells(app, line)
        elif i == 8:
            plantsString = line
        elif i == 9:
            
        i +=1

         
def saveData(app):
    #in order of lines:
    inventoryItems = getInventoryItems(app)
    numInventoryItems = getInventoryNums(app)
    dirtCells = getDirtCells(app)
    plants = getPlants(app)
    plantsDays = getPlantDays(app)
    plantsLocations = getPlantLocations(app)
    with open('data.csv', 'w') as file:
        file.write(f"{app.day}\n{app.frog.hunger}\n{app.frog.sleep}\n{app.money}\n{inventoryItems}\n{numInventoryItems}\n{dirtCells}\n{plants}\n{plantsDays}\n{plantsLocations}") #this rewrites the entire thing

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


