import grid
import genealogy
import inputs

import random
import copy

#List of all current living cells
CELLS= []
#List of all cells that have existed or currently existy in the game. Each cell's numberID unique corresponds to its index in the list
ALL_CELLS= []


MESSENGERS= ["thinkin", "schemin", "plottin", "dreamin", "electin", "choosin", "decidin", "figurin", "wafflin", "waverin"][:inputs.MESSENGER_PROTEIN_NUMBER]

PROTEINS= ["upin", "downin", "rightin", "leftin"]

BASE_MOD_INDEX= [
    "Nempty","Nfood", "Ncell", "Nsize",
    "Sempty","Sfood", "Scell", "Ssize",
    "Eempty","Efood", "Ecell", "Esize",
    "Wempty","Wfood", "Wcell", "Wsize",
    "food"]

MOD_INDEX= BASE_MOD_INDEX + MESSENGERS + PROTEINS

DEFAULT_VALUE_TABLE= dict.fromkeys(MOD_INDEX, 0)

NUM_GENE_ADD_DELETE= 0 #DEBUG
NUM_FULL_GENE_DUPES= 0 #DEBUG
NUM_MEGAMUTATIONS= 0 #DEBUG

#adds newly generated cell to list of living Cells at the correct speed postion. CELLS is ordered from fastest (greatest speed) to slowest cells
#This method keeps the list sorted
def addtoCELLS(newCell, cellSpeed):
    i= 0
    while i < len(CELLS) and cellSpeed < CELLS[i].speed:
        i+= 1
    CELLS.insert(i, newCell)

#mutates, mod, mov, and value table and returns them. Also processes gene/genome duplication
def mutateGenome(modtable, movementtable, valuetable, parent):
    modtable= mutate(modtable, parent)
    movementtable= mutate(movementtable, parent)
    proteinInfo= {}
    if random.randint(0, 2000) < (len(parent.messengers)):
        parent.nextchildmegamutation= True
        new_messengers= copy.deepcopy(parent.messengers)
        if random.randint(0,10) == 0: #random.randint(0,4) == 0:
            #full genome duplication
            #print("FULL GENOME DUPE!!!!!!!!!!!!!!!!!!!!!!!!!! ! ! ! ! ! ! ") #DEBUG
            #global NUM_FULL_GENE_DUPES #DEBUG
            #NUM_FULL_GENE_DUPES+= 1 #DEBUG
            for duplicatedMessenger in parent.messengers:
                newMessenger= nameDuplicatedGene(duplicatedMessenger)
                new_messengers.insert(new_messengers.index(duplicatedMessenger), newMessenger)
                modtable, movementtable, valuetable= duplicateGene(newMessenger, duplicatedMessenger, modtable, movementtable, valuetable)

        else:
            global NUM_GENE_ADD_DELETE #DEBUG
            NUM_GENE_ADD_DELETE+= 1 #DEBUG
            if random.randint(0,1) == 0:
                #print("DUPLICATION OF GENE!!!!!") #DEBUG
                #single gene duplication
                duplicatedMessengerIndex= random.randint(0, len(parent.messengers)-1)
                duplicatedMessenger= parent.messengers[duplicatedMessengerIndex]
                newMessenger= nameDuplicatedGene(duplicatedMessenger)

                new_messengers.insert(duplicatedMessengerIndex, newMessenger)
                modtable, movementtable, valuetable= duplicateGene(newMessenger, duplicatedMessenger, modtable, movementtable, valuetable)

            else:
                #print("DELETION OF GENE!!!!!") #DEBUG
                #single gene removal
                removedMessengerIndex= random.randint(0, len(parent.messengers)-1)
                removedMessenger= parent.messengers[removedMessengerIndex]

                new_messengers.pop(removedMessengerIndex)
                modtable, movementtable, valuetable= removeGene(removedMessenger, modtable, movementtable, valuetable)

            #print(str(NUM_FULL_GENE_DUPES) + " " + str(NUM_GENE_ADD_DELETE) + " " + str(NUM_MEGAMUTATIONS)) #DEBUG

        #print(len(ALL_CELLS)) #DEBUG
        proteinInfo["messengers"]= new_messengers
        proteinInfo["proteins"]= parent.proteins
        proteinInfo["index"]= BASE_MOD_INDEX + new_messengers + parent.proteins


    else:
        proteinInfo["messengers"]= parent.messengers
        proteinInfo["proteins"]= parent.proteins
        proteinInfo["index"]= parent.modIndex
  
    return (modtable, movementtable, valuetable, proteinInfo)

