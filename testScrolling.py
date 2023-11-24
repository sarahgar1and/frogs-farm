from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    app.image = Image.open('images/home.png')
    app.imageX = app.width/2
    app.imageY = app.height/2
    app.imageWidth, app.imageHeight = app.image.width, app.image.height
    app.cx = app.width/2
    app.cy = app.height/2
    app.margin = 40
    app.charAtEdge = False

def redrawAll(app):
    image = CMUImage(app.image)
    drawImage(image, app.imageX, app.imageY, align='center')
    drawCircle(app.cx, app.cy, 10, fill='black')

def onKeyPress(app, key):
    if key == 'left':
        app.cx -= 10
    elif key == 'right':
        app.cx += 10
    elif key == 'up':
        app.cy -= 10
    elif key == 'down':
        app.cy += 10
    scroll(app)

def scroll(app):
    # don't scroll if at edge of image
    # shift image x if circle touching margin on left/right
    # shift image y if circle tought margin on top/bottom 
    # don't let character off edge <-----
    if (app.cx + 10 <= app.margin and 
        not (app.imageWidth/2 - app.imageX <= app.margin)): #char on left edge
        #shift image to the right
        app.imageX += app.margin
        app.charAtEdge = True
        app.cx += 10
    elif (app.cx + 10 >= app.width - app.margin): #char on right edge
        #shift image to the left
        app.imageX -= app.margin
        app.charAtEdge = True
        app.cx -= 10
    if app.cy + 10 <= app.margin: #at top edge
        #shift image down
        app.imageY += app.margin
        app.charAtEdge = True
        app.cy += 10
    elif app.cy + 10 >= app.height - app.margin: #char at bottom edge
        #shift image up
        app.imageY -= app.margin
        app.charAtEdge = True
        app.cy -= 10

def main():
    runApp()

main()