import grid
import cell
import genealogy
import random
import thoughts
import inputs

import re

PHYLOGENYBOTTOMDISPLAY= False
BOTTOM_DISPLAY= []

MULTITRACK= False

def printDisplay(map, trackedCell):
    BOTTOM_DISPLAY.clear()
    mapDisplay= assembleMapDisplay(map)
    dataDisplay= assembleDataDisplay(map, trackedCell)
    finalDisplay= stitchDisplays(mapDisplay, dataDisplay)
    if PHYLOGENYBOTTOMDISPLAY:
        finalDisplay.extend(BOTTOM_DISPLAY)
    printableDisplay="\n\n\n"
    for line in finalDisplay:
        printableDisplay+= "\n" + line
    print(printableDisplay)
    # print("\n\n\n")
    # for line in finalDisplay:
    #     print(line)

def assembleMapDisplay(map):
    alpha= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    firstLine= "+   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z"[:((map.columns*2)+ 4)]
   
    display= [firstLine, (" "*len(firstLine))]
   
    i= 0
    line=""
    for y in map.container:
        line=""
        line+= alpha[i]+ "   "
        i+= 1
        for x in y:
            line+= str(x) + " "
        display.append(line)
    return display

def assembleDataDisplay(map, trackedCell):
    display= [" Total Turns:  " + str(map.totalturns) + "  |  Total Doplings:  " + str(map.totalcellsspawned),
        " Living Doplings: " + str(len(cell.CELLS))]
    if trackedCell is None:
        if MULTITRACK:
            genealogy.untrackAll()
            display.extend(assembleMultitrackDisplay())
        else:
            display.extend(assembleExpandedSpeciesDisplay())
    else:
        display.extend(assembleTrackedCellDisplay(trackedCell))
        
    return display

#combines two display list of strings to be printed into one list, with display1 on the left and display2 on the right and 2 spaces in between
#recurses
def stitchDisplays(display1, display2):
    #check different versions of [] inputs
    if not display1:
        return display2
    elif not display2:
        return display1
    
    line= display1.pop(0) + "  " + display2.pop(0)

    lowerDisplay= stitchDisplays(display1, display2)
    lowerDisplay.insert(0, line)
    return lowerDisplay


def assembleExpandedSpeciesDisplay():
    display= []

    display.append("")
    gca= genealogy.getGCA(cell.CELLS)
    if gca is None:
        gcaPrint= "None"
    else:
        gcaTaxon= gca.genealogy.taxon
        gcaPrint= "\x1b[" + gcaTaxon.color + "m" + gca.name + "\x1b[0m | \x1b[" + gcaTaxon.color + "m" + gca.genealogy.taxon.genus + " " + gca.genealogy.taxon.species + "\x1b[0m"
    display.append("Last Common Ancestor: " + gcaPrint)

    if not gca is None:
        if gca.lysed:
            display.append("Died " + str(gca.map.totalturns - gca.deathdate) + " Turns Ago")
        else:
            display.append("Current Location: " + gca.location.id)


    display.append("")
    display.append("Extant Species:")
    display.append("------------------")

    #this list will contain all currently extant species
    currentSpecies= []
    #this list will contain the number of the extant species at the matchiong index in currentSpecies
    currentSpeciesCount= []
    #this loop checks each living cell and adds their species to the list of extant species, or adds 1 to the count for that sopecies if it is already listed

    for liveCell in cell.CELLS:
        taxon= liveCell.genealogy.taxon
        if taxon in currentSpecies:
            currentSpeciesCount[currentSpecies.index(taxon)] += 1
        else:
            currentSpecies.append(taxon)
            currentSpeciesCount.append(1)
    
    #this is for later use when constructing the phylogeny display. It is copied now before the species are all popped from the original currentSpecies list
    phylogenyCurrentSpecies= currentSpecies.copy()

    #figure out whihc species has the longest display name to allow for alligning of member count in the display
    speciesDisplayLengths= []
    for s in currentSpecies:
        speciesDisplayLengths.append(len(s.genus + " " + s.species))
    maxSpeciesDisplayLength= max(speciesDisplayLengths)

    spacer= ""
    for c in range(0, maxSpeciesDisplayLength):
        spacer += " "
         
    displayedSpeciesCount=0
    
    #while current species is not the empty list: find the species with the most living members, and add it to the speciesDisplayList, repeat until alll species have been appended in order of most to least members
    while currentSpecies:
        count= 0
        species= None
        maxIndex= 0
        for i in range(0, len(currentSpeciesCount)):
            if currentSpeciesCount[i] > count:
                count= currentSpeciesCount[i]
                species= currentSpecies[i]
                maxIndex= i
        display.append("\x1b[" +species.color + "m" + species.genus + " " + species.species + "\x1b[0m " + spacer[:maxSpeciesDisplayLength-speciesDisplayLengths[maxIndex]] + str(currentSpeciesCount[maxIndex]) + " Doplings")
        displayedSpeciesCount+= 1
        if displayedSpeciesCount <=3:
            display.append("")
        currentSpeciesCount.pop(maxIndex)
        currentSpecies.pop(maxIndex)
        speciesDisplayLengths.pop(maxIndex)



    if not gca is None:
        display.append("")
        phylogenyCurrentSpecies.append(gcaTaxon)
        phylogenyDisplay= assemblePhylogenyDisplay(gcaTaxon, phylogenyCurrentSpecies)
        if PHYLOGENYBOTTOMDISPLAY:
            BOTTOM_DISPLAY.extend(phylogenyDisplay)
        else:
            display.extend(phylogenyDisplay)

    return display


