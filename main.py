import grid
import cell
import genealogy
import display
import helpMessages

import random


helpMessages.displayStartupMessages()

# max size 52 x52
MAP= grid.Grid(45, 52)

for c in range(0, 15):
    MAP.spawnCell(5)
#display.printDisplay(MAP, None)


inp= ""
i=0
trackedCell= None
while inp != "X":   
    for f in range(0,1):
        MAP.spawnFood(3)
    moveList= cell.CELLS.copy()
    for z in moveList:
        z.move()
        # print(str(z)) #DEBUG
        # print(len(display.removeANSI(str(z))))
    MAP.totalturns+= 1
    while len(cell.CELLS)< 15:
        MAP.spawnCell(5)
    if i<1:
        display.printDisplay(MAP, trackedCell)
        inp= input()


        #help input
        if inp == "help":
            helpMessages.displayHelpMessages()

        #report generation input processing
        if inp == "report":
            reportLocation= input("Please list the location of the dopling, or list multiple locations separted only by a ',':\n")
            if reportLocation.count(",") > 0:
                locationList= reportLocation
                for section in range(0, reportLocation.count(",")+1):
                    if locationList.count(",")>0:
                        reportLocation= locationList[:locationList.index(",")]
                    else:
                        reportLocation=locationList
                    queriedCell= MAP.getCellAlphgrid(reportLocation)
                    if queriedCell is None:
                        print("no dopling found in " + str(reportLocation))
                    else:
                        queriedCell.report()
                    if locationList.count(",")>0:
                        locationList= locationList[locationList.index(",")+1:]
            else:
                queriedCell= MAP.getCellAlphgrid(reportLocation)
                if queriedCell is None:
                    print("no dopling found in " + str(reportLocation))
                else:
                    queriedCell.report()
            inp= input()
            

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
            jumpstartCutoff= int(input("How many living doplings should there be? "))
            i=1

        #track and untrack input processing
        if inp == "track":
            trackIdentifier= (input("Enter the ID, beginning with '#', or the grid location ('YX') of the dopling to be tracked: "))
            if "#" in trackIdentifier:
                trackID= int(trackIdentifier[1:])
                trackedCell= cell.ALL_CELLS[trackID]
            else:
                trackedCell= MAP.getCellAlphgrid(trackIdentifier)

            if trackedCell is None:
                print("No dopling found @" + str(trackIdentifier))
            else:
                genealogy.untrackAll()
                trackedCell.genealogy.track("main")
     
        if inp == "untrack":
            trackedCell= None
            trackedTotal= len(genealogy.TRACKED_CELLS)
            genealogy.untrackAll()
            print(str(trackedTotal) + " cells untracked")

        #toggle moving phylogeny display from right side to bottom
        if inp == "bottom":
            display.PHYLOGENYBOTTOMDISPLAY= not display.PHYLOGENYBOTTOMDISPLAY


        #process "pedigree" input
        if inp == "pedigree":
            display.printPedigree()
            inp= input()


        #double check if input is to end simulation       
        if inp == "X":
            doubleCheck= input("Are you sure you want to end the simulation? Type 'X' to end, or anything else to continue:")
            if not doubleCheck == "X":
                inp = ""

    else:
        if inp == "jumpstart":
            if len(cell.CELLS) < jumpstartCutoff:
                i+=1
            if MAP.totalturns%5000==0:
                print("Total Turns: " + str(MAP.totalturns) + "  Doplings generated: " + str(len(cell.ALL_CELLS)) + "  Doplings Alive: " + str(len(cell.CELLS)))
        else:
            if i%(numTotalRounds/10) == 0:
                print("percentage complete: " + str(percentage) + "%")
                percentage+= 10
        i-= 1




"""
Features to Implement:
-----------------------




5) Pedigree creation single cell
6) Pedigree creation for all currently living cells

7) refactored/cleaner report output (use tracked cell display)

10) add status window to right of map with current oldest cell, extant species, etc.
-add cell "thoughts" to traking HUD  

-Track total number of megamutations and mutations? in lineage

-add ability to adjust ranges for track cell mod table via input

-add ability to view mod/mov tables of multiple cells within species/across species



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
"""