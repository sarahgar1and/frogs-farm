from cmu_graphics import *
from PIL import Image
from mapGeneration import forest_createMap


class Frog:
    def __init__(self, app):
    # metrics: 20/20 is the maximum
        self.hunger = 20
        self.sleep = 20
        self.counter = 0
        self.careButtons = [LittleButton('eat'), LittleButton('sleep')]

        self.isMoving=self.doneWorking=self.atRightEdge=self.atLeftEdge=False
        self.showMenu = False
        self.x = app.width/2
        self.y = app.height/2
        self.dx = 12
        self.dy = 12

    # images/sprites:
        self.standing = Image.open("images/standing.png")
        self.width, self.height = getNewDims(self.standing, 6)
        self.standing = CMUImage(self.standing)

        walkingLeftSpriteList = [] # (From lecture demo)
        walkingRightSpriteList = []
        walkingPng = Image.open("images/walking.png")
        for frame in range(walkingPng.n_frames):
            walkingPng.seek(frame)
            image = walkingPng.resize((walkingPng.size[0], walkingPng.size[1]))
            walkingLeftSpriteList.append(CMUImage(image))
            walkingRightSpriteList.append(CMUImage(image.transpose(Image.FLIP_LEFT_RIGHT)))
        self.walkingLeft = walkingLeftSpriteList
        self.walkingRight = walkingRightSpriteList

        blinkingSpriteList = []
        blinkingPng = Image.open('images/blinking.png')
        for frame in range(blinkingPng.n_frames):
            blinkingPng.seek(frame)
            image = blinkingPng.resize((blinkingPng.size[0], blinkingPng.size[1]))
            blinkingSpriteList.append(CMUImage(image))
        self.blinking = blinkingSpriteList

    def takeStep(self, app):
        if self.direction == 'left' and not self.atLeftEdge:
            self.x -= self.dx
        elif self.direction == 'right' and not self.atRightEdge:
            self. x += self.dx
        elif self.direction == 'up' and self.y > 0:
            self. y -= self.dy
        elif self.direction == 'down' and self.y < app.height:
            self. y += self.dy
    
    def draw(self):
        i = self.counter
        if self.isMoving:
            if self.direction == 'right':
                walkingList = self.walkingRight
            else: walkingList = self.walkingLeft
            image = walkingList[i % len(walkingList)]
            drawImage(image, self.x, self.y,align='center',
                    width=self.width,height=self.height)
        else:
            image = self.blinking[i % len(self.blinking)]
            drawImage(image, self.x, self.y,align='center',
                    width=self.width, height=self.height)
        drawLabel(f'Sleep:{self.sleep} Hunger:{self.hunger}', 
                  20, 20, size=16, align='left')
        if self.doneWorking:
            drawLabel('I need some care!', self.x, 
                      self.y-75, size=16)
        if self.showMenu:
            self.careButtons[0].x =self.careButtons[1].x =self.x + 50
            self.careButtons[0].y = self.y
            self.careButtons[1].y = self.y - 50
            for button in self.careButtons:
                button.draw()

    def nearPlot(self, app, cellLeft, cellTop):
        if (cellLeft-50 <= self.x <= cellLeft+app.cellWidth+20 and
        cellTop-50 <= self.y <= cellTop+app.cellHeight+20):
            return True
        return False

    def wasClicked(self, x, y):
        if (self.x - self.width/2 <= x <= self.x + self.width/2 and 
            self.y - self.height/2 <= y <= self.y +self.height/2):
            return True
        return False

    def bedtime(self, app):
        self.sleep = 20
        app.day += 1
        for cell in app.plants:
            if app.plants[cell] != 'dirt' and app.plants[cell].watered:
                app.plants[cell].grow()
                app.plants[cell].watered = False

    def eat(self):
        if self.hunger + 3 > 20:
            self.hunger = 20
        else: self.hunger += 3
            