#returns a list display of the phylogeny for Taxon gcaTaxon containg all displayed species. All taxons in displayedSpecies must decend from or be gcaTaxon
def assemblePhylogenyDisplay(gcaTaxon, displayedSpecies):
    #if this taxon is extinct and has no descended taxons: return the empty list (this means it will not be displayed)
    if gcaTaxon.isExtinct and (not gcaTaxon.descendedTaxons) and (not gcaTaxon in displayedSpecies):
        return []

    display=[]

    if gcaTaxon in displayedSpecies:
        display.append("\x1b[" + gcaTaxon.color + "m" + gcaTaxon.genus[0] + ". " + gcaTaxon.species + "\x1b[0m")
        gcaNameLength= len(gcaTaxon.genus[0] + ". " + gcaTaxon.species)
    else:
        display.append("X")
        gcaNameLength= len(display[0])

    spacer= ""
    for i in range(0, gcaNameLength):
        spacer+= " "
    #gcaPhylogeny= genealogy.generatePhylogeny(gcaTaxon)
    descendants= 0
    for descendant in gcaTaxon.descendedTaxons:
      
        descendantPhylogenyDisplay= assemblePhylogenyDisplay(descendant, displayedSpecies)
        #if the returned display is not the empty list:
        if descendantPhylogenyDisplay:
            descendants+= 1
            if descendants == 1:           
                display[0]= display[0] + "--" + descendantPhylogenyDisplay[0]
            else:
                descendantPhylogenyDisplay[0]=  "|_" + descendantPhylogenyDisplay[0]

            for lineIndex in range(0, len(descendantPhylogenyDisplay)):
                #if descendantPhylogenyDisplay[lineIndex][0] == " ":
                 #   descendantPhylogenyDisplay[lineIndex]= spacer + "| " + descendantPhylogenyDisplay[lineIndex][1:]
                if lineIndex == 0:
                    descendantPhylogenyDisplay[lineIndex]= spacer + descendantPhylogenyDisplay[lineIndex]
                else:
                    descendantPhylogenyDisplay[lineIndex]= spacer + "  " + descendantPhylogenyDisplay[lineIndex]
                
            #this line has already been appended to the display so it needs to be removed before the next one is appended
            if descendants == 1:
                descendantPhylogenyDisplay.pop(0)

            display.extend(descendantPhylogenyDisplay)

    if gcaTaxon.isExtinct and (descendants == 0):
        return []

    return display

