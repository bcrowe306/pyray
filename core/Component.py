from core.Entity import Entity

class Component:

    def __init__(self, parent: Entity):
        self.parent: Entity = parent

    def notify(self, event_id: str, *args, **kwargs):
        fully_qualified_event_id: str = f"{type(self).__name__}.{event_id}"
        self.parent.notify(fully_qualified_event_id, self, *args, **kwargs)
