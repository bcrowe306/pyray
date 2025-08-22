from .EventObject import EventObject


class Entity(EventObject):

    def __init__(self, parent: EventObject, id: int, name: str = None):
        super().__init__()
        self.id: int = id
        self.parent: EventObject = parent
        if name is None:
            name = f"Entity_{id}"
        self.name: str = name
        self.components: dict[type, object] = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def get_component(self, component_type):
        return self.components.get(component_type)

    def get_type_name(self) -> str:
        return self.name

    def notify(self, event_id: str, *args, **kwargs):
        if event_id in self._listeners:
            for callback in self._listeners[event_id]:
                callback(*args, **kwargs)
        self.parent.notify(f"{self.get_type_name()}.{event_id}", self, *args, **kwargs)
