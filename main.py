from cmu_graphics import *
from mapGeneration import *
from startData import *
from classes import *
from cheatKeys import *
from PIL import Image
import random


def onAppStart(app):
    app.width = 944
    app.height = 656
    app.margin = 30
    app.stepsPerSecond = 10
    app.rows = 7
    app.cols = 10
    app.cellWidth = 100
    app.cellHeight = 100
    app.boardTop = 0
    app.boardLeft = 0
    app.scrollX = 0
# frog :3
    app.frog = Frog(app)
# plants
    app.plants = dict() #positions of all plant cells and species
    app.dirtCells = set() #cellLeft, cellTop of all 'hoed' cells
    app.toolX, app.toolY = 0,0
    app.shovelEquipped = app.wateringCanEquipped = False
    app.selectedItem = None
    app.inventory = [[None, None, None, None, None, None, None], 
                     [None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None]] #start empty 7x7
    
    initBuyItemsList(app)
    initImages(app)
    initButtons(app)

    app.weather = 'sunny'
    app.forestScrollX = app.forestScrollY = 0
    app.goodie = Crop('blueberry')

    loadStartFile(app)

    app.bedroomColor = 'lightBlue'
    app.colors = ['pink', 'gold', 'orange', 'lightGreen', 'lightBlue', 'violet']
    app.bed = Decor('bed4')
    

def initBuyItemsList(app):
    app.cost = 0
    app.buyItemsList = [[Seed('tomato'), Seed('strawberry'), Seed('wheat')], 
                        [Seed('blueberry'), Seed('carrot'), Seed('lettuce')]] #2x3
    for row in range(len(app.buyItemsList)):
        for col in range(len(app.buyItemsList[0])):
            app.buyItemsList[row][col].num = 0

