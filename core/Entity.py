class Entity:

    def __init__(self, id: int):
        self.id: int = id
        self.listeners: dict[str, list[callable]] = {}
        self.components: dict[type, object] = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def get_component(self, component_type):
        return self.components.get(component_type)

    def subscribe(self, event_id: str, callback):
        if event_id not in self.listeners:
            self.listeners[event_id] = []
        self.listeners[event_id].append(callback)

    def unsubscribe(self, event_id: str, callback):
        if event_id in self.listeners:
            self.listeners[event_id].remove(callback)

    def notify(self, event_id: str, *args, **kwargs):
        if event_id in self.listeners:
            for callback in self.listeners[event_id]:
                if callable(callback):
                    callback(*args, **kwargs)