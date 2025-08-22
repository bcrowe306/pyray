from pyray import *
from core.EntityManager import EntityManager
from core.GameContext import GameContext
from core.SystemsManager import SystemsManager
from core.systems.RectangleSystem import RectangleSystem
from core.systems.MovementSystem import MovementSystem
from core.components.PositionComponent import PositionComponent
from core.components.MovementComponent import MovementComponent
from core.components.RectangleComponent import RectangleComponent


gravity_acceleration_in_pixels = 9.81 * 200  # Convert m/s^2 to pixels/s^2

def lerp(value, i_min, i_max, o_min, o_max):
    """
    Linear interpolation function.
    """
    return (value - i_min) / (i_max - i_min) * (o_max - o_min) + o_min
square_size: int = 25

def create_player(entity_manager: EntityManager, position: Vector2):
    p = entity_manager.create_entity()
    p.add_component(PositionComponent(p, position.x, position.y))
    p.add_component(RectangleComponent(p, offset=Vector2(0, -square_size), size=Vector2(square_size, square_size), color=RED))
    p.add_component(MovementComponent(p))
    p.subscribe(
        "MovementComponent.grounded", 
        lambda c, *args, **kwargs: 
        entity_manager.remove_entity(p)
    )

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    entity_manager = EntityManager()
    systems_manager = SystemsManager()
    systems_manager.add_system(RectangleSystem())
    systems_manager.add_system(MovementSystem())

    create_player(entity_manager, Vector2(screen_width / 2, screen_height / 2))

    init_window(screen_width, screen_height, "Pyray Window")

    set_target_fps(60)
    
    # Main game loop
    while not window_should_close():

        # Input handling

        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            mouse_position = get_mouse_position()
            create_player(entity_manager, mouse_position)

        # Update
        delta_time = get_frame_time()
        elapsed_time = get_time()
        context = GameContext(get_fps(), Vector2(screen_width, screen_height), delta_time, elapsed_time)

        systems_manager.input(context, entity_manager)
        systems_manager.update(context, entity_manager)

        # Update Box2D world

        # Draw
        begin_drawing()
        clear_background(RAYWHITE)
        systems_manager.render(context, entity_manager)
        end_drawing()

    # De-Initialization
    close_window()  # Close window and OpenGL context

if __name__ == "__main__":
    main()
