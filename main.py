from cmu_graphics import *
from PIL import Image
import copy

class Frog:
    def __init__(self, app):
    # metrics: 10/10 is the maximum
        self.mood = 10
        self.hunger = 10
        self.sleep = 10

        self.isMoving = self.atRightEdge = self.atLeftEdge = False
        self.x = app.width/2
        self.y = app.height/2
        self.dx = 10
        self.dy = 10

    # images/sprites:
        self.standing = Image.open("images/standing.png")

        walkingSpriteList = [] # (From lecture demo)
        walkingPng = Image.open("images/walking.png")
        for frame in range(walkingPng.n_frames):
            walkingPng.seek(frame)
            image = walkingPng.resize((walkingPng.size[0], walkingPng.size[1]))
            walkingSpriteList.append(image)
        self.walking = walkingSpriteList

        blinkingSpriteList = []
        blinkingPng = Image.open('images/blinking.png')
        for frame in range(blinkingPng.n_frames):
            blinkingPng.seek(frame)
            image = blinkingPng.resize((blinkingPng.size[0], blinkingPng.size[1]))
            blinkingSpriteList.append(image)
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
            image = self.walking[i % len(self.walking)]
            if self.direction == 'right':
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            newWidth, newHeight = getNewDims(image, 6)
            image = CMUImage(image)
            drawImage(image, self.x, self.y,align='center',
                    width=newWidth,height=newHeight)
        else:
            image = self.blinking[i % len(self.blinking)]
            newWidth, newHeight = getNewDims(image, 6)
            image = CMUImage(image)
            drawImage(image, self.x, self.y,align='center',
                    width=newWidth, height=newHeight)
            
class Plant:
    harvestTimes = {'tomato': 3, 
                    'strawberry': 4,
                    'wheat': 3,
                    'blueberry': 5,
                    'carrot': 3,
                    'lettuce': 4}
    plantImages = {'tomato-1': Image.open('images/tomato.png'),
                   'strawberry-1': Image.open('images/strawberry.png'),
                   'wheat-1': Image.open('images/wheat.png'),
                   'blueberry-1': Image.open('images/blueberry.png'),
                   'carrot-1': Image.open('images/carrot.png'),
                   'lettuce-1': Image.open('images/lettuce.png'),
                   'tomato-0': Image.open('images/baby_fruit.png'),
                   'strawberry-0': Image.open('images/baby_fruit.png'),
                   'wheat-0': Image.open('images/baby_wheat.png'),
                   'blueberry-0': Image.open('images/baby_berry.png'),
                   'carrot-0': Image.open('images/baby_leaves.png'),
                   'lettuce-0': Image.open('images/baby_leaves.png')}
    def __init__(self, species):
        self.species = species
    # 4 stages: seed, baby, adolescent, adult  
        self.stage = 'seed' 
        self.image = Image.open("images/seed.png")
    # harvestable once daysTillHarvest == harvestTime
        self.days = 0 

    def grow(self): # call when watered!!
        self.days += 1
        if self.days == Plant.harvestTimes[self.species]:
            self.stage = 'ready!'
        if self.days == 1:
            self.image = Image.open("images/sapling.png")
        elif self.days == 2:
            self.image = Plant.plantImages[f'{self.species}-0']
        elif self.days == 4: # spend 2 days as an adolescent
            self.image = Plant.plantImages[f'{self.species}-1']
    
    def draw(self):
        image = CMUImage(self.image)
        self.width, self.height = getNewDims(self.image, 6)
        drawImage(image, self.x, self.y, align='center',
                  width=self.width, height=self.height)
            

class Button:
    buttonImages = {'farm': Image.open("images/play.png"),
                    'about': Image.open("images/about.png"),
                    'undo': Image.open('images/return.png'),
                    'shovel': Image.open('images/shovel.png'),
                    'wateringCan': Image.open('images/watering_can.png'),
                    'settings': Image.open('images/settings.png'),
                    'inventory': Image.open('images/inventory.png')}
    buttonPos = {'farm': (175, 200),
                 'about': (175,300),
                 'undo': (0,5),
                 'shovel': (472, 590),
                 'wateringCan': (402, 590),
                 'settings': (874, 5),
                 'inventory': (804, 5)}
    def __init__(self, task):
        self.task = task
        self.image = Button.buttonImages[task]
        self.x, self.y = Button.buttonPos[task]
    
    def __repr__(self):
        return f'{self.task}'

    def draw(self): #For big letter buttons
        image = self.image
        self.width, self.height = getNewDims(image, 6)
        image = CMUImage(image)
        drawImage(image, self.x, self.y,
                  width=self.width, height=self.height) # don't align center
        
    def wasClicked(self, mx, my):
        if (self.x < mx < (self.x + self.width) 
            and self.y < my < (self.y + self.height)):
            return True
        return False

