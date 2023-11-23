from cmu_graphics import *
from PIL import Image

class Frog:
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
        # (From lecture demo)
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
            
class Plant:
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
            

class Button:
    buttonImages = {'farm': Image.open("images/play.png"),
                    'about': Image.open("images/about.png")}
    buttonPos = {'farm': (175, 200),
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
        
    def wasClicked(self, mx, my):
        if (self.x < mx < (self.x + self.width) 
            and self.y < my < (self.y + self.height)):
            return True
        else: return False

def getNewDims(image, factor):
    width,height = image.width, image.height
    return width/factor, height/factor 

#------------------------------------------Drawing a Board (CS Academy)
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill='lightGreen', border='lightGreen')

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = col * cellWidth
    cellTop = row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.width / app.cols
    cellHeight = app.height / app.rows
    return (cellWidth, cellHeight)

#------------------------------------------
def onAppStart(app):
    app.width = 944
    app.height = 656
    app.stepsPerSecond = 10
    app.rows = 20
    app.cols = 20
# frog :3
    app.frog = Frog(app)
    app.frog.isMoving = False
    app.frog.counter = 0
# plants
    app.plantsList = []
# buttons
    app.play = Button('farm')
    app.about = Button('about')
    app.startButtons = [app.play, app.about]

#------------------------------------------START
def start_redrawAll(app):
    screen = Image.open("images/home.png")
    newWidth, newHeight = getNewDims(screen, 2.5)
    screen = CMUImage(screen)
    drawImage(screen, app.width/2, app.height/2, 
              align='center', width=newWidth, height=newHeight)
    app.play.draw()
    app.about.draw()

def about_redrawAll(app):
    drawLabel("About: ", app.width/2, 20)

def start_onMousePress(app, mouseX, mouseY):
    for button in app.startButtons:
        if button.wasClicked:
            setActiveScreen(button.task)
            break

#------------------------------------------FARM
def farm_redrawAll(app):
    drawBoard(app)
    app.frog.draw()

def farm_onKeyPress(app, key):
    if key == 'left' or key == 'right' or key =='up' or key == 'down':
        app.frog.direction = key
        app.frog.isMoving = True
        app.frog.takeStep()

def farm_onKeyRelease(app, key):
    app.frog.isMoving = False

def farm_onStep(app):
    if app.frog.isMoving:
        app.frog.takeStep()
        app.frog.counter += 1
#------------------------------------------

def main():
    runAppWithScreens(initialScreen='start')

main()