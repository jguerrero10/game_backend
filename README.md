# Rock, Paper, Scissors Game Backend - FastAPI

This repository contains the backend for a web-based Rock, Paper, Scissors game developed using FastAPI. The game follows the classic rules with additional logic for multiple rounds and victory conditions.

### 📋 Game Rules

The game is designed for two registered players and follows these rules:
- Rock beats Scissors 
- Scissors beat Paper 
- Paper beats Rock 
- If both players choose the same move, the round ends in a draw.

### 🎯 Objective

The objective is to win 3 rounds to secure victory in the game.

## 🕹️ Gameplay Flow

1. Player Registration 
   - Two players must register before starting the game. 
   - Each player must provide their full name, and the system will automatically assign them a unique ID.

2. Game Rounds 
   - Each round requires both players to choose one of the following moves:
     - Rock 
     - Paper 
     - Scissors
   - The system enforces turn order:
     - Player 1 makes their move first. 
     - Player 2 can only make their move after Player 1 has selected theirs. 
   - After both players have submitted their moves, the system will:
     - Display the winner of the round (or indicate a draw). 
     - Update the score.

3. Winning Conditions 
   - The game continues until one of the players achieves 3 round victories.

4. End of Game 
   - Once the game concludes, players are prompted to:
     - Restart the game with the same players. 
     - Start a new game, requiring two new players to register.

### 🚀 Tech Stack
- Django with Django REST framework (DRF). 
- Python - Core programming language.
- PostgreSQL - For storing player data and game history.
- Docker - For containerizing the application.

### 📖 How to Run
1. Clone the repository:
   ```bash
   git clone