# Welcome to The Gene Machine!
*a (super neat) program by Harry B Samuels*

**This is an **evolution simulator** that creates simple creatures called doplings. They look like this:** `a`

**The doplings live on a tiny grid that looks like this:**
```
+   0 1 2 3 4 5 6 7 8

0   . . . . . . . . .
1   . . . b . . . . .
2   . * . . . . . . .
3   . . . . . . a . .
4   . . . . . . . . .
```

# What are doplings?
- Doplings are modelled after single-celled organisms
- They can move around the grid, see their surroundings, eat food, reproduce, mutate, and _EVOLVE_

# What do the doplings do?

- Each turn, every dopling moves 1 space on the grid (up, down, right, or left)
- If a dopling runs off of the grid, or into another dopling, it lyses (and dies :c)
- Doplings decide which direction to move, and when to "split" into 2 doplings, using a system of proteins
- Every 10 turns, a dopling will grow up by one letter, reflecting its age:
    - doplings start as an `a`, then grow to `b`, then `c`, and so on, until they reach `z` and then `A`
    - after `Z` the dopling becomes an "elder", and will look like this: `&`

# Why are doplings?
- This simulation is meant to demonstrate (at a very simplified scale) how single-celled organisms "work" on a functional level 
- Cells use a massive number of proteins, encoded in DNA as "genes", to interact with their environment, reproduce, and perform all sorts of important actions
- The doplings let users take a look "inside the cell" to see how genes (and their corresponding proteins) can evolve over time to create intricate systems using simple pieces

Initially, the doplings will move randomly, and without purpose. But! After enough generations (and a little luck), the doplings will begin to ***evolve*** in new and exciting ways

# How do the doplings work? (The Nitty-Gritty)
*This section details the inner workings of the doplings: how they move, reproduce, and evolve.*\
*To learn more about using the simulation, skip to "How to Use the Simulation", or skip to "Quickstart Guide" if you want to act first and learn later.*
### Doplings need food to move
- Food looks like this: `*`          or this: `$`  (for alotta food)
- Doplings use a little food each time they move, and they need more food to move the bigger they get
- If a dopling runs out of food, it lyses (and dies :c)
- If a dopling runs into another dopling that 25% smaller, it will eat that dopling and gain its food
    - If the other dopling is bigger or the same size, then the moving dopling will lyse instead
- Each dopling has a set *speed*, which allows them to use extra food in order to move faster than other doplings
### Doplings decide where to move using proteins
- Each dopling has 4 *movement proteins*: upin, downin, leftin, and rightin
    - Each turn, the dopling will move in the direction of whichever movement protein has the highest value (a 4 way tie goes up)
    - The quantity of each movement protein is determined by a dopling's messenger proteins
- A dopling has multiple *messenger proteins*: thinkin, schemin, plottin, dreamin, etc.
    - Each turn, each messenger protein increases the quantity of (activates) certain movement proteins and decreases the quantity of (inhibits) others
    - The higher the quantity of a messenger protein, the more strongly it affects the quantities of the movement proteins 
    - The quantity of each messenger protein is determined by what the dopling "sees", its current food value, and the value of all other proteins
### Doplings can see 5 spaces in each direction (north, south, east & west)
- Doplings can see how far away food, walls/edges, and other doplings are
    - They can also see how "big" other doplings are (how much food they have)
- Doplings can only see the closest thing in each direction
- If something is more than 5 spaces away, the dopling will see nothing in that direction
### Doplings can "split" to reproduce, creating mutations
- In additon to the 4 movement proteins, doplings also have a splitting protein, called "splittin"
    - If there is a higher quantity of splittin than any movement protein, the dopling will split and make a second dopling
    - Splittin is regulated in the same way as the movement proteins
- A daughter dopling gets half of the mother doplings's food and proteins 
- There is a small chance for each of the new dopling's activation and inhibition values (and speed) to ***mutate*** and change slightly
    - There is an even smaller chance for that value to change A LOT, which is called a ***MEGAMUTATION***
    - When a dopling has a ***MEGAMUTATION***, it becomes a new species (and also a new color)
- There is also a very small chance for the dopling to have a ***gene duplication*** or ***deletion***
    - This causes the dopling to gain a second copy of a given protein (for a duplication) or lose an entire protien (for a deletion)
        - The new protein will have the same activation and inhibition values as the original (with a chance for mutation)
        - The new protein has the same name as the original protein, plus the ID number of the dopling that had the duplication
            - Duplication can also produce *secondary messenger proteins*, which have the same activation and inhibition values as the messenger they are duplicated from, but don't affect movement proteins
    - Doplings can also experience a ***full genome duplication***, in which all of its proteins will be duplicated
    - Upin, downin, leftin, rightin, and splittin cannot be duplicated (consider them "highly conserved")

# How to Use the Simulation
*This section gives a comprehensive breakdown of how to use the simulation. To start quickly, skip to "Quickstart Guide"*
## Starting the simulation
1. Run the main.py python file in terminal from the simulation directory
2. Read the start up messages and press 'Enter'
3. Press 'Enter' to advance the simulation turn by turn
## Interacting with the simulation
There are a number of command line inputs you can use to view and interact with the simulation:

