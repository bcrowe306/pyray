from pyray import Vector2
from ..Component import Component
from ..Entity import Entity

class MovementComponent(Component):

    class Events:
        SPEED = "MovementComponent.speed"
        VELOCITY = "MovementComponent.velocity"
        DIRECTION = "MovementComponent.direction"
        GROUNDED = "MovementComponent.grounded"
        GRAVITY = "MovementComponent.gravity"

    def __init__(
            self, 
            parent: Entity, 
            speed: int = 300, 
            velocity: tuple[int, int] = (0, 0),
            gravity: bool = True,
            ):
        super().__init__(parent)
        self._speed: int = speed
        self._velocity: Vector2 = Vector2(*velocity)
        self._direction: bool = False
        self._grounded: bool = False
        self._gravity: bool = gravity  # Whether gravity is applied

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: int):
        if self._speed == value:
            return
        self._speed = value
        self.notify("speed", value)

    @property
    def velocity(self) -> Vector2:
        return self._velocity

    @velocity.setter
    def velocity(self, value: Vector2):
        if self._velocity == value:
            return
        self._velocity = value
        self.notify("velocity", value)

    @property
    def direction(self) -> bool:
        return self._direction

    @direction.setter
    def direction(self, value: bool):
        if self._direction == value:
            return
        self._direction = value
        self.notify("direction", value)

    @property
    def grounded(self) -> bool:
        return self._grounded

    @grounded.setter
    def grounded(self, value: bool):
        if self._grounded == value:
            return
        self._grounded = value
        self.notify("grounded", value)

    @property
    def gravity(self) -> bool:
        return self._gravity

    @gravity.setter
    def gravity(self, value: bool):
        if self._gravity == value:
            return
        self._gravity = value
        self.notify("gravity", value)
