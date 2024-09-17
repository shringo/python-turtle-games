# i was bored during class so i made this

import turtle as turt
import math
import time
from functools import partial

winCombos = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
]

'''
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
'''

def RESET():
    global clickCache
    for t in clickCache: 
        t.clear()
        t.hideturtle()
    turt.onkeypress(None, "Return")
    turt.listen()
    turt.update()
    init()

def drawX(turtle):
    x = turtle.xcor()
    y = turtle.ycor()
    turtle.color("blue")
    turtle.pensize(8)
    for pair in [[50,50], [50, -50]]:
        turtle.penup()
        turtle.goto(x-pair[0], y-pair[1])
        turtle.pendown()
        turtle.goto(x+pair[0], y+pair[1])
    turtle.hideturtle()
    turt.update()

def drawO(turtle):
    x = turtle.xcor()
    y = turtle.ycor()
    turtle.color("red")
    turtle.pensize(8)
    turtle.goto(x,y-50)
    turtle.pendown()
    turtle.circle(250*1/5)
    turtle.hideturtle()
    turt.update()

def checkWin():
    global gameBoard, winCombos
    winner = ""
    for combo in winCombos:
        if gameBoard[combo[0]] == gameBoard[combo[1]] and gameBoard[combo[1]] == gameBoard[combo[2]] and not (gameBoard[combo[0]] == None):
            winner = 'O' if turn else 'X'
    if gameBoard.count(None) == 0 or len(winner) > 0:
        if len(winner) == 0:
            winner = "Tie"
        messenger = turt.Turtle("blank")
        messenger.penup()
        messenger.goto(0, 255)
        messenger.write(winner if winner == "Tie" else (winner + " won!"), font="Arial 40", align="center")
        messenger.goto(0,-315)
        messenger.write("Press ENTER to reset", font="Arial 40", align="center")
        for x in clickCache: x.onclick(None)
        clickCache.append(messenger)
        turt.onkeypress(RESET, "Return")
        turt.listen()
        turt.update()

def onclick(x,y,turtle,id):
    global gameBoard, winCombos, turn
    drawX(turtle) if turn else drawO(turtle)
    gameBoard[id] = turn
    turn = not turn
    checkWin()

def setHitbox():
    for x in range(9):
        row = math.floor(x/3)
        col = x % 3
        coord = [0,0]
        if not col == 1:
            coord[0] = 250 * 2/3
            if col == 0: coord[0] *= -1
        if not row == 1:
            coord[1] = 250 * 2/3
            if row == 2: coord[1] *= -1
        tile = turt.Turtle("square")
        tile.penup()
        tile.goto(coord[0], coord[1])
        tile.shapesize(8)
        tile.color("white")
        tile.onclick(partial(onclick, turtle=tile, id=x))
        clickCache.append(tile)

def init(): 
    global linedrawer, clickCache, turn, gameBoard
    turt.tracer(0,0)
    turt.setup(600, 650)
    linedrawer = turt.Turtle("blank")
    linedrawer.pensize(5)
    clickCache = []
    turn = True
    gameBoard = [None] * 9
    for x in [250,-250]:
        linedrawer.penup()
        linedrawer.goto(-x, x*(1/3))
        linedrawer.pendown()
        linedrawer.goto(x, x*(1/3))
        linedrawer.penup()
        linedrawer.goto(x*(1/3), -x)
        linedrawer.pendown()
        linedrawer.goto(x*(1/3), x)
        linedrawer.penup()
    clickCache.append(linedrawer)
    setHitbox()
    turt.update()
init()

turt.update()
turt.mainloop()