# This is a treasure hunt game.
#
# The world is a grid (defined by GRID_SIZE).  The player starts in position (1,1).
# A monster is randomly positioned within the world, along with a number of
# treasures.  The player must find all treasures without getting eaten by the
# monster.
#
# The player is warned when they are near the monster, which should help them evade it.
#
# The player can use the commands L, R, U, and D to move.  They can quit the game with the
# Q command.


import random

#
# This class defines a location within the game grid.  It has both an X- and Y- coordinate.
class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def isEqualTo(self, pt):
        if (pt == None):
            return False

        if (self.x == pt.x and self.y == pt.y):
            return True

        return False

    def isAdjacentTo(self, pt):
        if ((self.y < pt.y - 1) or (self.y > pt.y + 1)):
            return False

        if ((self.x < pt.x - 1) or (self.x > pt.x + 1)):
            return False

        return True

treasures = ['gem', 'ruby', 'diamond', 'coin', 'emerald', 'goblet']
GRID_SIZE = 5
treasure_locations = []
monster_location = Point(0,0)
player_location = Point(0,0)
foundTreasureCount = 0

# Initialize a new game
def initGame():
    global player_location
    global treasure_locations
    global monster_location
    global foundTreasureCount

    foundTreasureCount = 0

    # Position the player in the top left corner of the grid (1,1)
    player_location = Point(1,1)
    occupied_locations = [player_location]

    # Choose a random location for the monster, excluding the player's location
    monster_location = chooseUnoccupiedLocation(occupied_locations)

    # Randomly locate each of the treasures in unoccupied spaces
    for i in range(0, len(treasures)):
        treasure_locations.append(chooseUnoccupiedLocation(occupied_locations))

# Find a point within a list and return its position, or -1 if not found
def findPoint(list, pt):
    for i in range(0, len(list)):
        if (list[i].isEqualTo(pt)):
            return i

    return -1


# Choose a random unoccupied position within a list of used locations.  The new location is added to the
# list, and the new location is returned.
def chooseUnoccupiedLocation(usedLocations):
    while True:
        location = Point(random.randint(1, GRID_SIZE), random.randint(1, GRID_SIZE))

        if (findPoint(usedLocations, location) < 0):
            usedLocations.append(location)
            return location

# Handle the player entering a new location in the game
def enterLocation(location):
    global player_location
    global monster_location
    global foundTreasureCount

    player_location = location

    print "You are now in location " + player_location.toString()

    # If the monster is here, the game is over
    if (monster_location.isEqualTo(player_location)):
        print("Oh no!!  You've been eaten by a hungry monster!")
        return False

    # Determine if any treasure is in the location
    treasure = findPoint(treasure_locations, player_location)

    if (treasure >= 0):
        print "You found the " + treasures[treasure]
        treasures[treasure] = None

        foundTreasureCount += 1

        # Determine if the game has been won (i.e., all treasure found).  Otherwise, let the player know how many
        # treasures are left.
        if (foundTreasureCount == len(treasures)):
            print "You found all " + str(foundTreasureCount) + " treasures!  You win!!"
            return False
        else:
            remainingTreasures = len(treasures) - foundTreasureCount

            print "You have " + str(remainingTreasures) + " more treasure" + ("s" if remainingTreasures > 1 else "") + " to find!"

    # If the monster is nearby, let the player know
    if (monster_location.isAdjacentTo(player_location)):
        print "You can hear a growling sound nearby!"

    return True

# Process a command from the player
def processCommand(command):
    command = command.lower()

    if (command == ""):
        print "What??"
        return False

    if (command == "q"):
        return True

    newLocation = None

    # Handle a possible movement command
    if (command == "l"):
        if (player_location.x > 1):
            newLocation = Point(player_location.x - 1, player_location.y)
    elif (command == "r"):
        if (player_location.x < GRID_SIZE):
            newLocation = Point(player_location.x + 1, player_location.y)
    elif (command == "u"):
        if (player_location.y > 1):
            newLocation = Point(player_location.x, player_location.y - 1)
    elif (command == "d"):
        if (player_location.y < GRID_SIZE):
            newLocation = Point(player_location.x, player_location.y + 1)
    else:
        print "I don't know what you mean"
        return True

    if (newLocation == None):
        print "You can't move in that direction"
        return True

    return enterLocation(newLocation)

# Implement the game loop, which repeats until the game is over.
def game_loop():
    gameActive = enterLocation(player_location)

    while gameActive == True:
        print "\nWhat do you want to do? "
        option = raw_input()

        gameActive = processCommand(option)

# Initialize the gamer
initGame()
game_loop()

print "Thanks for playing!"


