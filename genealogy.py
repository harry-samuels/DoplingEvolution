import cell as cellModule
import grid

import random

#this list contains the genealogy object of all cells currently being tracked
TRACKED_CELLS= []

#the Genealogy class keeps track of a cells ancestors (who it split from, and who that cell split from before that, etc.)
"""
Genealogy Class instance variables:
-------------------------------------------------
Cell cell                  : the cell that this genealogy object represents
Genealogy mother           : the genealogy of the cell that the aforementioned cell split from, None if  cell was spontaneously generated
str color                  : string that is used to determine the color of the cell by class Cell when it is printed
list children              : list of genealogy objects representing all cells split from this cell
int generation             : number of cells between this cell and the spontaneously generated "originator", 0 if this is the first cell in the lineage
bool nextchildmegamutation : True if the most recently split child had a megamutation (this is used to change the child's color), False at all other times except when megamutated new child is initializing
str tracking               : represents if the cell is currently being tracked by the user, ="" if the cell is not being tracked, =ANSI escape seq for backround color if being tracked
str tracktype              : type of tracking being performed on this cell ("main", "offspring", "ancestor"), ="" if tracking == ""
Taxon taxon                : the Taxon object for this cell's species
"""
class Genealogy:
    #genealogy init inputs:
    #Cell cell: the cell represented by this genealogy
    #Genealogy mothergenealogy: genealogy object for the mother of this cell, if it was split from another cell
    def __init__(self, cell, mothergenealogy=None):
        self.cell= cell

        #set self.mother and match color to mother if not None
        if mothergenealogy is None:
            self.mother= None
            self.generation= 0
            self.color= random.choice(["31","32","33","34","35","36"])
            self.children=[]
            self.tracking= ""
            self.tracktype= ""
            self.taxon= Taxon(self)
        else:
            self.mother= mothergenealogy
            self.mother.children.append(self)
            self.generation= self.mother.generation + 1

            #check if this cell had a MegaMutation and change color from mother's color if True
            if self.mother.nextchildmegamutation:
                #create a list of possible colors and remove the mother cell's color from the options before randomly choosing a color
                coloroptions= ["31","32","33","34","35","36"]
                coloroptions.pop(coloroptions.index(self.mother.color))
                self.color= random.choice(coloroptions)
                #reset the mother's nextchildmegamutation to False to prevent next split from being impacted
                self.mother.nextchildmegamutation= False

                self.taxon= Taxon(self)

            else:
                self.color= self.mother.color
                self.mother.taxon.addToSpecies(self)

            self.children=[]
            #check if mother cell is being tracked and initialize correct self.tracking and self.tracktype values
            self.initializeTracking()

        
        self.nextchildmegamutation= False

    #begin tracking cell and assign proper values to self.tracking and self.tracktype based on str input tracktype
    #this function recurses in a DFS in order to track all offspring (children and children's children etc.) and direct ancestors of main cell
    def track(self, tracktype):
        TRACKED_CELLS.append(self)
        if tracktype == "main":
            self.tracktype= "main"
            #set backround color to white
            self.tracking= "\x1b[47m"
            #Apply offspring tracking to all decendents of this cell using DFS
            for c in self.children:
                c.track("offspring")
            #if cell has mother apply ancestor tracking to all prior cells in lineage
            if not (self.mother is None):
                    self.mother.track("ancestor")
        elif tracktype == "offspring":
            self.tracktype= "offspring"
            self.tracking= "\x1b[46m"

            #Apply offspring tracking to all decendents of this cell using DFS
            for c in self.children:
                c.track("offspring")
        elif tracktype == "ancestor":
            self.tracktype= "ancestor"
            self.tracking= "\x1b[45m"
            #track all ancestor cells of this cell
            if not (self.mother is None):
                #prevents recusion error by stopping after dead ancestor is found
                if not self.mother.cell.lysed:             
                    self.mother.track("ancestor")
        elif tracktype == "multitrack":
            self.tracktype= "multitrack"
            #underline
            self.tracking= "\x1b[4m"
        elif tracktype == "species1":
            self.tracktype == "species1"
            self.tracking= "\x1b[47m"
        elif tracktype == "species2":
            self.tracktype == "specie2"
            self.tracking= "\x1b[46m"
        elif tracktype == "species3":
            self.tracktype == "species3"
            self.tracking= "\x1b[45m"


    #stop tracking cell
    def untrack(self):
        TRACKED_CELLS.pop(TRACKED_CELLS.index(self))
        self.tracking= ""
        self.tracktype= ""

    #set inital self.tracking and self.tracktype values based on mother cell's tracking status
    #only able to be used on cells that were not spontaneously generated (ie: were split from another cell)
    def initializeTracking(self):
        #if mother cell is not being tracked, both values are the empty string
        if self.mother.tracking == "":
            self.tracking= ""
            self.tracktype= ""
            return
        #if the mother cell is being tracked as the ancestor of anopther cell, both values are the empty string
        elif self.mother.tracktype == "ancestor":
            self.tracking= ""
            self.tracktype= ""
            return
        #if the mother cell si being tracked as the main cell or as offspring, the cell is being tracked as "offspring"
        elif self.mother.tracktype == "main" or self.mother.tracktype == "offspring":
            self.track("offspring")
            return
        #non-heritable tracktypes
        else:
            self.tracking= ""
            self.tracktype= ""


#untrack all cells being tracked
def untrackAll(map):
    map.trackedCell= None
    for tracked_cell in range(0,len(TRACKED_CELLS)):
        TRACKED_CELLS[tracked_cell].tracking= ""
        TRACKED_CELLS[tracked_cell].tracktype= ""
    TRACKED_CELLS.clear()





