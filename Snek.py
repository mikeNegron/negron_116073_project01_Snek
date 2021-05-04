from graphics import*
from random import randrange


# Game defs:
def grid(WIDTH, GRID_HEIGHT, window):
    """Generates a grid up until where the UI is generated."""
    for i in range(20, WIDTH, 20):
        GRID_VERTICAL = Line(Point(i, 0), Point(i, GRID_HEIGHT))
        GRID_VERTICAL.setOutline(color_rgb(25, 25, 25))
        GRID_VERTICAL.draw(window)

        GRID_HORIZONTAL = Line(Point(0, i), Point(WIDTH, i))
        GRID_HORIZONTAL.setOutline(color_rgb(25, 25, 25))
        GRID_HORIZONTAL.draw(window)


def UI(WIDTH, HEIGHT, window):
    """Generates a green rectangle at the bottom of the display."""
    USER = Rectangle(Point(0, 400), Point(WIDTH, HEIGHT))
    USER.setFill(color_rgb(113, 191, 46))
    USER.setOutline(color_rgb(113, 191, 46))
    USER.draw(window)


def display(width, height, window):
    """Generates display (grid/user UI)."""
    grid(width, width, window)
    UI(width, height, window)


def game_over_UI(WIDTH, HEIGHT, window):
    """Generates Game Over screen and pauses the screen until user clicks it."""
    USER = Rectangle(Point(0, 400), Point(WIDTH, HEIGHT))
    USER.setFill("Black")
    USER.draw(window)

    END_TEXT = Text(USER.getCenter(), "GAME OVER")
    END_TEXT.setSize(20)
    END_TEXT.setFill("White")
    END_TEXT.draw(window)

    window.getMouse()


def score_counter_and_display(SCORE, window):
    """Generates score display and returns the score (Text object)."""
    COUNTER = Text(Point(75, 435), f"Score: {SCORE}")
    COUNTER.setSize(20)
    COUNTER.setFill("White")
    COUNTER.draw(window)

    return COUNTER


def limits(X_LIM1, Y_LIM1, X_LIM2, Y_LIM2, limits):
    """Validates if snake is at any on the limits to end game."""
    if(X_LIM1 >= limits[0] or X_LIM1 <= 0):
        return False
    elif(Y_LIM1 >= limits[1] or Y_LIM1 <= 0):
        return False
    elif(X_LIM2 >= limits[0] or X_LIM2 <= 0):
        return False
    elif(Y_LIM2 >= limits[1] or Y_LIM2 <= 0):
        return False
    else:
        return True


def Snek_Reward(WIDTH, GRID_HEIGHT, window):
    """Generates a reward for the snake and return the reward (Rectangle object)."""
    REWARD_X = randrange(20, WIDTH - 20, 20)
    REWARD_Y = randrange(20, GRID_HEIGHT - 20, 20)

    PRIZE = Rectangle(
        Point(REWARD_X, REWARD_Y),
        Point(REWARD_X + 20, REWARD_Y + 20)
        )
    PRIZE.setFill("Red")
    PRIZE.draw(window)
    return PRIZE


def score_manipulation(file: str, score_mode: str, window, score=0):
    """
    Reads and/or writes score from file.
        Modes:
            1. read: Reads score from file.
            2. v/w: Verifies if score is higher than previous. If True, it is added to the file.

    Note: File must have a Int Type value saved before using v/w mode.
    """

    if score_mode == "read":
        with open(file, "r") as CHALLENGE:
            HIGHEST = CHALLENGE.readline()

            CHALLENGE_SCORE = Text(Point(285, 435), f"High Score: {HIGHEST}")
            CHALLENGE_SCORE.setSize(20)
            CHALLENGE_SCORE.setFill("White")
            CHALLENGE_SCORE.draw(window)

    elif score_mode == "v/w":
        with open(file, "r+") as CHALLENGE:
            if (int(CHALLENGE.readline()) < score):
                position = 0

                CHALLENGE.seek(position)
                CHALLENGE.write(str(score))


def controls(arrow, axis, length, moves):
   
    return moves.get(arrow)()


