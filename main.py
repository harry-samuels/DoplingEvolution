import grid
import cell
import genealogy
import display
import helpMessages
import inputs

import random


helpMessages.displayStartupMessages()

#make this an actual input value?
cell.Cell.SPLIT_SPEED_RATIO= inputs.FOOD_TO_SPLIT/inputs.FOOD_TO_MOVE

# max size 52 x52
MAP= grid.Grid(inputs.MAP_ROWS, inputs.MAP_COLUMNS)

#don't actually need these three lines
#for c in range(0, 15):
    #MAP.spawnCell(5)


inp= ""
i=0
trackedCell= None
while inp != "X":   
    for f in range(0,inputs.FOOD_PER_TURN):
        MAP.spawnFood(inputs.FOOD_VALUE)
    moveList= cell.CELLS.copy()
    for z in moveList:
        z.move()

    MAP.totalturns+= 1

    while len(cell.CELLS)< inputs.BASE_CELL_NUMBER:
        MAP.spawnCell(food=inputs.SPAWNED_CELL_FOOD)

    MAP.latestgeneration= cell.ALL_CELLS[-1].genealogy.generation

    if i<1:
        display.printDisplay(MAP, trackedCell)
        inp= input()


        #help input
        if inp == "help":
            helpMessages.displayHelpMessages()

        #report generation input processing CURRENTLY DEPRECATED while being switched from alphagrid
        # if inp == "report":
        #     reportLocation= input("Please list the location of the dopling, or list multiple locations separted only by a ',':\n")
        #     if reportLocation.count(",") > 0:
        #         locationList= reportLocation
        #         for section in range(0, reportLocation.count(",")+1):
        #             if locationList.count(",")>0:
        #                 reportLocation= locationList[:locationList.index(",")]
        #             else:
        #                 reportLocation=locationList
        #             queriedCell= MAP.getCellAlphgrid(reportLocation)
        #             if queriedCell is None:
        #                 print("no dopling found in " + str(reportLocation))
        #             else:
        #                 queriedCell.report()
        #             if locationList.count(",")>0:
        #                 locationList= locationList[locationList.index(",")+1:]
        #     else:
        #         queriedCell= MAP.getCellAlphgrid(reportLocation)
        #         if queriedCell is None:
        #             print("no dopling found in " + str(reportLocation))
        #         else:
        #             queriedCell.report()
        #     inp= input()
            

        #speed rounds input processing
        if inp == "speed":
            # catch misinput to prevent error
            try:
                i= int(input("How many moves should be run before next check-in?: "))
                numTotalRounds= i
                percentage= 0
            except (ValueError):
                print("Non-numeric value input: Unable to reach warp-speed")
        

        #jumpstart rounds input processing
        if inp == "jumpstart":
            try:
                jumpstartCutoff= int(input("How many GENERATIONS should there be?: "))
                #old version for cell count
                #jumpstartCutoff= int(input("How many living doplings should there be? "))
                i=1
            except (ValueError):
                print("Non-numeric value input: Unable to reach warp-speed")


        #track and untrack input processing
        if inp == "track":
            display.MULTITRACK= False
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
                    print("Incorrect coordinate input, please be sure to include both x and y separated by a comma ','")

            if trackedCell is None:
                print("No dopling found @" + str(trackIdentifier))
            else:
                genealogy.untrackAll()
                trackedCell.genealogy.track("main")
     
        if inp == "untrack":
            trackedCell= None
            display.MULTITRACK= False
            trackedTotal= len(genealogy.TRACKED_CELLS)
            genealogy.untrackAll()
            print(str(trackedTotal) + " cells untracked")

        #renaming tracked cell
        if inp == "name":
            if not (trackedCell is None):
                trackedCell.name= input("What would you like to name this dopling?: ")
            else:
                print("\nno dopling currently tracked, please track the dopling to be renamed")

        #saving tracked cell
        if inp == "save":
            if trackedCell:
                trackedCell.saveCell()
                print("saved " + trackedCell.name)
            else:
                print("No current tracked cell to be saved")

        if inp == "multitrack":
            genealogy.untrackAll()
            trackedCell= None
            if input("Type 'species' to view the top 3 species: ") == "species":
                display.MULTITRACK= True
            
        if inp == "load":
            cellFile= input("Please enter the filepath for the saved Cell: ")
            spawnCoords= input("Please enter the desired grid location ('X, Y') of the dopling to be loaded: ")
            spawnLocation= None
            try:
                    spawnX= int(spawnCoords[:spawnCoords.index(',')])
                    spawnY= int(spawnCoords[spawnCoords.index(',') +1:])
                    spawnLocation= MAP.getNode(spawnX, spawnY)
            except(ValueError, IndexError):
                print("Incorrect coordinate input, please be sure to include both x and y separated by a comma ','")
            if spawnLocation:
                loadedCell= cell.loadCell(cellFile, MAP, spawnLocation)
                genealogy.untrackAll()
                #track the newly loaded cell
                trackedCell= loadedCell
                trackedCell.genealogy.track("main")

                

        #toggle moving phylogeny display from right side to bottom
        if inp == "bottom":
            display.PHYLOGENYBOTTOMDISPLAY= not display.PHYLOGENYBOTTOMDISPLAY


        #process "pedigree" input
        if inp == "pedigree":
            display.printPedigree()
            inp= input()


        if inp == "wall":
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
        #double check if input is to end simulation       
        if inp == "X":
            doubleCheck= input("Are you sure you want to end the simulation? Type 'X' to end, or anything else to continue:")
            if not doubleCheck == "X":
                inp = ""

    else:
        if inp == "jumpstart":
            #old version using cell count:
            #if len(cell.CELLS) < jumpstartCutoff:
            if MAP.latestgeneration < jumpstartCutoff:
                i+=1
            if MAP.totalturns%5000==0:
                print("Total Turns: " + str(MAP.totalturns) + "  Doplings generated: " + str(len(cell.ALL_CELLS)) + "  Doplings Alive: " + str(len(cell.CELLS)) + "  Latest Generation: " + str(MAP.latestgeneration))
        else:
            if i%(numTotalRounds/10) == 0:
                print("percentage complete: " + str(percentage) + "%")
                percentage+= 10
        i-= 1



#def runTurn(MAP)


"""
Features to Implement:
-----------------------



--------VISUAL/TRACKING:

5) Pedigree creation single cell

7) refactored/cleaner report output (use tracked cell display)

10) add status window to right of map with current oldest cell, extant species, etc.
-add cell "thoughts" to traking HUD  

-Track total number of megamutations and mutations? in lineage

-add ability to adjust ranges for track cell mod table via input

-add ability to view mod/mov tables of multiple cells within species/across species




-----SAVING CELLS
-add cell to favorites (yellow highlights)
-ability to rebirth favorited cell?

-save cells as csv for ressurection


-----SIMULATION FEATURES

-add ability to bottleneck and kill large number of cells?

-preset walls? (ie: halves/quarters)
-build mountain range? (over time mountain range grows and then recedes across screen? could be really neat)

-secondary messengers? more messenger hormone options? (stretch goal)

-make hormones cost food?

-Allow cells to mutate duplicate/remove hormones





DONE:
------
X Backround highlight tracking for individual cell
X Backround highlighttracking for all of cell's offspring
X Backround highlight tracking for all of cell's ancestors
X add color to Elder (&) cells
X cell.numberID based lookup for living and dead cells
X add ability to speed through rounds until enough cells exist to indicate intelligent life
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
"""