def initImages(app):
    app.startScreen = Image.open("images/home.png")
    app.startWidth, app.startHeight = getNewDims(app.startScreen, 2.5) 
    app.startScreen = CMUImage(app.startScreen)

    app.aboutScreen = Image.open('images/aboutscreen.png')
    app.aboutWidth, app.aboutHeight = getNewDims(app.aboutScreen, 2.5)
    app.aboutScreen = CMUImage(app.aboutScreen)

    app.coin = Image.open('images/money.png')
    app.coinWidth, app.coinHeight = getNewDims(app.coin, 8)
    app.coin = CMUImage(app.coin)

    app.rainSpriteList = []
    rainGif = Image.open('images/rain.png')
    for frame in range(rainGif.n_frames):
        rainGif.seek(frame)
        image = rainGif.resize((rainGif.size[0]//2, rainGif.size[1]//2))
        app.rainSpriteList.append(CMUImage(image))
    
    app.seedImage = Image.open("images/seed.png")
    app.seedImageWidth, app.seedImageHeight = getNewDims(app.seedImage, 5)
    app.seedImage = CMUImage(app.seedImage)

    app.bedroomScreen = Image.open('images/bedroom.png')
    app.bedroomWidth, app.bedroomHeight = getNewDims(app.bedroomScreen, 2.5)
    app.bedroomScreen = CMUImage(app.bedroomScreen)

def initButtons(app):
    app.play = Button('farm')
    app.about = Button('about')
    app.undo = LittleButton('undo')
    app.startButtons = [app.play, app.about]
    app.seeSettings = LittleButton('settings')
    app.seeInventory = LittleButton('inventory')
    app.marketSell = LittleButton('marketSell')
    app.marketBuy = LittleButton('marketBuy')
    app.shovel = LittleButton('shovel')
    app.wateringCan = LittleButton('wateringCan')
    app.farmButtons = [app.seeSettings, app.seeInventory, 
                       app.shovel, app.wateringCan, app.marketSell,
                       app.marketBuy]
    app.buy = Button('buy')
    app.clearCart = LittleButton('clear')
    app.save = Button('save')
    app.paint = LittleButton('paint')
    app.decor = LittleButton('decor')

#------------------------------------------START
def start_redrawAll(app):
    drawImage(app.startScreen, app.width/2, app.height/2, 
              align='center', width=app.startWidth, height=app.startHeight)
    app.play.draw()
    app.about.draw()

def start_onMousePress(app, mouseX, mouseY):
    for button in app.startButtons:
        if button.wasClicked(mouseX, mouseY):
            setActiveScreen(button.task)
            break

def about_redrawAll(app):
    drawImage(app.aboutScreen, app.width/2, app.height/2, 
              align='center', width=app.aboutWidth, height=app.aboutHeight)
    app.undo.draw()

def about_onMousePress(app, mouseX, mouseY):
    if app.undo.wasClicked(mouseX, mouseY):
        setActiveScreen('start')

#------------------------------------------FARM
def farm_redrawAll(app):
    drawBoard(app)
#plants
    drawField(app)
#frog/metrics
    app.frog.draw()
#money
    drawImage(app.coin, 179, 4, width=app.coinWidth, height=app.coinHeight)
    drawLabel(f'{app.money} coins', 258, 31, align='left',size=16)
#buttons
    app.seeSettings.draw()
    app.seeInventory.draw()
    app.wateringCan.draw()
    app.shovel.draw()
    app.marketBuy.draw()
    app.marketSell.draw()
#tools
    drawTools(app)
#weather
    if app.weather == 'rain':
        image = app.rainSpriteList[app.frog.counter % len(app.rainSpriteList)]
        drawImage(image, app.width/2, app.height/2, align='center')

def farm_onMousePress(app, mouseX, mouseY):
    clicked = None
    for button in app.farmButtons:
        if button.wasClicked(mouseX, mouseY):
            clicked = button
            break
    if clicked != None:
        if clicked.task == 'shovel':
            app.shovelEquipped = not app.shovelEquipped
            app.toolX, app.toolY = mouseX, mouseY
        elif clicked.task == 'wateringCan':
            app.wateringCanEquipped = not app.wateringCanEquipped
            app.toolX, app.toolY = mouseX, mouseY
        else:
            app.highlightedCell = None
            app.selectedItem = None
            setActiveScreen(clicked.task)
    elif app.frog.wasClicked(mouseX, mouseY):
        app.frog.showMenu = not app.frog.showMenu
    if app.frog.showMenu:
        for button in app.frog.careButtons:
            if button.wasClicked(mouseX, mouseY):
                app.frog.showMenu = False
                if button.task == 'sleep':
                    updateWeather(app)
                elif button.task == 'eat':
                    app.selectedItem = None
                    app.highlightedCell = None
                setActiveScreen(button.task)
    #digging with shovel
    elif app.shovelEquipped and not app.frog.doneWorking:
        dig(app, mouseX, mouseY)
    #watering the plants
    elif app.wateringCanEquipped and not app.frog.doneWorking:
        water(app, mouseX, mouseY)
    #if not shoveling/watering check if trying to plant/harvest a crop
    #can only plant if frog is near cell
    elif (not app.shovelEquipped and 
        not app.wateringCanEquipped and 
        not app.frog.doneWorking):
        plantSeed(app, mouseX, mouseY)
    
    if app.frog.hunger == 0 or app.frog.sleep == 0:
        app.frog.doneWorking = True

def getCellClicked(app, x, y):
    for cellLeft, cellTop in getAllCellCoords(app):
        if (cellLeft <= x <= cellLeft+app.cellWidth 
            and cellTop <= y <= cellTop+app.cellHeight):
            return (cellLeft, cellTop)

def getAllCellCoords(app):
    cellCoords=set()
    for row in range(app.rows):
        for col in range(app.cols):
            cellCoords.add((getCellLeftTop(app, row, col)))
    return cellCoords

def dig(app, mouseX, mouseY):
    if mouseY < 590: #don't dig when equipping the tool
            clicked = (getCellClicked(app, mouseX, mouseY))
            if clicked != None:
                cellLeft, cellTop = clicked
                cellLeft -= app.scrollX
                if (cellLeft, cellTop) not in app.dirtCells:
                    app.dirtCells.add((cellLeft, cellTop))
                    x, y = cellLeft+app.cellWidth/2, cellTop+app.cellHeight/2
                    app.plants[(x, y)] = 'dirt' #can put something here
                    if len(app.dirtCells) % 5 == 0:
                        app.frog.sleep -= 1
                    if len(app.dirtCells) % 3 == 0:
                        app.frog.hunger -= 1

def plantSeed(app, mouseX, mouseY): #plant or harvest
    cellLeft, cellTop = getCellClicked(app, mouseX, mouseY)
    cellLeft -= app.scrollX
    x, y  = cellLeft+app.cellWidth/2, cellTop+app.cellHeight/2
    if ((x, y) in app.plants and app.frog.nearPlot(app, cellLeft, cellTop)):
        if app.plants[(x, y)] == 'dirt':
            if type(app.selectedItem) == Seed:
                app.plants[(x, y)] = Plant(app.selectedItem.type)
                removeFromInventory(app, app.selectedItem)
                app.selectedItem = None
                if app.weather == 'rain':
                    app.plants[(x,y)].watered = True
        elif app.plants[(x, y)].stage == 'ready!':
            crop = Crop(app.plants[(x, y)].species)
            addToInventory(app, crop)
            app.plants.pop((x, y))
            app.dirtCells.remove((cellLeft, cellTop))
        app.frog.sleep -= 1
        app.frog.hunger -= 1
  
def water(app, mouseX, mouseY):
    cellLeft, cellTop = getCellClicked(app, mouseX, mouseY)
    cellLeft -= app.scrollX
    x, y  = cellLeft+app.cellWidth/2, cellTop+app.cellHeight/2
    if ((x, y) in app.plants and app.frog.nearPlot(app, cellLeft, cellTop) and
        app.plants[(x, y)] != 'dirt' and not app.plants[(x, y)].watered):
        app.plants[(x, y)].watered = True
        app.frog.hunger -= 1
        app.frog.sleep -= 1

def farm_onMouseMove(app, mouseX, mouseY):
    if app.shovelEquipped or app.wateringCanEquipped or app.selectedItem != None:
        app.toolX, app.toolY = mouseX, mouseY

def farm_onKeyPress(app, key):
    if key == 'left' or key == 'right' or key =='up' or key == 'down':
        app.frog.direction = key
        app.frog.isMoving = True 
    elif key == 'h':
        makeAllPlantsHarvestable(app)
    elif key == 'm':
        getLotsOfMoney(app)   

def farm_onKeyRelease(app, key):
    app.frog.isMoving = False

def farm_onStep(app):
    if app.frog.isMoving:
        app.frog.takeStep(app)
        if app.frog.x >= app.width - app.margin:
            scroll(app, 'left')
            app.frog.atRightEdge = True
        else: app.frog.atRightEdge = False
        if app.frog.x <= app.margin:
            scroll(app, 'right')
            app.frog.atLeftEdge = True
        else: app.frog.atLeftEdge = False
    app.frog.counter += 1

    #go to scavanging area
    if 400 <= app.frog.x <= 700 and app.frog.y <= 0:
        forest_createMap(app)
        app.frog.x, app.frog.y = app.width/2, app.height/2
        setActiveScreen('forest')

def scroll(app, direction):
    if app.cols < 20: app.cols +=1
    if direction == 'left':
        app.scrollX -= 10
    elif direction == 'right':
        if app.boardLeft + app.scrollX == 0: return
        app.scrollX +=10
    # for cellLeft, cellTop in copy.copy(app.dirtCells):
    #         newCellLeft = cellLeft + app.scrollX
    #         app.dirtCells.add((newCellLeft, cellTop))
    #         app.dirtCells.remove((cellLeft, cellTop))

#drawing a board (CS Academy: https://academy.cs.cmu.edu/notes/5504)
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
    # "gate" to scavanging area
    drawRect(400, 0, 300, 50, fill='green')
    drawLabel('To Forest', 550, 20, size=16, fill='white')

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    #if cell is crop cell, fill brown, else green
    if (cellLeft-app.scrollX, cellTop) in app.dirtCells:
        fill='brown'
    else: fill='lightGreen'
    drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight,
            fill=fill, border=fill)

def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + app.scrollX + col * app.cellWidth
    cellTop = app.boardTop + row * app.cellHeight
    return (cellLeft, cellTop)

def drawTools(app):
    if app.shovelEquipped:
        image = app.shovel.image
        drawImage(image, app.toolX, app.toolY, 
                  align='center', width=app.shovel.width, 
                  height=app.shovel.height)
        drawRect(app.shovel.x, app.shovel.y, app.shovel.width, app.shovel.height,
                  fill=None, border='green')
    elif app.wateringCanEquipped:
        image = app.wateringCan.image
        drawImage(image, app.toolX, app.toolY, 
                  align='center', width=app.wateringCan.width, 
                  height=app.wateringCan.height)
        drawRect(app.wateringCan.x, app.wateringCan.y, app.wateringCan.width, 
                 app.wateringCan.height, fill=None, border='green')
    elif app.selectedItem != None and type(app.selectedItem) == Seed:
        drawImage(app.seedImage, app.toolX, app.toolY, align='center', 
                width=app.seedImageWidth, height=app.seedImageHeight)

def drawField(app):
    for cell in app.plants:
        x, y = cell
        x += app.scrollX
        if app.plants[cell] == 'dirt':
            if app.frog.nearPlot(app, x, y):
                drawLabel('Plant Here', x, y)
        else:
            app.plants[cell].draw(app, x, y)

#------------------------------------------Settings
def settings_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='lightGreen', border=None)
    app.undo.draw()
    app.save.draw()

