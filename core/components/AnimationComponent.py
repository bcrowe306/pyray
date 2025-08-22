from pyray import Vector2, Rectangle, load_texture, draw_texture_pro, WHITE
from ..Component import Component

class Animation:

    def __init__(
        self,
        duration: float,
        frame_files: list | str = None,
        loop=True,
        offset: Vector2 = Vector2(0, 0),
        auto_play: bool = True
    ):
        self.duration: float = duration
        if isinstance(frame_files, str):
            frame_files = [frame_files]
        self.frames: list[str] = frame_files if frame_files else []
        self.offset = offset
        self.__load_textures()
        self.loop: bool = loop
        self.__is_playing: bool = auto_play
        self.current_frame_index: int = 0
        self.elapsed_time: float = 0.0

    def __load_textures(self):
        # Load textures for the animation frames
        self.textures = [load_texture(frame) for frame in self.frames]

    def start(self):
        self.current_frame_index = 0
        self.elapsed_time = 0.0

    def stop(self):
        self.current_frame_index = 0
        self.elapsed_time = 0.0

    def toggle_pause(self):
        self.__is_playing = not self.__is_playing

    def process(self, delta_time):
        if not self.__is_playing:
            return
        self.elapsed_time += delta_time
        if self.elapsed_time >= self.duration:
            self.elapsed_time = 0.0
            frame_index = self.current_frame_index + 1
            if frame_index >= len(self.textures):
                if self.loop:
                    frame_index = 0
                else:
                    frame_index = len(self.textures) - 1

            self.current_frame_index = frame_index

    def render(
        self,
        position: Vector2,
        size: Vector2 = None,
        flip_horizontally: bool = False,
        flip_vertically: bool = False,
    ):
        current_texture = self.textures[self.current_frame_index]
        if size is None:
            size = Vector2(current_texture.width, current_texture.height)

        source_rec = Rectangle(0, 0, current_texture.width, current_texture.height)
        if flip_horizontally:
            source_rec.width *= -1

        if flip_vertically:
            source_rec.height *= -1

        rendered_position = Vector2(
            position.x + self.offset.x, position.y + self.offset.y
        )
        dest_rec = Rectangle(rendered_position.x, rendered_position.y, size.x, size.y)
        origin = Vector2(dest_rec.width // 2, dest_rec.height // 2)
        draw_texture_pro(current_texture, source_rec, dest_rec, origin, 0.0, WHITE)


class AnimationComponent(Component):
    def __init__(self):
        super().__init__()
        self.animations: dict[str, Animation] = {}
        self.current_animation: Animation | None = None

    def add_animation(self, name: str, animation: Animation):
        self.animations[name] = animation

    def select_and_start_animation(self, name: str):
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_animation.start()

    def select_animation(self, name: str):
        if name in self.animations:
            self.current_animation = self.animations[name]

    def stop_animation(self):
        if self.current_animation:
            self.current_animation.stop()

    def start_animation(self):
        if self.current_animation:
            self.current_animation.start()

    def toggle_pause(self):
        if self.current_animation:
            self.current_animation.toggle_pause()

    def process(self, delta_time: float):
        if self.current_animation:
            self.current_animation.process(delta_time)

    def render(self, position: Vector2, size: Vector2 = None, flip_horizontally: bool = False, flip_vertically: bool = False):
        if self.current_animation:
            self.current_animation.render(position, size, flip_horizontally, flip_vertically)