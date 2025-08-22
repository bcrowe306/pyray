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
        for entity in em.get_entities_with(RectangleComponent, PositionComponent):
            rect_comp = entity.get_component(RectangleComponent)
            pos_comp = entity.get_component(PositionComponent)
            x_pos = pos_comp.position.x + rect_comp.offset.x
            y_pos = pos_comp.position.y + rect_comp.offset.y
            draw_rectangle_v(Vector2(x_pos, y_pos), rect_comp.size, rect_comp.color)