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

    for i in range(10):
        update(10)
    

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
        return True
    elif(Y_LIM1 >= limits[1] or Y_LIM1 <= 0):
        return True
    elif(X_LIM2 >= limits[0] or X_LIM2 <= 0):
        return True
    elif(Y_LIM2 >= limits[1] or Y_LIM2 <= 0):
        return True
    else:
        return False


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
    return True, PRIZE


def score_manipulation(file: str, score_mode: str, window, score=0):
    """
    Reads and/or writes score from file.
        Modes:
            1. read: Reads score from file.
            2. v/w: Verifies if score is higher than previous. If True, it is added to the file.

    Note: File must be created prior to manipulation.
    """

    if score_mode == 'read':
        with open(file, 'r') as challenge:
            highest = '0' if (temp := challenge.readline()) == '' else temp

            challenge_score = Text(Point(285, 435), f'High Score: {highest}')
            challenge_score.setSize(20)
            challenge_score.setFill('White')
            challenge_score.draw(window)

    elif score_mode == 'v/w':
        with open(file, 'r+') as challenge:

            try:
                test = False
                test = int(challenge.readline()) < score

            except ValueError:
                challenge.write(str(score))
            
            if test:
                position = 0

                challenge.seek(position)
                challenge.write(str(score))


def snake(x, y, side_length):
    """Creates the snake's template for head/body."""

    container = {}
    container[0] = Rectangle(
        Point(x - 20 - side_length, y - side_length),
        Point(x - 20 + side_length, y + side_length)
        )

    return container


def snake_to_reward(snake, reward_status):
    """Reports if the snake has obtained the reward and removes it if it was obtained."""
    
    center1 = reward_status.getCenter().getX() == snake[0].getCenter().getX()
    center2 = reward_status.getCenter().getY() == snake[0].getCenter().getY()

    if center1 and center2:
        reward_status.undraw()

    return center1 and center2


def game_has_ended(snake):
    """Only returns True when one of the conditions are met to end the game."""

    EDGE1, EDGE2 = snake[0].getP1().getX(), snake[0].getP1().getY()

    EDGE3, EDGE4 = snake[0].getP2().getX(), snake[0].getP2().getY()
        
    if limits(EDGE1, EDGE2, EDGE3, EDGE4, (400, 400)):
        return True

    for i in range(1, len(snake)):
        if(snake[0].getCenter().getX() == snake[i].getCenter().getX() and snake[0].getCenter().getY() == snake[i].getCenter().getY()):
                
            return True

    return False


def try_again(window, width=400, height=400):
    interface = Rectangle(Point(0, 0), Point(width, height))
    interface.setFill('Grey')
    interface.draw(window)

    option = Text(Point(width/2, height/2), 'Do you wish to try again?\n\nPress ENTER to try again or any other key to exit.')
    option.setFill('White')
    option.setSize(12)
    option.draw(window)

    if(window.getKey() == 'Return'):
        window.close()

        return True
    
    else: 
        window.close()

        return False


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
    SPAWN = False
    X = 30
    Y = 70
    SCORE = 0
    FRAMES = 5
    y_dir = {"Up": -LENGTH, "Down": LENGTH}
    x_dir = {"Left": -LENGTH, "Right": LENGTH}

    # Playing field
    ui = display(WIDTH, HEIGHT)
    STREAK = score_counter_and_display(SCORE, ui)

    # Snake values to be drawn
    PLAYER = snake(X, Y, SIDE)

    #Gets High Score
    score_manipulation('scores.txt', 'read', ui)

    # Running game:
    while True:
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

        # Active head coordinates of snake
        PLAYER[0] = Rectangle(
            Point(X - SIDE, Y - SIDE),
            Point(X + SIDE, Y + SIDE)
            )
        PLAYER[0].setOutline("White")
        PLAYER[0].setFill("Cyan")
        PLAYER[0].setWidth(2)
        PLAYER[0].draw(ui)

        # Game over if edges are touched
        if(game_has_ended(PLAYER)):
            PLAYER[0].undraw()
            PLAYER[0].setFill(color_rgb(220, 20, 60))
            PLAYER[0].setWidth(2)
            PLAYER[0].draw(ui)
            break

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
            SPAWN, OBJECTIVE = Snek_Reward(WIDTH, GRID_HEIGHT, ui)

        # Creates new reward, speeds up game and updates score
        if snake_to_reward(PLAYER, OBJECTIVE):
            SPAWN = False
            SCORE += 1
            PLAYER_LENGTH += 1
            if(FRAMES < 10):
                FRAMES += 1

        # Controls Snake speed
        update(FRAMES)
    
    #If score is nigher than High Score, registers it
    score_manipulation('scores.txt', 'v/w', ui, SCORE)

    game_over_UI(WIDTH, HEIGHT, ui)

    return ui


def main():
    sentinel = True
    while sentinel:
        game = run()
        sentinel = try_again(game)
    

if __name__ == '__main__':
    main()