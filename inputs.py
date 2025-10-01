"""
Changing these values will allow you to create new evolutionary environments for the doplings! 
- You can us the example custom maps as a reference for how to make new ones
- While each of these inputs can be changed, be cautious when making changes
- The more a given set of inputs differ from the default, the more likely you are to encounter glitches
- The only current know way for the simulation to "get stuck" and break without crashing, is when there are no available spaces for new food to be spawned due to an overabundance of doplings filling up every space
- Try weird stuff anyway!
"""

#used in main

# How many rows the map has (positive int). Should be at least 50+ for the display to look correct
MAP_ROWS= 100
# How many columns the map has (positive int) 
MAP_COLUMNS= 100
# If the map is too small for the number of doplings, the simulation will be unable to spawn food and loop infinitely, breaking

# How many pieces of food are spawned per turn (positive int). Can be 0
FOOD_PER_TURN= 9
# How much food value should each piece of spawned food provide (float)
FOOD_VALUE= 1

# What is the minimum number of living doplings (positive int)
BASE_CELL_NUMBER= 25
# How much food should spontaneously generated doplings have
SPAWNED_CELL_FOOD= 5


#used in cell

# What is the minimum food cost for a dopling to move
FOOD_TO_MOVE= 0.025

#How many messenger proteins should spontaneously generated dopling have
MESSENGER_PROTEIN_NUMBER= 4
#How many secondary messenger proteins should spontaneously generated dopling have
SECONDARY_MESSENGER_NUMBER= 0

#used in grid

# Pac-Man mode creates an edgeless map by connecting the left side of the map to the right, and the top of the map to the bottom
PAC_MAN_MODE= False

# If True, the map json file located at CUSTOM_MAP_FILE will be used as the map for the simulation
USE_CUSTOM_MAP= False
# What is the path of the custom map file to be used
CUSTOM_MAP_FILE= "custom_maps/canyon.json"


# DEFAULT VALUES

# MAP_ROWS= 100
# MAP_COLUMNS= 100
# FOOD_PER_TURN= 9
# FOOD_VALUE= 1
# BASE_CELL_NUMBER= 25
# SPAWNED_CELL_FOOD= 5
# FOOD_TO_MOVE= 0.025
# MESSENGER_PROTEIN_NUMBER= 4
# SECONDARY_MESSENGER_NUMBER= 0
# PAC_MAN_MODE= False
# USE_CUSTOM_MAP= False
# CUSTOM_MAP_FILE= "custom_maps/canyon.json"