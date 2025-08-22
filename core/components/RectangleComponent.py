from pyray import RED, Color, Vector2
from ..Component import Component
from ..Entity import Entity

class RectangleComponent(Component):

    class Events:
        OFFSET = "offset"
        SIZE = "size"
        COLOR = "color"

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
        if self._offset == value:
            return
        self._offset = value
        self.notify(RectangleComponent.Events.OFFSET, value)

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, value: Vector2):
        if self._size == value:
            return
        self._size = value
        self.notify(RectangleComponent.Events.SIZE, value)

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color):
        if self._color == value:
            return
        self._color = value
        self.notify(RectangleComponent.Events.COLOR, value)