def run():
    # Variables used:
    WIDTH = 400
    HEIGHT = 470
    GRID_HEIGHT = WIDTH
    BODY = 0
    SIDE = 10
    LENGTH = SIDE * 2
    PLAYER_LENGTH = 3
    DIRECTION = "Down"
    GAME = True
    OVER = False
    SPAWN = False
    X = 30
    Y = 70
    SCORE = 0
    FRAMES = 5
    move_set = {
        'Up' : lambda : Y - LENGTH,
        'Left' : lambda : X - LENGTH,
        'Down' : lambda : Y + LENGTH,
        'Right' : lambda : X + LENGTH
        }

    # Main GUI:
    win = GraphWin("SNEK", WIDTH, HEIGHT, autoflush=False)
    win.setBackground(color_rgb(15, 15, 15))

    # Snake values to be drawn
    PLAYER = {}
    PLAYER[0] = Rectangle(
        Point(X - 20 - SIDE, Y - SIDE),
        Point(X - 20 + SIDE, Y + SIDE)
        )

    # Playing field
    display(WIDTH, HEIGHT, win)
    STREAK = score_counter_and_display(SCORE, win)

    #Gets High Score
    score_manipulation("scores.txt", "read", win)

    # Running game:
    while GAME:
        STREAK.undraw()
        STREAK = score_counter_and_display(SCORE, win)

        # Makes existing and potential new body
        if len(PLAYER) < PLAYER_LENGTH:
            BODY += 1
            PLAYER[BODY] = PLAYER[BODY - 1].clone()

        # Makes body follow
        PLAYER[0].undraw()
        for i in range(1, len(PLAYER)):
            PLAYER[len(PLAYER) - i].undraw()
            PLAYER[len(PLAYER) - i] = PLAYER[len(PLAYER) - i - 1].clone()
            PLAYER[len(PLAYER) - i].draw(win)

        # Head coordinates of snake
        PLAYER[0] = Rectangle(
            Point(X - SIDE, Y - SIDE),
            Point(X + SIDE, Y + SIDE)
            )
        PLAYER[0].setOutline("White")
        PLAYER[0].setFill("Cyan")
        PLAYER[0].setWidth(2)
        PLAYER[0].draw(win)

        # Screen edges
        EDGE1 = PLAYER[0].getP1().getX()
        EDGE2 = PLAYER[0].getP1().getY()

        EDGE3 = PLAYER[0].getP2().getX()
        EDGE4 = PLAYER[0].getP2().getY()

        GAME = limits(EDGE1, EDGE2, EDGE3, EDGE4, (WIDTH, GRID_HEIGHT))

        # Game over if edges are touched
        if(GAME == OVER):
            PLAYER[0].undraw()
            PLAYER[0].setFill(color_rgb(220, 20, 60))
            PLAYER[0].setWidth(2)
            PLAYER[0].draw(win)

        # Game over if head touches body
        for i in range(1, len(PLAYER)):
            if(PLAYER[0].getCenter().getX() == PLAYER[i].getCenter().getX() and PLAYER[0].getCenter().getY() == PLAYER[i].getCenter().getY()):
                PLAYER[0].undraw()
                PLAYER[0].setFill(color_rgb(220, 20, 60))
                PLAYER[0].setWidth(2)
                PLAYER[0].draw(win)
                GAME = OVER

        # User controls
        TEMP = win.checkKey()
        if TEMP == "Up":
            DIRECTION = "Up"
        elif TEMP == "Left":
            DIRECTION = "Left"
        elif TEMP == "Down":
            DIRECTION = "Down"
        elif TEMP == "Right":
            DIRECTION = "Right"

        if(DIRECTION == "Up" or DIRECTION == "Down"): #Testing dictionaries with lambda function
            Y = controls(DIRECTION, Y, LENGTH, move_set)

        elif(DIRECTION == "Left" or DIRECTION == "Right"): #Testing dictionaries with lambda function
            X = controls(DIRECTION, X, LENGTH, move_set)

        # Snake objective spawning
        if(SPAWN == False):
            OBJECTIVE = Snek_Reward(WIDTH, GRID_HEIGHT, win)
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
    score_manipulation("scores.txt", "v/w", win, SCORE)

    game_over_UI(WIDTH, HEIGHT, win)
    win.close()


def main():
    run()
    

if __name__ == '__main__':
    main()