def settings_onMousePress(app, mouseX, mouseY):
    if app.save.wasClicked(mouseX, mouseY):
        saveData(app)
    elif app.undo.wasClicked(mouseX, mouseY):
        setActiveScreen('farm')

#------------------------------------------Inventory
def inventory_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='green')
    drawRect(40, 40, app.width-80, app.height-80, fill='white')
    drawLabel("Your Stuff:", app.width/2, 20, fill='white', size=20)
    app.undo.draw()
    # app.seeInventory.draw()
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            drawInventoryCell(app, row, col)

def drawInventoryCell(app, row, col):
    cellLeft, cellTop = getInventoryCellLeftTop(app, row, col)
    if (row, col) == app.highlightedCell:
        drawRect(cellLeft, cellTop, 100, 75, fill='green',
                 align='left', border=None, opacity=40)
    if app.inventory[row][col] != None:
        app.inventory[row][col].draw(app, cellLeft, cellTop)
        drawRect(cellLeft, cellTop, 100, 75, fill=None, align='left', 
                 border=app.inventory[row][col].border)

def getInventoryCellLeftTop(app, row, col):
    cellLeft = 100 + col * 100
    cellTop = 100 + row * 100
    return cellLeft, cellTop

def inventory_onMousePress(app, mouseX, mouseY):
    selected = getSelectedItem(app, mouseX, mouseY)
    if selected != None:
        app.selectedItem, row, col = selected
    elif app.undo.wasClicked(mouseX, mouseY):
        setActiveScreen('farm')

