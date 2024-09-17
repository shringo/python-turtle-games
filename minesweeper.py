import turtle as turt
import random as rand
from functools import partial
from platform import system
from time import time

# Determines which button is the right click button based on the operating system (macOS, Linux, Windows)
rightClickBtn = 3 if system() == "Windows" else 2

columns = 12
rows = 10

# Colors each number on a minesweeper map based upon this list
colors = [
    # Color  | # Amount of mines nearby
    "#DDDDDD", # 0 (same as background color - nothing should be showing)
    "#0000FF", # 1
    "#00DD00", # 2
    "#FF0000", # 3
    "#FF00FF", # 4
    "#FF9900", # 5
    "#00FFFF", # 6
    "#FFFF00", # 7
    "#000000", # 8 (unlikely)
    "#FFFFFF", # 9 (impossible but why not)
]

# Draws a checkmark (appears in the upper left corner)
def drawCheck(relX=0, relY=0, scale=1):
    statusTurtle.clear()
    statusTurtle.color("#11EF11")
    statusTurtle.pensize(10)
    statusTurtle.hideturtle()
    statusTurtle.penup()
    statusTurtle.goto(relX, relY)
    statusTurtle.goto(statusTurtle.xcor()-10*scale,statusTurtle.ycor())
    statusTurtle.pendown()
    statusTurtle.goto(statusTurtle.xcor()+5*scale, statusTurtle.ycor()-10*scale)
    statusTurtle.goto(statusTurtle.xcor()+15*scale, statusTurtle.ycor()+20*scale)

    # Frequently used method in this program, this updates what appears on the game screen.
    turt.update()

# Draws a X (fail mark) (appears in the upper left corner)
def drawFail(relX=0, relY=0, scale=1):
    statusTurtle.clear()
    statusTurtle.color("#FF0000")
    statusTurtle.pensize(10)
    statusTurtle.hideturtle()
    statusTurtle.penup()
    statusTurtle.goto(relX, relY)
    statusTurtle.pendown()
    statusTurtle.goto(statusTurtle.xcor()-10*scale, statusTurtle.ycor()+10*scale)
    statusTurtle.goto(statusTurtle.xcor()+20*scale, statusTurtle.ycor()-20*scale)
    statusTurtle.penup()
    statusTurtle.goto(statusTurtle.xcor()-20*scale, statusTurtle.ycor())
    statusTurtle.pendown()
    statusTurtle.goto(statusTurtle.xcor()+20*scale, statusTurtle.ycor()+20*scale)
    turt.update()

# Draws a bomb when you click on a tile with a bomb
def drawBomb(turtle):
    turtle.color("#000000")
    turtle.begin_fill()
    turtle.goto(turtle.xcor()-20,turtle.ycor()+2)
    for _ in range(9):
        turtle.forward(40)
        turtle.left(200)
    turtle.end_fill()
    turtle.hideturtle()
    turtle.setheading(0)
    turt.update()

# Draws the grid when you run the program
def drawGrid():
    t = turt.Turtle("circle")
    t.color("#000000")
    t.pensize(2)
    t.hideturtle()
    for x in range(columns+1):
        xcor = -300 + x*50
        t.penup()
        t.goto(xcor, 200)
        t.pendown()
        t.goto(xcor, 200 - (rows*50))
    for x in range(rows+1):
        ycor = 200 - x*50
        t.penup()
        t.goto(-300, ycor)
        t.pendown()
        t.goto(-300 + (50*columns), ycor)
    turt.update()

# This function triggers every time the user right clicks on a tile on the game screen. This flags or unflags a tile.
# The xc and yc arguments are used to select the corresponding object from the gameBoard list.
# _x and _y, are unused because they are the coordinates of where the user clicked on the screen, and NOT numbers that can get us objects from the gameBoard list.
def onFlagClick(_x,_y,   xc, yc):

    # We use yc first because we have to select the row then column.
    entry = gameBoard[yc][xc]

    # Checks to see if the user has a board with numbers/empty tiles already showing.
    # Also check to see if the game ended already
    if firstClick and not end:

        # In Minesweeper, users can flag any tile, even if it doesn't have a bomb.
        if not entry["flagged"]:
            # If the turtle wasn't flagged, change the color to red and mark it as flagged.
            entry["flagged"] = True
            entry["turtle"].color("#FF1111")
        else:
            # If the turtle was flagged, change the color back to gray and mark it as not flagged.
            entry["flagged"] = False
            entry["turtle"].color("#AAAAAA")
        turt.update()

