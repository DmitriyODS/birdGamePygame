from random import Random

import pygame as pg
import pygame.mixer
from pygame.event import Event

from components.button_brush import ButtonEvents
from layouts.background_layout import BackgroundLayout
from pages.abstract_page import AbstractPage, Props
from pages.game_over import GameOver
from pages.main_menu import MainMenu
from pages.main_scene import MainScene
from pages.records import Records
from state.state import State, Pages, StateEvents

NAME_GAME = "BirdGame"
MAX_FPS = 30


def init_pygame():
    pg.init()
    pg.display.set_caption(NAME_GAME)


def init_events():
    pg.event.set_allowed([pg.KEYDOWN,
                          pg.KEYUP,
                          pg.MOUSEMOTION,
                          pg.MOUSEBUTTONUP,
                          pg.MOUSEBUTTONDOWN,
                          pg.QUIT,
                          ButtonEvents.CLICK,
                          StateEvents.CHANGE_PAGE])


def init_cursor():
    img_cursor = pg.image.load("./src/cursor.png")
    img_cursor = pg.transform.scale(img_cursor, (40, 40))
    new_cur = pg.cursors.Cursor((0, 0), img_cursor)
    pg.mouse.set_cursor(new_cur)


def init_sound():
    pass


class App:
    app = None

    def __new__(cls, *args, **kwargs):
        if cls.app is None:
            cls.app = super().__new__(cls)
        return cls.app

    def __init__(self, store):
        self.rand_gen = Random()
        self.store = store
        self.state = State()
        self.is_run = True
        self.display_size = (1280, 720)
        self.width, self.height = self.display_size

        init_pygame()
        init_events()
        init_cursor()

        self.main_screen = pg.display.set_mode(self.display_size)
        self.clock = pg.time.Clock()

        props = Props(self.state, self.store, self.rand_gen)
        self.pages: map[Pages: AbstractPage] = {
            Pages.MainMenu: MainMenu(self.display_size, props),
            Pages.MainScene: MainScene(self.display_size, props),
            Pages.Records: Records(self.display_size, props),
            Pages.GameOver: GameOver(self.display_size, props)
        }

        self.background_layout = BackgroundLayout(self.display_size, self.rand_gen)

    def quit_game(self):
        self.is_run = False

    def processing_keydown(self, event: Event):
        self.pages[self.state.get_cur_page()].processing_keydown(event)

    def processing_keyup(self, event: Event):
        self.pages[self.state.get_cur_page()].processing_keyup(event)

    def mouse_motion(self, event: Event):
        self.pages[self.state.get_cur_page()].mouse_motion(event)

    def mouse_button_down(self, event: Event):
        self.pages[self.state.get_cur_page()].mouse_button_down(event)

    def mouse_button_up(self, event: Event):
        self.pages[self.state.get_cur_page()].mouse_button_up(event)

    def click_button(self, event: Event):
        self.pages[self.state.get_cur_page()].click_button(event)

    def change_page(self, event: Event):
        self.state.set_cur_page(event.page)
        if event.reset:
            self.pages[self.state.get_cur_page()].reset()

    def processing_events(self):
        for event in pg.event.get():
            match event.type:
                case pg.KEYDOWN:
                    self.processing_keydown(event)
                case pg.KEYUP:
                    self.processing_keyup(event)
                case pg.MOUSEMOTION:
                    self.mouse_motion(event)
                case pg.MOUSEBUTTONDOWN:
                    self.mouse_button_down(event)
                case pg.MOUSEBUTTONUP:
                    self.mouse_button_up(event)
                case ButtonEvents.CLICK:
                    self.click_button(event)
                case StateEvents.CHANGE_PAGE:
                    self.change_page(event)
                case pg.QUIT:
                    self.quit_game()
                    return

    def render(self):
        self.background_layout.update()
        self.pages[self.state.get_cur_page()].render()

    def draw(self):
        self.background_layout.draw(self.main_screen)
        self.pages[self.state.get_cur_page()].draw(self.main_screen)

    def run(self):
        while self.is_run:
            self.clock.tick(MAX_FPS)

            self.processing_events()
            self.render()
            self.draw()

            pg.display.update()

    def __del__(self):
        pg.quit()