def inventory_onMouseMove(app, mouseX, mouseY):
    app.highlightedCell = (getHoveringOverCell(app, mouseX, mouseY))

def getHoveringOverCell(app, x, y):
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            left, top = getInventoryCellLeftTop(app, row, col)
            if (left <= x <= left + 100 and
                top <= y <= top + 100):
                return row, col

def getSelectedItem(app, x, y):
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            left, top = getInventoryCellLeftTop(app, row, col)
            if (left <= x <= left + 100 and
                top <= y <= top + 100):
                return app.inventory[row][col], row, col

def addToInventory(app, item):
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            if item == app.inventory[row][col]:
                app.inventory[row][col].num += 1
                return
    # otherwise, add new
    row, col = getNextEmptySlot(app)
    app.inventory[row][col] = item

def removeFromInventory(app, item):
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            if item == app.inventory[row][col]:
                if app.inventory[row][col].num == 1:
                    app.inventory[row][col] = None
                else: app.inventory[row][col].num -=1
                return

def getNextEmptySlot(app):
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            if app.inventory[row][col] == None:
                return row, col

#------------------------------------------Bedroom
def sleep_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.bedroomColor)
    drawLabel(f"Tomorrow's weather is...{app.weather}!", 
              app.width/2, 20, size=20)
    drawImage(app.bedroomScreen, 0, 0, width=app.bedroomWidth, height=app.bedroomHeight)
    app.undo.draw()
    app.paint.draw()
    app.decor.draw()
    app.bed.draw()

