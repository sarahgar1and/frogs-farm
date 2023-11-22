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
            imageWidth, imageHeight = image.width, image.height
            if self.direction == 'right':
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            image = CMUImage(image)
            newWidth, newHeight = imageWidth//5, imageHeight//5
            drawImage(image, self.x, self.y,align='center',
                    width=newWidth,height=newHeight)
        else:
            imageWidth, imageHeight = self.standing.width, self.standing.height
            newWidth, newHeight = imageWidth//5, imageHeight//5
            image = CMUImage(self.standing)
            drawImage(image, self.x, self.y,align='center',
                    width=newWidth, height=newHeight)
            
class Plant():
    def __init__(self, species):
        self.species = species
    # 4 stages: seed, baby, adolescent, adult  
        self.stage = 0 
        self.watered = False
    # harvestable once daysTillHarvest == harvestTime
    # do not progess if not watered
        self.daysTillHarvest = 0 

    def harvestTime(self):
        pass
    def agingTime(sef):
        pass
    def plantImages(self):
        pass

def drawMap(app):
    pass

def onAppStart(app):
    app.stepsPerSecond = 10
    app.frog = Frog(app)
    app.frog.isMoving = False
    app.frog.counter = 0

def redrawAll(app):
    drawMap(app)
    app.frog.draw()

def onKeyPress(app, key):
    if key == 'left' or 'right' or 'up' or'down':
        app.frog.direction = key
        app.frog.isMoving = True
        app.frog.takeStep()

def onStep(app):
    if app.frog.isMoving:
        app.frog.takeStep()
        app.frog.counter += 1

def onKeyRelease(app, key):
    app.frog.isMoving = False

def main():
    runApp(1000, 700)

main()