#tracks multiple cells and returns display
def assembleMultitrackDisplay():
    
    #list that will contain all extant species in order from most to least living members
    currentSpecies= []
    for liveCell in cell.CELLS:
        taxon= liveCell.genealogy.taxon
        if not taxon in currentSpecies:
            i= 0
            taxonLivingCells= len(taxon.memberlist) - taxon.deadMembers
            while i < len(currentSpecies) and (taxonLivingCells < (len(currentSpecies[i].memberlist) - currentSpecies[i].deadMembers)):
                i+= 1
            currentSpecies.insert(i, taxon)


    display=[]
    #add key for + and - indicators
    display.append("")
    display.append("Key: \x1b[41m--\x1b[0m <-5  \x1b[41m-\x1b[0m <-2  \x1b[31m--\x1b[0m <-1  \x1b[31m-\x1b[0m <-0.1  \x1b[32m+\x1b[0m >0.1  \x1b[32m++\x1b[0m >1  \x1b[42m+\x1b[0m >2  \x1b[42m++\x1b[0m >5")
    display.append("")
    numDisplays= 0
    while numDisplays < 3 and numDisplays < len(currentSpecies):
        taxon= currentSpecies[numDisplays]
        memberIndex= 0
        stillSearching= True
        while stillSearching and memberIndex < len(taxon.memberlist) -1:
            if taxon.memberlist[memberIndex].lysed:
                memberIndex+= 1
            else:
                stillSearching= False
        multitrackedCell= taxon.memberlist[memberIndex]
        multitrackedCell.genealogy.track("multitrack")
        display.append("\x1b[" + taxon.color + "m" + taxon.genus + " " + taxon.species + "\x1b[0m" + " ~ " + str(len(taxon.memberlist) - taxon.deadMembers) + " Alive ~ " + str(taxon.generations) + " Gens since Turn " + str(taxon.advent))
        display.append("Oldest Member: " + "\x1b[" + multitrackedCell.genealogy.color + "m" + multitrackedCell.fullname() + "\x1b[0m" + " ~ " + str(multitrackedCell) + " ~ Gen: " + str(multitrackedCell.genealogy.generation))
        #remove valuline from track cell display
        display.extend(assembleModTableDisplay(multitrackedCell)[1:])
        display.append("")
        display.extend(assembleMovTableDisplay(multitrackedCell))
        display.append("")
        numDisplays+=1
    return display

#creates printable table representation of trackedCell's modtable and partial valuetable with key
def assembleModTableDisplay(trackedCell):
    display=[]
    valuesLine= " #: |"
    for v in range(0, cell.MOD_INDEX.index("food")):
        valuesLine+= str(trackedCell.valuetable[v]) + " |"
    display.append(valuesLine)
    display.append("In:  NE NF NC SE SF SC EE EF EC WE WF WC Fd Th Sc Pl Dr Up Dw Rt Lf")
    messengersI=  ["Th: ", "Sc: ", "Pl: ", "Dr: "]
    for m in range(len(messengersI)):
        tableLine= messengersI[m]
        for v in range(len(trackedCell.valuetable)):
            tableLine+= "|" + convertModDisplay(trackedCell.modtable[v][m])
        display.append(tableLine + "|")

    return display

#creates printable table representation of trackedCell's movementtable
def assembleMovTableDisplay(trackedCell):
    display= []
    display.append("In:    Th     Sc     Pl     Dr")
    proteinsI=  ["Up: ", "Dw: ", "Rt: ", "Lf: "]
    for p in range(len(proteinsI)):
        tableLine= proteinsI[p]
        # next loop uses length of movement table to determine number of messenger hormones
        for m in range(len(trackedCell.movementtable)):
            tableLine+= "|" + convertMovDisplay(trackedCell.movementtable[m][p])
        display.append(tableLine + "|")

    return display

#converts modtable value (mod) into display ready length 2 str with specified color/highlighting based on value
def convertModDisplay(mod):
    if (mod < 0.1) and (mod > -0.1):
        return "0 "
    if mod > 5: 
        return "\x1b[42m++\x1b[0m"
    if mod > 2:
        return "\x1b[42m+\x1b[0m "
    if mod > 1:
        return "\x1b[32m++\x1b[0m"
    if mod > 0:
        return "\x1b[32m+\x1b[0m "
    if mod < -5:
        return "\x1b[41m--\x1b[0m"
    if mod < -2:
        return "\x1b[41m-\x1b[0m "
    if mod < -1:
        return "\x1b[31m--\x1b[0m"
    if mod < 0:
        return "\x1b[31m-\x1b[0m "

#converts movementtable value (mov) into display ready length 6 str for use in cell tracking display
def convertMovDisplay(mov):
    color= ""
    if mov > 2:
        color= "\x1b[42m"
    elif mov > 0.1:
        color= "\x1b[32m"
    elif mov < -2:
        color= "\x1b[41m"
    elif mov < -0.1:
        color= "\x1b[31m"
    printableMov= str(round(mov, 2))
    mLen= len(printableMov)

    if mLen > 6:
        printableMov= printableMov[:6]

    #spacers contains 6 lists, one for each possible sub-6 length (0-5) of printableMov,  
    #each contain a pair of frontend and backend blank spaces to center the test in the printed table
    spacers= [["   ", "   "], ["  ", "   "], ["  ", "  "], [" ", "  "], [" ", " "], ["", " "]]
    if mLen < 6:
        #now printable mov is length 6
        printableMov= spacers[mLen][0] + printableMov + spacers[mLen][1]
    return color + printableMov + "\x1b[0m"