# This shows in the game screen the tile's number. Entry is any non-list element from the gameBoard list.
def showNumber(entry):
    if entry["sign"] == 0 or not type(entry["sign"]) == int: return

    # The tile has to be hidden in order to see the number
    entry["turtle"].hideturtle()
    entry["turtle"].clear()

    # We select from the colors list the color based off of the sign
    # I arranged the colors list in such a way where the sign corresponded to the color in the list, i.e. 3 translated as index for the color all 3s should be
    entry["turtle"].color(colors[entry["sign"]])

    # Move the turtle so the text is perfectly centered in the tile's space on the game screen.
    entry["turtle"].goto(entry["turtle"].xcor()+1,entry["turtle"].ycor()-17)
    entry["turtle"].write(entry["sign"], align="center", font=("Times New Roman", 25, "bold"))
    entry["turtle"].color('#FFFF00')
    entry["turtle"].goto(entry["turtle"].xcor()-1,entry["turtle"].ycor()+17)

# This reveals the numbers and nearby tiles if the space is empty (no bombs nearby)
def remove(xc, yc):
    # We iterate through a list of coordinates of all tiles nearby a given coordinate (xc and yc)
    # Tiles that are diagonal are included, as well as the original pair.
    for pair in [
        [xc+1,yc],
        [xc-1,yc],
        [xc,yc+1],
        [xc,yc-1],

        [xc+1,yc+1],
        [xc-1,yc-1],
        [xc-1,yc+1],
        [xc+1,yc-1],

        [xc,yc]
    ]:
        try:
            # If any of the modified coordinates are negative, ignore it (this causes Python to index the list by going to the end of the list)
            if pair[0] < 0 or pair[1] < 0: continue

            # Select an element with the modified coordinates
            entry = gameBoard[pair[1]][pair[0]]

            # Only consider revealing the tile if it:
            # - Has not been clicked yet
            # - Isn't a mine
            # - Isn't flagged
            if entry["turtle"].isvisible() and type(entry["sign"]) == int and entry["flagged"] == False:

                # If the tile is empty (no mines nearby, including diagonally), reveal the blank tile but run this function again to get rid of adjacent blank tiles, until we run into adjacent number tiles
                if entry["sign"] == 0:
                    entry["turtle"].hideturtle()

                    # We run this function until all adjacent blank tiles and number tiles are revealed. 'True' is provided here so we also eventually reveal the tile we initially clicked on. 
                    remove(pair[0], pair[1])
                else:
                    # If the tile has bombs nearby, then show the number and do nothing else.
                    showNumber(entry)
            else:
                continue

        # Ignore any errors if we try to index the list with a number longer than the list's length.
        # For example, we cant get the 13th tile in a row if the board is 12 tiles long.
        except IndexError:
            pass

