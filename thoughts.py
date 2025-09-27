import cell

import random

def think(thinkerCell):
    if thinkerCell.lysed:
        thought= [
            "Heaven is real!!!!!!",
            "Hell is real :( :( :(",
            "Youch",
            "Ouch",
            "So long, cruel world",
            "One minute you're hot and the next you're not",
            "My favorite place on earth was " + thinkerCell.location.coordDisplay,
            "oooOOoooOOOooo I'm a ghost now",
            "Was it something I said?",
            "Oh no, I'm dead now"
        ][thinkerCell.numberID%10]   #int(str(thinkerCell.numberID)[len(str(thinkerCell.numberID))-1:])]

    else:
        thought= random.choice([
            "I love " + random.choice(TOPICS),
            "I hate " + random.choice(TOPICS),
            "Have you heard about " + random.choice(TOPICS) + "?",
            "I've been really into " + random.choice(TOPICS) + " lately",
            SKYLANDERS[thinkerCell.numberID%6] + " is the best Skylanders game",
            familyThought(thinkerCell)
        ])

    return thought

def familyThought(thinkerCell):
    #if cell has children and 50% probabilty:
    if (len(thinkerCell.genealogy.children) > 0) and (random.randint(0,1) == 1):
        thought= random.choice([
            "I'm a little worried about " + random.choice(thinkerCell.genealogy.children).cell.name,
            "Don't tell the rest, but " + thinkerCell.genealogy.children[0].cell.name + " is my favorite child",
            "I dont care for " + random.choice(thinkerCell.genealogy.children).cell.name,
            "One day maybe " + random.choice(thinkerCell.genealogy.children).cell.name + " will be the greatest common ancestor"
            ""
        ])
    #if cell was spontaneously generated:
    elif thinkerCell.genealogy.mother is None:
        thought= random.choice([
            "How did I get here?",
            "Take that Louis Pasteur!",
            "I'm here for a good time, not for a long time",
            "How do you work this thing?",
            "Why couldn't I have been born a eukaryote?"
        ])
    #if cell has siblings:
    elif len(thinkerCell.genealogy.mother.children) >1:
        siblingList= (thinkerCell.genealogy.mother.children).copy()
        #remove this cell from sibling list
        siblingList.pop(siblingList.index(thinkerCell.genealogy))
        sibling= (random.choice(siblingList)).cell
        siblingStatus= "still alive"
        if sibling.lysed:
            siblingStatus= "dead"
        thought= random.choice([
            "My mother always liked " + sibling.name + " better",
            "Mom says " + sibling.name + " got the brains, but I got the looks",
            sibling.name + " thinks they're a big hotshot out in " + sibling.location.coordDisplay,
            "I miss " + sibling.name,
            sibling.name + " makes me embarrassed to be a " + thinkerCell.genealogy.taxon.species,
            "I can't believe " + sibling.name + " is " + siblingStatus
        ])

    #cell is an only child:
    else:
        thought= random.choice([
            "Can you tell I'm an only child?",
            "I think we live in a Simulation",
            "I need " + thinkerCell.genealogy.mother.cell.name + " to make me a sibling",
            "God I'm bored",
            "Do you know any good jokes?",
            "I must carry on " + thinkerCell.genealogy.mother.cell.name + "'s genetic legacy, lotta pressure",
            "One is the lonliest number",
            "Wanna play Skylanders?"
        ])
    
    return thought








TOPICS=[
    #videogamez
    "Webkinz",
    "Club Penguin",
    "Moshi Monsters",
    "World of Warcraft",
    "Overwatch",
    "Dig Dug",
    "Fortnite",
    "agar.io",
    "Minecraft Hunger Games",
    "Just Dance",
    "Skylanders: Spyro's Adventure",
    "Skylanders: Giants",
    "Skylanders: Swap Force",
    "Skylanders: Trap Team",
    "Skylanders: Super Chargers",
    "Skylanders: Imaginators",
    #animals
    "French Bulldogs",
    "Pelicans",
    #video media
    "Ghostbusters 2",
    "Ocean's 12",
    "Air Bud",
    "Love Actually",
    "The Smurfs",
    "Ant-Man and the Wasp",
    "Grey's Anatomy",
    "Pretty Little Liars",
    "Gossip Girl",
    "Gilmore Girls",
    "The Golden Girls",
    "Sex and the City",
    "New Girl",
    "The Wire",
    "The Sopranos",
    "Breaking Bad",
    "Casablanca",
    "Bakugan",
    "Power Rangers",
    "The Snorks",
    #Books
    "The Hunger Games",
    "Diary of a Wimpy Kid",
    "Animorphs",
    "Twilight",
    "MAD Magazine",
    "Ender's Game",
    "Murder on the Orient Express",
    "Of Mice and Men",
    #fictional characters
    "Scrappy-Doo",
    "Magneto",
    "Kylo Ren",
    "Jar Jar Binks",
    "Chester Cheeto",
    "Captain Crunch",
    "the Trix Rabbit",
    "the Lorax",
    "Fred FLinstone",
    "George Jetson",
    #activities
    "Rugby",
    "Woodworking",
    "Rubik's Cubing",
    "Fishkeeping",
    "Horse Racing",
    "Karate",
    "Unicycling",
    "Needlepointing",
    "Reflexology",
    "Performative Activism",
    "Horticulture",
    "Bowling",
    "Birdwatching",
    "Geocaching",
    "Cow Tipping",
    "Pheasant Hunting",
    "Hang Gliding",
    "Coin Magic",
    "Fly Fishing",
    "Bedazzling",
    "Solitaire",
    "Magic the Gathering",
    #food
    "Brewing Kombucha",
    "Sourdough Bread",
    "Rainbow bagels",
    "Cacti",
    "Pistachios",
    "Pastrami",
    "White Bread",
    "Chicken Parmesean",
    "Kerrygold Butter",
    "Pasta Salad",
    "Seltzer",
    "Alka-Seltzer",
    "Olive Oil",
    #objects
    "Mechanical Pencils",
    "Participation Trophies",
    "The Holy Grail",
    "Flourescent Lightbulbs",
    "Polo Shirts",
    "Aquariums",
    "Disco Balls",
    "Ouji Boards",
    "Billiards",
    "Silent Film",
    "Analog Clocks",
    "Hot Wheels",
    "Adirondack Chairs",
    #Misc
    "Monsanto",
    "Walgreens",
    "Fubo TV",
    "Astrology",
    "Polka-Dots",
    "The Former Yugoslavia",
    "The Ship of Theseus",
    "The New York Jets",
    "NPR",
    #People
    "Pete Davidson",
    "Grover Cleveland",
    "Mr. Beast",
    #Music
    "Hall & Oates",
    "Weezer",
    "The Wiggles"
]

SKYLANDERS= [
    "Skylanders: Spyro's Adventure",
    "Skylanders: Giants",
    "Skylanders: Swap Force",
    "Skylanders: Trap Team",
    "Skylanders: Super Chargers",
    "Skylanders: Imaginators"
]