#adds relevent strings to list display for displaying trackedCell information and returns the display
def assembleTrackedCellDisplay(trackedCell):
    display=[]
    display.append("")
    display.append("Tracking: \x1b[" + trackedCell.genealogy.color + "m" + trackedCell.fullname() + "\x1b[0m | " + str(trackedCell) + " | \x1b[" +trackedCell.genealogy.taxon.color + "m" + trackedCell.genealogy.taxon.genus + " " + trackedCell.genealogy.taxon.species + "\x1b[0m")
    status= "\x1b[32mAlive\x1b[0m" 
    if trackedCell.lysed:
        status="\x1b[31mDead\x1b[0m (Turn "+ str(trackedCell.deathdate) + ") " + trackedCell.deathmessage
    #display.append("Status: " + status)
    display.append("Location: " + trackedCell.location.id + " | Status: " + status)
    #display.append("Species: \x1b[" +trackedCell.genealogy.taxon.color + "m" + trackedCell.genealogy.taxon.genus + " " + trackedCell.genealogy.taxon.species + "\x1b[0m")


    display.append("")
    display.append("\x1b[36mProgeny\x1b[0m and \x1b[35mAncestors\x1b[0m are highlighted")

    display.append("")
    display.append("Currently Thinking:")
    display.append('"' + thoughts.think(trackedCell) + '"')

    display.append("")
    foodAlert= ""
    if trackedCell.valuetable[cell.MOD_INDEX.index("food")]/inputs.FOOD_TO_MOVE < 20:
        foodAlert= "\x1b[31m"
    display.append("Food: " + foodAlert + str(trackedCell.valuetable[cell.MOD_INDEX.index("food")])[:5] + "\x1b[0m" + " | Split @ " + str(trackedCell.splitThreshold)[:5] + " | Speed: 522.2")
    display.append("Age: " + str(trackedCell.age))
    display.append("Generation: " + str(trackedCell.genealogy.generation))
    display.append("Children: " + str(len(trackedCell.genealogy.children)))
    if not(trackedCell.genealogy.mother is None):
        display.append("Siblings: " + str(len(trackedCell.genealogy.mother.children)-1))
    
    display.append("")
    display.append("Messenger Hormones:")
    display.append("")
    messengerValues=[trackedCell.valuetable[cell.MOD_INDEX.index("thinkin")], trackedCell.valuetable[cell.MOD_INDEX.index("schemin")], trackedCell.valuetable[cell.MOD_INDEX.index("plottin")], trackedCell.valuetable[cell.MOD_INDEX.index("dreamin")]]
    messengerMax= max(messengerValues)
    barGraph="|||||||||||||||||||||"#                                                         \/prevents divide by zero
    display.append("Thinkin:\x1b[44m " + barGraph[:((round((messengerValues[0]/(messengerMax+.0001))*20)))] + "\x1b[0m" + str(round(messengerValues[0], 1)))
    display.append("Schemin:\x1b[42m " + barGraph[:((round((messengerValues[1]/(messengerMax+.0001))*20)))] + "\x1b[0m" + str(round(messengerValues[1], 1)))
    display.append("Plottin:\x1b[41m " + barGraph[:((round((messengerValues[2]/(messengerMax+.0001))*20)))] + "\x1b[0m" + str(round(messengerValues[2], 1)))
    display.append("Dreamin:\x1b[45m " + barGraph[:((round((messengerValues[3]/(messengerMax+.0001))*20)))] + "\x1b[0m" + str(round(messengerValues[3], 1)))

    display.append("")
    display.append("Movement Proteins:")
    display.append("")
    movementValues=[trackedCell.valuetable[cell.MOD_INDEX.index("upin")], trackedCell.valuetable[cell.MOD_INDEX.index("downin")], trackedCell.valuetable[cell.MOD_INDEX.index("rightin")], trackedCell.valuetable[cell.MOD_INDEX.index("leftin")]]
    movementMax= max(movementValues)
    display.append("Upin   :\x1b[47m " + barGraph[:((round((movementValues[0]/(movementMax+.0001))*20)))] + "\x1b[0m" + str(round(movementValues[0], 1)))
    display.append("Downin :\x1b[43m " + barGraph[:((round((movementValues[1]/(movementMax+.0001))*20)))] + "\x1b[0m" + str(round(movementValues[1], 1)))
    display.append("Rightin:\x1b[47m " + barGraph[:((round((movementValues[2]/(movementMax+.0001))*20)))] + "\x1b[0m" + str(round(movementValues[2], 1)))
    display.append("Leftin :\x1b[43m " + barGraph[:((round((movementValues[3]/(movementMax+.0001))*20)))] + "\x1b[0m" + str(round(movementValues[3], 1)))

    display.append("")
    display.extend(assembleModTableDisplay(trackedCell))
    #add key for + and - indicators
    display.append("")
    display.append("Key: \x1b[41m--\x1b[0m <-5  \x1b[41m-\x1b[0m <-2  \x1b[31m--\x1b[0m <-1  \x1b[31m-\x1b[0m <-0.1  \x1b[32m+\x1b[0m >0.1  \x1b[32m++\x1b[0m >1  \x1b[42m+\x1b[0m >2  \x1b[42m++\x1b[0m >5")
    display.append("")
    display.extend(assembleMovTableDisplay(trackedCell))
    # valuesLine= " #: |"
    # for v in range(0, cell.MOD_INDEX.index("food")):
    #     valuesLine+= str(trackedCell.valuetable[v]) + " |"
    # display.append(valuesLine)
    # display.append("In:  NE NF NC SE SF SC EE EF EC WE WF WC Fd Th Sc Pl Dr Up Dw Rt Lf")
    # messengersI=  ["Th: ", "Sc: ", "Pl: ", "Dr: "]
    # for m in range(len(messengersI)):
    #     tableLine= messengersI[m]
    #     for v in range(len(trackedCell.valuetable)):
    #         tableLine+= "|" + convertModDisplay(trackedCell.modtable[v][m])
    #     display.append(tableLine + "|")

    # #add key for + and - indicators
    # display.append("")
    # display.append("Key: \x1b[41m--\x1b[0m <-5  \x1b[41m-\x1b[0m <-2  \x1b[31m--\x1b[0m <-1  \x1b[31m-\x1b[0m <-0.1  \x1b[32m+\x1b[0m >0.1  \x1b[32m++\x1b[0m >1  \x1b[42m+\x1b[0m >2  \x1b[42m++\x1b[0m >5")

    # display.append("")
    # display.append("In:    Th     Sc     Pl     Dr")
    # proteinsI=  ["Up: ", "Dw: ", "Rt: ", "Lf: "]
    # for p in range(len(proteinsI)):
    #     tableLine= proteinsI[p]
    #     # next loop uses length of movement table to determine number of messenger hormones
    #     for m in range(len(trackedCell.movementtable)):
    #         tableLine+= "|" + convertMovDisplay(trackedCell.movementtable[m][p])
    #     display.append(tableLine + "|")

    return display



