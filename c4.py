# if you get more than 2 people to play this, it gets really fun

import turtle as turt
import random as rand
from functools import partial

turt.tracer(0,0)
turt.Screen().setup(720,800)
players = None# 2
while players is None:
    players = turt.numinput(
        title="HOW MANY PLAYERS?",
        prompt="How many players are playing?",
        default=2, minval=2, maxval=10)
players = int(players)
columns = None #7
while columns is None:
    columns = turt.numinput(
        title="HOW MANY COLUMNS?",
        prompt="How many columns? (Vertical)",
        default=7, minval=7, maxval=21)
columns = int(columns)
rows = None#6
while rows is None:
    rows = turt.numinput(
        title="HOW MANY ROWS?",
        prompt="How many rows? (Horizontal)",
        default=6, minval=6, maxval=18)
rows = int(rows)
RANDOM = None#6
while RANDOM is None:
    RANDOM = turt.numinput(
        title="ALLOW RNG?",
        prompt="Allow random turns? (0=no,1=yes) (No order in turns, turns will NOT repeat)",
        default=0, minval=0, maxval=1)
RANDOM = RANDOM == 1
scaleFactor = ((6/rows) + (7/columns)) / 2
beginX = scaleFactor * (-(columns/2)*100+44)
beginY = scaleFactor * (-(rows/2)*100-40)

pointerColors = [
    (200,0,0),
    (200,200,0),
    (0,0,180),
    (0,200,0),
    (200,0,200),
    (0,200,200),
    (200,0,90),
    (200,90,0),
    (150,82,200),
    (100,100,100)
]

pieceColors  = [
    (255,0,0),
    (255,255,0),
    (0,0,200),
    (0,255,0),
    (255,0,255),
    (0,255,255),
    (255,0,100),
    (255,100,0),
    (170,102,255),
    (200,200,200)
]

def showHelp():
    turt.textinput(
        "HOW TO PLAY CONNECT 4",
        "Get 4 of your colored pieces in a row. You can match 4 pieces vertically, horizontally, and diagonally."
    )
    turt.listen()
    turt.update()

def updatePointer():
    lowest = 0
    for slice in gameBoard:
        if slice[pointer["column"]]["player"] is None: break
        else: lowest += 1
    if lowest >= rows:
        pointer["turtle"].color((0,0,0))
#    else: pointer["turtle"].color((200,0,0) if turn else (200,200,0))
    else: pointer["turtle"].color(pointerColors[turn])

def runWin(any=True):
    turt.onkeypress(init, "space")
    turt.onkeypress(None, key="Left")
    turt.onkeypress(None,key="Right")

    pointer["turtle"].clear()
    pointer["turtle"].hideturtle()
    WRITE.clear()
    v = turt.Turtle("blank")
    v.penup()
    v.goto(0,300)
    if any: 
        #v.write("Victory royale to: " + ("Yellow" if turn else "Red"), font=("Arial", 30, "normal"), align="center")
        v.write("Victory royale to: Player " + str(players if turn == 0 else turn), font=("Arial", 30, "normal"), align="center")
    else:
        v.write("Victory royale to NO ONE", font=("Arial", 30, "normal"), align="center")
    v.goto(0,270)
    v.write("PRESS SPACE TO RESET", font=("Arial", 14, "normal"), align="center")
    turt.update()

def checkWin():
    for y in range(len(gameBoard)):
        for x in range(len(gameBoard[y])):
            status = gameBoard[y][x]["player"]
            if status is None: continue
            else:
                slices = []
                tempSlice = []
                for ele in gameBoard[y]:
                    tempSlice.append(ele["player"])
                slices.append(tempSlice)
                tempSlice = []
                for row in gameBoard:
                    tempSlice.append(row[x]["player"])
                slices.append(tempSlice)
                for diag in [
                    [1,  1],
                    [1, -1],
                    [-1, 1],
                    [-1,-1]
                ]:
                    tempSlice = []
                    run = True
                    tempX = x
                    tempY = y
                    while run:
                        try:
                            if tempY < 0 or tempX < 0: break
                            tempSlice.append(gameBoard[tempY][tempX]["player"])
                            tempY += diag[0]
                            tempX += diag[1]
                        except IndexError:
                            run = False
                    slices.append(tempSlice)
                counter = 0
                for slice in slices:
                    if counter >= 3: break
                    counter = 0
                    lastElement = None
                    for s in range(len(slice)):
                        if counter >= 3: break
                        if slice[s] is not None and slice[s] == lastElement:
                            counter += 1
                        else: counter = 0
                        lastElement = slice[s]
                if counter == 3:
                    runWin()
    if all(all(y["player"] is not None for y in x) for x in gameBoard):
        runWin(False)

