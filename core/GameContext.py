from pyray import Vector2


class GameContext:
    def __init__(
        self, fps: int, window_size: Vector2, delta_time: float, elapsed_time: float
    ):
        self.fps: int = fps
        self.window_size: Vector2 = window_size
        self.delta_time: float = delta_time
        self.elapsed_time: float = elapsed_time