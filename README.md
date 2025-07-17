# 2048 Game 

This is an advanced version of the classic 2048 game built using Python and Pygame. It includes several modern features like Undo, Theme toggle, Pause/Resume, Timer, Save/Load, and more.

## Installation

### Requirements
- Python 3.10+
- Pygame library

### Install Pygame
```bash
pip install pygame
```
## Run the Game

```bash
python 2048_game.py
```
## Features

### Core Gameplay
- Classic 4x4 2048 grid logic
- Merges tiles by swiping in four directions
- Random new tile (2 or 4) appears after every move

###  Game Logic
- Undo the previous move
- Checks for game-over state automatically
- Tracks score and high score

###  Themes
- **Green Theme**: Calm, nature-inspired
- **Blue Theme**: Cool, night-style interface
- Toggle between themes using the **Theme** button

### Timed Mode
- You have **180 seconds** (3 minutes) to get the highest score
- Timer pauses when the game is paused
- Timer countdown is displayed at the bottom

### Pause and Resume
- Pause the game using the **Pause** button
- Timer is frozen when paused
- Resume with another click

### Save and Load
- Save your current game board and score using **Save**
- Restore the last saved state using **Load**

### Undo
- Undo the last move using **Undo**
- Supports only **one-step undo**

---

## Controls

### Mouse Buttons (click on GUI)
- **Undo**: Reverts the last move
- **Theme**: Toggles between Green and Blue themes
- **Pause**: Pauses or resumes the game
- **Save**: Saves the current game state to file
- **Load**: Loads the previously saved game state

###  Arrow Keys
- `← Left`: Move tiles left  
- `→ Right`: Move tiles right  
- `↑ Up`: Move tiles up  
- `↓ Down`: Move tiles down  

---

##  Files

- `2048_game.py` – Main game script
- `highscore.txt` – Stores highest score across sessions
- `savefile.json` – Stores board and score for saving/loading


## Screenshot
<img width="685" height="955" alt="2048 game proof" src="https://github.com/user-attachments/assets/9656c19f-4962-4e87-b3c1-759c88fe086a" />



