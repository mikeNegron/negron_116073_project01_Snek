# negron_116073_project01_Snek

The game I decided to recreate for this project is snake (which I dubbed Snek). It is a game where the user controls a snake that travels at an increasing speed (eventually it becomes constant) and has the objective of feeding the snake "rewards" to make it grow. All while the user must avoid hitting the walls or having a collision with his own body. The moment a collision occurs, it is game over. This version of snake will report your current score and save the highest score in a text file.

The main algorithm of Snek is making the snake grow and follow. It does this by using a dictionary to create the snake head and body according to a predetermined value (length). In this case the length value is set to 3. So, once the game boots up, you will have the head and 2 body parts which are clones of the head (as are the rest of the body). As the snake feeds, the length increases and so does the body. The body follows the head by undrawing and drawing a clone of the head in its previous position. It continues this until it reaches current snake length.

This version of snake takes inspiration from user **ifsoMarcus'** version of snake posted on [Code Review](https://codereview.stackexchange.com/).

### Similarities:
1. Style (in an attempt to follow [PEP8](https://www.python.org/dev/peps/pep-0008/) standards).
2. GUI dimensions.
4. Some of the logic behind the snake's behavior.

### Differences:
1. Efficiency (many parts had redundant declarations that could be simplified using loops or control structures).
2. Simplified user control.
3. Ways in how the game can end.
4. How the reward is generated and obtained.
5. The score display.
6. How the display changes once the game ends.
7. How the game manipulates a file to report the highest score ever obtained.

You can find the original version [here](https://codereview.stackexchange.com/questions/226180/snake-game-using-graphics-py).
