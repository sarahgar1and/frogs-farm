from classes import *

def makeAllPlantsHarvestable(app): #press 'h'
    for cell in app.plants:
        if app.plants[cell] != 'dirt':
            app.plants[cell].image = Plant.plantImages[f'{app.plants[cell].species}-1']
            app.plants[cell].stage = 'ready!'

def getLotsOfMoney(app): #press 'm'
    app.money += 100
