import inputs

starterMessage= """
Welcome to \x1b[35mTHE GENE MACHINE\x1b[0m
a (super neat) program by Harry \x1b[34mB\x1b[0m Samuels

This is an \x1b[32mevolution simulator\x1b[0m that creates simple creatures called \x1b[35mdoplings\x1b[0m. They look like this: \x1b[34ma\x1b[0m
The doplings live on a tiny grid that looks like this:

+   0 1 2 3 4 5 6 7 8

1   . . . . . . . . .
2   . . . \x1b[33mb\x1b[0m . . . . .
3   . * . . . . . . .
4   . . . . . . \x1b[34ma\x1b[0m . .
5   . . . . . . . . .

Each turn, every dopling \x1b[36mmoves\x1b[0m 1 space on the grid (up, down, right, or left)
If a dopling runs off of the grid, or into another dopling, it \x1b[31mlyses\x1b[0m (and \x1b[31mdies\x1b[0m :c)

Every 10 turns, a dopling will grow up one letter, reflcting its age:
    -each dopling starts as an \x1b[32ma\x1b[0m, then grows to \x1b[32mb\x1b[0m, then \x1b[32mc\x1b[0m and so on, until it reaches \x1b[32mz\x1b[0m and then \x1b[32mA\x1b[0m
    -after \x1b[32mZ\x1b[0m the dopling becomes an "elder", and will look like this: \x1b[32m&\x1b[0m

The doplings are modeled after single celled organisms:
    -each dopling has several messenger proteins (thinkin, schemin, plottin, dreamin, etc.)
    -each dopling has 4 movement proteins (upin, downin, rightin, and leftin)
    -before moving a dopling looks north, south, east, and west for five spaces in each direction
    -all messenger proteins are seprately \x1b[32mactivated\x1b[0m (increased) or \x1b[31minhibited\x1b[0m (decreased) by what the dopling sees
    -the messenger proteins are also affected by the dopling's food and the prior values of all proteins
    -all 4 movement proteins are then activated and inhibited by the 4 messenger proteins
    -the dopling moves in the direction of the movement protein with the greatest value (a 4-way tie goes up)

The grid also contains \x1b[34mfood\x1b[0m, which looks like this: *      or this: $  (for alotta food)
    -doplings use a little food each time they move
    -if a dopling runs out of food, it lyses (and dies :c)

Doplings can split by using splittin (another protein)
    -a daughter cell gets half of the mother cell's food and protein
    -there is a small chance for each of its activation and inhibition values to \x1b[32mmutate\x1b[0m and change slightly
    -there is an even smaller chance for that value to change A LOT, which is called a \x1b[35mMEGA\x1b[32mMUTATION\x1b[0m
    -when a dopling has a \x1b[35mMEGA\x1b[32mMUTATION\x1b[0m, it becomes a new species (and also a new color)
    -doplings can also duplicate or delete specific protein genes when splitting 

Initially, the doplings will move randomly, and without purpose.
But! After enough generations (and a little luck), the doplings will begin to \x1b[32mevolve\x1b[0m in new and exciting ways

"""