#add mutations to a given 2-D dictionary mod or movement table
def mutate(table, parent):
    for r in table:
        for c in table[r]:
            if random.randint(0, 100) <5:
                if random.randint(0,100) == 1:
                    table[r][c]= table[r][c] * (random.uniform(-5, 5))
                    #this will allow the newly created cell to have a different color from the mother cell using its genealogy init
                    parent.genealogy.nextchildmegamutation= True
                    global NUM_MEGAMUTATIONS#DEBUG
                    NUM_MEGAMUTATIONS+= 1 #DEBUG
                else:
                    table[r][c]= table[r][c] + (random.uniform(-0.99, 0.99))
    return table

#add mutation to splitThreshold
def mutateSplitThreshold(splitThreshold, parent):
    if random.randint(0, 100) < 5:
        if random.randint(0, 100) == 1:
            splitThreshold= splitThreshold * random.choice([random.uniform(0.2, 0.5), random.uniform(2, 5)])
            parent.genealogy.nextchildmegamutation= True
        else:
            splitThreshold= splitThreshold * random.uniform(0.9, 1.1)
    return splitThreshold

def mutateSpeed(speed, parent):
    if random.randint(0, 100) < 5:
        if random.randint(0, 100) == 1:
            speed= speed * random.choice([random.uniform(0.2, 0.5), random.uniform(2, 5)])
            parent.genealogy.nextchildmegamutation= True
        else:
            speed= speed * random.uniform(0.9, 1.1)
    #prevent speed form going below default value
    if speed < inputs.FOOD_TO_MOVE:
        speed= inputs.FOOD_TO_MOVE
    return speed

def nameDuplicatedGene(oldName):
    #WILL NEED TO CHANGE THIS LATER TO BE LESS LONG AFTER 2+ duplications
    newName= oldName + "-" + str(len(ALL_CELLS))
    return newName


#adds newGene (str) to the modtable, movementable, and valuetable by duplicating oldGene (str)
def duplicateGene(newGene, oldGene, modtable, movementtable, valuetable):
    #add newGene as copy of oldGene for all mods in modtable
    for v in modtable:
        modtable[v][newGene]= copy.deepcopy(modtable[v][oldGene])
    #add newGene as value in modtable and copy oldGene mods which now include newGene
    modtable[newGene]= copy.deepcopy(modtable[oldGene])
    movementtable[newGene]= copy.deepcopy(movementtable[oldGene])
    valuetable[newGene]= copy.deepcopy(valuetable[oldGene])
    return(modtable, movementtable, valuetable)

def removeGene(removedGene, modtable, movementtable, valuetable):
    #remove removedGene key from all modtable dictionaries
    for v in modtable:
        del modtable[v][removedGene]
    #remove removedGene dictionary from modtable
    del modtable[removedGene]
    del movementtable[removedGene]
    del valuetable[removedGene]
    return (modtable, movementtable, valuetable)


