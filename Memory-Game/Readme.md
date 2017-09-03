# DNA-Arcade
Modified version of the classic memory game

<br/>


![Game Menu](Screenshots/game_menu.png?raw=true "Menu")

![Select Difficulty](Screenshots/levels.png?raw=true "Levels")

![Game Board](Screenshots/Game.png?raw=true "Game Board")


### How to use
* To clone the repository:

 ```bash
 git clone https://github.com/Aksh77/Pygame.git
 ```
* Browse to Game directory :

 ```bash
 cd Pygame/Memory-Game
 ```

* Install the dependencies
 
 ```bash
 sudo pip install -r requirements.txt
 ```
 
* Compile and run the program :

 ```bash
 python DNA_Arcade.py
 ```
 
 
### Dependencies
* Python 2.x
* Pygame 1.9


### How to Play

This is the modified version of the classic Memory Game.
You need to match the tiles having Complimentary Base pairs of DNA i.e A should match with T and G should match with C.

* Both the tiles should have the letters with the same colour in order to match i.e a green **A** should pair with a green **T**.
* The tiles that are paired disappear. The game ends when the board is empty.
* Scoring is based on number of moves taken to finish the game.

### Features
3 Difficulty levels :

* Easy   (Board size: 4 X 4)

* Medium (Board size: 6 X 5)

* Hard   (Board Size: 8 X 7)

### To-Do

* Count Number of moves.
* Save Highscore.
* Add Sound effects.
