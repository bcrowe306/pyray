from .EventObject import EventObject
from .Component import Component
from typing import Any

class Entity(EventObject):

    def __init__(self, parent: EventObject, name: str, id: int):
        super().__init__()
        self.id: int = id
        self.parent: EventObject = parent
        if not name:
            name = f"Entity_{id}"
        self.name: str = name
        self.components: dict[type, Component] = {}

    def add_component(self, component: Component) -> Component:
        self.components[type(component)] = component
        return component

    def get_component(self, component_type) -> object:
        return self.components.get(component_type)

    def get_type_name(self) -> str:
        return self.name

    def notify(self, event_id: str, *args, **kwargs):
        if event_id in self._listeners:
            for callback in self._listeners[event_id]:
                callback(*args, **kwargs)
        self.parent.notify(f"{self.name}.{event_id}", self, *args, **kwargs)