class Cell:
    SPLIT_SPEED_RATIO= inputs.FOOD_TO_SPLIT / inputs.FOOD_TO_MOVE
    #Grid: map, Node: location, int: food, []: modtable, []: movementtable, []: valuetable
    def __init__(self, map, location, food, modtable=None, movementtable=None, valuetable=None, proteinInfo=None, mothergenealogy=None, splitThreshold=None, speed=None):

        self.age= 0
        self.name= (random.choice(["ba", "po", "li", "re", "xi", "shu", "cra", "psy", "tri", "fro", "woo", "do", "ki", "epi", "ono", "uba", "aro", "immo", "qui", "gra", "hu", "mi", "vee", "yoo", "zo"]) + 
            random.choice(["tep", "xer", "vill", "rax", "dop", "bell", "twip", "zar", "gloop", "bass", "quail", "lint", "jell", "vex", "darg", "wag", "los"]) + 
            random.choice(["allo", "otron", "ling", "forp", "ilious", "udo", "ali", "atic", " ESQ", "erba", "ark", "idious", "indu", "onco", "abongo", "ack"]))

        self.lysed= False
        #deathmessage and deathdate are finalized when cell is lysed (hopefully much later)
        self.deathmessage= ""
        self.deathdate= 0

        self.map= map
        self.map.totalcellsspawned+= 1

        self.location= location
        self.location.insert(self)

        if proteinInfo == None:
            self.messengers= MESSENGERS
            self.proteins= PROTEINS
            self.modIndex= MOD_INDEX
        else:
            self.messengers= proteinInfo["messengers"]
            self.proteins= proteinInfo["proteins"]
            self.modIndex= proteinInfo["index"]
        
        if valuetable is None:
            self.valuetable= copy.deepcopy(DEFAULT_VALUE_TABLE)
            self.valuetable["food"]= food
        else:
            self.valuetable= valuetable
            self.valuetable["food"]= food

        self.modtable= self.generateModTable(modtable)
        self.movementtable= self.generateMovementTable(movementtable)

        self.genealogy= genealogy.Genealogy(self, mothergenealogy)

        #how many other cells this cell has eaten
        self.cellsEaten= 0

        if splitThreshold is None:
            splitThreshold= inputs.FOOD_TO_SPLIT
        self.splitThreshold= splitThreshold
        if speed is None:
            speed= inputs.FOOD_TO_MOVE
        if (splitThreshold / speed) > Cell.SPLIT_SPEED_RATIO:
            speed= splitThreshold / Cell.SPLIT_SPEED_RATIO
        self.speed= speed

        

        #add cell to the list of living cells
        addtoCELLS(self, self.speed)
        #add cell tio list of all cells that have existed
        ALL_CELLS.append(self)
        #set unique identification number corresponding to ALL_CELLS index
        self.numberID= len(ALL_CELLS)-1
        


    def fullname(self):
        return self.name + " (#" + str(self.numberID) + ")"

    def __str__(self):
        alpha= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        classification= self.age//10
        if classification > (len(alpha) -1):
            return "\x1b[" + self.genealogy.color + "m" + self.genealogy.tracking + "&" + "\x1b[0m"
        else:
            return "\x1b[" + self.genealogy.color + "m" + self.genealogy.tracking + alpha[classification] + "\x1b[0m"

    #create a new modifier table, if no mod table is given determine all modifiers randomly, otherwise return the given modtable
    def generateModTable(self, modtable=None):
        if modtable is None:
            modtable= {}
            for v in self.modIndex:
                modtable[v]= {}
                for m in self.messengers:
                    modtable[v][m]= ((random.uniform(0,0.5))**2)*random.choice([-1,1])
            return modtable

        else:
            return modtable

    #create a new movement table, if no movement table is given determine all modifiers randomly, otherwise return the given momovementtable
    def generateMovementTable(self,movementtable=None):
        if movementtable is None:
            movementtable={}
            for m in self.messengers:
                movementtable[m]= {}
                for p in self.proteins:
                    movementtable[m][p]= ((random.uniform(0,0.5))**2)*random.choice([-1,1])
            return movementtable
        else:
            return movementtable 

    #lyse the cell if it is not already lysed, spawn a food object at current location with value equal to own food value
    def lyse(self, deathmessage="adios ;)"):
        if self.lysed:
            return
        self.deathmessage= ("'" + deathmessage + "'")
        self.deathdate= self.map.totalturns
        self.location.clear()
        if self.valuetable["food"] > 0:
            self.map.spawnFood(self.valuetable["food"], self.location)
        self.genealogy.taxon.addDeadMember()
        #self.location= None -->need to keep this value for tracking/report output
        #self.valuetable[MOD_INDEX.index("food")]=0 ---> want to keep this value for tracking as well
        self.lysed= True
        CELLS.pop(CELLS.index(self))

    #moves the cell to an adjacent node, lyses the cell if an impossible move is requested
    def move(self):
        self.age+= 1
        goingTo= None
        #food cost to move
        self.valuetable["food"]-= self.speed 
        if self.valuetable["food"] <= 0:
            self.lyse("hungry :(")

        #ensure the cell is still alive
        if self.lysed:
            return

        self.setSightValues()
        messengerMods= self.calculateMessengerMods()
        self.applyMessengerMods(messengerMods)

        #set negative messenger values to zero
        for m in self.messengers:
            if self.valuetable[m] < 0:
                self.valuetable[m]= 0

        movementMods= self.calculateMovementMods()
        self.applyMovementMods(movementMods)

        #set negative messenger values to zero
        for p in self.proteins:
            if self.valuetable[p] < 0:
                self.valuetable[p]= 0

        #pick direction
        #IDEA GPT suggests probabilistic movement, this is a good idea but does go against my belief that cells are governed purely by physics
        direction= self.pickDirection()

        #ensure the cell is still alive
        if self.lysed:
            return

        #set the correct next location and check if the cell can move there, lyse the cell if it cannot
        if direction == "N":
            goingTo= self.location.north
            self.checkMoveValidity(goingTo)
        elif direction == "S":
            goingTo= self.location.south
            self.checkMoveValidity(goingTo)
        elif direction == "E":
            goingTo= self.location.east
            self.checkMoveValidity(goingTo)
        elif direction == "W":
            goingTo= self.location.west
            self.checkMoveValidity(goingTo)
   
        #ensure the cell is STILL alive
        if self.lysed:
            return
        
        #check if ready to split
        if self.valuetable["food"] > self.splitThreshold:
            self.split(goingTo)
        else:
            #this was above the if statement but i moved it down, this has stimmied evolution it appears
            self.checkFood(goingTo) # <-----
            previousPosition= self.location
            self.location= goingTo
            goingTo.insert(self)
            previousPosition.clear()        
            

    def setSightValues(self):
        #check North
        i= 5
        stillSearching= True
        nextNorth= self.location.north
        while i > 0 and stillSearching:
            if nextNorth is None or nextNorth.isWall():
                self.valuetable["Nempty"]= i
                self.valuetable["Nfood"]= 0
                self.valuetable["Ncell"]= 0
                self.valuetable["Nsize"]= 0
                stillSearching= False
            elif nextNorth.isFood():
                self.valuetable["Nempty"]= 0
                self.valuetable["Nfood"]= i
                self.valuetable["Ncell"]= 0
                self.valuetable["Nsize"]= 0
                stillSearching= False
            elif nextNorth.isFull():
                self.valuetable["Nempty"]= 0
                self.valuetable["Nfood"]= 0
                self.valuetable["Ncell"]= i
                self.valuetable["Nsize"]= nextNorth.contains.valuetable["food"]
                stillSearching= False
            else:
                nextNorth= nextNorth.north
                i= i - 1

        if stillSearching:
            self.valuetable["Nempty"]= 0
            self.valuetable["Nfood"]= 0
            self.valuetable["Ncell"]= 0
            self.valuetable["Nsize"]= 0
            stillSearching= False

        #check south
        i= 5
        stillSearching= True
        nextSouth= self.location.south
        while i > 0 and stillSearching:
            if nextSouth is None or nextSouth.isWall():
                self.valuetable["Sempty"]= i
                self.valuetable["Sfood"]= 0
                self.valuetable["Scell"]= 0
                self.valuetable["Ssize"]= 0                
                stillSearching= False
            elif nextSouth.isFood():
                self.valuetable["Sempty"]= 0
                self.valuetable["Sfood"]= i
                self.valuetable["Scell"]= 0
                self.valuetable["Ssize"]= 0
                stillSearching= False
            elif nextSouth.isFull():
                self.valuetable["Sempty"]= 0
                self.valuetable["Sfood"]= 0
                self.valuetable["Scell"]= i
                self.valuetable["Ssize"]= nextSouth.contains.valuetable["food"]
                stillSearching= False
            else:
                nextSouth= nextSouth.south
                i= i - 1

        if stillSearching:
            self.valuetable["Sempty"]= 0
            self.valuetable["Sfood"]= 0
            self.valuetable["Scell"]= 0
            self.valuetable["Ssize"]= 0
            stillSearching= False


        #check east
        i= 5
        stillSearching= True
        nextEast= self.location.east
        while i > 0 and stillSearching:
            if nextEast is None or nextEast.isWall():
                self.valuetable["Eempty"]= i
                self.valuetable["Efood"]= 0
                self.valuetable["Ecell"]= 0
                self.valuetable["Esize"]= 0
                stillSearching= False
            elif nextEast.isFood():
                self.valuetable["Eempty"]= 0
                self.valuetable["Efood"]= i
                self.valuetable["Ecell"]= 0
                self.valuetable["Esize"]= 0
                stillSearching= False
            elif nextEast.isFull():
                self.valuetable["Eempty"]= 0
                self.valuetable["Efood"]= 0
                self.valuetable["Ecell"]= i
                self.valuetable["Esize"]= nextEast.contains.valuetable["food"]
                stillSearching= False
            else:
                nextEast= nextEast.east
                i= i - 1

        if stillSearching:
            self.valuetable["Eempty"]= 0
            self.valuetable["Efood"]= 0
            self.valuetable["Ecell"]= 0
            self.valuetable["Esize"]= 0
            stillSearching= False

        #check west
        i= 5
        stillSearching= True
        nextWest= self.location.west
        while i > 0 and stillSearching:
            if nextWest is None or nextWest.isWall():
                self.valuetable["Wempty"]= i
                self.valuetable["Wfood"]= 0
                self.valuetable["Wcell"]= 0
                self.valuetable["Wsize"]= 0
                stillSearching= False
            elif nextWest.isFood():
                self.valuetable["Wempty"]= 0
                self.valuetable["Wfood"]= i
                self.valuetable["Wcell"]= 0
                self.valuetable["Wsize"]= 0
                stillSearching= False
            elif nextWest.isFull():
                self.valuetable["Wempty"]= 0
                self.valuetable["Wfood"]= 0
                self.valuetable["Wcell"]= i
                self.valuetable["Wsize"]= nextWest.contains.valuetable["food"]
                stillSearching= False
            else:
                nextWest= nextWest.west
                i= i - 1

        if stillSearching:
            self.valuetable["Wempty"]= 0
            self.valuetable["Wfood"]= 0
            self.valuetable["Wcell"]= 0
            self.valuetable["Wsize"]= 0
            stillSearching= False

        return



    def calculateMessengerMods(self):
        mods={}  
        for m in self.messengers:
            mods[m]= 0
            for v in self.modIndex:
                mods[m]+= ((self.valuetable[v]) * (self.modtable[v][m]))
        return mods

    def applyMessengerMods(self, messengerMods):
        for m in self.messengers:
            self.valuetable[m]+= messengerMods[m]
        return

    def calculateMovementMods(self):
        mods={}  
        for p in self.proteins:
            mods[p]= 0
            for m in self.messengers:
                mods[p]+= ((self.valuetable[m]) * (self.movementtable[m][p]))
        return mods

    def applyMovementMods(self, movementMods):
        for p in self.proteins:
            self.valuetable[p]+= movementMods[p]
        return

    def pickDirection(self):
        directions= ["N","S","E","W"]
        proteinValues= [self.valuetable["upin"],self.valuetable["downin"],self.valuetable["rightin"],self.valuetable["leftin"]]
        return directions[proteinValues.index(max(proteinValues))]

        #check if the cell can move into Node goingTo and lyse the cell if it cannot
    def checkMoveValidity(self, goingTo):
        if (goingTo is None):
            self.lyse("wanderlust")
            return
        elif (goingTo.isWall()):
            self.lyse("splat")
            return
        elif (goingTo.isFull()):
            self.collide(goingTo.contains)
            return
    
    # process collision between two cells (this cell which is attempting to move into the node occupied by the collidee)
    def collide(self, collidee):
        selfFood= self.valuetable["food"]
        collideeFood= collidee.valuetable["food"]
        #if collidee is at least 50% bigger than this cell: lyse this cell
        if collideeFood > selfFood * 0.5:
            self.lyse("collision")
        #if this cell is the bigger one, the other cell lyses (and this cell then moves into it's space, "eating it"), tie goes to the runner
        else:
            collidee.lyse("got chomped")
            self.cellsEaten+= 1


    def checkFood(self, goingTo):
        if goingTo.isFood():
            self.valuetable["food"]+= goingTo.contains.value
            return
        else:
            return

    def split(self, position):
        if position.isFull():
            return
        self.valuetable["food"]= self.valuetable["food"]/2
        for m in self.messengers:
            self.valuetable[m]= (self.valuetable[m])/2
        for p in self.proteins:
            self.valuetable[p]= (self.valuetable[p])/2

        new_modtable, new_movementtable, new_valuetable, new_proteinInfo= mutateGenome(copy.deepcopy(self.modtable), copy.deepcopy(self.movementtable), copy.deepcopy(self.valuetable), self)


        c= Cell(self.map, position, self.valuetable["food"], new_modtable, new_movementtable, new_valuetable, new_proteinInfo, self.genealogy, mutateSplitThreshold(self.splitThreshold, self), mutateSpeed(self.speed, self))
        c.move()
        return c

    # def report(self):
    #     messengers= ["thinkin", "schemin", "plottin", "dreamin"]
    #     proteins= ["upin", "downin", "rightin", "leftin"]
    #     print("\n\nREPORT: "+ self.fullname())
    #     print("--------------------------------\n")
    #     print("Current Location  :  " + self.location.coordDisplay + "\n")
    #     #"  Siblings #: "+ str(len(self.genealogy.mother.children)-1) + (needed to remove as not compatible with sponateously generated cells)
    #     print("Current Age: " + str(self.age) + "  Generation: "+ str(self.genealogy.generation) + " Children #: "+ str(len(self.genealogy.children)) + "\n")
    #     print("Value Table:")
    #     for i in range(0, len(MOD_INDEX)):
    #         print(MOD_INDEX[i] + ":  " + str(self.valuetable[i]))
    #     print("\n"+ "Mod Table:")
    #     print("thinkin                        schemin                        plottin                        dreamin")
    #     for table in self.modtable:
    #         mods= ""
    #         for val in table:
    #             #truncate output to 6 digits including negative side
    #             mods= mods+ str(val)[:6] +",            "
    #         print(mods)
    #     print("\n"+ "Movement Table:")
    #     print("upin                    downin                    rightin                    leftin")
    #     for table2 in self.movementtable:
    #         movs= ""
    #         for val2 in table2:
    #             movs= movs+ str(val2)[:6] +",  "
    #         print(movs)
        




#Food object class
class Food:
    #creates a new food object with 
        #int value equal to the food it will provide cell
        #Node node where the food resides
    def __init__(self, value, node):
        self.value= value
        self.location= node
        self.location.insert(self)

    def __str__(self):
        if self.value > inputs.FOOD_VALUE * 2:
            return "$"
        else:
            return "*"



      