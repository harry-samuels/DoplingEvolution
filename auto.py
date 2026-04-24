import grid
import cell
import genealogy
import display
import helpMessages
import inputs

import random
import os

def runSimulation():
    #helpMessages.displayStartupMessages()
    #cell.Cell.SPLIT_SPEED_RATIO= inputs.FOOD_TO_SPLIT/inputs.FOOD_TO_MOVE  #make this an actual input value?
    MAP= grid.Grid(inputs.MAP_ROWS, inputs.MAP_COLUMNS) # max size 999x999 


    runTurn(MAP)

    testCell= random.choice(cell.CELLS)
    testCell.name= "TEST_" + testCell.name
    testCell.saveCell()

    fourbyFile= "saved_doplings/fourby.json"
    spawnLocation= MAP.getNode(20, 20)
    cell.loadCell(fourbyFile, MAP, spawnLocation)

    SIMULATING= True
    generationThreshold= 100
    
    while SIMULATING:
        runTurn(MAP)
        #display.printDisplay(MAP)
        #SIMULATING= processInput(MAP, input())
        if MAP.latestgeneration > generationThreshold:
            sampleCell= random.choice(cell.CELLS)
            sampleCell.name= str(generationThreshold) + "_" + sampleCell.name
            sampleCell.saveCell()
            generationThreshold +=500
           # if generationThreshold > 1000:
            #    SIMULATING= False

def runTurn(MAP):
    #increase turn counter
    MAP.totalturns+= 1
    #create food
    for f in range(0,inputs.FOOD_PER_TURN):
        MAP.spawnFood(inputs.FOOD_VALUE)
    #move all doplings in order
    moveList= cell.CELLS.copy()
    for dopling in moveList:
        dopling.move()
    #spawn doplings until minimum dopling count is reached 
    while len(cell.CELLS)< inputs.BASE_CELL_NUMBER:
        MAP.spawnCell(food=inputs.SPAWNED_CELL_FOOD)
    #set latest generation to most recently created cell's generation
    #MAP.latestgeneration= cell.ALL_CELLS[-1].genealogy.generation

runSimulation()

