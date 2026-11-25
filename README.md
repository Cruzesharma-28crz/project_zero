# PROJECT ZERO: COMBAT SIMULATION

A lightweight isometric arcade shooter built with Python + Pygame. The project is designed to keep its rendering and game logic modest on older PCs, including systems with 4 GB RAM, older Intel Core i3 CPUs and integrated graphics.

## Run

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run `py -m pip install -r requirements.txt` (or `python -m pip install -r requirements.txt`).
4. Run `py main.py` (or `python main.py`).

## Controls

- WASD / arrow keys: move
- Mouse: aim
- Left mouse button / Space: fire
- E: pulse blast
- Escape: pause
- R: restart after game over
- Gamepad: left stick / D-pad to move, right stick to aim, A / right trigger to fire, Y to pulse, Start to pause

Gamepad mappings vary by controller and driver. Keyboard and mouse are always available.

## Performance design

- Small internal render surface, scaled to the window.
- Camera-aware tile drawing: only tiles near the viewport are considered.
- Static arena background cached to a surface.
- Reused projectile objects (object pool) to avoid constant allocation.
- Capped particle count and short-lived, inexpensive effects.
- Enemy update throttling based on distance.
- Simple geometry and distance-based collision checks.
- Configurable render scale, particle density and FPS cap.
- F3 toggles the performance overlay.

## Notes

This is an early playable prototype. The minimum hardware target is a design goal, not a verified benchmark across all machines. Actual performance depends on operating system, display resolution, drivers and background applications. Start with the Performance preset if needed.
