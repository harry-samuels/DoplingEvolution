import grid
import genealogy
import inputs

import random
import copy

#List of all current living cells
CELLS= []
#List of all cells that have existed or currently existy in the game. Each cell's numberID unique corresponds to its index in the list
ALL_CELLS= []

MOD_INDEX= [
    "Nempty","Nfood", "Ncell",
    "Sempty","Sfood", "Scell",
    "Eempty","Efood", "Ecell",
    "Wempty","Wfood", "Wcell",
    "food",
    "thinkin", "schemin", "plottin", "dreamin",
    "upin", "downin", "rightin", "leftin"
]

#adds newly generated cell to list of living Cells at the correct speed postion. CELLS is ordered from fastest (greatest speed) to slowest cells
#This method keeps the list sorted
def addtoCELLS(newCell, cellSpeed):
    i= 0
    while i < len(CELLS) and cellSpeed < CELLS[i].speed:
        i+= 1
    CELLS.insert(i, newCell)

#create a new modifier table, if no mod table is given determine all modifiers randomly, otherwise return the given modtable
def generateModTable(modtable=None):
    messengers= ["thinkin", "schemin", "plottin", "dreamin"]
    if modtable is None:
        modtable= []
        for input in range(0,len(MOD_INDEX)):
            modtable.append([])
            for m in messengers:
                modtable[input].append(((random.uniform(0,0.5))**2)*random.choice([-1,1]))
        return modtable

    else:
        return modtable

#create a new movement table, if no movement table is given determine all modifiers randomly, otherwise return the given momovementtable
def generateMovementTable(movementtable=None):
    messengers= ["thinkin", "schemin", "plottin", "dreamin"]
    proteins= ["upin", "downin", "rightin", "leftin"]
    if movementtable is None:
        movementtable=[]
        for m in range(0, len(messengers)):
            movementtable.append([])
            for p in range(0, len(proteins)):
                movementtable[m].append(((random.uniform(0,0.5))**2)*random.choice([-1,1]))
        return movementtable
    else:
        return movementtable 

#add mutations to a given 2-D mod or movement table
def mutate(table, parent):
    for r in range(0, len(table)):
        for c in range(0, len(table[r])):
            if random.randint(0, 100) <5:
                if random.randint(0,100) == 1:
                    table[r][c]= table[r][c] * (random.uniform(-5, 5))
                    #this will allow the newly created cell to have a different color from the mother cell using its genealogy init
                    parent.genealogy.nextchildmegamutation= True
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


