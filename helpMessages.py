starterMessage= """
Welcome to \x1b[35mSIMULATIN!\x1b[0m
a (super neat) program by Harry \x1b[34mB\x1b[0m Samuels

This is an \x1b[32mevolution simulator\x1b[0m that creates simple creatures called \x1b[35mdoplings\x1b[0m. They look like this: \x1b[34ma\x1b[0m
The doplings live on a tiny grid that looks like this:

+   A B C D E F G H I

A   . . . . . . . . .
B   . . . \x1b[33mb\x1b[0m . . . . .
C   . * . . . . . . .
D   . . . . . . \x1b[34ma\x1b[0m . .
E   . . . . . . . . .

Each turn, every dopling \x1b[36mmoves\x1b[0m 1 space on the grid (up, down, right, or left)
If a dopling runs off of the grid, or into another dopling, it \x1b[31mlyses\x1b[0m (and \x1b[31mdies\x1b[0m :c)

Every 10 turns, a dopling will grow up one letter, refelcting its age:
    -each dopling starts as an \x1b[32ma\x1b[0m, then grows to \x1b[32mb\x1b[0m, then \x1b[32mc\x1b[0m and so on, until it reaches \x1b[32mz\x1b[0m and then \x1b[32mA\x1b[0m
    -after \x1b[32mZ\x1b[0m the dopling becomes an "elder", and will look like this: \x1b[32m&\x1b[0m

The doplings are modeled after single celled organisms:
    -each dopling has 4 messenger proteins (thinkin, schemin, plottin, and dreamin)
    -each dopling has 4 movement proteins (upin, downin, rightin, and leftin)
    -before moving a dopling looks north, south, east, and west for five spaces in each direction
    -all 4 messenger proteins are seprately \x1b[32mactivated\x1b[0m (increased) or \x1b[31minhibited\x1b[0m (decreased) by what the dopling sees
    -the messenger proteins are also affected by the dopling's food and the prior values of all 8 proteins
    -all 4 movement proteins are then activated and inhibited by the 4 messenger proteins
    -the dopling moves in the direction of the movement protein with the greatest value (a 4-way tie goes up)

The grid also contains \x1b[34mfood\x1b[0m, which looks like this: *      or this: $  (for alotta food)
    -doplings use a little food each time they move
    -if a dopling runs out of food, it lyses (and dies :c)
    -if a dopling gets enough food, it will split and make a daughter cell

A daughter cell gets half of the mother cell's food and protein
    -there is a small chance for each of its activation and inhibition values to \x1b[32mmutate\x1b[0m and change slightly
    -there is an even smaller chance for that value to change A LOT, which is called a \x1b[35mMEGA\x1b[32mMUTATION\x1b[0m
    -when a dopling has a \x1b[35mMEGA\x1b[32mMUTATION\x1b[0m, it becomes a new species (and also a new color)

Initially, the doplings will move randomly, and without purpose.
But! After enough generations (and a little luck), the doplings will begin to \x1b[32mevolve\x1b[0m in new and exciting ways

"""

