from core.GameContext import GameContext
from core.EntityManager import EntityManager

from abc import ABC, abstractmethod


class System(ABC):

    def input(self, context: GameContext, em: EntityManager):
        pass

    @abstractmethod
    def update(self, context: GameContext, em: EntityManager):
        pass

    def render(self, context: GameContext, em: EntityManager):
        pass