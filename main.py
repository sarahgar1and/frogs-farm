from cmu_graphics import *
from PIL import Image

class Frog():
    def __init__(self, app):
    # metrics: 10/10 is the maximum
        self.mood = 10
        self.hunger = 10
        self.sleep = 10
        self.x = app.width/2
        self.y = app.height/2
        self.dx = 10
        self.dy = 10

    # images/sprites:
        self.standing = Image.open("images/standing.png")

        walkingSpriteList = []
        walkingGIF = Image.open("images/walking.gif")
        for frame in range(walkingGIF.n_frames):
            walkingGIF.seek(frame)
            image = walkingGIF.resize((walkingGIF.size[0], walkingGIF.size[1]))
            walkingSpriteList.append(image)

        self.walking = walkingSpriteList

    def takeStep(self):
        if self.direction == 'left':
            self.x -= self.dx
        elif self.direction == 'right':
            self. x += self.dx
        elif self.direction == 'up':
            self. y -= self.dy
        elif self.direction == 'down':
            self. y += self.dy
    
    def draw(self):
        i = self.counter
        if self.isMoving:
            image = self.walking[i % len(self.walking)]
            if self.direction == 'right':
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            newWidth, newHeight = getNewDims(image, 5)
            image = CMUImage(image)
            drawImage(image, self.x, self.y,align='center',
                    width=newWidth,height=newHeight)
        else:
            newWidth, newHeight = getNewDims(self.standing, 5)
            image = CMUImage(self.standing)
            drawImage(image, self.x, self.y,align='center',
                    width=newWidth, height=newHeight)
            
class Plant():
    harvestTimes = {}
    plantImages = {}
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
        drawImage(image, self.x, self.y)
            

class Button():
    buttonImages = {'play': Image.open("images/play.png"),
                    'about': Image.open("images/play.png")}
    buttonPos = {'play': (175, 200),
                 'about': (175,300)}
    def __init__(self, task):
        self.task = task
        self.image = Button.buttonImages[task]
        self.x, self.y = Button.buttonPos[task]
    
    def __repr__(self):
        return f'{self.task}'

    def draw(self):
        image = self.image
        self.width, self.height = getNewDims(image, 6)
        image = CMUImage(image)
        drawImage(image, self.x, self.y,
                  width=self.width, height=self.height) # don't align center

def getNewDims(image, factor):
    width,height = image.width, image.height
    return width/factor, height/factor 

#------------------------------------------Screens Functions
def drawFarm(app):
    drawBoard(app)

def drawStartScreen(app):
    screen = Image.open("images/home.png")
    newWidth, newHeight = getNewDims(screen, 2.5)
    screen = CMUImage(screen)
    drawImage(screen, app.width/2, app.height/2, 
              align='center', width=newWidth, height=newHeight)
    app.play.draw()
    app.about.draw()

def drawAboutScreen(app):
    pass

#------------------------------------------Drawing a Board (CS Academy)
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

#------------------------------------------

def onAppStart(app):
    app.stepsPerSecond = 10
# frog :3
    app.frog = Frog(app)
    app.frog.isMoving = False
    app.frog.counter = 0

    app.screen = 'start'
# buttons
    app.play = Button('play')
    app.about = Button('about')
    app.buttonsList = [app.play, app.about]

def redrawAll(app):
    if app.screen == 'start':
        drawStartScreen(app)
        return
    elif app.screen == 'about':
        drawAboutScreen(app)
        return
    elif app.screen == 'farm':
        drawFarm(app)
    app.frog.draw()

def onKeyPress(app, key):
    if key == 'left' or 'right' or 'up' or'down':
        app.frog.direction = key
        app.frog.isMoving = True
        app.frog.takeStep()

def onKeyRelease(app, key):
    app.frog.isMoving = False

def onMousePress(app, mouseX, mouseY):
    button = getButtonClicked(app, mouseX, mouseY)
    if button != None:
        app.screen = button.task

def getButtonClicked(app, mx, my):
    for button in app.buttonsList:
        if (button.x < mx < (button.x + button.width) 
            and (button.y + button.height) < button.y < my):
            # re-center frog
            app.frog.x, app.frog.y = app.width/2, app.height/2
            return button
    return None

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def onStep(app):
    if app.frog.isMoving:
        app.frog.takeStep()
        app.frog.counter += 1

def main():
    runApp(944, 656)

main()