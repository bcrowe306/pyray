from ..GameContext import GameContext
from ..System import System
from ..EntityManager import EntityManager
from ..components.RectangleComponent import RectangleComponent
from ..components.PositionComponent import PositionComponent
from pyray import draw_rectangle_v, Vector2

class RectangleSystem(System):
    def update(self, context: GameContext, em: EntityManager):
        pass

    def render(self, context: GameContext, em: EntityManager):
        # get all entities with RectangleComponent and PositionComponent and sort by layer

        for i, layer in enumerate(em.get_sorted_layers()):
            # Get entities with RectangleComponent and PositionComponent
            # and sort them by their layer
            print(f"Rendering Layer {i}: {layer.name}")
            if not layer.visible:
                continue
            for entity in layer.get_entities_with(RectangleComponent, PositionComponent):

                rect_comp: RectangleComponent = entity.get_component(RectangleComponent) # type: ignore
                pos_comp: PositionComponent = entity.get_component(PositionComponent) # type: ignore
                x_pos = pos_comp.position.x + rect_comp.offset.x
                y_pos = pos_comp.position.y + rect_comp.offset.y
                draw_rectangle_v(Vector2(x_pos, y_pos), rect_comp.size, rect_comp.color)