class Cell:
    #Grid: map, Node: location, int: food, []: modtable, []: movementtable, []: valuetable
    def __init__(self, map, location, food, modtable=None, movementtable=None, valuetable=None, mothergenealogy=None, splitThreshold=None, speed=None):

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
        
        if valuetable is None:
            self.valuetable=[
                0,0,0,
                0,0,0,
                0,0,0,
                0,0,0,
                food,
                10, 10, 10, 10,
                10, 10, 10, 10
            ]
        else:
            self.valuetable= valuetable
            self.valuetable[MOD_INDEX.index("food")]= food

        self.modtable= generateModTable(modtable)
        self.movementtable= generateMovementTable(movementtable)

        self.genealogy= genealogy.Genealogy(self, mothergenealogy)

        #how many other cells this cell has eaten
        self.cellsEaten= 0

        if splitThreshold is None:
            splitThreshold= inputs.FOOD_TO_SPLIT
        self.splitThreshold= splitThreshold
        print("inputs FTS == " + str(inputs.FOOD_TO_SPLIT)) #DEBUG
        print("self.split == " + str(self.splitThreshold)) #DEBUG
        if speed is None:
            speed= inputs.FOOD_TO_MOVE
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

    #lyse the cell if it is not already lysed, spawn a food object at current location with value equal to own food value
    def lyse(self, deathmessage="adios ;)"):
        if self.lysed:
            return
        self.deathmessage= ("'" + deathmessage + "'")
        self.deathdate= self.map.totalturns
        self.location.clear()
        if self.valuetable[MOD_INDEX.index("food")] > 0:
            self.map.spawnFood(self.valuetable[MOD_INDEX.index("food")], self.location)
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
        self.valuetable[MOD_INDEX.index("food")]-= self.speed 
        if self.valuetable[MOD_INDEX.index("food")] <= 0:
            self.lyse("hungry :(")

        #ensure the cell is still alive
        if self.lysed:
            return

        self.setSightValues()
        messengerMods= self.calculateMessengerMods()
        self.applyMessengerMods(messengerMods)

        #set negative messenger/protein values to zero
        for vindex in range(MOD_INDEX.index("thinkin"), len(MOD_INDEX)):
            if self.valuetable[vindex] < 0:
                #print("corrected negative:" + MOD_INDEX[vindex] + ": " + str(self.valuetable[vindex]))
                self.valuetable[vindex]= 0

        movementMods= self.calculateMovementMods()
        self.applyMovementMods(movementMods)

        #BUG subzero va;ues are still being used in calculations
        for vindex in range(MOD_INDEX.index("thinkin"), len(MOD_INDEX)):
            if self.valuetable[vindex] < 0:
                #print("hormal imbalance of " + MOD_INDEX[vindex] + ":" + str(self.valuetable[vindex]) + " ~ " + self.name)
                self.valuetable[vindex]= 0
                #self.lyse("hormal imbalance of " + MOD_INDEX[self.valuetable.index(value)] + ":" + str(value))

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
        if self.valuetable[MOD_INDEX.index("food")] > self.splitThreshold:
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
                self.valuetable[MOD_INDEX.index("Nempty")]= i
                self.valuetable[MOD_INDEX.index("Nfood")]= 0
                self.valuetable[MOD_INDEX.index("Ncell")]= 0
                stillSearching= False
            elif nextNorth.isFood():
                self.valuetable[MOD_INDEX.index("Nempty")]= 0
                self.valuetable[MOD_INDEX.index("Nfood")]= i
                self.valuetable[MOD_INDEX.index("Ncell")]= 0
                stillSearching= False
            elif nextNorth.isFull():
                self.valuetable[MOD_INDEX.index("Nempty")]= 0
                self.valuetable[MOD_INDEX.index("Nfood")]= 0
                self.valuetable[MOD_INDEX.index("Ncell")]= i
                stillSearching= False
            else:
                nextNorth= nextNorth.north
                i= i - 1

        if stillSearching:
            self.valuetable[MOD_INDEX.index("Nempty")]= 0
            self.valuetable[MOD_INDEX.index("Nfood")]= 0
            self.valuetable[MOD_INDEX.index("Ncell")]= 0
            stillSearching= False

        #check south
        i= 5
        stillSearching= True
        nextSouth= self.location.south
        while i > 0 and stillSearching:
            if nextSouth is None or nextSouth.isWall():
                self.valuetable[MOD_INDEX.index("Sempty")]= i
                self.valuetable[MOD_INDEX.index("Sfood")]= 0
                self.valuetable[MOD_INDEX.index("Scell")]= 0
                stillSearching= False
            elif nextSouth.isFood():
                self.valuetable[MOD_INDEX.index("Sempty")]= 0
                self.valuetable[MOD_INDEX.index("Sfood")]= i
                self.valuetable[MOD_INDEX.index("Scell")]= 0
                stillSearching= False
            elif nextSouth.isFull():
                self.valuetable[MOD_INDEX.index("Sempty")]= 0
                self.valuetable[MOD_INDEX.index("Sfood")]= 0
                self.valuetable[MOD_INDEX.index("Scell")]= i
                stillSearching= False
            else:
                nextSouth= nextSouth.south
                i= i - 1

        if stillSearching:
            self.valuetable[MOD_INDEX.index("Sempty")]= 0
            self.valuetable[MOD_INDEX.index("Sfood")]= 0
            self.valuetable[MOD_INDEX.index("Scell")]= 0
            stillSearching= False


        #check east
        i= 5
        stillSearching= True
        nextEast= self.location.east
        while i > 0 and stillSearching:
            if nextEast is None or nextEast.isWall():
                self.valuetable[MOD_INDEX.index("Eempty")]= i
                self.valuetable[MOD_INDEX.index("Efood")]= 0
                self.valuetable[MOD_INDEX.index("Ecell")]= 0
                stillSearching= False
            elif nextEast.isFood():
                self.valuetable[MOD_INDEX.index("Eempty")]= 0
                self.valuetable[MOD_INDEX.index("Efood")]= i
                self.valuetable[MOD_INDEX.index("Ecell")]= 0
                stillSearching= False
            elif nextEast.isFull():
                self.valuetable[MOD_INDEX.index("Eempty")]= 0
                self.valuetable[MOD_INDEX.index("Efood")]= 0
                self.valuetable[MOD_INDEX.index("Ecell")]= i
                stillSearching= False
            else:
                nextEast= nextEast.east
                i= i - 1

        if stillSearching:
            self.valuetable[MOD_INDEX.index("Eempty")]= 0
            self.valuetable[MOD_INDEX.index("Efood")]= 0
            self.valuetable[MOD_INDEX.index("Ecell")]= 0
            stillSearching= False

        #check west
        i= 5
        stillSearching= True
        nextWest= self.location.west
        while i > 0 and stillSearching:
            if nextWest is None or nextWest.isWall():
                self.valuetable[MOD_INDEX.index("Wempty")]= i
                self.valuetable[MOD_INDEX.index("Wfood")]= 0
                self.valuetable[MOD_INDEX.index("Wcell")]= 0
                stillSearching= False
            elif nextWest.isFood():
                self.valuetable[MOD_INDEX.index("Wempty")]= 0
                self.valuetable[MOD_INDEX.index("Wfood")]= i
                self.valuetable[MOD_INDEX.index("Wcell")]= 0
                stillSearching= False
            elif nextWest.isFull():
                self.valuetable[MOD_INDEX.index("Wempty")]= 0
                self.valuetable[MOD_INDEX.index("Wfood")]= 0
                self.valuetable[MOD_INDEX.index("Wcell")]= i
                stillSearching= False
            else:
                nextWest= nextWest.west
                i= i - 1

        if stillSearching:
            self.valuetable[MOD_INDEX.index("Wempty")]= 0
            self.valuetable[MOD_INDEX.index("Wfood")]= 0
            self.valuetable[MOD_INDEX.index("Wcell")]= 0
            stillSearching= False

        return



    def calculateMessengerMods(self):
        messengers= ["thinkin", "schemin", "plottin", "dreamin"]
        mods=[]  
        for z in range(0, len(messengers)):
            mods.append(0)
            for i in range(0, len(MOD_INDEX)):
                mods[z]+= ((self.valuetable[i]) * (self.modtable[i][z]))
        return mods

    def applyMessengerMods(self, messengerMods):
        messengers= ["thinkin", "schemin", "plottin", "dreamin"]
        for m in range(0, len(messengerMods)):
            self.valuetable[MOD_INDEX.index(messengers[m])]+= messengerMods[m]

        return

    def calculateMovementMods(self):
        messengers= ["thinkin", "schemin", "plottin", "dreamin"]
        proteins= ["upin", "downin", "rightin", "leftin"]
        mods=[]  
        for p in range(0, len(proteins)):
            mods.append(0)
            for m in range(0, len(messengers)):
                mods[p]+= ((self.valuetable[MOD_INDEX.index(messengers[m])]) * (self.movementtable[m][p]))
        return mods

    def applyMovementMods(self, movementMods):
        proteins= ["upin", "downin", "rightin", "leftin"]
        for p in range(0, len(movementMods)):
            self.valuetable[MOD_INDEX.index(proteins[p])]+= movementMods[p]
        return

    def pickDirection(self):
        directions= ["N","S","E","W"]
        proteins= [self.valuetable[MOD_INDEX.index("upin")],self.valuetable[MOD_INDEX.index("downin")],self.valuetable[MOD_INDEX.index("rightin")],self.valuetable[MOD_INDEX.index("leftin")]]
        return directions[proteins.index(max(proteins))]

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
        selfFood= self.valuetable[MOD_INDEX.index("food")]
        collideeFood= collidee.valuetable[MOD_INDEX.index("food")]
        #if collidee is at least 10% bigger than this cell: lyse this cell
        if collideeFood > selfFood * 0.9:
            self.lyse("collision")
        #if this cell is the bigger one, the other cell lyses (and this cell then moves into it's space, "eating it"), tie goes to the runner
        else:
            collidee.lyse("got chomped")
            self.cellsEaten+= 1


    def checkFood(self, goingTo):
        if goingTo.isFood():
            self.valuetable[MOD_INDEX.index("food")]+= goingTo.contains.value
            return
        else:
            return

    def split(self, position):
        messengers= ["thinkin", "schemin", "plottin", "dreamin"]
        proteins= ["upin", "downin", "rightin", "leftin"]
        if position.isFull():
            return
        self.valuetable[MOD_INDEX.index("food")]= self.valuetable[MOD_INDEX.index("food")]/2
        for m in messengers:
            self.valuetable[MOD_INDEX.index(m)]= (self.valuetable[MOD_INDEX.index(m)])/2
        for p in proteins:
            self.valuetable[MOD_INDEX.index(p)]= (self.valuetable[MOD_INDEX.index(p)])/2

        #SQUASHED BUG!
        c= Cell(self.map, position, self.valuetable[MOD_INDEX.index("food")], mutate(copy.deepcopy(self.modtable), self), mutate(copy.deepcopy(self.movementtable), self), copy.deepcopy(self.valuetable), self.genealogy, mutateSplitThreshold(self.splitThreshold, self), mutateSpeed(self.speed, self))
        #print("split " + c.name + " @ " + str(position.id) + " from " + self.name + " @ " + str(self.location.id)) #DEBUG
        c.move()
        return c

    def report(self):
        messengers= ["thinkin", "schemin", "plottin", "dreamin"]
        proteins= ["upin", "downin", "rightin", "leftin"]
        print("\n\nREPORT: "+ self.fullname())
        print("--------------------------------\n")
        print("Current Location  :  " + self.location.id + "\n")
        #"  Siblings #: "+ str(len(self.genealogy.mother.children)-1) + (needed to remove as not compatible with sponateously generated cells)
        print("Current Age: " + str(self.age) + "  Generation: "+ str(self.genealogy.generation) + " Children #: "+ str(len(self.genealogy.children)) + "\n")
        print("Value Table:")
        for i in range(0, len(MOD_INDEX)):
            print(MOD_INDEX[i] + ":  " + str(self.valuetable[i]))
        print("\n"+ "Mod Table:")
        print("thinkin                        schemin                        plottin                        dreamin")
        for table in self.modtable:
            mods= ""
            for val in table:
                #truncate output to 6 digits including negative side
                mods= mods+ str(val)[:6] +",            "
            print(mods)
        print("\n"+ "Movement Table:")
        print("upin                    downin                    rightin                    leftin")
        for table2 in self.movementtable:
            movs= ""
            for val2 in table2:
                movs= movs+ str(val2)[:6] +",  "
            print(movs)
        




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



      