class Plant:
    harvestTimes = {'tomato': 4, 
                    'strawberry': 5,
                    'wheat': 4,
                    'blueberry': 6,
                    'carrot': 4,
                    'lettuce': 5}
    plantImages = {'tomato-1': CMUImage(Image.open('images/tomato.png')),
                   'strawberry-1': CMUImage(Image.open('images/strawberry.png')),
                   'wheat-1': CMUImage(Image.open('images/wheat.png')),
                   'blueberry-1': CMUImage(Image.open('images/blueberry.png')),
                   'carrot-1': CMUImage(Image.open('images/carrot.png')),
                   'lettuce-1':CMUImage(Image.open('images/lettuce.png')),
                   'tomato-0': CMUImage(Image.open('images/baby_fruit.png')),
                   'strawberry-0': CMUImage(Image.open('images/baby_fruit.png')),
                   'wheat-0': CMUImage(Image.open('images/baby_wheat.png')),
                   'blueberry-0': CMUImage(Image.open('images/baby_berry.png')),
                   'carrot-0': CMUImage(Image.open('images/baby_leaves.png')),
                   'lettuce-0': CMUImage(Image.open('images/baby_leaves.png'))}
    saplingImage = CMUImage(Image.open("images/sapling.png"))
    def __init__(self, species):
        self.species = species
    # 4 stages: seed, baby, adolescent, adult  
        self.stage = 'seed' 
        self.image = Image.open("images/seed.png")
        self.width, self.height = getNewDims(self.image, 5)
        self.image = CMUImage(self.image)
    # harvestable once daysTillHarvest == harvestTime
        self.days = 0 
        self.watered = False

    def grow(self): #call when for watered plants when sleep!!
        self.days += 1
        if self.days == Plant.harvestTimes[self.species]:
            self.stage = 'ready!'
        elif self.days == 1:
            self.image = Plant.saplingImage
        elif self.days == 2:
            self.image = Plant.plantImages[f'{self.species}-0']
        elif self.days == 4: # spend 2 days as an adolescent
            self.image = Plant.plantImages[f'{self.species}-1']
    
    def draw(self,app, x, y):
        drawImage(self.image, x, y, align='center',
                  width=self.width, height=self.height)
        if not self.watered and self.stage != 'ready!':
            drawLabel("I'm thirsty!", x, y+20, size=16, fill='lightBlue')
        elif self.stage == 'ready!':
            drawLabel("Harvest me!", x, y+20, size=16, fill='yellow')
            
class Button:
    buttonImages = {'farm': Image.open("images/play.png"),
                    'about': Image.open("images/about.png"),
                    'undo': Image.open('images/return.png'),
                    'shovel': Image.open('images/shovel.png'),
                    'wateringCan': Image.open('images/watering_can.png'),
                    'settings': Image.open('images/settings.png'),
                    'inventory': Image.open('images/inventory.png'),
                    'eat': Image.open('images/eat.png'),
                    'sleep': Image.open('images/sleep.png')}
    buttonPos = {'farm': (175, 200),
                 'about': (175,300),
                 'undo': (0,5),
                 'shovel': (472, 590),
                 'wateringCan': (402, 590),
                 'settings': (874, 5),
                 'inventory': (804, 5),
                 'eat': (None, None),
                 'sleep': (None, None)}
    def __init__(self, task):
        self.task = task
        self.image = Button.buttonImages[task]
        self.width, self.height = getNewDims(self.image, 6)
        self.image = CMUImage(self.image)
        self.x, self.y = Button.buttonPos[task]
    
    def __repr__(self):
        return f'{self.task}'

    def draw(self): #For big letter buttons
        drawImage(self.image, self.x, self.y,
                  width=self.width, height=self.height) # don't align center
        
    def wasClicked(self, mx, my):
        if (self.x, self.y) == (None, None): return
        if (self.x < mx < (self.x + self.width) 
            and self.y < my < (self.y + self.height)):
            return True
        return False

class LittleButton(Button):
    def __init__(self, task):
        super().__init__(task)
        self.image = Button.buttonImages[task]
        self.width, self.height = getNewDims(self.image, 8)
        self.image = CMUImage(self.image)
    
    def draw(self):
        drawImage(self.image, self.x, self.y,
                  width=self.width, height=self.height)

class Item: #stuff in inventory
    def __init__(self, thing):
        self.type = thing
        self.num = 1
        self.image = Image.open('images/seed.png')
        self.width, self.height = getNewDims(self.image, 8)

    def __repr__(self):
        return f'{self.type}'

