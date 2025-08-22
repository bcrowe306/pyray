import itertools

from .Component import Component
from .Entity import Entity
from .EventObject import EventObject
from .components import PositionComponent, MovementComponent, RectangleComponent  # Assuming these components are defined in components.py

class EntityManager(EventObject):

    # List of component types that can be added to entities
    
    class Components:
        POSITION = PositionComponent
        MOVEMENT = MovementComponent
        RECTANGLE = RectangleComponent

    def __init__(self):
        super().__init__()
        self._next_id = itertools.count(1)  # unique entity IDs
        self.entities: dict[int, Entity] = {}
        self.__entity_removal_queue: list[int] = []
        self.__entity_addition_queue: list[Entity] = []
        self.__iterating_entities: bool = False

    def create_entity(self, name:str) -> Entity:
        entity_id: int = next(self._next_id)
        entity: Entity = Entity(self, name, entity_id)
        self.entities[entity_id] = entity
        return entity
    
    def add_entity(self, entity: Entity) -> None:
        self.__entity_addition_queue.append(entity)

    def get_new_entity_id(self) -> int:
        return next(self._next_id)

    def entity_count(self) -> int:
        return len(self.entities)

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

    def add_component(self, entity: Entity, component: Component) -> None:
        if entity:
            entity.add_component(component)

    def get_component(self, entity: Entity, component_type: type[Component]) -> Component | None:
        if entity:
            return entity.get_component(component_type) # type: ignore
        return None

    def get_entities_with(self, *component_types):
        if not component_types:
            return iter(self.entities.values())
        
        self.__iterating_entities = True
        for entity in self.entities.values():
            if all(entity.get_component(t) for t in component_types):
                yield entity
        self.__iterating_entities = False

    def get_type_name(self):
        return "EntityManager"

    def notify(self, event_id, *args, **kwargs):
        print(f"EntityManager received event: {event_id}")
        return super().notify(event_id, *args, **kwargs)