# This function triggers every time the user left clicks on a tile on the game screen. This triggers the remove function and ends the game if you click on a bomb or reveal all non-bomb tiles.
# The xc and yc arguments have the same purpose from the onFlagClick function, _x and _y are unused for the same reason as well.
def onTileClick(_x, _y,   xc, yc):
    global gameBoard, firstClick, textTurtle, end, start

    # Ignore clicks post-game
    if end: return

    # If this is the user's first move on the game board, then run the code inside this if statement.
    if not firstClick:
        # This section of code makes it so when you make the first move on the board, you will click on an empty space so you don't immediately end the game by clicking on a bomb tile
        
        # Used to show the user how much time they took to complete a board
        start = time()
        
        # We generate a new minesweeper board until the xc and yc coordinate is an empty tile.
        isEmpty = False
        while not isEmpty:
            # Reset board by setting all signs to 0
            for row in gameBoard:
                for tile in row:
                    tile["sign"] = 0

            # Setting mines
            # Create a copy of mines variable so we don't modify the mines variable.
            _mines = mines * 1
            while _mines > 0:
                # Set random tiles on the board to a bomb until we reach the amount of bombs the mines variable is.
                randx = rand.choice(range(len(gameBoard[0])))
                randy = rand.choice(range(len(gameBoard)))
                # Prevent a tile from being set to a bomb again
                if gameBoard[randy][randx]["sign"] != "X":
                    gameBoard[randy][randx]["sign"] = "X"
                    _mines -= 1

            # Set number tiles
            for x in range(len(gameBoard[0])):
                for y in range(len(gameBoard)):
                    # Ignore bomb tiles
                    if gameBoard[y][x]["sign"] == "X": continue

                    # Check all adjacent tiles, including diagonals
                    for pair in [
                        [x+1,y], # Right
                        [x-1,y], # Left
                        [x,y+1], # Up
                        [x,y-1], # Down

                        [x+1,y+1], # Up right
                        [x-1,y+1], # Up left
                        [x-1,y-1], # Down left
                        [x+1,y-1]  # Down right
                    ]:
                        try:
                            # If any of the coordinates are negative, ignore it, as it will wrap around to the other side of the board.
                            if gameBoard[pair[1]][pair[0]]["sign"] == "X" and not (pair[0] < 0 or pair[1] < 0):
                                gameBoard[y][x]["sign"] += 1
                        except IndexError:
                            pass
            # Sets isEmpty to a boolean value, where it is true if we clicked on an empty tile on the newly generated board
            # If this value is false, the loop repeats until it is.
            isEmpty = gameBoard[yc][xc]["sign"] == 0
        # This makes it so a new board doesn't generate every time we click on the game board.
        firstClick = True

    entry = gameBoard[yc][xc]
    # Prevent user from clearing a flagged tile if it is safe
    if entry["flagged"]: return
    if type(entry["sign"]) == int:
        # If the user clicked on a tile that isn't a bomb, we remove the tile if it has no surrounding bombs, otherwise we show the number if there are bombs.
        if entry["sign"] == 0: remove(xc,yc)
        else: showNumber(entry)

        # This code ends the game if the user clicked on all tiles that aren't bombs.
        if all(all(not tile["turtle"].isvisible() for tile in row if type(tile["sign"]) == int) for row in gameBoard):
            textTurtle.clear()
            textTurtle.goto(50,250)
            textTurtle.write("Minesweeper", font=("Arial", 30, "bold"), align="center")
            textTurtle.goto(50,235)
            textTurtle.write("You win!", font=("Arial", 10, "normal"), align="center")
            textTurtle.goto(50,220)
            textTurtle.write("Time: " + str(round((time() - start))) + " seconds", font=("Arial", 10, "normal"), align="center")
            textTurtle.goto(50,205)
            textTurtle.write("Press your spacebar key to reset.", font=("Arial", 10, "normal"), align="center")

            # Helps to remove any click functionality
            end = True

            # Make the program wait for you to press the spacebar to start a new game
            turt.onkeypress(init, key="space")
            turt.listen()
    elif entry["sign"] == "X":
        # Helps to remove any click functionality
        end = True

        # End the game if the user clicked on a bomb tile.
        drawFail(-250,250,3)

        # Set numbers to show how many bombs the user incorrectly flagged or correctly identified
        minesFound = 0
        misflagged = 0

        # Iterate through the entire board
        for row in gameBoard:
            for tile in row:
                if tile["sign"] == "X":
                    if tile["flagged"]:
                        # Make color green, changes any turtles that were already red on the game board
                        tile["turtle"].color("#11FF11")
                        minesFound += 1
                    else:
                        # Draw bombs revealing where every bomb was
                        drawBomb(tile["turtle"])
                elif tile["sign"] != "X":
                    if tile["flagged"]:
                        misflagged += 1

        textTurtle.clear()
        textTurtle.goto(50,250)
        textTurtle.write("Minesweeper", font=("Arial", 30, "bold"), align="center")
        textTurtle.goto(50,235)
        textTurtle.write("You clicked on a mine!", font=("Arial", 10, "normal"), align="center")
        textTurtle.goto(50,220)
        textTurtle.write("You flagged " + str(minesFound) + " mines (green) and misflagged " + str(misflagged) + " tiles (red).", font=("Arial", 10, "normal"), align="center")
        textTurtle.goto(50,205)
        textTurtle.write("Press your spacebar key to reset.", font=("Arial", 10, "normal"), align="center")

        # Make the program wait for you to press the spacebar to start a new game
        turt.onkeypress(init, key="space")
        turt.listen()

    turt.update()

def setHitboxes():
    # Fill the board with clickable tile objects based on the turtle class
    for x in range(len(gameBoard[0])):
        # Precise number to make sure that the turtle perfectly aligns in the black lines on the game board
        xcor = -275.5 + x*50
        for y in range(len(gameBoard)):
            ycor = 175.5 - y*50
            ttl = turt.Turtle("square")
            ttl.penup()
            # Colored slightly darker so the user can tell the difference between an empty tile and a non-interacted tile
            ttl.color("#AAAAAA")
            ttl.shapesize(5.3**.5)
            ttl.goto(xcor, ycor)

            gameBoard[y][x]["turtle"] = ttl

            # The 'partial' function makes it possible to feed more than the click's x and y coordinate to an event handler.
            # In this case, I give the partial function the position of where the turtle would appear on the gameBoard list used in my program.

            # This is what will happen if the user left-clicks on a turtle.
            ttl.onclick(partial(onTileClick, xc=x, yc=y), btn=1)

            # This is what will happen if the user right-clicks on a turtle.
            ttl.onclick(partial(onFlagClick, xc=x, yc=y), btn=rightClickBtn)

    turt.update()

