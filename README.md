# Rock, Paper, Scissors Game Backend - Django

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
   git clone https://github.com/jguerrero10/game_backend.git
   cd game_backend
    ```
2. Build the Docker image:
   ```bash
   docker-compose build
   docker-compose up
   ```
3. Access the API documentation at `http://localhost:8000/api` to interact with the game backend.

### 🧪 Testing
- Run the test suite using the following command:
  ```bash
  docker-compose run app sh -c "python manage.py test"
  ```
- The test suite includes unit tests for the game logic and integration tests for the API endpoints.
- The tests are designed to ensure the game functions correctly and that the API endpoints return the expected responses.
- The test suite is run automatically on each push to the main branch using GitHub Actions.

- coverage run --source='.' manage.py test
- coverage report
```
Name                           Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------
game/admin.py                      5      0      0      0   100%
game/models.py                    26      0      2      0   100%
game/serializers.py               20      0      0      0   100%
game/service/game_service.py      21      0     10      0   100%
game/views.py                     36      0      6      0   100%
--------------------------------------------------------------------------
TOTAL                            108      0     18      0   100%

```