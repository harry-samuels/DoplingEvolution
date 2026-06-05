import grid
import cell
import genealogy
import display
import helpMessages
import inputs

import random
import os
import json

def runSimulation():
    MAP= loadState("saved_states/500_Generations.json") # max size 999x999 


    runTurn(MAP)

    SIMULATING= True
    generationThreshold= 100
    
    while SIMULATING:
        runTurn(MAP)
        #print(MAP.latestgeneration) #DEBUG
        if MAP.latestgeneration > generationThreshold:
            saveState(MAP, "currentState")
            generationThreshold +=500


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


#save a loadable copy of the current map and all living doplings with their current valuetables
#MAP is the Grid object being saved
#file_name is a str 
def saveState(MAP, file_name):
    stateData= {}
    stateData["FOOD_PER_TURN"]= inputs.FOOD_PER_TURN
    stateData["FOOD_VALUE"]= inputs.FOOD_VALUE
    stateData["BASE_CELL_NUMBER"]= inputs.BASE_CELL_NUMBER
    stateData["SPAWNED_CELL_FOOD"]= inputs.SPAWNED_CELL_FOOD
    stateData["FOOD_TO_MOVE"]= inputs.FOOD_TO_MOVE
    stateData["MESSENGER_PROTEIN_NUMBER"]= inputs.MESSENGER_PROTEIN_NUMBER
    stateData["SECONDARY_MESSENGER_NUMBER"]= inputs.SECONDARY_MESSENGER_NUMBER
    stateData["PAC_MAN_MODE"]= inputs.PAC_MAN_MODE

    stateData["MAP"]= MAP.saveGrid()

    with open("saved_states/" + file_name + ".json", "w") as stateFile:
                stateFile.write(json.dumps(stateData, indent=4))


# Load the state file (str path to state file) from inputs.py
# Configure the simluation input vairables to match the saved state file and
# Return the Grid Object of the saved state file in the input file
def loadState(stateFile):
    stateData= json.load(open(stateFile))

    inputs.FOOD_PER_TURN= stateData["FOOD_PER_TURN"] 
    inputs.FOOD_VALUE= stateData["FOOD_VALUE"] 
    inputs.BASE_CELL_NUMBER= stateData["BASE_CELL_NUMBER"] 
    inputs.SPAWNED_CELL_FOOD= stateData["SPAWNED_CELL_FOOD"] 
    inputs.FOOD_TO_MOVE= stateData["FOOD_TO_MOVE"] 
    inputs.MESSENGER_PROTEIN_NUMBER= stateData["MESSENGER_PROTEIN_NUMBER"] 
    inputs.SECONDARY_MESSENGER_NUMBER= stateData["SECONDARY_MESSENGER_NUMBER"] 
    inputs.PAC_MAN_MODE= stateData["PAC_MAN_MODE"] 

    inputs.USE_CUSTOM_MAP= False

    MAP= grid.createStateGrid(stateData["MAP"])

    return MAP

runSimulation()

