import itertools

from .Component import Component
from .Entity import Entity
from .EventObject import EventObject
from .components import PositionComponent, MovementComponent, RectangleComponent  # Assuming these components are defined in components.py
from .Layer import Layer
class EntityManager(EventObject):

    # List of component types that can be added to entities

    class Components:
        POSITION = PositionComponent
        MOVEMENT = MovementComponent
        RECTANGLE = RectangleComponent

    def __init__(self):
        super().__init__()
        self._next_id = itertools.count(1)  # unique entity IDs
        self.layers: dict[int, Layer] = {}
        self.entity_layer_map: dict[int, int] = {}  # Maps entity IDs to layer IDs

    def create_entity(self, name:str, layer:int = 0) -> Entity:
        """        Creates a new entity with a unique ID and adds it to the specified layer.
        If the layer does not exist, it will be created."""
        entity_id: int = next(self._next_id)
        entity: Entity = Entity(self, name, entity_id)

        if layer not in self.layers:
            self.layers[layer] = Layer(f"Layer_{layer}")
        self.layers[layer].add_entity(entity)
        self.entity_layer_map[entity_id] = layer
        return entity

    def get_sorted_layers(self) -> list[Layer]:
        """
        Returns a list of layers sorted by the layers dictionary key.
        """
        # return list of layers orderd by layers key which is an int
        return [self.layers[key] for key in sorted(self.layers.keys())]

    def get_layer(self, layer_id: int) -> Layer | None:
        """
        Returns the layer with the given ID, or None if it doesn't exist.
        """
        return self.layers.get(layer_id)
    
    def get_entity(self, entity_id: int) -> Entity | None:
        """
        Returns the entity with the given ID, or None if it doesn't exist.
        """
        layer = self.entity_layer_map.get(entity_id)
        if layer is not None and layer in self.layers:
            return self.layers[layer].get_entity(entity_id)
        return None

    def remove_entity(self, entity: Entity) -> None:
        layer_id = self.entity_layer_map.get(entity.id)
        if layer_id is not None and layer_id in self.layers:
            self.layers[layer_id].remove_entity(entity)
            del self.entity_layer_map[entity.id]

    def get_new_entity_id(self) -> int:
        return next(self._next_id)

    def entity_count(self) -> int:
        entity_count = 0
        for layer in self.layers.values():
            entity_count += layer.get_entity_count()
        return entity_count

    def add_component(self, entity: Entity, component: Component) -> None:
        if entity:
            entity.add_component(component)

    def get_component(self, entity: Entity, component_type: type[Component]) -> Component | None:
        if entity:
            return entity.get_component(component_type) # type: ignore
        return None

    def get_type_name(self):
        return "EntityManager"

    def notify(self, event_id, *args, **kwargs):
        print(f"EntityManager received event: {event_id}")
        return super().notify(event_id, *args, **kwargs)
    
    def process_queues(self):
        for layer in self.layers.values():
            layer.process_queues()