commandsMessage= """
\x1b[34mHow to use the simulation\x1b[0m:

Pressing '\x1b[31mEnter\x1b[0m' advances the simulation one turn by moving all of the doplings
The top right corner of the display will show the total number of turns that have passed, as well as the total number of doplings

There are several command inputs that allow you to to fully utilize the program by typing them into the command line:

'\x1b[36mspeed\x1b[0m': run the simulation at warp speed for a set number of turns
    - Typing the speed command will prompt you to enter a number of turns that should be run automatically
    - These turns are run without printing the diplay, allowing the simulation to run as fast as possible
    - There is no way to stop this command until the rounds are all complete, so be sure to start small and work your way up

'\x1b[32mjumpstart\x1b[0m': "jump" to a point in the simulation after a specified number of generations have passed
    - Typing the jumpstart command will promt you to enter a desired number of generations
        - The simulation will then run in 'speed' mode until the doplings reach the desired generation
    - There is no way to stop this command until the desired generation count is reached
        - If the entered generation is too high, the simulation may become stuck, so be cautious
    - '200' is a good number for reaching 'smarter' doplings on a default, 100x100, sized grid (though it may take a couple tries)

'\x1b[35mtrack\x1b[0m': view the specific traits and protein levels of a given dopling
    - Typing the track command will prompt you to enter either the grid location of a certain dopling, or its ID Number
        -  Grid locations are written as "x-coordinate, y-coordinate", separated by a comma
            - Ex: "5,22" or "47,52"
        -  An ID number is written with the '#' symbol
            - Ex: "#12" or "#14850"
    - Tracking a dopling will highlight it in white on the map and provide a ton of information about the dopling on the right side of the display
        - you can view the dopling's name, species, relatives, thoughts, protein levels, activation/inhibition values, and much more!
    - Only living doplings can be tracked using this command
    - Type '\x1b[33mname\x1b[0m' while tracking a dopling to rename it
    - Type '\x1b[32msave\x1b[0m' while tracking a dopling to save it as a .json file
    - Type '\x1b[35mparent\x1b[0m' while tracking a dopling to track an ancestor of that dopling
    - Type '\x1b[36mchildren\x1b[0m' while tracking a dopling to track a child of that dopling

'\x1b[35muntrack\x1b[0m': stop tracking all doplings

'\x1b[35mmultitrack\x1b[0m': view and compare multiple doplings simultaneously

'\x1b[34mpedigree\x1b[0m': create a pedigree (family tree) containing all living doplings
    - A pedigree can only be made if all doplings are descended from a common ancestor

'\x1b[33mbottom\x1b[0m': move the phylogeny display to the bottom of the display
    - Typing the bottom command again will move the phylogeny display back to the right side of the display 
    - This is useful for if the phylogeny grows too long and starts to wrap around

'\x1b[31mwall\x1b[0m': construct or remove walls on the map
    - Doplings "see" walls as identical to the edge of the map

'\x1b[32mload\x1b[0m' : load a saved dopling into the simulation
    - Attempting to load any file that is not a saved dopling will immediately crash the simulation so please do not do that

'\x1b[31mX\x1b[0m': end the simulation
    - This is final and will permanently destroy all the doplings :c

'help':
    - Typing "help" will redisplay these help messages at any time (so no need for memorizing)

"""

OLDtableMessage="""
Reading the \x1b[32mactivation\x1b[0m/\x1b[31minhibition\x1b[0m table (\x1b[36mif you're just starting out, you can ignore this section\x1b[0m):

-the messenger activation/inhibition table shown by the tracked dopling's display looks like this:

 #: |5 |0 |0 |0 |0 |0 |1 |0 |0 |0 |3 |0 |0 |0 |0 |0 |5 | 
In:  NE NF NC NS SE SF SC SS EE EF EC SS WE WF WC WS Fd Th Sc Pl Dr Up Dw Rt Lf
Th: |0 |\x1b[31m-\x1b[0m |0 |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |\x1b[32m+\x1b[0m |0 |\x1b[31m-\x1b[0m |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |
Sc: |0 |0 |\x1b[32m+\x1b[0m |0 |0 |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |
Pl: |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |\x1b[31m-\x1b[0m |0 |0 |0 |0 |0 |\x1b[31m-\x1b[0m |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |
Dr: |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |\x1b[31m-\x1b[0m |0 |\x1b[31m-\x1b[0m |0 |0 |0 |0 |0 |\x1b[31m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |0 |0 |

-the second row lists each of the inputs (In) that can activate and inhibit each of the 4 messenger proteins
    -NE, NF, NC, & NS stand for North Edge (the end of the grid), North Food, North Cell (another dopling), and North Size (the size of that)
    -S, E, and W stand for South, East and West respectively
    -Fd is "food", and the last 8 (Th Sc Pl Dr Up Dw Rt Lf) are the 8 proteins
-the first row shows the values that represent what the dopling sees
    -a dopling can see up to 5 spaces in each direction
    -something right next to the dopling has a value of 5, and something 5 spaces away has a value of 1
    -If all 5 spaces in a given direction are unnocupied, all 3 sight values for that direction will be 0
    -a dopling can only see the closest thing in each direction, so it will not see another dopling behind a piece of food
-the final 4 rows show the activation and inhibition effects of each input on the mesenger hormone in that row
-the value of each activation or inhibiton is represented using 0's, \x1b[32m+\x1b[0m's and \x1b[31m-\x1b[0m's

-the activation/inhibition table for the 4 movement proteins looks similar, but the only columns are the 4 messenger proteins

"""

