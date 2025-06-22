import cell
import inputs

import random
import json

class Node:

    #creates new Node with int x and int y
    def __init__(self, x, y):
        #id of this cell (DEPRECATED)
        #self.id=
        #x-coordinate of node
        self.x= x
        #y-coordinate of node
        self.y= y
        #coordinate display of node
        self.coordDisplay= "(" + str(x) + ", " + str(y) + ")"
        #current object occupying Node, None if empty
        self.contains= None
        #True if this node is a wall
        self.wall= False
        #Node north of this node
        self.north= None
        #Node south of this node
        self.south= None
        #Node east of this node
        self.east= None
        #Node west of this node
        self.west= None
        

    #returns the Node id as a string when printed
    def __str__(self):
        if self.isFull() or self.isFood():
            return str(self.contains)
        elif self.isWall():
            return "\x1b[41m \x1b[0m"       
        else:
            return "."

    #returns True if the Node is occupied by a cell, False if the Node is empty or contains food
    def isFull(self):
        return type(self.contains) is cell.Cell

    def isFood(self):
        return type(self.contains) is cell.Food

    def isWall(self):
        return self.wall

    def getNorth(self):
        return self.north

    def getSouth(self):
        return self.south

    def getEast(self):
        return self.east

    def getWest(self):
        return self.west
    
    def insert(self, object):
        self.contains= object

    def clear(self):
        self.contains= None

    def makeWall(self):
        self.wall= True
        if self.isFull():
            self.contains.lyse()
        self.clear()
    
    def removeWall(self):
        self.wall= False


#Create a new grid filled with fully linked nodes and return the containing list
def createGrid(rows,columns):
        alpha= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        container= []
        for y in range(0,rows):
            old=None
            new=None
            #create new row
            container.append([])
            #create first node in row
            new= Node(0,y)
            #add new first node to row
            container[y].append(new)
            #check if this is the first row
            if y==0:              
                old= new
                for x in range (1,columns):
                    #create next node
                    new= Node(x, y)
                    #add node to correct row
                    container[y].append(new)

                    new.west=old
                    old.east=new

                    old= new
            else:
                new.north= container[y-1][0]
                container[y-1][0].south= new
                old=new
                for x in range (1,columns):
                    #create next node
                    new= Node(x, y)
                    #add node to correct row
                    container[y].append(new)

                    new.west=old
                    old.east=new

                    new.north= container[y-1][x]
                    container[y-1][x].south= new

                    old= new

        #create edgeless map if Pac-Man Mode is enabled
        if inputs.PAC_MAN_MODE:
            #link left side and right side to eachother
            for rowIndex in range(0, len(container)):
                westEdge= container[rowIndex][0]
                eastEdge= container[rowIndex][-1]
                westEdge.west= eastEdge
                eastEdge.east= westEdge
            #link top and bottom to eachother
            for columnIndex in range(0, len(container[1])):
                northEdge= container[0][columnIndex]
                southEdge= container[-1][columnIndex]
                northEdge.north= southEdge
                southEdge.south= northEdge

        return container


def createCustomGrid(rows, columns, customMapList):
    container= createGrid(rows, columns)
    for y in range(0, rows):
        row= customMapList[y].replace(" ", "")
        for x in range(0, columns):
            if row[x] == "X":
                container[y][x].makeWall()
    return container
            


class Grid:
    
    def __init__(self, rows, columns):
        self.totalturns= 0
        self.totalcellsspawned= 0
        #contains the generation of the most recently created cell
        self.latestgeneration= 0
        if inputs.USE_CUSTOM_MAP:
            customMapFile= open(inputs.CUSTOM_MAP_FILE)
            customMapJSON= json.load(customMapFile)
            customMapList= customMapJSON["map"]
            self.rows= len(customMapList)
            self.columns= len(customMapList[0].replace(" ", ""))
            self.container= createCustomGrid(self.rows, self.columns, customMapList)
            
        else:
            self.rows= rows
            self.columns= columns
            self.container= createGrid(rows, columns)


        
    #DEPRECATED AFTER SWITCHING FROM APLPHAGRID TO COORDINATE GRID
    def __str__(self):
        return "oops! don't call print on the map"
    #     alpha= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    #     i= 0

    #     string= ("    Total Turns: " + str(self.totalturns) + " | Living Cells: " + str(len(cell.CELLS)) + " | Cells Spawned: " + str(self.totalcellsspawned) + "\n\n" +
    #         "+   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z"[:((self.columns*2)+ 4)] +
    #         "\n\n")
        
    #     for y in self.container:
    #         string+= alpha[i]+ "   "
    #         i+= 1
    #         for x in y:
    #             string+= str(x) + " "
    #         string+= "\n"
    #     return string

    def getNode(self, x, y):
        return self.container[y][x]

    def getCellFromCoordinates(self, x, y):
        if self.container[y][x].isFull():
            return self.container[y][x].contains
        else:
            return None

    #builds a wall of length wallLength (int) in direction direction("horizontal"/"h"/"H" or "vertical"/"v"/"V") starting from the top/left node @ (topleftX, topleftY)
    def buildWall(self, direction, topleftX, topleftY, wallLength):
        if (topleftX >= self.columns) or (topleftY >= self.rows):
            print("top left coordinate out of bounds")
            return
        topleftNode= self.container[topleftY][topleftX]
        if (direction == "H") or (direction == "h") or (direction == "horizontal"):
            i=0
            nextNode= topleftNode
            while i< wallLength:
                if nextNode is None:
                    return
                else:
                    nextNode.makeWall()
                    nextNode= nextNode.east
                i+= 1

        elif (direction == "V") or (direction == "v") or (direction == "vertical"):
            i=0
            nextNode= topleftNode
            while i< wallLength:
                if nextNode is None:
                    return
                else:
                    nextNode.makeWall()
                    nextNode= nextNode.south
                i+= 1

        else:
            print("invalid wall directional input")
            return

    def removeWalls(self):
        for row in self.container:
            for node in row:
                node.removeWall()


    def spawnFood(self, value=1, location=None):
        #spawn food randomly
        if location is None:
            available= False
            while not available:
                y= random.randint(1,self.rows -2)
                x= random.randint(1,self.columns -2)
                location= self.container[y][x]
                if (not location.isFull()) and (not location.isWall()):
                    available= True
                    cell.Food(value, location)
        else:
            cell.Food(value, location)

    #spawn a randomly generated new cell on a random available map node (if none is specified) with food value int "food"
    def spawnCell(self,food=5, location=None):
        if location is None:
            available= False
            while not available:
                y= random.randint(1,self.rows -2)
                x= random.randint(1,self.columns -2)
                location= self.container[y][x]
                if (not location.isFull()) and (not location.isFood()) and (not location.isWall()):
                    available= True
                    cell.Cell(self, location, food)

        else:
            cell.Cell(self, location, food)


                



                    

            

        