def sleep_onMousePress(app, mouseX, mouseY):
    if app.undo.wasClicked(mouseX, mouseY):
        app.frog.bedtime()
        updatePlants(app)
        app.day += 1
        setActiveScreen('farm')
    elif app.paint.wasClicked(mouseX, mouseY):
        changeWallColor(app)

def updateWeather(app):
    num = random.randint(0,10)
    if 0 <= num <= 3:
        weather = 'rain'
    else:
        weather = 'sunny'
    app.weather = weather

def updatePlants(app):
    for cell in app.plants:
        if app.plants[cell] != 'dirt' and app.plants[cell].watered:
            app.plants[cell].grow()
            if app.weather == 'rain':
                app.plants[cell].watered = True
            else: app.plants[cell].watered = False

def changeWallColor(app):
    i = random.randint(0,5)
    app.bedroomColor = app.colors[i]

#------------------------------------------EAT
def eat_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='pink')
    drawRect(40, 40, app.width-80, app.height-80, fill='white')
    app.undo.draw()
    drawLabel('Click on something to eat!', app.width/2, 20, size=16)

    drawLabel("Hunger: ", 20, 636, align='left', size=14)
    drawRect(75, 636, app.frog.hunger*10, 10, fill='orange', border=None,
                align='left')
    drawRect(75, 636, 200, 10, fill=None, border='black',align='left')
    
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            drawInventoryCell(app, row, col)

def eat_onMousePress(app, mouseX, mouseY):
    app.selectedItem = None
    selected = getSelectedItem(app, mouseX, mouseY)
    if selected != None:
        selected, row, col = getSelectedItem(app, mouseX, mouseY)
        if type(selected) == Crop:
            if app.inventory[row][col].num == 1:
                app.inventory[row][col] = None
            else: app.inventory[row][col].num -=1
            app.frog.eat()
    elif app.undo.wasClicked(mouseX, mouseY):
        setActiveScreen('farm')

def eat_onMouseMove(app, mouseX, mouseY):
    app.highlightedCell = (getHoveringOverCell(app, mouseX, mouseY))

#------------------------------------------SCAVANGING
def forest_redrawAll(app):
    drawMap(app)
    app.undo.draw()
    app.frog.draw()

def drawMap(app):
    for row in range(len(app.forestMap)):
        for col in range(len(app.forestMap[0])):
            if 0 <= app.forestMap[row][col] <= 10:
                fill='lightGreen'
            elif app.forestMap[row][col] == -1:
                fill='brown'
            else: fill='green'
            drawForestCell(app, row, col, fill)

def drawForestCell(app, row, col, fill):
    cellLeft, cellTop = getForestCellLeftTop(app, row, col)
    drawRect(cellLeft, cellTop, 100, 100, 
             fill=fill, border=fill, align='left')
    if app.forestMap[row][col] == app.randomValue:
        #this is the random value used to initialize the map board
        #so it shouldn't appear too frequently
        app.goodie.draw(app, cellLeft, cellTop)
        drawRect(cellLeft, cellTop+75, 100, 75, fill=fill, align='left')

def getForestCellLeftTop(app, row, col):
    cellLeft = app.forestScrollX + col * app.cellWidth
    cellTop = app.forestScrollY + row * app.cellHeight
    return (cellLeft, cellTop)