def displayStartupMessages():
    print(starterMessage)
    input("press 'Enter' to learn how to use the simulation")
    print(commandsMessage)
    input("press 'Enter' to begin the simulation")
    #print(tableMessage)
    #print('type "help" at any time if you need a refresher')
    # if input("Write 'custom' to use custom parameters or press 'Enter' to begin the simulation: ") == "custom":
    #     print("\nNOTE: changing the default parameters may introduce unforseen bugs (be careful!...or don't)")

    #     FPTinput= input("\nInput how many pieces of food will be spawned per turn (int), or hit 'Enter' to use default (" + str(inputs.FOOD_PER_TURN) + "): ")
    #     if FPTinput != "":
    #         inputs.FOOD_PER_TURN= int(FPTinput)
    #         print("Food per turn: " + FPTinput)

    #     FVinput= input("\nInput how much food value each spawned food should provide (float), or hit 'Enter' to use default (" + str(inputs.FOOD_VALUE) + "): ")
    #     if FVinput != "":
    #         inputs.FOOD_VALUE= float(FVinput)
    #         print("Spawned food value: " + FVinput)

    #     BCNinput= input("\nInput the starting number of doplings (int), or hit 'Enter' to use default (" + str(inputs.BASE_CELL_NUMBER) + "): ")
    #     if BCNinput != "":
    #         inputs.BASE_CELL_NUMBER= int(BCNinput)
    #         print("Base dopling number: " + BCNinput)

    #     SCFinput= input("\nInput the starting amount of food for spawned doplings (float), or hit 'Enter' to use default (" + str(inputs.SPAWNED_CELL_FOOD) + "): ")
    #     if SCFinput != "":
    #         inputs.SPAWNED_CELL_FOOD= float(SCFinput)
    #         print("\nSpawned dopling food: " + SCFinput)

    #     FTMinput= input("\nInput the amount of food a dopling uses to move (float), or hit 'Enter' to use default (" + str(inputs.FOOD_TO_MOVE) + "): ")
    #     if FTMinput != "":
    #         inputs.FOOD_TO_MOVE= float(FTMinput)
    #         print("Food to move: " + FTMinput)

    #     FTSinput= input("\nInput the amount of food a dopling needs to split (float), or hit 'Enter' to use default (" + str(inputs.FOOD_TO_SPLIT) + "): ")
    #     if FTSinput != "":
    #         inputs.FOOD_TO_SPLIT= float(FTSinput)
    #         print("Food needed to split: " + FTSinput)

    #     PMMinput= input("\nType 'Y' to enable edgeless map (Pac-Man mode), or hit 'Enter' to keep 'hard edges': ")
    #     if PMMinput == "Y":
    #         inputs.PAC_MAN_MODE= True
    #         print("Pac-Man Mode enabled")
        
        



def displayHelpMessages():
    print(starterMessage)
    input("press 'Enter' to see the available command line inputs (1/2)")
    print(commandsMessage)
    print('type "help" at any time if you need it')
    input("press 'Enter' to resume the simulation")