def moveEvent(isLeft):
    global pointer
    pt = pointer["turtle"]
    if (pointer["column"] == 0 and isLeft) or (pointer["column"] == columns-1 and not isLeft): return
    pointer["column"] += -1 if isLeft else 1
    pt.goto(beginX + pointer["column"]*100*scaleFactor, pt.ycor())
    updatePointer()
    turt.update()

def enterEvent():
    global pointer, gameBoard, turn
    lowest = 0
    for slice in gameBoard:
        if slice[pointer["column"]]["player"] is None: break
        else: lowest += 1
    if lowest >= rows: return
    else: pointer["turtle"].color((200,255,0))
#    gameBoard[lowest][pointer["column"]]["turtle"].color((255,0,0) if turn else (255,255,0))
    gameBoard[lowest][pointer["column"]]["turtle"].color(pieceColors[turn])
    gameBoard[lowest][pointer["column"]]["player"] = turn
    if RANDOM:
        _turn = turn
        while _turn is turn:
            _turn = rand.randint(0,players-1)
        turn = _turn
    else: turn += 1
    if turn > players-1:
        turn = 0
    updatePointer()
    checkWin()
    turt.update()

def drawGrid():
    global gameBoard
    temp = turt.Turtle("blank")
    temp.color("#000077")
    temp.pensize(4)
    temp.penup()
    temp.goto( scaleFactor * (-(columns/2)*100-20) ,  scaleFactor * ((rows/2)*100-80))
    temp.begin_fill()
    temp.goto( scaleFactor * ((columns/2)*100+10),  scaleFactor * ((rows/2)*100-80))
    temp.goto( scaleFactor * ((columns/2)*100+10),  scaleFactor * (-(rows/2)*100-100))
    temp.goto( scaleFactor * (-(columns/2)*100-20), scaleFactor * ( -(rows/2)*100-100))
    temp.fillcolor("#000077")
    temp.end_fill()

    for x in range(columns):
        for y in range(rows):
            temp = turt.Turtle("circle")
            turt.colormode(255)
            temp.color((255,255,255))
            temp.penup()
            temp.shapesize(4.7*scaleFactor)
            temp.goto(beginX+x*100*scaleFactor, beginY+y*100*scaleFactor)
            gameBoard[y][x]["turtle"] = temp
    turt.update()

def init():
    global gameBoard, pointer, turn, WRITE
    turn = rand.randint(0,players-1) if RANDOM else 0
    turt.Screen().clear()
    turt.tracer(0,0)
    gameBoard = [ [ {"turtle": None, "player": None} for __ in range(columns)] for _ in range(rows) ]
    drawGrid()
    pointer = {"turtle": turt.Turtle("triangle"), "column": 0} 
    pointer["turtle"].color(pointerColors[turn])
    pointer["turtle"].penup()
    pointer["turtle"].shapesize(3*scaleFactor)
    pointer["turtle"].left(30)
    pointer["turtle"].goto(beginX, beginY+(rows*100+10)*scaleFactor)
    
    WRITE = turt.Turtle("blank")
    WRITE.penup()
    WRITE.goto(0,295)
    WRITE.write(("Connect 4" if players == 2 else "Emotional " + str(int(players))) + " - \"H\" for help.\nArrow keys to navigate.\nSPACE to drop tiles.", font=("Arial", 20, "normal"), align="center")

    turt.onkeypress(showHelp, "h")
    turt.onkeypress(enterEvent, "space")
    turt.onkeypress(partial(moveEvent, True), key="Left")
    turt.onkeypress(partial(moveEvent, False),key="Right")
    turt.listen()
    turt.update()

init()

turt.mainloop()