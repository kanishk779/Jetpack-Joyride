# Jetpack-Joyride
Game in Python
## Context
This is the first project of the course Design and Analysis of Software Systems
that i took in 4th semester in my college. 
## Objective
1. The expected outcome of this project to get a good hang of OOPS concept in
python, and there could be nothing better than making a game.
2. The OOPS concept used in the game are :
  1. Encapsulation - Use of classes for designing the game ensures
	 Encapsulation.
  2. Polymorphism - Use of createDragon method which is overridden by Manda and
	 Viserion for rendering different dragons ensures Polymorphism.
  3. Inheritance - Use of godObject from which all the game object inherits
	 ensures Inheritance is being taken care of.
  4. Abstraction - Use of private variables in the class Location ensures that
	 unnecessary details to the outside world.
3. The game should be a terminal-based Python3 game.
## About the game
1. The protagonist of the game is Manda living in the post-empire era. He is one
   of the last remaining members of his clan in the galaxy and is currently on a 
   mission for the Guild. He needs to rescue The child , who strikingly
   resembles Master.
2. The objective of the game is to collect as many coins as possible, fight the
   obstacles on the way, defeat the boss enemy and rescue Baby Yoda.
## Description of classes created
1. GodObject - this is the class from which every other game object inherits.
2. Location - this class is used to describe the location and size of an object.
3. Person - every living character in the game inherit from this class.
4. Mandalorian - this represents the main character of the game.
5. Viserion - this represents the main Villian (Boss enemy) of the game.
6. Game - this class controls the whole game, it has various functions to
   control the flow of the game.
7. LargeGrid - this class represents the background grid of the game which has 
   different object randomly generated as obstacles in the game.
8. SmallGrid - this class represents the current background of the game which is
   loaded from the large grid.
9. Screen - this class is responsible for loading and rendering the game screen
   at each iteration.
10. Utility - this class helps to get the non blocking input from the user.
## How to run this game
```
pip3 install -r requirements.txt
python3 main.py
```
## Controls
1. w for jumping up
2. a for moving left
3. d for moving right
4. b for shooting bullets
5. v for speeding up the game(for some amount of time)
6. '.' space bar for obtaining the shield if it is present. It refills after
   fixed amount of time.
## Features
1. Collect coins to increase your score.
2. If the bullets hit the fire beam they(beams) are destroyed and it adds to your score.
3. If the player hits the beams than his life is reduced.
4. The player can take the Dragon Bonus shown by 'D' which turn him to a dragon.
5. If the player hits a fire beam and he is in dragon mode than he is changed
   back to normal player without decreasing the life.
6. The player can use the shield to protect him from obstacles.
7. The magnet which appears somewhere in the middle of the game pulls the player
   up.
8. The boss enemy appears at the end, which is a dragon and shoots Ice balls at
   the player which he must dodge, otherwise his life will be reduced.
9. The boss enemy follows the player.
10. You win the game after defeating the boss enemy and rescuing Yoda.
