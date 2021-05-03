# negron_116073_project01_Snek

The game I decided to recreate for this project is snake (which I dubbed Snek). It is a game where the user controls a snake that travels at an increasing speed (eventually it becomes constant) and has the objective of feeding the snake "rewards" to make it grow. All while the user must avoid hitting the walls or having a collision with his own body. The moment a collision occurs, it is game over. This version of snake will report your current score and save the highest score in a text file.

The main algorithm of Snek is making the snake grow and follow. It does this by using a dictionary to create the snake head and body according to a predetermined value (length). In this case the length value is set to 3. So, once the game boots up, you will have the head and 2 body parts which are clones of the head (as are the rest of the body). As the snake feeds, the length increases and so does the body. The body follows the head by undrawing and drawing a clone of the head in its previous position. It continues this until it reaches current snake length.

This version of snake takes inspiration from user **ifsoMarcus'** version of snake posted on [Code Review](https://codereview.stackexchange.com/).

### Similarities:
1. Style (in an attempt to follow [PEP8](https://www.python.org/dev/peps/pep-0008/) standards).
2. GUI dimensions:
   - ```python
     WIDTH = 400
     HEIGHT = 470
     GRID_HEIGHT = WIDTH
     
     win = GraphWin("SNEK", WIDTH, HEIGHT, autoflush=False)
     win.setBackground(color_rgb(15, 15, 15))
     ```
3. Some of the logic behind the snake's behavior:
   - The snake's growth:
     ```python
     if len(PLAYER) < PLAYER_LENGTH:
        BODY += 1
        PLAYER[BODY] = PLAYER[BODY - 1].clone()
     ```
   - The snake's lagging movement: 
     ```python
     PLAYER[0].undraw()
     for i in range(1, len(PLAYER)):
        PLAYER[len(PLAYER) - i].undraw()
        PLAYER[len(PLAYER) - i] = PLAYER[len(PLAYER) - i - 1].clone()
        PLAYER[len(PLAYER) - i].draw(win)
     ```

### Differences:
1. Efficiency: 
   - Grid:
     - Original:
     ```python
     lineX = 20
     while lineX < width:
        gridX = Line(Point(lineX,0),Point(lineX,gridHeight))
        gridX.setOutline(color_rgb(25,25,25))
        gridX.draw(win)
        lineX += 20
     lineY = 20
     while lineY <= gridHeight:
        gridX = Line(Point(0,lineY),Point(width,lineY))
        gridX.setOutline(color_rgb(25,25,25))
        gridX.draw(win)
        lineY += 20
     ```
     - New:
     ```python
     def grid(WIDTH, GRID_HEIGHT):
        for i in range(20, WIDTH, 20):
            GRID_VERTICAL = Line(Point(i, 0), Point(i, GRID_HEIGHT))
            GRID_VERTICAL.setOutline(color_rgb(25, 25, 25))
            GRID_VERTICAL.draw(WIN)

            GRID_HORIZONTAL = Line(Point(0, i), Point(WIDTH, i))
            GRID_HORIZONTAL.setOutline(color_rgb(25, 25, 25))
            GRID_HORIZONTAL.draw(WIN)
     ```
   - User Interface:
     - Original:
     ```python
     UI = Rectangle(Point(0,400),Point(width,height))
     UI.setFill(color_rgb(102,51,0))
     UI.setOutline(color_rgb(102,51,0))
     UI.draw(win)
     snakeTitle = Text(Point(width/2,420),"SNAKE")
     snakeTitle.setTextColor("green")
     snakeTitle.setSize(20)
     snakeTitle.draw(win)
     scoreTitle = Text(Point(320,424),"SCORE")
     scoreTitle.setTextColor("white")
     scoreTitle.setSize(10)
     scoreTitle.draw(win)
     scoreUI = Text(Point(320,435),score)
     scoreUI.setTextColor("white")
     scoreUI.setSize(10)
     scoreUI.draw(win)
     ```
     - New:
     ```python
     def UI(WIDTH, HEIGHT):
        USER = Rectangle(Point(0, 400), Point(WIDTH, HEIGHT))
        USER.setFill(color_rgb(113, 191, 46))
        USER.setOutline(color_rgb(113, 191, 46))
        USER.draw(WIN)
     ```
2. Simplified user control:
   - Original:
   ```python
   if keyboard.is_pressed("Up") and key != "Down":
      key = "Up"
   elif keyboard.is_pressed("Left") and key != "Right":
      key = "Left"
   elif keyboard.is_pressed("Down") and key != "Up":
      key = "Down"
   elif keyboard.is_pressed("Right") and key != "Left":
      key = "Right"
      
   if key == "Up":
      y -= length
   elif key == "Left":
      x -= length
   elif key == "Down":
      y += length
   elif key == "Right":
      x += length
   ```
   - New:
   ```python
   TEMP = win.checkKey()
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
   ```
3. How the reward is generated and obtained:
   - Original:
   ```python
   if countDown == 150:
      countDown = 0
      if cherryPoints == False: # generates new cherry from countdown
         cherryPoint = Rectangle(Point(cherryRandomX-pointRadius,cherryRandomY-pointRadius),Point(cherryRandomX+pointRadius,cherryRandomY+pointRadius))
         cherryPoint.setFill(color_rgb(213,0,50))
         cherryPoint.setWidth(2)
         cherryPoint.draw(win)
         cherryPoints = True
   if cherryPoints == True:
      for i in range(2, 6): # cherry blinks between countdown 40 to 100
         if countDown == 20*i:
            cherryPoint.undraw()
         elif countDown == 10+(20*i):
            cherryPoint.draw(win)
      if countDown >= 100: # when countdown becomes 100, remove cherry and reset count down
         cherryPoints = False
         countDown = 0
         cherryRandomX = random.choice(coordX)
         cherryRandomY = random.choice(coordY)
   
   if cherryPoints==True and player[0].getCenter().getX() == cherryPoint.getCenter().getX() and player[0].getCenter().getY() == cherryPoint.getCenter().getY():
      cherryPoint.undraw()
      score += 500
      cherryRandomX = random.choice(coordX)
      cherryRandomY = random.choice(coordY)
      for i in range(len(player)):
         if (cherryPoint.getCenter().getX() == player[i].getCenter().getX() and cherryPoint.getCenter().getY() == player[i].getCenter().getY()) or (cherryPoint.getCenter().getX() == point.getCenter().getX() and cherryPoint.getCenter().getY() == point.getCenter().getY()):
            cherryRandomX = random.choice(coordX)
            cherryRandomY = random.choice(coordY)
      for i in range(len(poison)): # regenerate x and y coordinate if cherry shares the same coordinate to other array of poisons
         if cherryPoint.getCenter().getX() == poison[i].getCenter().getX() and cherryPoint.getCenter().getY() == poison[i].getCenter().getY():
            cherryRandomX = random.choice(coordX)
            cherryRandomY = random.choice(coordY)
      cherryPoints = False
   ```
   - New:
   ```python
   def Snek_Reward(WIDTH, GRID_HEIGHT):
      REWARD_X = randrange(20, WIDTH - 20, 20)
      REWARD_Y = randrange(20, GRID_HEIGHT - 20, 20)

      PRIZE = Rectangle(
               Point(REWARD_X, REWARD_Y),
               Point(REWARD_X + 20, REWARD_Y + 20)
               )
               
      PRIZE.setFill("Red")
      PRIZE.draw(WIN)
      return PRIZE
   
   #WITHIN MAIN:
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
   ```
4. The score display:
   - Original:
   ```python
   scoreUI.undraw()
   scoreUI = Text(Point(320,435),score)
   scoreUI.setTextColor("white")
   scoreUI.setSize(10)
   scoreUI.draw(win)
   ```
   - New:
   ```python
   def score_counter_and_display(SCORE):
      COUNTER = Text(Point(75, 435), f"Score: {SCORE}")
      COUNTER.setSize(20)
      COUNTER.setFill("White")
      COUNTER.draw(WIN)

      return COUNTER
   ```
5. "Game Over" conditions:
   - Original:
   ```python
   for i in range(2, len(player)): # if player touches its own body or reach out of window
      if (player[0].getCenter().getX() == player[i].getCenter().getX() and player[0].getCenter().getY() == player[i].getCenter().getY()) or x < 0 or x > width or y < 0 or y > gridHeight:
      game = False
   ```
   - New:
   ```python
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
   
   #Within main:
   for i in range(1, len(PLAYER)):
      if(PLAYER[0].getCenter().getX() == PLAYER[i].getCenter().getX() and PLAYER[0].getCenter().getY() == PLAYER[i].getCenter().getY()):
         PLAYER[0].undraw()
         PLAYER[0].setFill(color_rgb(220, 20, 60))
         PLAYER[0].setWidth(2)
         PLAYER[0].draw(WIN)
         GAME = OVER
   ```

### New Additions:
1. The game manipulates a file to report the highest score ever obtained.
2. Displays a game over screen once any of the "Game Over" conditions are met.

You can find the original version [here](https://codereview.stackexchange.com/questions/226180/snake-game-using-graphics-py).
