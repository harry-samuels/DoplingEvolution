import grid
import cell
import genealogy
import display
import helpMessages
import inputs

import random
import os

#import cProfile

def runSimulation():
    helpMessages.displayStartupMessages()
    #cell.Cell.SPLIT_SPEED_RATIO= inputs.FOOD_TO_SPLIT/inputs.FOOD_TO_MOVE  #make this an actual input value?
    MAP= grid.Grid(inputs.MAP_ROWS, inputs.MAP_COLUMNS) # max size 999x999 

    SIMULATING= True
    while SIMULATING:
        runTurn(MAP)
        display.printDisplay(MAP)
        SIMULATING= processInput(MAP, input())


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
    MAP.latestgeneration= cell.ALL_CELLS[-1].genealogy.generation

#processes user input and returns True if the simulation will continue, False if it should end
def processInput(MAP, inp):  
    if inp == "X":
        doubleCheck= input("Are you sure you want to end the simulation? Type 'X' to end, or anything else to continue:")
        if doubleCheck == "X":
            return False
    
    elif inp == "help":
        helpMessages.displayHelpMessages()
    elif inp == "speed":
        speed(MAP, input("How many TURNS should be run before next check-in?: "))
    elif inp == "jumpstart":
        jumpstart(MAP, input("How many GENERATIONS should there be before next check-in?: "))
    elif inp == "track":
        track(MAP)
    elif inp == "untrack":
        untrack(MAP)
    elif inp == "name":
        name(MAP)
    elif inp == "save":
        save(MAP)
    elif inp == "multitrack":
        multitrack(MAP)
    elif inp == "load":
        load(MAP)
    elif inp == "bottom":
        bottom()
    elif inp == "pedigree":
        pedigree()
    elif inp == "wall":
        wall(MAP)
    return True
 
    
def speed(MAP, numTurnsInput):
    try:
        numTotalTurns= int(numTurnsInput)
    except (ValueError):
        print("Non-numeric input: Unable to reach warp-speed")
        return

    i= numTotalTurns
    percentage= 0
    while i > 0:
        if i%(numTotalTurns/10) == 0:
            print("percentage complete: " + str(percentage) + "%")
            percentage+= 10
        runTurn(MAP)
        i-= 1


def jumpstart(MAP, numGenerationsInput):
    try:
        jumpstartCutoff= int(numGenerationsInput)
    except (ValueError):
        print("Non-numeric input: Unable to reach warp-speed")
        return
    
    while MAP.latestgeneration < jumpstartCutoff:
        if MAP.totalturns%5000==0:
            print("Total Turns: " + str(MAP.totalturns) + "  Doplings generated: " + str(len(cell.ALL_CELLS)) + "  Doplings Alive: " + str(len(cell.CELLS)) + "  Latest Generation: " + str(MAP.latestgeneration))
        runTurn(MAP)

def track(MAP):
    trackedCell= None
    trackIdentifier= (input("Enter the ID, beginning with '#', or the grid location ('X, Y') of the dopling to be tracked: "))
    if "#" in trackIdentifier:
        try:
            trackID= int(trackIdentifier[1:])
            trackedCell= cell.ALL_CELLS[trackID]
        except(ValueError, IndexError):
            print("Improper cell ID #")
    else:
        try:
            trackX= int(trackIdentifier[:trackIdentifier.index(',')])
            trackY= int(trackIdentifier[trackIdentifier.index(',') +1:])
            trackedCell= MAP.getCellFromCoordinates(trackX, trackY)
        except(ValueError, IndexError):
            print("Incorrect coordinate input, please be sure to include both x and y coordinates separated by a comma ','")

    if trackedCell is None:
        print("No dopling found @" + str(trackIdentifier))
    else:
        display.MULTITRACK_TYPE= ""
        genealogy.untrackAll(MAP)
        trackedCell.genealogy.track("main")
        MAP.trackedCell= trackedCell
       
def untrack(MAP):
    display.MULTITRACK_TYPE= ""
    trackedTotal= len(genealogy.TRACKED_CELLS)
    genealogy.untrackAll(MAP)
    print(str(trackedTotal) + " cells untracked")

def name(MAP):
    if MAP.trackedCell:
        MAP.trackedCell.name= input("What would you like to name this dopling?: ")
    else:
        print("\nno dopling currently tracked, please track the dopling to be renamed")

def save(MAP):
    if MAP.trackedCell:
        MAP.trackedCell.saveCell()
        print("saved " + MAP.trackedCell.name)
    else:
        print("No current tracked cell to be saved")

def multitrack(MAP):
    genealogy.untrackAll(MAP)
    display.MULTITRACK_TYPE= ""
    print("")
    print("1  -  Top Species\n2  -  Single Species\n3  -  Oldest Doplings")
    print("")
    multitrackType= input("Please enter the number of the desired tracking catergory: ")
    if multitrackType == "1" or multitrackType == "top species":
        display.MULTITRACK_TYPE= "topSpecies"

    elif multitrackType == "2" or multitrackType == "single species":
        currentSpecies= genealogy.getCurrentSpecies()
        print("\nExtant Species: ")
        print("-----------------------")
        for taxonIndex in range(0, len(currentSpecies)):
            taxon= currentSpecies[taxonIndex]
            print(str(taxonIndex) + "  -  " + "\x1b[" +taxon.color + "m" + taxon.genus + " " + taxon.species + "\x1b[0m ")
        desiredTaxonNumber= input("Please enter the index number of the species to be tracked: ")
        try:
            trackedTaxon= currentSpecies[int(desiredTaxonNumber)]
        except (ValueError, IndexError):
            print("Non-numeric or incompatiable input, unable to match to listed taxon")
            return
        display.MULTITRACK_TYPE= trackedTaxon

    elif multitrackType == "3" or multitrackType == "oldest doplings":
        display.MULTITRACK_TYPE= "oldestCells"
    return
    


