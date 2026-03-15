# VirtualGame — Settlers of Catan

A Python implementation of the classic board game **Settlers of Catan**, featuring a Pygame-based board visualizer, full game logic (dice rolling, trading, building, development cards), and a multi-player turn system.

---

## Project Structure

```
VirtualGame/
├── main.py                     # Entry point
├── CatanGame/
│   ├── Game.py                 # Core game loop and turn management
│   ├── Board.py                # Hex board generation and connectivity
│   ├── Player.py               # Player state and building mechanics
│   ├── BoardVisualizer.py      # Pygame visual renderer
│   ├── Tile.py                 # Hexagonal tile model
│   └── Node.py                 # Settlement/city node model
├── UnitTests/
│   ├── BoardTests.py           # Board connectivity tests
│   └── PlayerTests.py          # Player mechanics tests
└── Server/                     # Flask backend (in progress)
```

---

## Setup

### 1. Create and activate the virtual environment

```bash
cd VirtualGame
python3 -m venv CatanVM
source CatanVM/bin/activate
```

### 2. Install dependencies

```bash
pip install pygame networkx matplotlib scipy
```

---

## Running the Game

```bash
python main.py
```

This will:
1. Generate a randomized 19-tile hexagonal board.
2. Open a Pygame window with a visual representation of the board.
3. Start a 4-player game in a background thread.

---

## How to Play

### Players

The game starts with 4 players:

| Name   | Color  |
|--------|--------|
| Pesto  | Green  |
| Sky    | Blue   |
| Grape  | White  |
| Banana | Yellow |

### Setup Phase

Each player places **2 settlements** and **2 roads** on the board in turn order. Starting settlements grant resources from adjacent tiles.

Press **SPACE** in the Pygame window to advance the display between turns.

### Turn Sequence

Each turn consists of three phases:

1. **Dice Roll** — Two dice are rolled (2–12).
   - Resources are distributed to all players with settlements/cities adjacent to tiles matching the roll number.
   - On a **7**: Players with more than 7 cards must discard half, and the active player moves the **Robber** to block a tile and steal from an adjacent opponent.

2. **Trading Phase** — Propose trades with other players.
   - Enter trade offers via terminal prompts.
   - Other players can **accept**, **reject**, or **counteroffer**.

3. **Building Phase** — Spend resources to build or buy:

   | Structure        | Cost                              | Benefit              |
   |-----------------|-----------------------------------|----------------------|
   | Road            | 1 Wood + 1 Mud                    | Extend network       |
   | Settlement      | 1 Wood + 1 Mud + 1 Wheat + 1 Sheep | +1 VP               |
   | City            | 3 Rock + 2 Wheat                  | Upgrades settlement, +1 VP |
   | Development Card | 1 Rock + 1 Wheat + 1 Sheep       | See below            |

### Development Cards

| Card           | Qty | Effect                                           |
|----------------|-----|--------------------------------------------------|
| Knight         | 14  | Move Robber, steal from opponent                 |
| Year of Plenty | 2   | Take any 2 resources from the bank               |
| Monopoly       | 2   | Steal all of one resource from all players       |
| Road Building  | 2   | Place 2 roads for free                           |
| Victory Point  | 5   | +1 VP (held secret until win condition)          |

### Special Bonuses

- **Longest Road** (5+ connected road segments) → **+2 VP**
- **Largest Army** (3+ Knights played) → **+2 VP**

Both bonuses transfer to whoever surpasses the current holder.

### Winning

The first player to reach **10 Victory Points** wins. Points come from settlements (1 VP each), cities (2 VP each), development card VPs, and the Longest Road / Largest Army bonuses.

---

## Running Tests

```bash
python -m pytest UnitTests/
```

Or individually:

```bash
python UnitTests/BoardTests.py
python UnitTests/PlayerTests.py
```

---

## Next Steps

The next planned phase of this project is **training a bot using Reinforcement Learning (RL)**.

The goal is to build an RL agent that learns to play Catan by interacting with the game environment — making decisions about where to build, when to trade, and which cards to play — optimizing toward the 10-VP win condition. The existing game engine will serve as the RL environment, with the player interface abstracted into an action/observation space suitable for training.