### Speeding up the simulation:
- '***speed***' : run the simulation at warp speed for a set number of turns
    - Typing the speed command will prompt you to enter a number of turns that should be run automatically
    - These turns are run without printing the diplay, allowing the simulation to run as fast as possible
    - There is no way to stop this command until the rounds are all complete, so be sure to start small and work your way up
- '***jumpstart***' : "jump" to a point in the simulation after a specified number of generations have passed
    - Typing the jumpstart command will promt you to enter a desired number of generations
        - The simulation will then run in 'speed' mode until the doplings reach the desired generation
    - There is no way to stop this command until the desired generation count is reached
        - If the entered generation is too high, the simulation may become stuck, so be cautious\
    - '200' is a good number for reaching 'smarter' doplings on a default-sized grid (though it may take a couple tries)

### Tracking Doplings:
- '***track***' : view the specific traits and protein levels of a given dopling
    - Typing the track command will prompt you to enter either the grid location of a certain dopling, or its ID Number
        -  Grid locations are written as "x-coordinate, y-coordinate", separated by a comma
            -  Ex: "5,22" or "47,52"
        -  An ID number is written with the '#' symbol
            -  Ex: "#12" or "#14850"
    -  Tracking a dopling will highlight it in white on the map and provide a ton of information about the dopling on the right side of the display
        - you can view the dopling's name, species, relatives, thoughts, protein levels, activation/inhibition values, and much more!
    -  Only living doplings can be tracked using this command
- '***untrack***' : stop tracking all doplings
    - Typing the untrack command will stop tracking any individual dopling and/or multitracked doplings
- '***multitrack***' : view and compare multiple doplings (or groups of doplings) simultaneously
    - Typing the multitrack command will allow you to pick from several group tracking options including the 3 most prolific species, 1 single species, the oldest living doplings, or a random dopling
 
### Commands to use while tracking a dopling:
*These commands can only be used while the simulation is currently tracking a single dopling*
- '***name***' : rename the tracked dopling
    - Typing the name commands will allow you to enter a new name for the tracked dopling
- '***save***' : save the tracked dopling
    - Typing the save command will save the tracked dopling to the "saved_doplings" folder as a .json file
    - saved doplings can be loaded into any simulation at any time using the 'load' command
- '***parent***' : track an ancestor of the tracked dopling
    - Typing the parent command will prompt you to enter a number of generations that you wish to "go back" in the lineage of the tracked dopling
    - The ancestor dopling will then become the new tracked dopling
- '***children***' : track a child of the tracked dopling
    - Typing the children command will provide a numbered list of the tracked doplings children and prompt you to select one
    - The chosen child will then become the new tracked dopling
 
### Pedigree and Phylogeny Generation:
- '***pedigree***' : create a pedigree (family tree) containing all living doplings
    - Typing the pedigree command will output a pedigree that stretches back to the Last Common Ancestor and contains all living doplings
- '***bottom***' : move the phylogeny display to the bottom of the display
    - Typing the bottom command will move the phylogeny display to the bottom of the display, or move it back to the side if it is already on the bottom
    - This is useful for when the phylogeny grows to long and starts to wrap around, interrupting the map display

### Additional Commands:
- '***wall***' : construct or remove walls on the map
    - Typing the wall command will allow you to build or remove walls on the map
        - walls act just like the edges of the map, and are "seen" as idenitical to map edges by the doplings
    - Walls are contructed/removed in horizontal and vertical segments of specified lengths starting from a specified top/left coordinate
- '***load***' : load a saved dopling into the simulation
    - Typing the load command will prompt you to select a saved dopling and specify a location on the map for it to be placed onto
    - The newly loaded dopling will also become the current tracked dopling
    - Attempting to load any file that is not a saved dopling will immediately crash the simulation so please do not do that
- '***help***' : see a list of the available commands
    - Typing the help command will output up a list of available commands and information
- '***X***' : end the simulation
    - Typing "X" will cause the simulation to ask for confirmation of termination, and typing X a second time will permanently end the simulation
    - This command, like all others, will have no effect while either the 'speed' or 'jumpstart' command are being used, and cannot be used to exit them prematurely
 
# Quickstart Guide
*Here's how to jump right in:*
1. Run the main.py python file in terminal from the simulation directory
2. Press 'Enter' to advance the simulation turn by turn
3. Type the 'jumpstart' command and enter '200' generations when prompted
    + This will give the doplings time to evolve slightly "intelligent" behaviors
4. Type the 'multitrack' command to select a random dopling to track
5. See what happens!

What's Next?
- *You can let the doplings evolve even further by using 'jumpstart' to reach even higher generations!*
- *You can build walls using the 'wall' command and see how the doplings respond!*
    - *You can also build custom maps like the ones in the "custom_maps" folder*
- *You can save an interesting dopling and try tinkering around with its .json file, then load it back up and see how it acts!*
- *You can open up the inputs.py file and change the default values around to see how it changes the doplings' evolution!*

         