def load(MAP):
    print("")
    print("Saved Doplings: ")
    print("")
    cellFileList= os.listdir("saved_cells")
    fileIndex= 0
    for cFile in cellFileList:
        print(str(fileIndex).ljust(3, " ") + " -   " + cFile)
        print("")
        fileIndex+= 1
    try:
        cellFileIndex= int(input("Please enter the corresponding number of the dopling file to be loaded: "))
        cellFile= "saved_cells/" + cellFileList[cellFileIndex]

    except (ValueError, IndexError):
        print("Integer entry not recognized, please enter only the corresponding integer value for the desired file")
        return

    spawnCoords= input("Please enter the desired grid location ('X, Y') of the dopling to be loaded: ")
    spawnLocation= None
    try:
            spawnX= int(spawnCoords[:spawnCoords.index(',')])
            spawnY= int(spawnCoords[spawnCoords.index(',') +1:])
            spawnLocation= MAP.getNode(spawnX, spawnY)
    except(ValueError, IndexError):
        print("Incorrect coordinate input, please be sure to include both x and y separated by a comma ','")
        return
    if spawnLocation:
        loadedCell= cell.loadCell(cellFile, MAP, spawnLocation)
        genealogy.untrackAll(MAP)
        #track the newly loaded cell
        MAP.trackedCell= loadedCell
        loadedCell.genealogy.track("main")

def bottom():
    display.PHYLOGENYBOTTOMDISPLAY= not display.PHYLOGENYBOTTOMDISPLAY

def pedigree():
    display.printPedigree()

def wall(MAP):
    buildRemoveDestroy= input("Enter 'build' to build walls, 'remove' to remove walls, or 'destroy' to remove all walls: ")
    if buildRemoveDestroy == "build":
        direction= input("Enter 'H' for a horizontal wall or 'V' for a vertical wall: ")
        topleft= input("Enter the grid location of the top/left of the wall (X,Y): ")
        try:
            topleftX= int(topleft[:topleft.index(',')])
            topleftY= int(topleft[topleft.index(',') +1:])
            try:
                wallLength= int(input("Enter how many space long the wall should be: "))
                MAP.buildWall(direction, topleftX, topleftY, wallLength)
            except (ValueError):
                print("non-numeric entry for wall length")
        except(ValueError, IndexError):
            print("Incorrect coordinate input, please be sure to include both x and y separated by a comma ','")

    elif buildRemoveDestroy == "remove":
        direction= input("Enter 'H' for a horizontal removal or 'V' for a vertical removal: ")
        topleft= input("Enter the grid location of the top/left of the removal (X,Y): ")
        try:
            topleftX= int(topleft[:topleft.index(',')])
            topleftY= int(topleft[topleft.index(',') +1:])
            try:
                removeLength= int(input("Enter how many spaces of wall should be removed: "))
                MAP.removeWalls(direction, topleftX, topleftY, removeLength)
            except (ValueError):
                print("non-numeric entry for remove length")
        except(ValueError, IndexError):
            print("Incorrect coordinate input, please be sure to include both x and y separated by a comma ','")
        
    elif buildRemoveDestroy == "destroy":
        MAP.destroyWalls()

runSimulation()

#cProfile.run('runSimulation()', sort='ncalls')
"""
Features to Implement:
-----------------------



--------VISUAL/TRACKING:

5) Pedigree creation single cell

7) refactored/cleaner report output (use tracked cell display)

10) add status window to right of map with current oldest cell, extant species, etc.

-Track total number of megamutations and mutations? in lineage

-add ability to adjust ranges for track cell mod table via input

-add ability to view mod/mov tables of multiple cells within species/across species




-----SAVING CELLS
-add cell to favorites (yellow highlights)
-ability to rebirth favorited cell?



-----SIMULATION FEATURES

-add ability to bottleneck and kill large number of cells?

-preset walls? (ie: halves/quarters)
-build mountain range? (over time mountain range grows and then recedes across screen? could be really neat)

-make hormones cost food?

-different "eras" with respective food value/amount? different split/speed ratios?\\

-create splittin? allow cells to choose when to split rather than have set value?

-adjust speed calculation so all cells have base speed based on split size and then also an additional amount added on to become faster






DONE:
------
X Backround highlight tracking for individual cell
X Backround highlighttracking for all of cell's offspring
X Backround highlight tracking for all of cell's ancestors
X add color to Elder (&) cells
X cell.numberID based lookup for living and dead cells
X add ability to speed through rounds until enough cells exist to indicate intelligent life
X add cell "thoughts" to traking HUD
X add death message to track page after death (will need to condense death messages)
X add taxonomy (genus, species, etc.)
X Pedigree creation for all currently living cells
X rename cells
X allow cells to evolve faster "speed" to move first
X allow cells to change their split value 
X make food turns red on tracked cell display when cell is ten turns away from starving
X change collision behavior to allow cell with more food to "eat" other cell
X add ability to add walls
X track number of generations for all cells (make jumpstart work better?)
X secondary messengers? more messenger hormone options? (stretch goal)
X Allow cells to mutate duplicate/remove hormones
X save cells as json for ressurection

"""