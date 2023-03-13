from enum import IntEnum

import pygame.sprite
from pygame.surface import Surface
from pygame.event import Event

from components.button_brush import ButtonBrush
from components.text_brush import TextBrush
from pages.abstract_page import AbstractPage, Props
from globals.colors import Colors
from state.state import new_event_change_page, Pages


class ButtonIDs(IntEnum):
    RESUME = 1
    NEW_GAME = 2
    RECORDS = 3
    EXIT = 4


class MainMenu(AbstractPage):
    def __init__(self, display_size: tuple[int, int], props: Props):
        self.rand_gen = props.rand_gen
        self.display_size = display_size
        self.state = props.state
        self.store = props.store

        self.left_move_title = True
        self.pos_x_title = 460

        self.title = TextBrush(64, "BirdGame", Colors.FOREGROUND, (self.pos_x_title, 48))

        self.buttons = []
        self.init_buttons()

        self.main_sound = pygame.mixer.Sound('./src/sound.mp3')
        self.main_sound.play(-1)

    def init_buttons(self):
        self.buttons = [
            ButtonBrush(ButtonIDs.RESUME, 42, "Продолжить", Colors.FOREGROUND, Colors.NORMAL),
            ButtonBrush(ButtonIDs.NEW_GAME, 42, "Новая игра", Colors.FOREGROUND, Colors.NORMAL),
            ButtonBrush(ButtonIDs.RECORDS, 42, "Рекорды", Colors.FOREGROUND, Colors.NORMAL),
            ButtonBrush(ButtonIDs.EXIT, 42, "Выйти", Colors.FOREGROUND, Colors.NORMAL)
        ]

        h = 164
        for i in range(len(self.buttons)):
            self.buttons[i].set_color_hover(Colors.FOREGROUND, Colors.HOVER)
            self.buttons[i].set_color_pressed(Colors.PRESSED, Colors.PRESSED)
            self.buttons[i].set_color_disabled(Colors.DISABLED, Colors.DISABLED)

            self.buttons[i].set_pos((460, h))
            h += 128

        self.buttons[0].set_state_disabled()

    def draw(self, screen: Surface):
        self.title.draw(screen)
        for i in range(len(self.buttons)):
            self.buttons[i].draw(screen)

    def move_title(self):
        if self.pos_x_title < 64:
            self.left_move_title = False
        elif self.pos_x_title > 800:
            self.left_move_title = True

        if self.left_move_title:
            self.pos_x_title -= 8
        else:
            self.pos_x_title += 8

    def render(self):
        self.move_title()

        self.title.set_pos((self.pos_x_title, 48))
        self.title.render()

        for i in range(len(self.buttons)):
            self.buttons[i].render()

    def processing_keydown(self, event: Event):
        pass

    def processing_keyup(self, event: Event):
        pass

    def mouse_motion(self, event: Event):
        for i in range(len(self.buttons)):
            self.buttons[i].processing_hover(event.pos)

    def mouse_button_down(self, event: Event):
        for i in range(len(self.buttons)):
            self.buttons[i].processing_press(event.pos)

    def mouse_button_up(self, event: Event):
        for i in range(len(self.buttons)):
            self.buttons[i].processing_unpressed(event.pos)

    def click_button(self, event: Event):
        match event.btn_id:
            case ButtonIDs.RESUME:
                pygame.event.post(new_event_change_page(Pages.MainScene, False))
            case ButtonIDs.NEW_GAME:
                pygame.event.post(new_event_change_page(Pages.MainScene, True))
            case ButtonIDs.RECORDS:
                pygame.event.post(new_event_change_page(Pages.Records, True))
            case ButtonIDs.EXIT:
                pygame.event.post(Event(pygame.QUIT))

    def reset(self):
        if self.state.game_is_run:
            self.title.set_text("Пауза")
            self.buttons[0].set_state_normal()
        else:
            self.title.set_text("BirdGame")
            self.buttons[0].set_state_disabled()
