from pyray import *
from abc import ABC, abstractmethod

class Entity(ABC):

    def __init__(self):
        pass

    @abstractmethod 
    def process(self, delta_time, elapsed_time):
        # Process logic for the entity
        pass

    @abstractmethod
    def render(self):
        # Render the entity
        pass

class GameTick:

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


class Animation:

    def __init__(self, duration: float, frame_files: list | str = None, loop=True, offset: Vector2 = Vector2(0,0)):
        self.duration: float = duration
        if isinstance(frame_files, str):
            frame_files = [frame_files]
        self.frames: list[str] = frame_files if frame_files else []
        self.offset = offset
        self.__load_textures()
        self.loop: bool = loop
        self.current_frame_index: int = 0
        self.elapsed_time: float = 0.0

    def __load_textures(self):
        # Load textures for the animation frames
        self.textures = [load_texture(frame) for frame in self.frames]

    def process(self, delta_time):
        self.elapsed_time += delta_time
        if self.elapsed_time >= self.duration:
            frame_index = self.current_frame_index + 1
            if frame_index >= len(self.textures):
                if self.loop:
                    frame_index = 0
                else:
                    frame_index = len(self.textures) - 1

            self.current_frame_index = frame_index
            self.elapsed_time = 0.0

    def render(self, position: Vector2, size: Vector2 = None, flip_horizontally: bool = False, flip_vertically: bool = False):
        current_texture = self.textures[self.current_frame_index]
        if size is None:
            size = Vector2(current_texture.width, current_texture.height)
        
        source_rec = Rectangle(0, 0, current_texture.width, current_texture.height)
        if flip_horizontally:
            source_rec.width *= -1
        
        if flip_vertically:
            source_rec.height *= -1

        rendered_position = Vector2(position.x + self.offset.x, position.y + self.offset.y)
        dest_rec = Rectangle(rendered_position.x, rendered_position.y, size.x, size.y)
        origin = Vector2(dest_rec.width // 2, dest_rec.height // 2)
        draw_texture_pro(current_texture, source_rec, dest_rec, origin, 0.0, WHITE)


gravity_acceleration_in_pixels = 9.81 * 200  # Convert m/s^2 to pixels/s^2

def main():
    # Initialization
    screen_width = 800
    screen_height = 450
    game_tick = GameTick( )
    init_window(screen_width, screen_height, "Pyray Window")

    player_position = Vector2(screen_width // 2, screen_height // 2)
    player_velocity = Vector2(0, 0)
    player_direction = False  # False for right, True for left
    speed = 300
    jump_speed = 600
    is_grounded: bool = False

    # load textures
    idle_animation = Animation(
        duration=0.15,
        frame_files=[
            "assets/textures/player/adventurer-idle-00.png", 
            "assets/textures/player/adventurer-idle-01.png", 
            "assets/textures/player/adventurer-idle-02.png",
            "assets/textures/player/adventurer-idle-03.png",
            ],
        loop=True,
        offset=Vector2(0, -37)
    )
    # Set the target FPS
    set_target_fps(60)

    # Main game loop
    while not window_should_close():

        # Input handling
        is_horizontal_movement: bool = False
        if is_key_down(KeyboardKey.KEY_W):
            if is_grounded:
                player_velocity.y = -jump_speed

        # if is_key_down(KeyboardKey.KEY_S):
        #     player_velocity.y += 5

        if is_key_down(KeyboardKey.KEY_A):
            is_horizontal_movement = True
            player_direction = True
            player_velocity.x = -speed

        if is_key_down(KeyboardKey.KEY_D):
            is_horizontal_movement = True
            player_direction = False
            player_velocity.x = speed

        if not is_horizontal_movement:
            player_velocity.x = 0

        # Update
        delta_time = get_frame_time()
        elapsed_time = get_time()
        game_tick.update(delta_time)

        idle_animation.process(delta_time)

        # Movement physics
        player_position.x += player_velocity.x * delta_time
        player_position.y += player_velocity.y * delta_time

        player_velocity.y += gravity_acceleration_in_pixels * delta_time
        if player_position.y > screen_height:
            player_position.y = screen_height
            player_velocity.y = 0
            is_grounded = True
        else:
            is_grounded = False

        # Draw
        begin_drawing()
        clear_background(RAYWHITE)
        draw_text("Hello, Pyray!", 190, 200, 20, LIGHTGRAY)
        idle_animation.render(player_position, Vector2(100, 74), flip_horizontally=player_direction)
        end_drawing()

    # De-Initialization
    close_window()  # Close window and OpenGL context

if __name__ == "__main__":
    main()
