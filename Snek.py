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


def display(width, height):
    """Generates display (grid/user UI)."""

    # Main GUI:
    win = GraphWin("SNEK", 400, 470, autoflush=False)
    win.setBackground(color_rgb(15, 15, 15))

    grid(width, width, win)
    UI(width, height, win)

    return win


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

    Note: File must be created prior to manipulation.
    """

    if score_mode == "read":
        with open(file, "r") as CHALLENGE:
            HIGHEST = "0" if (temp := CHALLENGE.readline()) == "" else temp

            CHALLENGE_SCORE = Text(Point(285, 435), f"High Score: {HIGHEST}")
            CHALLENGE_SCORE.setSize(20)
            CHALLENGE_SCORE.setFill("White")
            CHALLENGE_SCORE.draw(window)

    elif score_mode == "v/w":
        with open(file, "r+") as CHALLENGE:

            temp = False

            try:
                temp = int(CHALLENGE.readline()) < score
            except ValueError:
                CHALLENGE.write(str(score))
            
            if (temp):
                position = 0

                CHALLENGE.seek(position)
                CHALLENGE.write(str(score))

#STILL BEING DEVELOPED
""" def crashed(current_dir: str, snake: dict):
    for i in range(1, len(snake)):
        if current_dir == "Up" or "Left":
            if snake[0].getP1().getX() + 20 == snake[i].getP1().getX() and snake[0].getP1().getY() == snake[i].getP1().getY():
                return False

        elif current_dir == "Down" or "Right":
            if snake[0].getP2().getX() + 20 == snake[i].getP2().getX() and snake[0].getP2().getY() == snake[i].getP2().getY():
                return False
        
        else:
            return True """

#Runs snake game:
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
    y_dir = {"Up": -LENGTH, "Down": LENGTH}
    x_dir = {"Left": -LENGTH, "Right": LENGTH}

    # Snake values to be drawn
    PLAYER = {}
    PLAYER[0] = Rectangle(
        Point(X - 20 - SIDE, Y - SIDE),
        Point(X - 20 + SIDE, Y + SIDE)
        )

    # Playing field
    ui = display(WIDTH, HEIGHT)
    STREAK = score_counter_and_display(SCORE, ui)

    #Gets High Score
    score_manipulation("scores.txt", "read", ui)

    # Running game:
    while GAME:
        STREAK.undraw()
        STREAK = score_counter_and_display(SCORE, ui)

        # Makes existing and potential new body
        if len(PLAYER) < PLAYER_LENGTH:
            BODY += 1
            PLAYER[BODY] = PLAYER[BODY - 1].clone()

        # Makes body follow
        PLAYER[0].undraw()
        for i in range(1, len(PLAYER)):
            PLAYER[len(PLAYER) - i].undraw()
            PLAYER[len(PLAYER) - i] = PLAYER[len(PLAYER) - i - 1].clone()
            PLAYER[len(PLAYER) - i].draw(ui)

        # Head coordinates of snake
        PLAYER[0] = Rectangle(
            Point(X - SIDE, Y - SIDE),
            Point(X + SIDE, Y + SIDE)
            )
        PLAYER[0].setOutline("White")
        PLAYER[0].setFill("Cyan")
        PLAYER[0].setWidth(2)
        PLAYER[0].draw(ui)

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
            PLAYER[0].draw(ui)

        # Game over if head touches body
        for i in range(1, len(PLAYER)):
            if(PLAYER[0].getCenter().getX() == PLAYER[i].getCenter().getX() and PLAYER[0].getCenter().getY() == PLAYER[i].getCenter().getY()):
                PLAYER[0].undraw()
                PLAYER[0].setFill(color_rgb(220, 20, 60))
                PLAYER[0].setWidth(2)
                PLAYER[0].draw(ui)
                GAME = OVER

        # User control validation:
        TEMP = ui.checkKey()

        if TEMP != "":
            DIRECTION = TEMP
        
        # User control execution:
        if DIRECTION in y_dir:
            Y += y_dir[DIRECTION]
        elif DIRECTION in x_dir:
            X += x_dir[DIRECTION]

        # Snake objective spawning
        if(SPAWN == False):
            OBJECTIVE = Snek_Reward(WIDTH, GRID_HEIGHT, ui)
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
    score_manipulation("scores.txt", "v/w", ui, SCORE)

    game_over_UI(WIDTH, HEIGHT, ui)
    win.close()


def main():
    run()
    

if __name__ == '__main__':
    main()