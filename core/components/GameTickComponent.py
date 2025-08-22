class GameTickComponent:

    def __init__(self, game_tick_fps=24, tick_callback=None):
        self.game_tick = 0
        self.game_tick_fps = game_tick_fps
        self.game_tick_seconds_per_frame = 1.0 / self.game_tick_fps
        self.game_tick_elapsed_time = 0.0
        self.tick_callback = tick_callback

    def update(self, delta_time):
        self.game_tick_elapsed_time += delta_time
        if self.game_tick_elapsed_time >= self.game_tick_seconds_per_frame:
            self.game_tick += 1
            self.game_tick_elapsed_time = 0.0
            if self.tick_callback and callable(self.tick_callback):
                self.tick_callback(self.game_tick)