def forest_onMousePress(app, mouseX, mouseY):
    if app.undo.wasClicked(mouseX, mouseY):
        app.frog.x, app.frog.y = app.width/2, app.height/2
        app.frog.isMoving = False
        setActiveScreen('farm')
    else:
        row, col = getCurrCell(app, mouseX, mouseY)
        cellLeft, cellTop = getForestCellLeftTop(app, row, col)
        if (app.forestMap[row][col] == app.randomValue and 
            app.frog.nearPlot(app, cellLeft, cellTop)):
            addToInventory(app, app.goodie)
            app.forestMap[row][col] = -1

def forest_onKeyPress(app, key):
    if key == 'left' or key == 'right' or key =='up' or key == 'down':
        app.frog.direction = key
        app.frog.isMoving = True    

def forest_onKeyRelease(app, key):
    app.frog.isMoving = False

def forest_onStep(app):
    if app.frog.isMoving and frogNotInTrees(app):
        app.frog.takeStep(app)
        if app.frog.x >= app.width - app.margin:
            scrollForest(app, 'left')
            app.frog.atRightEdge = True
        else: app.frog.atRightEdge = False
        if app.frog.x <= app.margin:
            scrollForest(app, 'right')
            app.frog.atLeftEdge = True
        else: app.frog.atLeftEdge = False
        if app.frog.y >= app.height - app.margin:
            scrollForest(app, 'up')
            app.frog.atBottomEdge = True
        else: app.frog.atBottomEdge = False
    app.frog.counter +=1

def scrollForest(app, direction):
    if direction == 'left':
        app.forestScrollX -= 10
    elif direction == 'right':
        app.forestScrollX += 10
    elif direction == 'up':
        app.forestScrollY -= 10


def frogNotInTrees(app): # "Trees" = dark green cells
    if app.frog.direction == 'up':
        #don't go off edge
        if getCurrCell(app, app.frog.x, app.frog.y-18) == None: 
            return False
        row, col = getCurrCell(app, app.frog.x, app.frog.y-18)
    elif app.frog.direction == 'down':
        if getCurrCell(app, app.frog.x, app.frog.y+98) == None: 
            return False
        row, col = getCurrCell(app, app.frog.x, app.frog.y+98)
    elif app.frog.direction == 'left':
        if getCurrCell(app, app.frog.x-68, app.frog.y) == None: 
            return False
        row, col = getCurrCell(app, app.frog.x-68, app.frog.y)
    elif app.frog.direction == 'right':
        if getCurrCell(app, app.frog.x+68, app.frog.y) == None: 
            return False
        row, col = getCurrCell(app, app.frog.x+68, app.frog.y)
    
    if (0 <= row < len(app.forestMap) and 
    0 <= col < len(app.forestMap[0]) and 
    app.forestMap[row][col] <= 10):
        return True
    else: return False

def getCurrCell(app, x, y):
    for row in range(len(app.forestMap)):
        for col in range(len(app.forestMap[0])):
            cellLeft, cellTop = getForestCellLeftTop(app, row, col)
            if (cellLeft <= x <= cellLeft + 100 and 
                cellTop <= y <= cellTop + 100):
                    return row, col

def getNextCell(app, x, y):
    currRow, currCol = getCurrCell(app, x, y)
    if app.frog.direction == 'up':
        dx, dy = 0, -1
    elif app.frog.direction == 'down':
        dx, dy = 0, 1
    elif app.frog.direction == 'left':
        dx, dy = -1, 0
    elif app.frog.direction == 'right':
        dx, dy = 1, 0
    return currRow+dy, currCol+dx

#------------------------------------------MARKET
def marketSell_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='gold')
    drawRect(40, 40, app.width-80, app.height-80, fill='white')
    app.undo.draw()
    drawImage(app.coin, app.width-280, 5, width=app.coinWidth, height=app.coinHeight)
    drawLabel(f'You have {app.money} frog coins!', app.width-200, 30, align='left',
              size=16)
    drawLabel('Click to sell!', app.width/2, 20, size=20)
    for row in range(len(app.inventory)):
        for col in range(len(app.inventory[0])):
            drawInventoryCell(app, row, col)
                
