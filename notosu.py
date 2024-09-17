# apparently a game i made

# turtle moves, you have to follow your mouse and click on the turtle within five seconds or you lose.
# goes really slow, i don't remember if it speeds up over time/gets harder.


# a121_catch_a_turtle.py
#-----import statements-----
import time
import turtle as turt
import math
import random as rand

#-----game configuration----
spot_color = "#ffffff"
spot_size = 0.01
spot_shape = "square"
#-----initialize turtle-----
i_hate_turtles = turt.Turtle("turtle")
i_hate_turtles.shape(spot_shape)
i_hate_turtles.color(spot_color)
currentColor = spot_color
i_hate_turtles.shapesize(spot_size)
i_hate_turtles.penup()
button_turtlee = turt.Turtle("blank")
button_turtlee.color("green")
button_turtlem = turt.Turtle("blank")
button_turtlem.color("gold")
button_turtleh = turt.Turtle("blank")
button_turtleh.color("red")
score = turt.Turtle("blank")
score.color("black")
score.penup()
score.shapesize(2)
score_count = 0
expectedScore = 0
already = False
message = None
defaulttime = 2
timer = turt.Turtle("blank")
timer.color("black")
timer.penup()
wn = turt.Screen()
#-----game functions--------
def keep_score():
    width = wn.window_width()/2
    height = wn.window_height()/2
    score.goto(-1*width+10, height-40)
    score.clear()
    score.write("YOUR SCORE: " + str(score_count), font=("Arial", 16, "normal"))
def spot_clicked(x,y):
    global already
    if already == False:
        already = True
        global score_count
        score_count += 1
        keep_score()
        global timenow,message
        timenow = 1
        message = "MOVING ON"
def change_pos():
    global already,expectedScore
    width = wn.window_width()//2
    height = wn.window_height()//2
    i_hate_turtles.speed(((expectedScore+25) / 25) + 3)
    i_hate_turtles.goto(rand.randint(-1*width+10,width-10),rand.randint(-1*height+10,height-10))
    global currentColor
    currentColor = '#' + ''.join(rand.choices('0123456789abcdef',k=6))
    i_hate_turtles.color(currentColor)
    i_hate_turtles.shapesize(rand.randint(1,5))
    already = False

def keep_track_of_time():
    width = wn.window_width()/2
    height = wn.window_height()/2
    timer.goto(-1*width+10, height-80)
    timer.clear()
    global timenow,message,currentColor
    global expectedScore
    global score_count,defaulttime
    timenow -=1
    # spot_clicked(0,0)
    if message:
        timer.write(message, font=("Arial", 16, "normal"))
        message = None
    else:
        timer.write("TIME LEFT: " + str(timenow), font=("Arial", 16, "normal"))
    if timenow > 0:
        wn.ontimer(keep_track_of_time,1000)
    else:
        expectedScore += 1
        if expectedScore == score_count:
            change_pos()
            timenow = 1+defaulttime*1
            keep_track_of_time()
            if score_count > 20:
                if score_count < 50:
                    wn.bgcolor("#ffccdd")
                elif score_count < 100:
                    wn.bgcolor("#ffbbbb")
                elif score_count < 150:
                    wn.bgcolor("#ff9ebe")
                elif score_count < 175:
                    wn.bgcolor("#ff4d88")
                elif score_count < 180:
                    if rand.randint(0,5) > 0:
                        wn.bgcolor("#000000")
                    else:
                        wn.bgcolor('#' + ''.join(rand.choices('0123456789abcdef',k=6)))
                    if rand.randint(0,1000):
                        wn.bgcolor(currentColor)
        else:
            message = "TIME UP"
            i_hate_turtles.clear()
            wn.bgcolor('#FF0000')
            score.clear()
            timer.clear()
            i_hate_turtles.shape("blank")
            i_hate_turtles.color("black")
            i_hate_turtles.goto(0,0)
            i_hate_turtles.write("YOU LOSE!!\n FINAL SCORE: " + str(score_count), align="center", font=("Arial", 20, "normal"))


#-----events----------------
def mainGame():
    global score_count
    global timenow,defaulttime
    timenow = 1+defaulttime*1
    keep_score()
    change_pos()
    i_hate_turtles.onclick(spot_clicked)
    keep_track_of_time()
    wn.mainloop()
   #if not expectedScore == score_count:
   #    break
mainGame()
def getDifficulty():
    button_turtlee.color("black")
    button_turtlee.write("CHOOSE DIFFICULTY", font=["arial", 20, "normal"])
    button_turtlee.color("green")
    button_turtlee.goto(0,-10)