commandsMessage= """
\x1b[34mHow to use the simulation\x1b[0m:

Pressing '\x1b[31mEnter\x1b[0m' advances the simulation one turn by moving all of the doplings
The top right corner of the display will show the total number of turns that have passed, as well as the total number of doplings

There are several command inputs that allow you to to fully utilize the program by typing them into the command line:

'\x1b[36mspeed\x1b[0m':
    -the speed command allows you to run the simulation at warp speed
    -typing the speed command will prompt you to enter a number of turns that should be run automatically
    -these turns are run withoput printing the diplay, allowing the simulation to run as fast as possible
    -there is no way to stop this command until the rounds are complete, so make sure to start small and work your way up
    -upon completion, the new grid will be displayed and the simulation can be interacted with once again

'\x1b[32mjumpstart\x1b[0m':
    -the jumpstart command allows you to "jump" to a point in the simulation with a specified number of living doplings
    -typing the jumpstart command will promt you to enter a desired number of living doplings
    -the simulation will then run in 'speed' mode until the living dopling count reaches the desired quantity
    -WARNING: the simulation will not be interactable until the desired living doping count is reached
    -if the entered desired dopling count is too high, the simulation may become stuck in an endless loop, so be cautious
    -'100' is a good number for reaching 'smarter' doplings on a default size grid (though it may take a couple tries)

'\x1b[35mtrack\x1b[0m':
    -the track command allows you to track a specific dopling
    -typing the track command will prompt you to enter either the grid location of a certain dopling, or its ID Number
    -grid locations are written as "y-coordinate" + "x-coordinate" 
    -for example on the grid above the coordinates are "BD" for the yellow dopling and "DG" for the blue one
    -an ID number is written with the '#' symbol, like "#12" or "#14850"
    -the track command also gives you much more information about the tracked dopling on the right side of the display
    -you can view the dopling's name, species, thoughts, protein levels, activation/inhibition values, and much more

'\x1b[35muntrack\x1b[0m':
    -the untrack command stops the tracking of all doplings

'\x1b[34mpedigree\x1b[0m':
    -the pedigree command generates and prints a family tree containing all living doplings 
    -a pedigree can only be made if all doplings are descended from a common ancestor

'\x1b[33mbottom\x1b[0m':
    -the bottom command moves the phylogeny diagram to the bottom of the display
    -typing the bottom command again will move the phylogeny display back to the right side of the display 
    -this is useful for if the phylogeny grows too long and starts to wrap around

'\x1b[31mX\x1b[0m':
    -typing X will prompt you to end the simulation by typing "X" again
    -this is final and will permanently destroy all the doplings :c

'help':
    -typing "help" will redisplay these help messages at any time (so no need for memorizing)

"""

tableMessage="""
Reading the \x1b[32mactivation\x1b[0m/\x1b[31minhibition\x1b[0m table (\x1b[36mif you're just starting out, you can ignore this section\x1b[0m):

-the messenger activation/inhibition table shown by the tracked dopling's display looks like this:

 #: |5 |0 |0 |0 |0 |0 |1 |0 |0 |0 |3 |0 |
In:  NE NF NC SE SF SC EE EF EC WE WF WC Fd Th Sc Pl Dr Up Dw Rt Lf
Th: |0 |\x1b[31m-\x1b[0m |0 |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |\x1b[32m+\x1b[0m |0 |\x1b[31m-\x1b[0m |0 |0 |0 |0 |0 |0 |
Sc: |0 |0 |\x1b[32m+\x1b[0m |0 |0 |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |0 |\x1b[32m+\x1b[0m |0 |
Pl: |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |\x1b[31m-\x1b[0m |0 |0 |0 |0 |0 |\x1b[31m-\x1b[0m |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |
Dr: |0 |\x1b[32m+\x1b[0m |0 |0 |0 |0 |0 |0 |0 |\x1b[31m-\x1b[0m |0 |\x1b[31m-\x1b[0m |0 |0 |0 |0 |0 |\x1b[31m+\x1b[0m |0 |0 |0 |

-the second row lists each of the inputs (In) that can activate and inhibit each of the 4 messenger proteins
    -NE, NF, & NC stand for North Edge (the end of the grid), North Food, and North Cell (another dopling)
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
    input("press 'Enter' to continue")
    print(tableMessage)
    print('type "help" at any time if you need a refresher')
    input("press 'Enter' to begin the simulation")

def displayHelpMessages():
    print(starterMessage)
    input("press 'Enter' to see the available command line inputs (2/3)")
    print(commandsMessage)
    input("press 'Enter' to learn about the activation/inhibition table (3/3)")
    print(tableMessage)
    print('type "help" at any time if you need it')
    input("press 'Enter' to resume the simulation")