from enum import IntEnum

import pygame


class StateEvents(IntEnum):
    CHANGE_PAGE = pygame.event.custom_type()


class Pages(IntEnum):
    MainMenu = 1
    MainScene = 2
    Records = 3
    GameOver = 4


def new_event_change_page(page: Pages, reset: bool) -> pygame.event.Event:
    return pygame.event.Event(StateEvents.CHANGE_PAGE, {"page": page, "reset": reset})


class State:
    def __init__(self):
        self._ping: bool = False
        self._cur_page: Pages = Pages.MainMenu
        self.game_is_run: bool = False
        self._cur_score = 0
        self._view_score = 0
        self._heart_count = 3

    def get_heart_count(self):
        return self._heart_count

    def add_heart(self):
        if self._heart_count < 3:
            self._heart_count += 1

    def del_heart(self):
        if self._heart_count > 0:
            self._heart_count -= 1

    def get_score(self):
        return self._view_score

    def get_system_score(self):
        return self._cur_score

    def reset_score(self):
        self._cur_score = 0
        self._view_score = 0
        self._heart_count = 3

    def add_score(self):
        self._cur_score += 1
        self._view_score = self._cur_score // 2

    def get_cur_page(self):
        return self._cur_page

    def set_cur_page(self, page: Pages):
        self._cur_page = page

    def set_ping(self):
        self._ping = True

    def unset_ping(self):
        self._ping = False

    def is_ping(self) -> bool:
        return self._ping
