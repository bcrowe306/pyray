from abc import ABC, abstractmethod

class EventObject(ABC):

    def __init__(self):
        self._listeners: dict[str, list[callable]] = {}

    def subscribe(self, event_id: str, callback: callable):
        if event_id not in self._listeners:
            self._listeners[event_id] = []
        self._listeners[event_id].append(callback)

    def unsubscribe(self, event_id: str, callback: callable):
        if event_id in self._listeners:
            self._listeners[event_id].remove(callback)

    def notify(self, event_id: str, *args, **kwargs):
        event_string = f"{self.get_type_name()}.{event_id}"
        if event_string in self._listeners:
            for callback in self._listeners[event_string]:
                callback(*args, **kwargs)

    @abstractmethod
    def get_type_name(self) -> str:
        pass