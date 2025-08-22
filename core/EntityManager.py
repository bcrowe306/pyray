import itertools

from .Component import Component
from .Entity import Entity

class EntityManager:

    def __init__(self):
        self._next_id = itertools.count(1)  # unique entity IDs
        self.entities: dict[int, Entity] = {}

    def create_entity(self) -> Entity:
        entity_id = next(self._next_id)
        entity = Entity(entity_id)
        self.entities[entity_id] = entity
        return entity

    def add_component(self, entity: Entity, component: Component) -> None:
        entity = self.entities.get(entity.id)
        if entity:
            entity.add_component(component)

    def get_component(self, entity: Entity, component_type: type[Component]) -> Component | None:
        entity = self.entities.get(entity.id)
        if entity:
            return entity.get_component(component_type)
        return None

    def get_entities_with(self, *component_types):
        for entity in self.entities.values():
            if all(entity.get_component(t) for t in component_types):
                yield entity


