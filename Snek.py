from graphics import*
from random import randrange


class ScoreHandling:
    def __init__(self, file):
        try:
            test = open(file, 'r')
        except Exception as e:
            print(f'[WARNING]: {e}. Creating file...')
            with open(file, 'w') as temp:
                temp.seek(0)
        else:
            test.close()
        finally:
            self.file = file

    def score_manipulation(self, score_mode, window, score = 0):
        if score_mode == 'read':
            with open(self.file, 'r') as challenge:
                highest = '0' if (temp := challenge.readline()) == '' else temp

                challenge_score = Text(Point(285, 435), f'High Score: {highest}')
                challenge_score.setSize(20)
                challenge_score.setFill('White')
                challenge_score.draw(window)

        elif score_mode == 'v/w':
            with open(self.file, 'r+') as challenge:

                try:
                    test = False
                    test = int(challenge.readline()) < score

                except ValueError:
                    challenge.write(str(score))
                
                if test:
                    position = 0

                    challenge.seek(position)
                    challenge.write(str(score))


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.name = 'SNEK'

        self.displayed = False
        self.counter = Text(Point(75, 435), '')
        
        self.grid_height = width

    def _grid(self, window):
        for i in range(20, self.width, 20):
            grid_vertical = Line(Point(i, 0), Point(i, self.grid_height))
            grid_vertical.setOutline(color_rgb(25, 25, 25))
            grid_vertical.draw(window)

            grid_horizontal = Line(Point(0, i), Point(self.width, i))
            grid_horizontal.setOutline(color_rgb(25, 25, 25))
            grid_horizontal.draw(window)

    def _interface(self, window):
        bar = Rectangle(Point(0, 400), Point(self.width, self.height))
        bar.setFill(color_rgb(113, 191, 46))
        bar.setOutline(color_rgb(113, 191, 46))
        bar.draw(window)

    def score_display(self, score, window):
        self.counter = Text(Point(75, 435), f"Score: {score}")
        self.counter.setSize(20)
        self.counter.setFill("White")
        self.counter.draw(window)
        return self.counter

    def game_over(self, window):
        status = Rectangle(Point(0, 400), Point(self.width, self.height))
        status.setFill("Black")
        status.draw(window)

        end_text = Text(status.getCenter(), "GAME OVER")
        end_text.setSize(20)
        end_text.setFill("White")
        end_text.draw(window)

        for i in range(10):
            update(10)

        window.getMouse() #Should call Play Again Screen Here
        window.close()

    def create_field(self):
        win = GraphWin(self.name, self.width, self.height, autoflush=False)
        win.setBackground(color_rgb(15, 15, 15))

        self._grid(win)
        self._interface(win)

        return win

    def get_limits(self):
        return (self.width, self.grid_height)



class Snake:
    def __init__(self):
        self.screen = Display(400, 470)
        self.field = self.screen.create_field()
        self.min_x, self.min_y = (0, 0)
        self.max_x, self.max_y = self.screen.get_limits()
        self.limits = {
            'x_eval' : lambda x : self.min_x + 20 <= x <= self.max_x - 20,
            'y_eval' : lambda y : self.min_y + 20 <= y <= self.max_y - 20,
            }

        self.score = 0

        self.doc = ScoreHandling('Scores.txt')
        self.doc.score_manipulation('read', self.field)

        self.frames = 5

        self.body = 0
        self.side = 10
        self.length = self.side * 2
        self.player_length = 3

        self.direction = "Down"

        self.x = 30
        self.y = 70

        self.y_dir = {"Up": -self.length, "Down": self.length}
        self.x_dir = {"Left": -self.length, "Right": self.length}

        self.prize = Rectangle(
            Point(0, 0),
            Point(0, 0)
        )
        self.reward_up = False

        self.container = {}
        self.container[0] = Rectangle(
            Point(self.x - 20 - self.side, self.y - self.side),
            Point(self.x - 20 + self.side, self.y + self.side)
            )

    def get_score(self):
        return self.score

    def point_comparison(self, obj1):
        center1 = obj1.getCenter().getX() == self.container[0].getCenter().getX()
        center2 = obj1.getCenter().getY() == self.container[0].getCenter().getY()
        
        return center1 and center2

    def rewards(self):
        if self.reward_up == False:

            reward_x = randrange(20, 380, 20)
            reward_y = randrange(20, 380, 20)

            self.prize = Rectangle(
                Point(reward_x, reward_y),
                Point(reward_x + 20, reward_y + 20)
            )
            self.prize.setFill('Red')

            self.prize.draw(self.field)
            self.reward_up = True

    def snake_at_reward(self):
        self.rewards()

        if self.reward_up:
            if self.point_comparison(self.prize):
                self.prize.undraw()
                self.player_length += 1
                self.score += 1
                self.reward_up = False
                if self.score < 10:
                    self.frames += 1

    def snake_death(self):
        p1 = (self.container[0].getP1().getX(), self.container[0].getP1().getY())
        p2 = (self.container[0].getP2().getX(), self.container[0].getP2().getY())

        for i, j in zip(p1, p2):
            if not self.limits['x_eval'](i) or not self.limits['x_eval'](j):
                return True

            elif not self.limits['y_eval'](i) or not self.limits['y_eval'](j):
                return True
            
        for i in range(1, len(self.container)):
            if self.point_comparison(self.container[i]):
                return True

        return False

    def controls(self):
        temp = self.field.checkKey()

        if not temp == '':
            self.direction = temp

        if self.direction in self.x_dir:
            self.x += self.x_dir[self.direction]
        elif self.direction in self.y_dir:
            self.y += self.y_dir[self.direction]

    def snake_factory(self):
        info = self.screen.score_display(self.score, self.field)

        while True:

            info.undraw()
            info = self.screen.score_display(self.score, self.field)

            if len(self.container) < self.player_length:
                self.body += 1
                self.container[self.body] = self.container[self.body - 1].clone()

            self.snake_at_reward()

            self.controls()
            
            self.container[0].undraw()
            for i in range(1, len(self.container)):
                self.container[len(self.container) - i].undraw()
                self.container[len(self.container) - i] = self.container[len(self.container) - i - 1].clone()
                self.container[len(self.container) - i].draw(self.field)

            self.container[0] = Rectangle(
                Point(self.x - self.side, self.y - self.side),
                Point(self.x + self.side, self.y + self.side)
                )
            
            self.container[0].setOutline("White")
            self.container[0].setFill("Cyan")
            self.container[0].setWidth(2)
            self.container[0].draw(self.field)

            if self.snake_death():
                self.container[0].undraw()
                self.container[0].setFill(color_rgb(220, 20, 60))
                self.container[0].setWidth(2)
                self.container[0].draw(self.field)
                break

            update(self.frames)

        self.doc.score_manipulation('v/w', self.field, self.score)

        self.screen.game_over(self.field)


def score_manipulation(file, score_mode, window, score=0):
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


def try_again(window, width=400, height=400):
    interface = Rectangle(Point(0, 0), Point(width, height))
    interface.setFill('Grey')
    interface.draw(window)

    option = Text(
        Point(width/2, height/2),
        'Do you wish to try again?\n\nPress ENTER to try again or any other key to exit.'
        )
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
            SPAWN, OBJECTIVE = snek_reward(WIDTH, GRID_HEIGHT, ui)

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
    temp = Snake()

    temp.snake_factory()


    

if __name__ == '__main__':
    main()