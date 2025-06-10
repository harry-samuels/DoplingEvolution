import cell
import inputs

import random

class Node:

    #creates new Node
    def __init__(self, id):
        #name of node
        self.id= id
        #current object occupying Node, None if empty
        self.contains= None
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
        else:
            return "."

    #returns True if the Node is occupied by a cell, False if the Node is empty or contains food
    def isFull(self):
        return type(self.contains) is cell.Cell

    def isFood(self):
        return type(self.contains) is cell.Food

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
            new= Node(alpha[y]+"A")
            #add new first node to row
            container[y].append(new)
            #check if this is the first row
            if y==0:              
                old= new
                for x in range (1,columns):
                    #create next node
                    new= Node(alpha[y]+alpha[x])
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
                    new= Node(alpha[y]+alpha[x])
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

class Grid:
    
    def __init__(self, rows, columns):
        self.rows= rows
        self.columns= columns

        self.container= createGrid(rows, columns)

        self.totalturns= 0
        self.totalcellsspawned= 0

        

    def __str__(self):
        alpha= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        i= 0

        string= ("    Total Turns: " + str(self.totalturns) + " | Living Cells: " + str(len(cell.CELLS)) + " | Cells Spawned: " + str(self.totalcellsspawned) + "\n\n" +
            "+   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z"[:((self.columns*2)+ 4)] +
            "\n\n")
        
        for y in self.container:
            string+= alpha[i]+ "   "
            i+= 1
            for x in y:
                string+= str(x) + " "
            string+= "\n"
        return string

    def getNode(self, y, x):
        return self.container[y][x]

    
    #returns the cell object at the specified alphabet-grid location, returns None if there is no cell at the specified location
    #location is a str containing two letters corresponding to a grid row and grid column (example: "xY")
    def getCellAlphgrid(self, location):
        alpha= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        #type and len check
        if (not type(location) == str) or (len(location) != 2):
            print("incompatible input for cell location")
            return None
        row= alpha.index(location[:1])
        column= alpha.index(location[1:])
        if (row > self.rows-1) or (column > self.columns -1):
            print("incompatible input for cell location")
            return None
        gridLocation= self.container[row][column]
        if gridLocation.isFull():
            return gridLocation.contains
        else:
            return None



        


    def spawnFood(self, value=1, location=None):
        #spawn food randomly
        if location is None:
            available= False
            while not available:
                y= random.randint(0,self.rows -2)
                x= random.randint(0,self.columns -2)
                location= self.container[y][x]
                if not location.isFull():
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
                if (not location.isFull()) and (not location.isFood()):
                    available= True
                    cell.Cell(self, location, food)

        else:
            cell.Cell(self, location, food)


                



                    

            

        
