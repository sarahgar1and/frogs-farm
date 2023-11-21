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
            image = walkingGIF.seek(frame)
            walkingSpriteList.append(image)

        self.walking = walkingSpriteList

    def takeStep(self, direction):
        if direction == 'left':
            self.x -= self.dx
        elif direction == 'right':
            self. x += self.dx
        elif direction == 'up':
            self. y -= self.dy
        elif direction == 'down':
            self. y += self.dy
    
    def draw(self):
        i = 0
        if self.isMoving == True:
            while self.isMoving == True:
                image = self.walking[i % len(self.walking)]
                # imageWidth, imageHeight = image.width, image.height
                image = CMUImage(image)
                # newWidth, newHeight = image.width//2, image.height//2
                drawImage(image, self.x, self.y,align='center',
                        width=200,height=200)
                i+=1
        else:
            imageWidth, imageHeight = self.standing.width, self.standing.height
            newWidth, newHeight = imageWidth//5, imageHeight//5
            image = CMUImage(self.standing)
            drawImage(image, self.x, self.y,align='center',
                    width=newWidth, height=newHeight)
            


def onAppStart(app):
    app.frog = Frog(app)
    app.frog.isMoving = False

def redrawAll(app):
    # drawLabel("hi", app.width/2, app.height/2)
    # drawImage(CMUImage(app.frog.standing),100,100,align='center',width=250,height=250)
    app.frog.draw()

def onKeyPress(app, key):
    print(key)
    if key == 'left' or 'right' or 'up' or'down':
        app.direction = key
        app.frog.isMoving = True
        app.frog.takeStep(key)

def onStep(app):
    if app.frog.isMoving:
        app.frog.takeStep(app.direction)

def main():
    runApp(1000, 700)

main()