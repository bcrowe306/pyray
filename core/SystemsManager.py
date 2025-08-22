from core.EntityManager import EntityManager
from core.GameContext import GameContext
from core.System import System


class SystemsManager:
    def __init__(self):
        self.systems: list[System] = []

    def add_system(self, system: System):
        self.systems.append(system)

    def input(self, context: GameContext, em: EntityManager):
        for system in self.systems:
            system.input(context, em)

    def update(self, context: GameContext, em: EntityManager):
        for system in self.systems:
            system.update(context, em)

    def render(self, context: GameContext, em: EntityManager):
        for system in self.systems:
            system.render(context, em)