#prints a pedigree depicting all living cells descended from the greatest common anscestor
def printPedigree():
    gca= genealogy.getGCA(cell.CELLS)
    if gca is None:
        print("No GCA for all currently living cells")
        return
    pedigree= genealogy.generatePedigree(gca)

    print("\nPedigree: Turn #" + str(gca.map.totalturns))
    print("-----------------------------------")
    print("Key:")
    print("species originators are \x1b[43mhighlighted\x1b[0m")
    print("living doplings are \x1b[4munderlined\x1b[0m")
    print("dead doplings are not underlined\n")

    pedigreeDisplay= generatePedigreeDisplay(pedigree)
    for line in pedigreeDisplay:
        print(line)




#retruns a display list of lines to be printed for the pedigree display, takes pedigree tuple from genealogy.generatePedigree as input
#recurses
def generatePedigreeDisplay(pedigree):
    display= []
    descendantPedigreeDisplays= []

    for descendantPedigree in pedigree[1]:
        descendantPedigreeDisplay= generatePedigreeDisplay(descendantPedigree)
        if descendantPedigreeDisplay:
            descendantPedigreeDisplays.append(descendantPedigreeDisplay)

    #if there are descendantPedigreeDisplays:
    if descendantPedigreeDisplays:

        #make all lists in descendantPedigreeDisplays the same length by appending matching size blank space strings to the lists
        firstDPD= descendantPedigreeDisplays[0] 
        for dpdIndex in range(0, len(descendantPedigreeDisplays)):
            #print(descendantPedigreeDisplays)
            if len(descendantPedigreeDisplays[dpdIndex]) > len(firstDPD):
                for extendIndex in range(0, dpdIndex):
                    while len(descendantPedigreeDisplays[dpdIndex]) > len(descendantPedigreeDisplays[extendIndex]):
                        descendantPedigreeDisplays[extendIndex].append(" " * len(removeANSI(descendantPedigreeDisplays[extendIndex][0])))

            elif len(firstDPD) > len(descendantPedigreeDisplays[dpdIndex]):
                while  len(firstDPD) > len(descendantPedigreeDisplays[dpdIndex]):
                    #print(descendantPedigreeDisplays[dpdIndex])
                    descendantPedigreeDisplays[dpdIndex].append(" " * len(removeANSI(descendantPedigreeDisplays[dpdIndex][0])))
        
        #create '|' and blank spacer above each descendant pedigree
        connector= ""
        for dpdIndex in range(0, len(descendantPedigreeDisplays)):
            connector+= ("|") #+ (" " * (len(removeANSI(descendantPedigreeDisplays[dpdIndex][0])) +1))
            if dpdIndex < (len(descendantPedigreeDisplays) -1):
                connector+= (" " * (len(removeANSI(descendantPedigreeDisplays[dpdIndex][0])) +1))
            else:
                connector+= (" " * (len(removeANSI(descendantPedigreeDisplays[dpdIndex][0])) -1))
            # if (len(removeANSI(descendantPedigreeDisplays[dpdIndex][0]))) == 1:
            #     connector+= " "
        display.insert(0, connector)

        #merge all lists in descendantPedigreeDisplays by stitching together the lists at index 0 and 1, then popping the list at index 1 and repeating the process
        while len(descendantPedigreeDisplays) > 1:
            for dpdLineIndex in range(0, len(descendantPedigreeDisplays[0])):
                descendantPedigreeDisplays[0][dpdLineIndex]+= "  " + descendantPedigreeDisplays[1][dpdLineIndex]
            descendantPedigreeDisplays.pop(1)

        displayLen= len(removeANSI(descendantPedigreeDisplays[0][0]))
        
        #add merged descendantPedigreedisplays to display
        display.extend(descendantPedigreeDisplays[0])

        if connector.count("|") > 1:
            #add top bar
            horizontalBar= "|" + ("_" * (connector.rindex("|")))
            horizontalBar+= (" " * (displayLen - len(horizontalBar)))
            display.insert(0, horizontalBar)
            #display.insert(0, ("-" * displayLen))

            #add second '|' connector line
            speciesName= pedigree[0].genealogy.taxon.genus +  " " + pedigree[0].genealogy.taxon.species
            speciesNameLength= len(speciesName)
            if displayLen > speciesNameLength + 3:
                display.insert(0, "| " + "\x1b[" + pedigree[0].genealogy.taxon.color + "m" + speciesName + "\x1b[0m" + (" " * (displayLen-speciesNameLength-2)))
            else:
                display.insert(0, ("|" + (" " * (displayLen-1))))

        #add pedigree cell str
        display.insert(0, (pedigreeString(pedigree[0]) + (" " * (displayLen-1))))

        return display
        
    

    #if there are no descendantPedigreeDisplays:
    else:
        #if pedigree cell is alive
        if pedigree[0] in cell.CELLS:
            #return str of pedigree cell
            return [pedigreeString(pedigree[0])]
        #if pedigree cell is dead:
        else:
            return []

            
#returns str coloredText without ANSCI sequence(s)
def removeANSI(coloredText):
    quarterCleaned= re.sub("\\x1b\[4m", "", coloredText)
    halfCleaned= re.sub("\\x1b\[.{2}m", "", quarterCleaned)
    cleaned=  re.sub("\\x1b\[0m", "", halfCleaned)
    return cleaned

def pedigreeString(pedigreeCell):
    letter= removeANSI(str(pedigreeCell))

    originatorHighlight= ""
    if pedigreeCell == pedigreeCell.genealogy.taxon.originator:
        originatorHighlight= "\x1b[4" + pedigreeCell.genealogy.color[1:] + "m"

    if pedigreeCell.lysed:
        return "\x1b[" + pedigreeCell.genealogy.color + "m" + pedigreeCell.genealogy.tracking + originatorHighlight + letter + "\x1b[0m"
    else:
        return "\x1b[4m\x1b[" + pedigreeCell.genealogy.color + "m" + pedigreeCell.genealogy.tracking + originatorHighlight + letter + "\x1b[0m"
