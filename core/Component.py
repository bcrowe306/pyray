from core.EventObject import EventObject


class Component:

    def __init__(self, parent: EventObject):
        self.parent: EventObject = parent

    def notify(self, event_id: str, *args, **kwargs):
        fully_qualified_event_id: str = f"{type(self).__name__}.{event_id}"
        self.parent.notify(fully_qualified_event_id, self, *args, **kwargs)
