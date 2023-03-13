from enum import IntEnum

import pygame
from pygame import Surface
from pygame.event import Event

from components.button_brush import ButtonBrush
from components.text_brush import TextBrush
from globals.colors import Colors
from models.score import Score
from pages.abstract_page import AbstractPage, Props
from state.state import new_event_change_page, Pages


class ButtonIDs(IntEnum):
    NEW_GAME = 1
    MAIN_MENU = 2


class GameOver(AbstractPage):
    def __init__(self, display_size: tuple[int, int], props: Props):
        self.rand_gen = props.rand_gen
        self.display_size = display_size
        self.state = props.state
        self.store = props.store

        self.left_move_title = True
        self.pos_x_title = 460

        self.title = TextBrush(64, "GameOver", Colors.FOREGROUND, (self.pos_x_title, 48))
        self.score_title = TextBrush(48, f"Счёт: {self.state.get_score()}", Colors.FOREGROUND, (self.pos_x_title, 164))

        self.buttons = []
        self.init_buttons()

        self.main_sound = pygame.mixer.Sound('./src/game_over.mp3')

    def init_buttons(self):
        h = 256
        back_btn = ButtonBrush(ButtonIDs.NEW_GAME, 42, "Новая игра", Colors.FOREGROUND, Colors.NORMAL, (460, h))
        back_btn.set_color_hover(Colors.FOREGROUND, Colors.HOVER)
        back_btn.set_color_pressed(Colors.PRESSED, Colors.PRESSED)
        back_btn.set_color_disabled(Colors.DISABLED, Colors.DISABLED)
        self.buttons.append(back_btn)

        h += 128
        back_btn = ButtonBrush(ButtonIDs.MAIN_MENU, 42, "Главное меню", Colors.FOREGROUND, Colors.NORMAL, (460, h))
        back_btn.set_color_hover(Colors.FOREGROUND, Colors.HOVER)
        back_btn.set_color_pressed(Colors.PRESSED, Colors.PRESSED)
        back_btn.set_color_disabled(Colors.DISABLED, Colors.DISABLED)
        self.buttons.append(back_btn)

    def move_title(self):
        if self.pos_x_title < 64:
            self.left_move_title = False
        elif self.pos_x_title > 800:
            self.left_move_title = True

        if self.left_move_title:
            self.pos_x_title -= 8
        else:
            self.pos_x_title += 8

    def draw(self, screen: Surface):
        self.title.draw(screen)
        self.score_title.draw(screen)
        for i in range(len(self.buttons)):
            self.buttons[i].draw(screen)

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
            case ButtonIDs.NEW_GAME:
                pygame.event.post(new_event_change_page(Pages.MainScene, True))
            case ButtonIDs.MAIN_MENU:
                pygame.event.post(new_event_change_page(Pages.MainMenu, True))

    def reset(self):
        self.store.add_score(Score(score=self.state.get_score()))
        self.score_title.set_text(f"Счёт: {self.state.get_score()}")
        self.main_sound.play()