class Crop(Item):
    def __init__(self, thing):
        super().__init__(thing)
        self.image = Plant.plantImages[(f'{self.type}-1')]

    def draw(self, app, x, y):
        drawImage(self.image, x, y, width=self.width, height=self.height)
        drawLabel(f'{self.type}  x{self.num}', 
                  x+self.width*2, y+self.height/2, align='left', size=16)
        if self == app.selectedItem:
            border = 'green'
        else: border = None
        drawRect(x, y, self.width, self.height, fill=None, border=border)

class Seed(Item):
    def __init__(self, thing):
        super().__init__(thing)
        self.image = CMUImage(self.image)

    def draw(self, app, x, y):
        drawImage(self.image, x, y, width=self.width, height=self.height)
        drawLabel(f'{self.type} seeds  x{self.num}', 
                  x+self.width*2, y+self.height/2, align='left', size=16)
        if self == app.selectedItem:
            border = 'green'
        else: border = None
        drawRect(x, y, self.width, self.height, fill=None, border=border)


#------------------------------------------
def getNewDims(image, factor):
    width,height = image.width, image.height
    return width/factor, height/factor 

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
    app.day = 0
# plants
    app.plants = dict() #positions of all plant cells and species
    app.dirtCells = set() #cellLeft, cellTop of all 'hoed' cells
# buttons
    app.play = Button('farm')
    app.about = Button('about')
    app.undo = LittleButton('undo')
    app.startButtons = [app.play, app.about]
    app.seeSettings = LittleButton('settings')
    app.seeInventory = LittleButton('inventory')
    app.shovel = LittleButton('shovel')
    app.wateringCan = LittleButton('wateringCan')
    app.farmButtons = [app.seeSettings, app.seeInventory, 
                       app.shovel, app.wateringCan]
    
    app.shovelEquipped = app.wateringCanEquipped = False
    app.selectedItem = None
    app.inventory = [Crop('strawberry'), Crop('tomato'), 
                     Seed('wheat')] #start empty
    app.forestSize = 9
#images
    app.startScreen = Image.open("images/home.png")
    app.startWidth, app.startHeight = getNewDims(app.startScreen, 2.5) 
    app.startScreen = CMUImage(app.startScreen)

    app.aboutScreen = Image.open('images/aboutscreen.png')
    app.aboutWidth, app.aboutHeight = getNewDims(app.aboutScreen, 2.5)
    app.aboutScreen = CMUImage(app.aboutScreen)

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
#buttons
    app.seeSettings.draw()
    app.seeInventory.draw()
    app.wateringCan.draw()
    app.shovel.draw()
#tools
    drawTools(app)

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
        elif clicked.task == 'settings':
            setActiveScreen('settings')
        elif clicked.task == 'inventory':
            setActiveScreen('inventory')
    elif app.frog.wasClicked(mouseX, mouseY):
        app.frog.showMenu = not app.frog.showMenu
    if app.frog.showMenu:
        for button in app.frog.careButtons:
            if button.wasClicked(mouseX, mouseY):
                app.frog.showMenu = False
                setActiveScreen(button.task)
    #digging with shovel
    if app.shovelEquipped and not app.frog.doneWorking:
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
                if (cellLeft, cellTop) not in app.dirtCells:
                    app.dirtCells.add((cellLeft, cellTop))
                    x, y = cellLeft+app.cellWidth/2, cellTop+app.cellHeight/2
                    app.plants[(x, y)] = 'dirt' #can put something here
                    if len(app.dirtCells) % 5 == 0:
                        app.frog.sleep -= 1
                    if len(app.dirtCells) % 3 == 0:
                        app.frog.hunger -= 1

def plantSeed(app, mouseX, mouseY):
    cellLeft, cellTop = getCellClicked(app, mouseX, mouseY)
    x, y  = cellLeft+app.cellWidth/2, cellTop+app.cellHeight/2
    if ((x, y) in app.plants and app.frog.nearPlot(app, cellLeft, cellTop)):
        if app.plants[(x, y)] == 'dirt':
            setActiveScreen('inventory')
            if type(app.selectedItem) == Seed:
                seed = app.selectedItem
                app.plants[(x, y)] = Plant(seed.type)
        elif app.plants[(x, y)].stage == 'ready':
            crop = Crop(app.plants[(x, y)].type)
            app.inventory.append(crop)
            app.plants.pop((x, y))
    
