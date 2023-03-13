from abc import ABC, abstractmethod
from random import Random

from pygame.event import Event
from pygame.surface import Surface

from state.state import State
from store.store import Store


class Props:
    def __init__(self, state: State, store: Store, rand_int: Random):
        self.state: State = state
        self.store: Store = store
        self.rand_gen: Random = rand_int


class AbstractPage(ABC):
    @abstractmethod
    def draw(self, screen: Surface):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def processing_keydown(self, event: Event):
        pass

    @abstractmethod
    def processing_keyup(self, event: Event):
        pass

    @abstractmethod
    def mouse_motion(self, event: Event):
        pass

    @abstractmethod
    def mouse_button_down(self, event: Event):
        pass

    @abstractmethod
    def mouse_button_up(self, event: Event):
        pass

    @abstractmethod
    def click_button(self, event: Event):
        pass

    @abstractmethod
    def reset(self):
        pass
