# SEIZURE WARNING.

import turtle as turt
import random
import time
import math

# i was learning the unit circle while taking this class
PI = math.atan(1) * 4.0

# depending if you answer N to the prompt. this program generates pixels with a size based on the stepper variable. YOU NEED A GOOD CPU IN ORDER TO DO SMALL VALUES (if you want it to go fast.)
stepper = 25
max = 300
turt.tracer(0,0)
me = turt.Turtle("blank")

def drawStuff(turtl):
    turtl.penup()
    turtl.clear()
    turtl.speed("fastest")
    x = max*1
    colors = {}
    while turtl.xcor() <= max and turtl.xcor() >= (max*-1):
        y = max*1
        turtl.goto(x,y)
        while turtl.ycor() <= max and turtl.ycor() >= (max*-1):
            id = 'x' + str(math.floor(x/stepper)) + 'y' + str(math.floor(y/stepper))
            if id in colors:
                color = colors[id]
            else:
                colors[id] = color = randomColor()
            turtl.color(color)
#            turtl.begin_fill()
#            turtl.circle(stepper)
#            turtl.end_fill()
#            turtl.goto(x,y)
            y-=stepper
            turtl.pendown()
            turtl.goto(x,y)
            turtl.penup()
        x-=1
    turtl.goto(max,max)
    turt.update()


def randomColor():
    return '#' + ''.join(random.choices("0123456789abcdef", k=6))
def epilepsyFunc(turtl):
    turtl.speed('fastest')
    turtl.penup()
    turtl.goto(0,-1000)
    fill(randomColor(), turtl)
def fill(color, turtl):
    turtl.begin_fill()
    turtl.color(color)
    turtl.circle(1000)
    turtl.end_fill()
    turt.update()
    turtl.clear()

inp = turt.textinput("Hello", "Do you want to have a seizure? [Y or n]")

if inp == 'Y':
    me.goto(-300, me.ycor())
   # me.write("In order to avoid a lawsuit, the epilepsy function only changes colors every few seconds instead of being instantaneous.")
   # time.sleep(5)
    func = epilepsyFunc
else:
    func = drawStuff
start_time = time.time()
while start_time > time.time() - 200:
    func(me)
turt.mainloop()

start_time = time.time()
while start_time > time.time() - 200:
    epilepsyFunc(me)