class LittleButton(Button):
    def __init__(self, task):
        super().__init__(task)
    
    def draw(self):
        image = self.image
        self.width, self.height = getNewDims(image, 8)
        image = CMUImage(image)
        drawImage(image, self.x, self.y,
                  width=self.width, height=self.height)

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
    app.cellCoords = set()

    for row in range(app.rows):
        for col in range(app.cols):
            app.cellCoords.add((getCellLeftTop(app, row, col)))
# frog :3
    app.frog = Frog(app)
    app.frog.counter = 0
# plants
    app.plantsList = []
    app.dirtCells = set()
# buttons
    app.play = Button('farm')
    app.about = Button('about')
    app.undo = LittleButton('undo')
    app.startButtons = [app.play, app.about]
    app.seeSettings = LittleButton('settings')
    app.seeInventory = LittleButton('inventory')
    app.shovel = LittleButton('shovel')
    app.wateringCan = LittleButton('wateringCan')
    app.farmButtons = [app.seeSettings, app.seeInventory, app.shovel, app.wateringCan]
    
    app.shovelEquipped = app.wateringCanEquipped = False
    

#------------------------------------------START
def start_redrawAll(app):
    screen = Image.open("images/home.png")
    newWidth, newHeight = getNewDims(screen, 2.5) 
    screen = CMUImage(screen)
    drawImage(screen, app.width/2, app.height/2, 
              align='center', width=newWidth, height=newHeight)
    app.play.draw()
    app.about.draw()

def start_onMousePress(app, mouseX, mouseY):
    for button in app.startButtons:
        if button.wasClicked(mouseX, mouseY):
            setActiveScreen(button.task)
            break

def about_redrawAll(app):
    screen = Image.open('images/aboutscreen.png')
    width, height = getNewDims(screen, 2.5)
    screen = CMUImage(screen)
    drawImage(screen, app.width/2, app.height/2, 
              align='center', width=width, height=height)
    app.undo.draw()

def about_onMousePress(app, mouseX, mouseY):
    if app.undo.wasClicked(mouseX, mouseY):
        setActiveScreen('start')

#------------------------------------------FARM
def farm_redrawAll(app):
    drawBoard(app)
#plants
    for plant in app.plantsList:
        plant.draw()

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
    #digging with shovel
    if app.shovelEquipped:
        if mouseY < 590: #don't dig when equipping the tool
            cellCoords = (getCellClicked(app, mouseX, mouseY))
            app.dirtCells.add(cellCoords)

def getCellClicked(app, x, y):
    for cellLeft, cellTop in app.cellCoords:
        if (cellLeft <= x <= cellLeft+app.cellWidth 
            and cellTop <= y <= cellTop+app.cellHeight):
            return (cellLeft, cellTop)

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

def scroll(app, direction):
    app.cols += 1
    app.boardLeft -= 10
    for row in range(app.rows):
        app.cellCoords.add((getCellLeftTop(app, row, app.cols-1)))

    if direction == 'left':
        for cellLeft, cellTop in copy.copy(app.dirtCells):
            newCellLeft = cellLeft - 10
            app.dirtCells.add((newCellLeft, cellTop))
            app.dirtCells.remove((cellLeft, cellTop))
        for cellLeft, cellTop in copy.copy(app.cellCoords):
            newCellLeft = cellLeft - 10
            app.cellCoords.add((newCellLeft, cellTop))
            app.cellCoords.remove((cellLeft, cellTop))
    elif direction == 'right':
        for cellLeft, cellTop in copy.copy(app.dirtCells):
            newCellLeft = cellLeft + 10
            app.dirtCells.add((newCellLeft, cellTop))
            app.dirtCells.remove((cellLeft, cellTop))
        for cellLeft, cellTop in copy.copy(app.cellCoords):
            newCellLeft = cellLeft + 10
            app.cellCoords.add((newCellLeft, cellTop))
            app.cellCoords.remove((cellLeft, cellTop))


#------------------------------------------Drawing a Board (CS Academy)
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    #if cell is crop cell, fill brown, else green
    if (cellLeft, cellTop) in app.dirtCells:
        fill='brown'
    else: fill='lightGreen'

    drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight,
             fill=fill, border=fill)

def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.cellWidth
    cellTop = app.boardTop + row * app.cellHeight
    # app.cellCoords.add((cellLeft, cellTop))
    return (cellLeft, cellTop)

def drawTools(app):
    if app.shovelEquipped:
        image = app.shovel.image
        width, height = getNewDims(image, 8)
        image = CMUImage(image)
        drawImage(image, app.toolX, app.toolY, 
                  align='center', width=width, height=height)
        drawRect(app.shovel.x, app.shovel.y, width, height,
                  fill=None, border='green')
    elif app.wateringCanEquipped:
        image = app.wateringCan.image
        width, height = getNewDims(image, 8)
        image = CMUImage(image)
        drawImage(image, app.toolX, app.toolY, 
                  align='center', width=width, height=height)
        drawRect(app.wateringCan.x, app.wateringCan.y, width, height,
                  fill=None, border='green')
#------------------------------------------

def main():
    runAppWithScreens(initialScreen='start')

main()