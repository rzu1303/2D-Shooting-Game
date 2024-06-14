# 2D Shooting Game

## Overview

This is a 2D shooting game built using Python and Pygame. It's designed for two players on separate computers connected through a router. Each player controls a character, navigating through obstacles while avoiding incoming bullets from the opponent.

## Features

- **Multiplayer Gameplay**: The game allows two players to connect over a network and play against each other.
  
- **Player Selection**: Players can choose to be either Player 1 or Player 2 before starting the game.
  
- **Controls**: Players control their characters using the keyboard. Both players use the arrow keys (Up, Down, Left, Right) for movement.
  
- **Obstacle Blocks**: The game includes blocks that serve as obstacles. Players need to navigate around these blocks while avoiding collisions.
  
- **Continuous Bullet Emission**: Bullets are continuously emitted from each player's character, creating a dynamic environment. Players need to strategize and navigate skillfully to avoid incoming bullets.
  
- **Winning Conditions**: The game ends when one player successfully hits the opponent. The winning player is then declared.

## How to Play

1. Run the game on two separate computers connected to the same router.
  
2. Each player selects their role as Player 1 or Player 2.
  
3. Wait for the opponent to connect, and the game will start once both players are ready.
  
4. Both players need to press the respective keys for movement (Arrow keys).
  
5. Navigate through the obstacles to avoid incoming bullets from the opponent.
  
6. The game ends when one player successfully hits the opponent three times. The winning player is declared, and the option to replay or close the game is presented.

## Requirements

- Python 3.x
  
- Pygame library

## How to Run

1. Install Python on your system.
  
2. Install the Pygame library by running the following command:
   pip install pygame

3. Clone the repository and navigate to the game directory.

4. Run the game using the following command:
   python your_game_file.py

5. Make sure to configure the `config.py` file according to your preferences.

## Technologies Used

1. Python: Programming language used for the game logic.
  
2. Pygame: Python library used for developing the game interface and handling graphics.

3. Socket Programming: Used for implementing multiplayer functionality, enabling communication between clients and server.

4. Threading: Utilized to manage concurrent execution of game logic and network operations.

5. Queue: Used for handling input and data exchange between threads.

6. pygame.locals: Provides constants and utilities for handling keyboard inputs and events.


## Video Demo

Watch the gameplay in action on [YouTube](https://www.youtube.com/watch?v=Gq0HsdapQws).

## Additional Notes

- Ensure that both players have access to the same network, and firewall settings allow communication between their computers.

- In case of connection issues, the game provides options to retry or close the application.


