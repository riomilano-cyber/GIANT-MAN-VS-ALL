# Giant Man: Last Stand

A top-down jungle arcade shooter built with Python and Pygame. Defend the perimeter, survive enemy waves, collect XP, and use Clicker World to convert accumulated clicks into game XP.

## Features

- Fast-paced mouse aiming and shooting
- Increasing enemy waves
- Red, green, and blue enemies with different durability
- XP drops from defeated enemies
- Temporary four-direction shooting power-up stars
- Clicker World bonus mode with 1:1 click-to-XP conversion
- Jungle-themed battlefield, pause menu, fullscreen support, and game-over redeployment

## Requirements

- Python 3.10 or newer
- Pygame 2.5.0 or newer

## Installation

From a PowerShell terminal in the project directory:

```powershell
python -m pip install -r requirements.txt
```

## Run the Game

```powershell
python main.py
```

## Controls

| Action | Control |
|---|---|
| Move | `WASD` or arrow keys |
| Aim | Mouse |
| Shoot | Left mouse button or `Space` |
| Pause/menu | `Esc` |
| Fullscreen | `F11` or `Alt+Enter` |

## Gameplay

The giant automatically faces the mouse position. Enemies enter from outside the arena and move toward the giant. Enemy contact ends the current run.

- **Red enemies:** Standard enemies with 1 hit point.
- **Green enemies:** Tough enemies that require 3 hits. Each hit also increases their speed.
- **Blue enemies:** Armored enemies with 25 hit points and an on-screen health bar.

Every defeated enemy drops one XP orb. Move close to the orb to collect it and increase your XP counter. Every 10 eliminations begins a stronger wave.

Gold power-up stars occasionally appear. Collect one to temporarily fire in four directions for five seconds.

## Clicker World

1. Press `Esc` to open the menu.
2. Select **CLICKER WORLD**.
3. Click the large **CLICK!** button to collect clicks.
4. Select **TRANSPORT CLICKS TO XP** to add all pending clicks to the game's XP counter at a 1:1 rate.
5. Press `Esc` to return to the battle.

## Project Structure

- `main.py` — Game loop, rendering, controls, enemies, XP, power-ups, and Clicker World
- `requirements.txt` — Python dependencies
- `README.md` — Setup instructions and gameplay documentation

## Troubleshooting

If Pygame is not installed or imports fail, install the dependency again:

```powershell
python -m pip install --upgrade pygame
```

If the game window does not fit your screen, use `F11` or `Alt+Enter` to change fullscreen mode.
