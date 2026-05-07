# Icy Tower

Inspired by the old-school Icy Tower game I played as a kid — one of those games that just stuck with me. Built it from scratch in Python with pygame to see if I could recreate that same feel.

## Gameplay

- **Move**: Arrow keys or `A` / `D`
- **Jump**: `Up`, `Space`, or `W`
- Bounce off the walls to build speed — faster you go, higher you jump
- Chain platforms to rack up combos
- Theme changes every 100 floors, safe platform every 100 floors
- Fall off the bottom and it's over

## Scoring

Highest floor reached is your score. Type in your name after a run and it saves to the top-10 leaderboard on the title screen.

## Project Structure

```
icy-tower/
├── main.py                 # Entry point — pygame init, event loop, 60 FPS clock
├── scores.json             # Leaderboard data (auto-created on first save)
└── game/
    ├── constants.py        # Physics values, colors, state flags, 10 visual themes
    ├── fonts.py            # Font registry (all Courier New, various sizes)
    ├── game.py             # Game class — state machine, physics update, all rendering
    ├── leaderboard.py      # Load/save scores.json
    ├── platform.py         # Platform class + procedural platform generator
    └── player.py           # Player class — movement state, pixel-art character drawing
```

## Requirements

- Python 3.8+
- pygame

```
pip install pygame
```

## Running

```
python main.py
```
