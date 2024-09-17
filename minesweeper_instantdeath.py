import turtle as turt
import random as rand
from functools import partial
from platform import system
from time import time

rightClickBtn = 3 if system() == "Windows" else 2
colors = [
    "#DDDDDD",
    "#0000FF",
    "#00DD00",
    "#FF0000",
    "#FF00FF",
    "#FF9900",
    "#00FFFF",
    "#FFFF00",
    "#000000",
    "#FFFFFF",
]

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

    turt.update()

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

def drawGrid():
    t = turt.Turtle("circle")
    t.color("#000000")
    t.pensize(2)
    t.hideturtle()
    for x in range(13):
        xcor = -300 + x*50
        t.penup()
        t.goto(xcor, 200)
        t.pendown()
        t.goto(xcor, -300)
        t.penup()
        if x > 10: continue
        ycor = 200 - x*50
        t.goto(-300, ycor)
        t.pendown()
        t.goto(300, ycor)
    turt.update()

def randColor():
    return "".join(rand.choices("ab138ff", k=6))
def onFlagClick(_x,_y,   xc, yc):

    entry = gameBoard[yc][xc]
    if firstClick:
        if not entry["flagged"]:
            entry["flagged"] = True
            entry["turtle"].color("#FF1111")
        else:
            entry["flagged"] = False
            entry["turtle"].color("#CCCCCC")

        turt.update()

def showNumber(entry):
    if entry["sign"] == 0 or not type(entry["sign"]) == int: return

    entry["turtle"].hideturtle()
    entry["turtle"].clear()
    entry["turtle"].color(colors[entry["sign"]])
    entry["turtle"].goto(entry["turtle"].xcor()+1,entry["turtle"].ycor()-17)
    entry["turtle"].write(entry["sign"], align="center", font=("Times New Roman", 25, "bold"))
    entry["turtle"].color('#FFFF00')
    entry["turtle"].goto(entry["turtle"].xcor()-1,entry["turtle"].ycor()+17)

def remove(xc, yc, iterated=False):
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
            if pair[0] < 0 or pair[1] < 0: continue
            entry = gameBoard[pair[1]][pair[0]]
            if entry["turtle"].isvisible() and type(entry["sign"]) == int and entry["flagged"] == False:

                if entry["sign"] == 0 and (not iterated or entry is not gameBoard[yc][xc]):
                    entry["turtle"].hideturtle()
                    remove(pair[0], pair[1], True)
                else:
                    showNumber(entry)
        except IndexError:
            pass

def onTileClick(_x, _y,   xc, yc):
    global gameBoard, firstClick, textTurtle
    entry = gameBoard[yc][xc]

    gameBoard[yc][xc]["sign"] = "X"
    for x in range(12):
        for y in range(10):
            if gameBoard[y][x]["sign"] == "X": continue
            for pair in [
                [x+1,y], 
                [x-1,y], 
                [x,y+1], 
                [x,y-1], 
                [x+1,y+1],
                [x-1,y+1],
                [x-1,y-1],
                [x+1,y-1] 
            ]:
                try:
                    if gameBoard[pair[1]][pair[0]]["sign"] == "X" and not (pair[0] < 0 or pair[1] < 0):
                        gameBoard[y][x]["sign"] += 1
                except IndexError:
                    pass
    drawFail(-250,250,3)
    minesFound = 0
    misflagged = 0

    for x in range(12):
        for y in range(10):
            gameBoard[y][x]["turtle"].onclick(None, btn=1)
            gameBoard[y][x]["turtle"].onclick(None, btn=rightClickBtn)
            if gameBoard[y][x]["sign"] == "X":
                if gameBoard[y][x]["flagged"]:
                    gameBoard[y][x]["turtle"].color("#11FF11")
                    minesFound += 1
                else:
                    drawBomb(gameBoard[y][x]["turtle"])
            elif gameBoard[y][x]["sign"] != "X":
                remove(y,x)
                if gameBoard[y][x]["flagged"]:
                    misflagged += 1

    textTurtle.clear()
    textTurtle.goto(50,250)
    textTurtle.write("Minesweeper", font=("Arial", 30, "bold"), align="center")
    textTurtle.goto(50,235)
    textTurtle.write("You clicked on a mine!", font=("Arial", 15, "normal"), align="center")
    textTurtle.goto(50,220)
    textTurtle.write("You flagged " + str(minesFound) + " mines (green) and misflagged " + str(misflagged) + " tiles (red).", font=("Arial", 15, "normal"), align="center")
    textTurtle.goto(50,205)
    textTurtle.write("Press your spacebar key to reset.", font=("Arial", 15, "normal"), align="center")
    turt.onkeypress(init, key="space")
    turt.listen()

    turt.update()

def setHitboxes():
    for x in range(12):
        xcor = -275.5 + x*50
        for y in range(10):
            ycor = 175.5 - y*50
            ttl = turt.Turtle("square")
            ttl.penup()
            ttl.color("#AAAAAA")
            ttl.shapesize(5.3**.5)
            ttl.goto(xcor, ycor)

            gameBoard[y][x]["turtle"] = ttl
            ttl.onclick(partial(onTileClick, xc=x, yc=y), btn=1)
            ttl.onclick(partial(onFlagClick, xc=x, yc=y), btn=rightClickBtn)

    turt.update()

def init():
    global textTurtle, gameBoard, statusTurtle, firstClick, start
    turt.Screen().clear()
    turt.title("Minesweeper")
    turt.setup(600, 600)
    turt.tracer(0, 0)
    turt.Screen().bgcolor("#DDDDDD")
    turt.hideturtle()
    firstClick = False
    gameBoard   = [ [ {"turtle": None, "sign": 0, "flagged": False} for __ in range(12) ] for _ in range(10) ]
    statusTurtle = turt.Turtle("circle")
    textTurtle = turt.Turtle("blank")
    textTurtle.penup()
    textTurtle.goto(50,250)
    textTurtle.write("Minesweeper", font=("Arial", 30, "bold"), align="center")
    textTurtle.goto(50,235)
    textTurtle.write("Left click on a tile to reveal itself", font=("Arial", 15, "normal"), align="center")
    textTurtle.goto(50,220)
    textTurtle.write("Right click on a tile to flag/unflag it as a mine (marked as red)", font=("Arial", 15, "normal"), align="center")
    textTurtle.goto(50,205)
    textTurtle.write("This map has " + str(1) + '/' + str(12*10) + " mine(s).", font=("Arial", 15, "normal"), align="center")
    drawGrid()
    drawCheck(-250,250,3)
    setHitboxes()
    start = time()

init()

turt.mainloop()