def marketSell_onMousePress(app, mouseX, mouseY):
    if app.undo.wasClicked(mouseX, mouseY):
        setActiveScreen('farm')
    else:
        app.selectedItem = None
        selected = getSelectedItem(app, mouseX, mouseY)
        if selected != None:
            selected, row, col = getSelectedItem(app, mouseX, mouseY)
            if (app.inventory[row][col] != None and 
                type(app.inventory[row][col]) == Crop):
                if app.inventory[row][col].num == 1:
                    app.inventory[row][col] = None
                else:
                    app.inventory[row][col].num -= 1
                app.money += 10

def marketSell_onMouseMove(app, mouseX, mouseY):
    app.highlightedCell = (getHoveringOverCell(app, mouseX, mouseY))

#------------------------------------------BUY
def marketBuy_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='gold')
    drawRect(40, 40, app.width-80, app.height-80, fill='white')
    drawLabel("Click to buy!", app.width/2, 20, size=20)
    drawImage(app.coin, app.width-280, 5, width=app.coinWidth, height=app.coinHeight)
    drawLabel(f'You have {app.money} frog coins!', app.width-200, 30, align='left',
              size=16)
    drawLabel(f'Total Cost = {app.cost}', 200, 300, size=16, bold=True, align='left')
    if app.money-app.cost < 0:
        drawLabel("You can't afford this :(", app.width/2, app.height-20, size=20)
    else: app.buy.draw()
    app.undo.draw()
    app.clearCart.draw()
    for row in range(len(app.buyItemsList)):
        for col in range(len(app.buyItemsList[0])):
            drawBuyCell(app, row, col)

def drawBuyCell(app, row, col):
    cellLeft, cellTop = getBuyCellLeftTop(app, row, col)
    if (row, col) == app.highlightedCell:
        drawRect(cellLeft, cellTop, 100, 75, fill='green',
                 align='left', border=None, opacity=40)
    app.buyItemsList[row][col].draw(app, cellLeft, cellTop)
    drawRect(cellLeft, cellTop, 100, 75, fill=None, align='left')

def getBuyCellLeftTop(app, row, col):
    cellLeft = 325 + col * 100
    cellTop = 100 + row * 100
    return cellLeft, cellTop

def marketBuy_onMousePress(app, mouseX, mouseY):
    if app.undo.wasClicked(mouseX, mouseY):
        initBuyItemsList(app)
        setActiveScreen('farm')
    elif app.clearCart.wasClicked(mouseX, mouseY):
        initBuyItemsList(app)
    elif app.buy.wasClicked(mouseX, mouseY) and not (app.money - app.cost < 0):
        app.money -= app.cost
        for row in range(len(app.buyItemsList)):
            for col in range(len(app.buyItemsList[0])):
                item = app.buyItemsList[row][col]
                if item.num > 0:
                    addToInventory(app, item)
        initBuyItemsList(app)
    elif app.money > 0: 
        selected = getSelectedSeed(app, mouseX, mouseY)
        if selected != None:
            item, row, col = getSelectedSeed(app, mouseX, mouseY)
            app.buyItemsList[row][col].num += 1
            app.cost += 10

def getSelectedSeed(app, x, y):
    for row in range(len(app.buyItemsList)):
        for col in range(len(app.buyItemsList[0])):
            left, top = getBuyCellLeftTop(app, row, col)
            if (left <= x <= left + 100 and
                top <= y <= top + 100):
                return app.buyItemsList[row][col], row, col

def marketBuy_onMouseMove(app, mouseX, mouseY):
    app.highlightedCell = (getCell(app, mouseX, mouseY))

def getCell(app, x, y):
    for row in range(len(app.buyItemsList)):
        for col in range(len(app.buyItemsList[0])):
            left, top = getBuyCellLeftTop(app, row, col)
            if (left <= x <= left + 100 and
                top <= y <= top + 100):
                return row, col


def main():
    runAppWithScreens(initialScreen='start')

main()