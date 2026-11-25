"""Runtime settings and low-end friendly defaults."""
from dataclasses import dataclass

INTERNAL_WIDTH = 640
INTERNAL_HEIGHT = 360
TILE_W = 64
TILE_H = 32
WORLD_COLS = 42
WORLD_ROWS = 42

@dataclass
class Settings:
    fps_cap: int = 60
    render_scale: float = 0.75
    particles: str = "medium"
    show_performance: bool = False
    fullscreen: bool = False

    def apply_preset(self, preset: str) -> None:
        if preset == "performance":
            self.render_scale, self.particles, self.fps_cap = 0.5, "low", 60
        elif preset == "quality":
            self.render_scale, self.particles, self.fps_cap = 1.0, "high", 60
        else:
            self.render_scale, self.particles, self.fps_cap = 0.75, "medium", 60
