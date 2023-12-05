from cmu_graphics import *
from PIL import Image

class Frog:
    def __init__(self, app):
    # metrics: 20/20 is the maximum
        self.hunger = 20
        self.sleep = 20
        self.counter = 0
        self.careButtons = [LittleButton('eat'), LittleButton('sleep')]

        self.isMoving=self.doneWorking=self.atRightEdge=self.atLeftEdge=False
        self.showMenu = self.atBottomEdge = False
        self.x = app.width/2
        self.y = app.height/2
        self.dx = 12
        self.dy = 12

    # images/sprites:
        self.standing = Image.open("images/standing.png")
        self.width, self.height = getNewDims(self.standing, 6)
        self.standing = CMUImage(self.standing)

        walkingLeftSpriteList = [] # (From lecture demo: https://piazza.com/class/lkq6ivek5cg1bc/post/2231)
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
        elif (self.direction == 'down' and self.y < app.height 
              and not self.atBottomEdge):
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
        #metrics
        drawLabel("Sleep: ", 20, 616, align='left', size=14)
        drawRect(75, 616, self.sleep*10, 10, fill='blue', border=None, 
                 align='left')
        drawRect(75, 616, 200, 10, fill=None, border='black', align='left')
        drawLabel("Hunger: ", 20, 636, align='left', size=14)
        drawRect(75, 636, self.hunger*10, 10, fill='orange', border=None,
                 align='left')
        drawRect(75, 636, 200, 10, fill=None, border='black',align='left')
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
        if (cellLeft-50 <= self.x <= cellLeft+app.cellWidth+50 and
        cellTop-50 <= self.y <= cellTop+app.cellHeight+50):
            return True
        return False

    def wasClicked(self, x, y):
        if (self.x - self.width/2 <= x <= self.x + self.width/2 and 
            self.y - self.height/2 <= y <= self.y +self.height/2):
            return True
        return False

    def bedtime(self):
        self.sleep = 20

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
    seedImage = Image.open("images/seed.png")
    def __init__(self, species):
        self.species = species
    # 4 stages: seed, baby, adolescent, adult  
        self.stage = 'seed' 
        self.image = Plant.seedImage
        self.width, self.height = getNewDims(self.image, 5)
        self.image = CMUImage(self.image)
    # harvestable once daysTillHarvest == harvestTime
        self.days = 0 
        self.watered = False

    def grow(self): #call when for watered plants when sleep!!
        self.days += 1
        if self.days == Plant.harvestTimes[self.species]:
            self.stage = 'ready!'
        if self.days == 4: # spend 2 days as an adolescent
            self.image = Plant.plantImages[f'{self.species}-1']
        elif self.days == 1:
            self.image = Plant.saplingImage
        elif self.days == 2:
            self.image = Plant.plantImages[f'{self.species}-0']
    
    def draw(self, app, x, y):
        drawImage(self.image, x, y, align='center',
                  width=self.width, height=self.height)
        if not self.watered and self.stage != 'ready!':
            drawLabel("I'm thirsty!", x, y+20, size=16, fill='lightBlue')
        elif self.stage == 'ready!':
            drawLabel("Harvest me!", x, y-50, size=16, fill='yellow')
            
class Button:
    buttonImages = {'farm': Image.open("images/play.png"),
                    'about': Image.open("images/about.png"),
                    'undo': Image.open('images/return.png'),
                    'shovel': Image.open('images/shovel.png'),
                    'wateringCan': Image.open('images/watering_can.png'),
                    'settings': Image.open('images/settings.png'),
                    'inventory': Image.open('images/inventory.png'),
                    'eat': Image.open('images/eat.png'),
                    'sleep': Image.open('images/sleep.png'),
                    'buy': Image.open('images/buy.png'),
                    'marketBuy': Image.open('images/marketbuy.png'),
                    'marketSell': Image.open('images/marketsell.png'),
                    'clear': Image.open('images/clear.png'),
                    'save': Image.open('images/save.png'),
                    'paint': Image.open('images/paint.png'),
                    'decor': Image.open("images/decor.png")}
    buttonPos = {'farm': (175, 200),
                 'about': (175,300),
                 'undo': (0,5),
                 'shovel': (472, 590),
                 'wateringCan': (402, 590),
                 'settings': (874, 5),
                 'inventory': (804, 5),
                 'eat': (None, None),
                 'sleep': (None, None),
                 'buy': (377, 300),
                 'marketBuy': (20, 10),
                 'marketSell': (100, 10),
                 'clear': (200, 320),
                 'save': (360, 200),
                 'paint': (860, 600),
                 'decor': (780, 600)}
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
        self.width, self.height = getNewDims(self.image, 6) #100 x 100

    def __repr__(self):
        return f'{self.type}'

class Crop(Item):
    def __init__(self, thing):
        super().__init__(thing)
        self.image = Plant.plantImages[(f'{self.type}-1')]

    def draw(self, app, x, y):
        drawImage(self.image, x, y, width=self.width, height=self.height,
                   align='left')
        drawLabel(f'{self.type}  x{self.num}', 
                  x+self.width/2, y+self.height/2, size=16)
        if self == app.selectedItem:
            self.border = 'green'
        else: self.border = None

class Seed(Item):
    def __init__(self, thing):
        super().__init__(thing)
        self.image = CMUImage(self.image)

    def draw(self, app, x, y):
        drawImage(self.image, x, y, width=self.width, height=self.height, 
                  align='left')
        drawLabel(f'{self.type}  x{self.num}', 
                  x+self.width/2, y+self.height/2, size=16)
        if self == app.selectedItem:
            self.border = 'green'
        else: self.border = None

class Decor:
    bedImages = {'bed1': Image.open("images/bed1.png"),
                'bed2': Image.open("images/bed2.png"),
                'bed3': Image.open("images/bed3.png"),
                'bed4': Image.open("images/bed4.png")}
    def __init__(self, thing):
        if 'bed' in thing:
            self.type = 'bed'
            self.image = Decor.bedImages[thing]
        elif 'poster' in thing:
            self.type = 'poster'
            self.image = Decor.posterImages[thing]
        self.width, self.height = getNewDims(self.image, 2.5)
        self.image = CMUImage(self.image)
    
    def draw(self):
        drawImage(self.image, 0, 0, width=self.width, height=self.height)

def getNewDims(image, factor):
    width,height = image.width, image.height
    return width/factor, height/factor 