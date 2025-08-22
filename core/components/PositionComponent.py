from pyray import Vector2
from ..Component import Component
from ..Entity import Entity

class PositionComponent(Component):

    def __init__(self, parent: Entity, x: float, y: float):
        super().__init__(parent)
        self._position = Vector2(x, y)

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value
        self.notify("position", value)
