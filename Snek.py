from graphics import*
from random import randrange

# Variables used:
WIDTH = 400
HEIGHT = 470
GRID_HEIGHT = WIDTH
FRAMES = 5
SCORE = 0
X = 30
Y = 70
BODY = 0
SIDE = 10
LENGTH = SIDE * 2
PLAYER_LENGTH = 3
DIRECTION = "Down"
GAME = True
OVER = False
SPAWN = False
REWARD = 0

# Main GUI:
WIN = GraphWin("SNEK", WIDTH, HEIGHT, autoflush=False)
WIN.setBackground(color_rgb(15, 15, 15))

# Game defs:
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

def game_over_UI(WIDTH, HEIGHT):
    USER = Rectangle(Point(0, 400), Point(WIDTH, HEIGHT))
    USER.setFill("Black")
    USER.draw(WIN)

    END_TEXT = Text(USER.getCenter(), "GAME OVER")
    END_TEXT.setSize(20)
    END_TEXT.setFill("White")
    END_TEXT.draw(WIN)

    WIN.getMouse()

def score_counter_and_display(SCORE):
    COUNTER = Text(Point(75, 435), f"Score: {SCORE}")
    COUNTER.setSize(20)
    COUNTER.setFill("White")
    COUNTER.draw(WIN)

    return COUNTER


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
    REWARD_X = randrange(20, WIDTH - 20, 20)
    REWARD_Y = randrange(20, GRID_HEIGHT - 20, 20)

    PRIZE = Rectangle(Point(REWARD_X, REWARD_Y),
                      Point(REWARD_X + 20, REWARD_Y + 20))
    PRIZE.setFill("Red")
    PRIZE.draw(WIN)
    return PRIZE


def main():
    global FRAMES, SCORE, X, Y, BODY, SIDE, LENGTH, PLAYER_LENGTH, DIRECTION, GAME, OVER, SPAWN, REWARD

    # Snake values to be drawn
    PLAYER = {}
    PLAYER[0] = Rectangle(Point(X - 20 - SIDE, Y - SIDE),
                          Point(X - 20 + SIDE, Y + SIDE))

    # Playing field
    grid(WIDTH, GRID_HEIGHT)
    UI(WIDTH, HEIGHT)
    STREAK = score_counter_and_display(SCORE)

    #Gets High Score
    with open("scores.txt", "r") as CHALLENGE:
        HIGHEST = CHALLENGE.readline()
        CHALLENGE_SCORE = Text(Point(290, 435), f"High Score: {HIGHEST}")
        CHALLENGE_SCORE.setSize(20)
        CHALLENGE_SCORE.setFill("White")
        CHALLENGE_SCORE.draw(WIN)
    
    NEW_HIGH = False

    # Running game:
    while GAME:
        STREAK.undraw()
        STREAK = score_counter_and_display(SCORE)

        # Makes existing and potential new body
        if len(PLAYER) < PLAYER_LENGTH:
            BODY += 1
            PLAYER[BODY] = PLAYER[BODY - 1].clone()

        # Makes body follow
        PLAYER[0].undraw()
        for i in range(1, len(PLAYER)):
            PLAYER[len(PLAYER) - i].undraw()
            PLAYER[len(PLAYER) - i] = PLAYER[len(PLAYER) - i - 1].clone()
            PLAYER[len(PLAYER) - i].draw(WIN)

        # Head coordinates of snake
        PLAYER[0] = Rectangle(Point(X - SIDE, Y - SIDE),
                              Point(X + SIDE, Y + SIDE))
        PLAYER[0].setOutline("White")
        PLAYER[0].setFill("Cyan")
        PLAYER[0].setWidth(2)
        PLAYER[0].draw(WIN)

        # Screen edges
        EDGE1 = PLAYER[0].getP1().getX()
        EDGE2 = PLAYER[0].getP1().getY()

        EDGE3 = PLAYER[0].getP2().getX()
        EDGE4 = PLAYER[0].getP2().getY()

        GAME = True if limits(EDGE1, EDGE2, EDGE3, EDGE4) else OVER

        # Game over if edges are touched
        if(GAME == OVER):
            PLAYER[0].undraw()
            PLAYER[0].setFill(color_rgb(220, 20, 60))
            PLAYER[0].setWidth(2)
            PLAYER[0].draw(WIN)

        # Game over if head touches body
        for i in range(1, len(PLAYER)):
            if(PLAYER[0].getCenter().getX() == PLAYER[i].getCenter().getX() and PLAYER[0].getCenter().getY() == PLAYER[i].getCenter().getY()):
                PLAYER[0].undraw()
                PLAYER[0].setFill(color_rgb(220, 20, 60))
                PLAYER[0].setWidth(2)
                PLAYER[0].draw(WIN)
                GAME = OVER

        # User controls
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

        # Snake objective spawning
        if(SPAWN == False):
            OBJECTIVE = Snek_Reward(WIDTH, GRID_HEIGHT)
            SPAWN = True

        # If objective is reached, update values
        CENTER1 = OBJECTIVE.getCenter().getX() == PLAYER[0].getCenter().getX()
        CENTER2 = OBJECTIVE.getCenter().getY() == PLAYER[0].getCenter().getY()

        # Creates new reward, speeds up game and updates score
        if(CENTER1 and CENTER2):
            SPAWN = False
            SCORE += 1
            PLAYER_LENGTH += 1
            if(FRAMES < 10):
                FRAMES += 1
            OBJECTIVE.undraw()

        # Controls Snake speed
        update(FRAMES)
    
    #If score is nigher than High Score, registers it
    with open("scores.txt", "r") as CHALLENGE:
        if(int(CHALLENGE.readline()) < SCORE):
            NEW_HIGH = True
    
    if(NEW_HIGH):
        with open("scores.txt", "w") as CHALLENGE:
            CHALLENGE.write(str(SCORE))

    game_over_UI(WIDTH, HEIGHT)
    WIN.close()

if __name__ == '__main__':
    main()