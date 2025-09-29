# Welcome to The Gene Machine!
a (super neat) program by Harry B Samuels

### This is an **evolution simulator** that creates simple creatures called doplings. They look like this: `a`
### The doplings live on a tiny grid that looks like this:
```
+   A B C D E F G H I

A   . . . . . . . . .
B   . . . b . . . . .
C   . * . . . . . . .
D   . . . . . . a . .
E   . . . . . . . . .
```

## What are doplings?
- Doplings are modelled after single-celled organisms
- They can move around the grid, see their surroundings, eat food, reproduce, mutate, and _EVOLVE_

## What do the doplings do?

- Each turn, every dopling moves 1 space on the grid (up, down, right, or left)
- If a dopling runs off of the grid, or into another dopling, it lyses (and dies :c)
- Doplings decide which direction to move, and when to "split" into 2 doplings, using a system of proteins
- Every 10 turns, a dopling will grow up by one letter, reflecting its age:
    - doplings start as an `a`, then grow to `b`, then `c`, and so on, until they reach `z` and then `A`
    - after `Z` the dopling becomes an "elder", and will look like this: `&`

## Why are doplings?
- This simulation is meant to demonstrate (at a very simplified scale) how single-celled organisms "work" on a functional level 
- Cells use a massive number of proteins, encoded in DNA as "genes", to interact with their environment, reproduce, and perform all sorts of important actions
- The doplings let users take a look "inside the cell" to see how genes (and their corresponding proteins) can evolve over time to create intricate systems using simple pieces
Initially, the doplings will move randomly, and without purpose. But! After enough generations (and a little luck), the doplings will begin to ***evolve*** in new and exciting ways

## How do the doplings work? (The Nitty-Gritty)
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
          
