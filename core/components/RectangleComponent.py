from pyray import RED, Color, Vector2
from ..Component import Component
from ..Entity import Entity

class RectangleComponent(Component):
    def __init__(self, parent: Entity, offset: Vector2, size: Vector2, color: Color = RED):
        super().__init__(parent)
        self._offset: Vector2 = offset
        self._size: Vector2 = size
        self._color: Color = color

    @property
    def offset(self) -> Vector2:
        return self._offset

    @offset.setter
    def offset(self, value: Vector2):
        self._offset = value
        self.notify("offset", value)

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, value: Vector2):
        self._size = value
        self.notify("size", value)

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value
        self.notify("color", value)
