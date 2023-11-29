from cmu_graphics import *
# from main import Item, Crop, Seed, Frog

def readStartFile():
    i = 1
    # line 1: day
    # line 2: inventory list
    # line 3: dirt cells
    # line 4: plants
    # frog hunger
    # frog sleep
    with open('start_data.txt', 'r') as file:
        for line in file:
            print(line)
            
def loadStartFile(app):
    readStartFile()

loadStartFile(app)