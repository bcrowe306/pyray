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

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    entity_manager = EntityManager()
    systems_manager = SystemsManager()
    systems_manager.add_system(RectangleSystem())
    systems_manager.add_system(MovementSystem())

    player = entity_manager.create_entity()
    player.add_component(PositionComponent(player, screen_width // 2, screen_height // 2))
    player.add_component(RectangleComponent(player, offset=Vector2(0, -50), size=Vector2(50, 50), color=RED))
    player.add_component(MovementComponent(player))

    init_window(screen_width, screen_height, "Pyray Window")
    set_target_fps(60)
    
    # Main game loop
    while not window_should_close():

        # Input handling

        if is_key_down(KeyboardKey.KEY_A):
            entity_manager.get_component(player, MovementComponent).velocity.x = -300

        if is_key_down(KeyboardKey.KEY_D):
            entity_manager.get_component(player, MovementComponent).velocity.x = 300

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
