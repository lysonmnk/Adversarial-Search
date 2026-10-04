# Tic-Tac-Toe 5x5 with Minimax AI

A Python-based Tic-Tac-Toe game on a 5x5 board where a human player competes against an AI agent powered by the Minimax algorithm. This project demonstrates the implementation of Adversarial Search, game-state evaluation, and interactive gameplay using Pygame.

## Features

- 5x5 Tic-Tac-Toe game board
- Human player vs. AI
- AI decision-making using the Minimax algorithm
- Game state evaluation
- Detection of win and draw conditions
- Interactive graphical interface using Pygame
- Turn-based gameplay between the human player and AI

## Tech Stack

| Technology | Purpose |
| ---------- | ------- |
| Python | Main programming language |
| Pygame | Graphical game interface |
| Minimax | AI decision-making algorithm |
| Adversarial Search | Game-playing strategy |

## Project Structure

```text
.
├── game_ui.py
└── README.md
```

> Update the structure above if the actual project contains additional files or directories.

## Getting Started

### Prerequisites

Make sure the following software is installed:

- Python 3
- Pygame

Check your Python installation:

```bash
python --version
```

### Installation

Clone the repository:

```bash
git clone [TODO: GitHub Repository URL]
cd [TODO: Project Directory]
```

Install Pygame:

```bash
pip install pygame
```

## Running the Application

Run the game using:

```bash
python game_ui.py
```

A game window will open and you can start playing Tic-Tac-Toe on the 5x5 board.

## How to Play

- The human player uses `X`.
- The AI uses `O`.
- Click an empty cell to place your move.
- Players take turns making moves.
- The game ends when a player wins or the board reaches a draw state.

## AI and Minimax

The AI uses the **Minimax algorithm**, a recursive decision-making algorithm commonly used in two-player competitive games.

The game models the players as:

- **MAX (`O`)** — the AI player that attempts to maximize the game score.
- **MIN (`X`)** — the human player that attempts to minimize the AI's score.

The general decision process is:

```text
Current Game State
        |
        v
Generate Possible Moves
        |
        v
Explore Game States
        |
        v
Evaluate Game States
        |
        v
      Minimax
     /       \
   MAX       MIN
     \       /
      Best Move
          |
          v
       AI Move
```

The Minimax algorithm evaluates possible moves and selects the move with the best outcome for the AI.

## Evaluation Function

Because a 5x5 board produces a large number of possible game states, exploring the entire game tree can become computationally expensive.

An evaluation function can therefore be used to estimate the quality of non-terminal game states.

A basic scoring concept is:

```text
AI Win       -> Positive score
Human Win    -> Negative score
Draw         -> 0
Other State  -> Position evaluation
```

The evaluation function can be improved by considering patterns such as consecutive AI or opponent symbols.

## Challenges and Future Improvements

### Alpha-Beta Pruning

The Minimax algorithm can be optimized using **Alpha-Beta Pruning**.

Alpha-Beta Pruning eliminates branches that do not need to be explored, allowing the AI to make decisions more efficiently.

### Improved Evaluation Function

The evaluation function can be improved by assigning different scores to promising board patterns.

For example:

```text
AI has 4 consecutive symbols       -> High positive score
AI has 3 consecutive symbols       -> Positive score

Opponent has 4 consecutive symbols -> High negative score
Opponent has 3 consecutive symbols -> Negative score
```

This allows the AI to make more strategic decisions instead of only considering immediate winning conditions.

### Adjustable AI Difficulty

The AI can be modified to occasionally make random moves to provide an easier difficulty level for beginners.

For example:

```python
if random.random() < 0.25:
    # Make a random move
else:
    # Use Minimax to find the best move
```

This gives the AI a 25% chance of choosing a random move instead of the optimal Minimax move.

## Learning Objectives

This project demonstrates the following concepts:

- Adversarial Search
- Zero-Sum Games
- Game State Representation
- Minimax Algorithm
- Evaluation Functions
- Recursive Search
- AI Decision Making
- Interactive Game Development with Pygame

## Screenshots

Add screenshots of the game interface here when available.

```markdown
![Tic-Tac-Toe 5x5](docs/screenshots/game.png)
```

## Author

**Lyson Paulus Esar Manik**


