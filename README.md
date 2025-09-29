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

### What are doplings?
- Doplings are modelled after single-celled organisms
- They can move around the grid, see their surroundings, eat food, and reproduce

### What do the doplings do?

- Each turn, every dopling moves 1 space on the grid (up, down, right, or left)
- If a dopling runs off of the grid, runs out of food, or runs into another dopling, it lyses (and dies :c)
- Doplings decide which direction to move, and when to "split" into 2 doplings, using a system of proteins
- Every 10 turns, a dopling will grow up by one letter, reflecting its age:
    - doplings start as an `a`, then grow to `b`, then `c`, and so on, until they reach `z` and then `A`
    - after `Z` the dopling becomes an "elder", and will look like this: `&`