def water(app, mouseX, mouseY):
    cellLeft, cellTop = getCellClicked(app, mouseX, mouseY)
    x, y  = cellLeft+app.cellWidth/2, cellTop+app.cellHeight/2
    if ((x, y) in app.plants and 
        cellLeft-50 <= app.frog.x <= cellLeft+app.cellWidth+20 and
        cellTop-50 <= app.frog.y <= cellTop+app.cellHeight+20 and
        app.plants[(x, y)] != 'dirt' and not app.plants[(x, y)].watered):
        app.plants[(x, y)].watered = True

def farm_onMouseMove(app, mouseX, mouseY):
    if app.shovelEquipped or app.wateringCanEquipped:
        app.toolX, app.toolY = mouseX, mouseY

def farm_onKeyPress(app, key):
    if key == 'left' or key == 'right' or key =='up' or key == 'down':
        app.frog.direction = key
        app.frog.isMoving = True    

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

#------------------------------------------Drawing a Board (CS Academy)
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

def drawField(app):
    for cell in app.plants:
        x, y = cell
        x += app.scrollX
        if app.plants[cell] == 'dirt':
            if (x-100 <= app.frog.x <= x+100 and
            y-100 <= app.frog.y <= y+100):
                drawLabel('Plant Here', x, y)
        else:
            app.plants[cell].draw(app, x, y)

#------------------------------------------Settings
def settings_redrawAll(app):
    pass

#------------------------------------------Inventory
def inventory_redrawAll(app):
    app.undo.draw()
    for i in range(len(app.inventory)):
        app.inventory[i].draw(app, app.width/2-80, 80+80*i)

def inventory_onMousePress(app, mouseX, mouseY):
    selected = getSelectedItem(app, mouseX, mouseY)
    if selected != None:
        app.selectedItem = selected
    if app.undo.wasClicked(mouseX, mouseY):
        setActiveScreen('farm')
    
def getSelectedItem(app, x, y):
   xCoord = app.width/2-80
   for i in range(len(app.inventory)):
       yCoord = 80+80*i
       if (xCoord <= x <= app.inventory[i].width+xCoord and 
           yCoord <= y <= app.inventory[i].height+yCoord):
           return app.inventory[i]

#------------------------------------------SLEEP
def sleep_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='lightBlue')
    drawLabel('zZzzZzz...', app.width/2, app.height/2, size=20)
    app.undo.draw()

def sleep_onMousePress(app, mouseX, mouseY):
    if app.undo.wasClicked(mouseX, mouseY):
        app.frog.bedtime(app)
        setActiveScreen('farm')

#------------------------------------------EAT
def eat_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='pink')
    drawRect(40, 40, app.width-80, app.height-80, fill='white')
    app.undo.draw()
    drawLabel('Click on something to eat!', app.width/2, 20, size=16)
    drawLabel(f'Hunger: {app.frog.hunger}', 90, 20, size=16, align='left')
    for i in range(len(app.inventory)):
        app.inventory[i].draw(app, app.width/2-80, 80+80*i)

def eat_onMousePress(app, mouseX, mouseY):
    selected = getSelectedItem(app, mouseX, mouseY)
    if selected != None:
        if type(selected) == Crop:
            i = app.inventory.index(selected)
            app.inventory.pop(i)
            app.frog.eat()
    elif app.undo.wasClicked(mouseX, mouseY):
        setActiveScreen('farm')

#------------------------------------------SCAVANGING
def forest_redrawAll(app):
    drawMap(app)
    app.undo.draw()

def drawMap(app):
    pass

def forest_onMousePress(app, mouseX, mouseY):
    if app.undo.wasClicked(mouseX, mouseY):
        app.frog.x, app.frog.y = app.width/2, app.height/2
        app.frog.isMoving = False
        setActiveScreen('farm')

#------------------------------------------
def main():
    runAppWithScreens(initialScreen='start')

main()