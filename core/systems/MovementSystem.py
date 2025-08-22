from ..GameContext import GameContext
from ..System import System
from ..EntityManager import EntityManager
from ..components.PositionComponent import PositionComponent
from ..components.MovementComponent import MovementComponent


class MovementSystem(System):
    def __init__(self):
        self.gravity_acceleration = 9.81 * 200  # Convert m/s^2 to pixels/s^2

    def update(self, context: GameContext, em: EntityManager):

        for layer in em.get_sorted_layers():

            for entity in layer.get_entities_with(PositionComponent, MovementComponent):
                pos_comp: PositionComponent = entity.get_component(PositionComponent)  # type: ignore
                move_comp: MovementComponent = entity.get_component(MovementComponent)  # type: ignore

                # Movement physics
                pos_comp.position.x += move_comp.velocity.x * context.delta_time
                pos_comp.position.y += move_comp.velocity.y * context.delta_time


                # Apply gravity if enabled
                if move_comp.gravity:
                    # Apply gravity to the vertical velocity
                    move_comp.velocity.y += self.gravity_acceleration * context.delta_time
                    if pos_comp.position.y >= context.window_size.y:
                        pos_comp.position.y = context.window_size.y
                        move_comp.velocity.y = 0
                        move_comp.grounded = True
                    else:
                        move_comp.grounded = False

    def render(self, context: GameContext, em: EntityManager):
        pass
