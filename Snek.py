from graphics import*
from random import*

#Variables used:
WIDTH = 400
HEIGHT = 470
GRID_HEIGHT = WIDTH
SCORE = 0
X = 30
Y = 70
i = 0
RADIUS = 10
LENGTH = RADIUS * 2
PLAYER_LENGTH = 3
DIRECTION = "Down"
GAME = True
OVER = False
SPAWN = False
REWARD = 0

#Reward coordinates:
REWARD_X = randrange(0, WIDTH - 20, 20)
REWARD_Y = randrange(0, GRID_HEIGHT - 20, 20)

#Main GUI:
WIN = GraphWin("SNEK", WIDTH, HEIGHT, autoflush=False)
WIN.setBackground(color_rgb(15, 15, 15))

#Game defs:
def grid(WIDTH, GRID_HEIGHT):
    for i in range(20, WIDTH, 20):
        GRID_VERTICAL = Line(Point(i, 0), Point(i, GRID_HEIGHT))
        GRID_VERTICAL.setOutline(color_rgb(25, 25, 25))
        GRID_VERTICAL.draw(WIN)
        
        GRID_HORIZONTAL = Line(Point(0, i), Point(WIDTH, i))
        GRID_HORIZONTAL.setOutline(color_rgb(25, 25, 25))
        GRID_HORIZONTAL.draw(WIN)

def UI(WIDTH, HEIGHT):
    USER = Rectangle(Point(0, 400), Point(WIDTH, HEIGHT))
    USER.setFill(color_rgb(113, 191, 46))
    USER.setOutline(color_rgb(113, 191, 46))
    USER.draw(WIN)

def limits(X_LIM1, Y_LIM1, X_LIM2, Y_LIM2):
    if(X_LIM1 >= WIDTH or X_LIM1 <= 0):
        return False
    elif(Y_LIM1 >= GRID_HEIGHT or Y_LIM1 <= 0):
        return False
    elif(X_LIM2 >= WIDTH or X_LIM2 <= 0):
        return False
    elif(Y_LIM2 >= GRID_HEIGHT or Y_LIM2 <= 0):
        return False
    else:
        return True

def Snek_Reward(WIDTH, GRID_HEIGHT):

    #Reward coordinates:
    REWARD_X = randrange(0, WIDTH - 20, 20)
    REWARD_Y = randrange(0, GRID_HEIGHT - 20, 20)

    PRIZE = Rectangle(Point(REWARD_X, REWARD_Y), Point(REWARD_X + 20, REWARD_Y + 20))
    PRIZE.setFill("Red")
    PRIZE.draw(WIN)
    return PRIZE


PLAYER = {}
PLAYER[0] = Rectangle(Point(X - 20 - RADIUS, Y - RADIUS), Point(X - 20 + RADIUS, Y + RADIUS))
PLAYER[1] = Rectangle(Point(X - 40 - RADIUS, Y - RADIUS), Point(X - 40 + RADIUS, Y + RADIUS))
PLAYER[2] = Rectangle(Point(X - 60 - RADIUS, Y - RADIUS), Point(X - 60 + RADIUS, Y + RADIUS))

j = 0

grid(WIDTH, GRID_HEIGHT)
UI(WIDTH, HEIGHT)

while GAME:
    #Makes existing and potential new body
    if len(PLAYER) < PLAYER_LENGTH:
            i += 1
            PLAYER[i] = PLAYER[i - 1].clone()

    #Makes body follow
    PLAYER[0].undraw()
    for i in range(1, len(PLAYER)):
        PLAYER[len(PLAYER) - i].undraw()
        PLAYER[len(PLAYER) - i] = PLAYER[len(PLAYER) - i - 1].clone()
        PLAYER[len(PLAYER) - i].draw(WIN)

    #Head coordinates of snake
    PLAYER[0] = Rectangle(Point(X - RADIUS, Y - RADIUS), Point(X + RADIUS, Y + RADIUS))
    PLAYER[0].setFill("Cyan")
    PLAYER[0].setWidth(2)
    PLAYER[0].draw(WIN)

    #Screen edges
    GAME = True if limits(PLAYER[0].getP1().getX(), PLAYER[0].getP1().getY(),
    PLAYER[0].getP2().getX(), PLAYER[0].getP2().getY()) else OVER

    #User controls
    TEMP = WIN.checkKey()
    if TEMP == "Up":
        DIRECTION = "Up"
    elif TEMP == "Left":
        DIRECTION = "Left"
    elif TEMP == "Down":
        DIRECTION = "Down"
    elif TEMP == "Right":
        DIRECTION = "Right"

    if DIRECTION == "Up":
        Y -= LENGTH
    elif DIRECTION == "Left":
        X -= LENGTH
    elif DIRECTION == "Down":
        Y += LENGTH
    elif DIRECTION == "Right":
        X += LENGTH

    #Snake objective spawning
    if(SPAWN == False):
        OBJECTIVE = Snek_Reward(WIDTH, GRID_HEIGHT)
        SPAWN = True

    #If objective is reached, update values
    CENTER1 = OBJECTIVE.getCenter().getX() == PLAYER[0].getCenter().getX()
    CENTER2 = OBJECTIVE.getCenter().getY() == PLAYER[0].getCenter().getY()
    
    if(CENTER1 and CENTER2):
        SPAWN = False
        PLAYER_LENGTH += 1
        OBJECTIVE.undraw()

    #Rest goes here
    update(10)

WIN.getMouse()
WIN.close()