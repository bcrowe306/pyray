import pyray as rl
from pyray import Vector2, MouseButton, KeyboardKey
from core.EntityManager import EntityManager
from core.GameContext import GameContext
from core.SystemsManager import SystemsManager
from core.systems.RectangleSystem import RectangleSystem
from core.systems.MovementSystem import MovementSystem
from core.components import PositionComponent, MovementComponent, RectangleComponent



gravity_acceleration_in_pixels = 9.81 * 200  # Convert m/s^2 to pixels/s^2

def lerp(value, i_min, i_max, o_min, o_max) -> float | int:
    """
    Linear interpolation function.
    """
    return (value - i_min) / (i_max - i_min) * (o_max - o_min) + o_min
square_size: int = 15

def create_player(entity_manager: EntityManager, position: Vector2):
    player_entity = entity_manager.create_entity("player_entity")
    player_entity.add_component(PositionComponent(player_entity, position.x, position.y))
    player_entity.add_component(RectangleComponent(player_entity, offset=Vector2(0, -square_size), size=Vector2(square_size, square_size), color=rl.RED))
    player_entity.add_component(MovementComponent(player_entity))
    # player_entity.subscribe(
    #     "MovementComponent.grounded", 
    #     lambda c, *args, **kwargs: 
    #     entity_manager.remove_entity(player_entity)
    # )
    entity_manager.subscribe(
        "player_entity.MovementComponent.grounded",
        lambda e, c, *args, **kwargs: print(f"Player {e} is grounded: {c}"),
    )

def generate_context() -> GameContext:
    return GameContext(
        fps=rl.get_fps(),
        window_size=Vector2(rl.get_screen_width(), rl.get_screen_height()),
        delta_time=rl.get_frame_time(),
        elapsed_time=rl.get_time()
    )

def main():
    # Initialization
    screen_width = 1280
    screen_height = 720

    entity_manager = EntityManager()
    systems_manager = SystemsManager()
    systems_manager.add_system(RectangleSystem())
    systems_manager.add_system(MovementSystem())

    create_player(entity_manager, Vector2(screen_width / 2, screen_height / 2))

    rl.init_window(screen_width, screen_height, "Pyray Window")

    rl.set_target_fps(60)
    
    # Main game loop
    while not rl.window_should_close():

        # Input handling

        if rl.is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
            mouse_position = rl.get_mouse_position()
            create_player(entity_manager, mouse_position)

        # Update
        context = generate_context()

        systems_manager.input(context, entity_manager)
        systems_manager.update(context, entity_manager)


        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        systems_manager.render(context, entity_manager)
        rl.draw_text(f"Entities: {entity_manager.entity_count()}", 10, 10, 20, rl.DARKGRAY)
        rl.end_drawing()

        entity_manager.process_queues()

    # De-Initialization
    rl.close_window()  # Close window and OpenGL context

if __name__ == "__main__":
    main()
