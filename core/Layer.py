from core.EventObject import EventObject
from core.Component import Component
from core.Entity import Entity


class Layer(EventObject):
    def __init__(self, name: str = ""):
        super().__init__()
        if not name:
            name = "Layer"
        self.name: str = name
        self.visible: bool = True
        self.entities: dict[int, Entity] = {}
        self.__entity_removal_queue: list[int] = []
        self.__entity_addition_queue: list[Entity] = []
        self.__iterating_entities: bool = False

    def get_type_name(self) -> str:
        return self.name

    def add_entity(self, entity: Entity) -> None:
        if entity.id not in self.entities:
            self.entities[entity.id] = entity

    def get_entity(self, entity_id: int) -> Entity | None:
        return self.entities.get(entity_id)

    def get_entities_with(self, *component_types):
        if not component_types:
            return iter(self.entities.values())

        self.__iterating_entities = True
        for entity in self.entities.values():
            if all(entity.get_component(t) for t in component_types):
                yield entity
        self.__iterating_entities = False

    def get_component(self, entity: Entity, component_type: type[Component]) -> Component | None:
        if entity:
            return entity.get_component(component_type) # type: ignore
        return None

    def remove_entity(self, entity: Entity) -> None:
        if self.__iterating_entities:

            if entity.id not in self.__entity_removal_queue:
                self.__entity_removal_queue.append(entity.id)
        else:
            if entity.id in self.entities:
                del self.entities[entity.id]

    def process_queues(self):
        for entity in self.__entity_addition_queue:
            self.entities[entity.id] = entity
        self.__entity_addition_queue.clear()

        for entity_id in self.__entity_removal_queue:
            if entity_id in self.entities:
                del self.entities[entity_id]
        self.__entity_removal_queue.clear()

    def get_entity_count(self) -> int:
        return len(self.entities)
