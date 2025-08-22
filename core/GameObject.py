import pyray as rl
from core.EntityManager import EntityManager
from core.SystemsManager import SystemsManager
from core.systems import RectangleSystem, MovementSystem
from core.GameContext import GameContext
from core.components import PositionComponent, MovementComponent, RectangleComponent
from pyray import Vector2, MouseButton


class GameObject:
    def __init__(self, title: str, screen_width: int = 1280, screen_height: int = 720, fps: int = 60):
        """Initialize the game object with a title and screen dimensions.
        """
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.title: str = title
        self.fps: int = fps

        self.entity_manager: EntityManager = EntityManager()
        self.systems_manager: SystemsManager = SystemsManager()
        self.systems_manager.add_system(RectangleSystem())
        self.systems_manager.add_system(MovementSystem())

        rl.init_window(screen_width, screen_height, title)
        rl.set_target_fps(fps)

        self.layer_counter = 0

    def run(self):        
        """
        Run the main game loop.
        """
        # Main game loop
        while not rl.window_should_close():

            # Input handling

            if rl.is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
                mouse_position = rl.get_mouse_position()
                self.create_player(mouse_position)

            # Update
            context = self.generate_context()

            self.systems_manager.input(context, self.entity_manager)
            self.systems_manager.update(context, self.entity_manager)

            # Draw
            rl.begin_drawing()
            rl.clear_background(rl.RAYWHITE)
            self.systems_manager.render(context, self.entity_manager)
            rl.draw_text(
                f"Entities: {self.entity_manager.entity_count()}", 10, 10, 20, rl.DARKGRAY
            )
            rl.end_drawing()

            self.entity_manager.process_queues()
        # De-Initialization
        rl.close_window()  # Close window and OpenGL context

    def generate_context(self) -> GameContext:
        return GameContext(
            fps=rl.get_fps(),
            window_size=Vector2(rl.get_screen_width(), rl.get_screen_height()),
            delta_time=rl.get_frame_time(),
            elapsed_time=rl.get_time()
        )
    
    def create_player(self, position: Vector2):
        square_size: int = 15
        player_entity = self.entity_manager.create_entity("player_entity", self.layer_counter)
        player_entity.add_component(PositionComponent(player_entity, position.x, position.y))
        player_entity.add_component(RectangleComponent(player_entity, offset=Vector2(0, -square_size), size=Vector2(square_size, square_size), color=rl.RED))
        player_entity.add_component(MovementComponent(player_entity))
        player_entity.subscribe(
            self.entity_manager.Components.MOVEMENT.Events.GROUNDED,
            lambda c, *args, **kwargs:
            self.entity_manager.remove_entity(player_entity)
        )
        self.entity_manager.subscribe(
            "player_entity.MovementComponent.grounded",
            lambda e, c, *args, **kwargs: print(f"Player {e} is grounded: {c}"),
        )
        self.layer_counter += 1