# In order to start a new game, all variables are reset so nothing from the previous game carries over into the next game
def init():
    global textTurtle, gameBoard, statusTurtle, firstClick, mines, end

    # Determine a random amount of mines to scatter across the map
    mines = rand.randint(int((columns*rows)/10), int((columns*rows)/5))

    # Reset the board
    turt.Screen().clear()
    turt.title("Minesweeper")
    turt.setup(600, 600)

    # This makes it so all drawings like the grid are created instantaneously by using the turt.update() method rather than animating the movement
    turt.tracer(0, 0)
    turt.Screen().bgcolor("#DDDDDD")
    turt.hideturtle()

    # Prevent the program from crashing if the user edits the code to have more mines on the board
    mines = round((columns*rows)/2) if mines > (columns*rows)/2 else mines

    '''
        The gameboard list will look like this in Python:
        [
            [ [{"turtle": <Turtle on Screen>, "sign": 1, "flagged": False}], [{"turtle": <Turtle on Screen>, "sign": 1 , "flagged": False}], [{"turtle": <Turtle on Screen>, "sign": 1, "flagged": False}], [{"turtle": <Turtle on Screen>, "sign": 0, "flagged": False}] ],
            [ [{"turtle": <Turtle on Screen>, "sign": 1, "flagged": False}], [{"turtle": <Turtle on Screen>, "sign":'X', "flagged": True }], [{"turtle": <Turtle on Screen>, "sign": 1, "flagged": False}], [{"turtle": <Turtle on Screen>, "sign": 0, "flagged": False}] ],
            [ [{"turtle": <Turtle on Screen>, "sign": 1, "flagged": False}], [{"turtle": <Turtle on Screen>, "sign": 1 , "flagged": False}], [{"turtle": <Turtle on Screen>, "sign": 1, "flagged": False}], [{"turtle": <Turtle on Screen>, "sign": 0, "flagged": False}] ]
        ]

        Here is a human readable version where only the "sign" value is displayed:
        [
                          <-4 columns (0 to 3)->
                ^         [  1,   1 ,  1,   0  ]
         3 rows (0 to 2)  [  1,  'X',  1,   0  ]
                V         [  1,   1 ,  1,   0  ]
        ]

        In order to make the list easier to work with in Python, each row is filled with objects instead of a list. 
        If I wanted to access the turtle element on a list, it would look like this:    element[0] (assuming that the first element contains the turtle used in the game window)
        If I wanted to access the turtle element on an object, it would look like this: element["turtle"], which is much easier to understand.

        This is what each property defined on each object does:
         - turtle:  This is the clickable tile on screen when you run this program
         - sign:    This displays the number of mines that is nearby the tile, OR it will display X to indicate it is a bomb.
            - The sign can be an integer value (numbers), or a string value like a letter.
            - If the sign is 0, it is an empty space. Numbers 1-8 will mean that amount of bomb(s) are nearby the tile.
            - If the sign is the letter X, then the tile is a bomb and clicking on it will end the game early.
         - flagged: This indicates to the user if they think the tile is a bomb by clicking on it, and can be assigned or removed when right clicking on a tile.
    '''

    # Allows the program to create a board where the user clicks on an empty space as their first move.
    firstClick = False

    # Set up a multi-dimensional list that has x columns and y rows.
    # See the huge block comment above on an explanation on how this list is used throughout the program
    gameBoard = [ [ {"turtle": None, "sign": 0, "flagged": False} for __ in range(columns) ] for _ in range(rows) ]

    # Create the turtle that draws the check/x-mark in the upper left corner
    statusTurtle = turt.Turtle("circle")

    # Writes text at top
    textTurtle = turt.Turtle("blank")
    textTurtle.penup()
    textTurtle.goto(50,250)
    textTurtle.write("Minesweeper", font=("Arial", 30, "bold"), align="center")
    textTurtle.goto(50,235)
    textTurtle.write("Left click on a tile to reveal itself", font=("Arial", 10, "normal"), align="center")
    textTurtle.goto(50,220)
    textTurtle.write("Right click on a tile to flag/unflag it as a mine (marked as red)", font=("Arial", 10, "normal"), align="center")
    textTurtle.goto(50,205)
    textTurtle.write("This map has " + str(mines) + '/' + str(12*10) + " mine(s).", font=("Arial", 10, "normal"), align="center")

    drawGrid()
    drawCheck(-250,250,3)
    setHitboxes()

    # Used to stop any clicking actions
    end = False

init()

# Prevents the program from immediately opening then closing
turt.mainloop()