# The Taxon Class represents a given species and keeps track of which cells are members of that species
"""
Taxon Class instance variables:
-----------------------------------
Cell originator      : the cell object of the first member of this species, from which all other members of the species are descended
list memberlist      : memberlist contains all members of the species that have existed, ordered from the originator to the most recent 
str color            : str of the two digit number from the ANSI sequence for the color of this species
int advent           : turn that this species was first created
int generations      : number of generations between the originator and the cell of this species with the highest generation
Taxon descendedFrom  : the Taxon for the mother of the originator, None if the originator was spontaneously generated
str genus            : name of the Genus for this species, the Genus name is the mother's species' name, or 'deus' if the originator was spontaneusly generated
str species          : name of the Species, randomly generated based on the originator's name
list descendedTaxons : contains all Taxons directly descended from this taxon
bool isExtinct       : False if there exist living members of this Species, True if all members of this species have been lysed
int deadMembers      : number of dead members of this Species
"""
class Taxon:
    #inputs: Geanealogy originatorGenealogy, the Genealogy object for the first cell of this species
    #        Grid map, the map that contains this cell
    def __init__(self, originatorGenealogy):
        self.originator= originatorGenealogy.cell
        self.memberlist= [self.originator]
        self.color= originatorGenealogy.color
        self.advent= self.originator.map.totalturns
        self.generations= 0
        self.descendedTaxons= []
        self.isExtinct= False
        self.deadMembers= 0

        if originatorGenealogy.mother is None:
            self.descendedFrom= None
            self.genus= "deus"
        else:
            self.descendedFrom= originatorGenealogy.mother.taxon
            self.genus= originatorGenealogy.mother.taxon.species
            self.descendedFrom.descendedTaxons.append(self)
            
        
        self.species= originatorGenealogy.cell.name[:len(self.originator.name)//2] + random.choice(["eus", "iens", "ococcus", "es", "us", "ans", "ae", "era", "dae", "pi", "ca", "sis"])


    #adds cell to this species and sets its taxon to this taxon
    def addToSpecies(self, cellGenealogy):
        #set cell's taxon in genealogy object and add the cell to the species memberlist
        cellGenealogy.taxon= self
        self.memberlist.append(cellGenealogy.cell)

        #if the generation gap between this cell in the original is larger than any previuous gap within the species, update self.generations
        if (cellGenealogy.generation - self.originator.genealogy.generation) > self.generations:
            self.generations= cellGenealogy.generation - self.originator.genealogy.generation

    def addDeadMember(self):
        self.deadMembers+= 1
        if self.deadMembers == len(self.memberlist):
            self.isExtinct= True


#returns the originator of the taxon which represents the greatest common ancestor of all cells in list cellList, returns None if no GCA exists
#cellList is a list of Cell objects
def getGCA(cellList):
    #check if cellList is empty
    if cellList:
        firstCell= cellList[0]
        taxonHistory= []
        listTaxon= firstCell.genealogy.taxon
        #create a list of all taxons that the first cell in cellList is descended from
        while (not listTaxon is None):
            taxonHistory.append(listTaxon)
            listTaxon= listTaxon.descendedFrom

        gcaTaxonIndex= 0
        # check all cells in cellList 
        for comparedCell in cellList:
            noGCA= True
            #increment gcaTaxonIndex if none of the cells in this lineage belong to the Taxon at taxonHistory[gcaTaxonIndex] and check again, 
            # stop checking if gcaTaxonIndex exce4eds the length of the taxonHistory list
            while noGCA and (len(taxonHistory) > gcaTaxonIndex):
                comparedTaxon= comparedCell.genealogy.taxon
                #check if each taxon in this lineage matches the taxon at gcaTaxonIndex
                while noGCA and (not comparedTaxon is None):
                    if comparedTaxon == taxonHistory[gcaTaxonIndex]:
                        noGCA= False
                    else:
                        comparedTaxon= comparedTaxon.descendedFrom
                if noGCA:
                    gcaTaxonIndex+=1
        if noGCA:
            return None
        else:
            return taxonHistory[gcaTaxonIndex].originator
                
    return None


#returns a phylogeny in tuple/list (detailed below) form that contains all taxons descended from gcaTaxon
"""
Example phylogeny and return

phylogeny (each letter represents a taxon):

      A
______|______
|            |
B            C
             |
        _____|_____
        |    |    |
        D    E    F
                  |
                  G

generatePhylogeny(A) output: (A , [ (B, []) , (C, [ (D,[]) , (E,[]) , (F, [(G,[])]) ]) ])
generatePhylogeny(F) output: ( F, [ (G , []) ] )

"""
def generatePhylogeny(gcaTaxon):
    #the first element of the tuple contains the taxon, and the second contains a list tuples for each of its descents and their descendants etc.
    #this tuple with an empty list will be returned if the gcaTaxon has no descended Taxons
    phylogeny= (gcaTaxon, [])
    for tax in gcaTaxon.descendedTaxons:
        phylogeny[1].append(generatePhylogeny)
    
    return phylogeny


#returns a pedigree containing all cells decended from gca that are currently alive or are the ancestors of living cells
"""
Example pedigree and return

Pedigree (each letter represents a cell):

      A
______|______
|            |
B            C
             |
        _____|_____
        |    |    |
        D    E    F
                  |
                  G

generatePedigree(A) output: (A , [ (B, []) , (C, [ (D,[]) , (E,[]) , (F, [(G,[])]) ]) ])
generatePedigree(F) output: ( F, [ (G , []) ] )

"""
#the first element of the tuple contains the gca, and the second contains a list tuples for each of its descents and their descendants etc.
#this tuple with an empty list will be returned if the gca has no descendants
def generatePedigree(gca):
    pedigree= (gca, [])
    for child in gca.genealogy.children:
        pedigree[1].append(generatePedigree(child.cell))
    return pedigree











    