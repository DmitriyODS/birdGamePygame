import pygame
from pygame import Surface
from pygame.event import Event

from components.button_brush import ButtonBrush
from components.text_brush import TextBrush
from globals.colors import Colors
from pages.abstract_page import AbstractPage, Props
from state.state import Pages, new_event_change_page

BUTTON_ID_BACK = 1


class Records(AbstractPage):
    def __init__(self, display_size: tuple[int, int], props: Props):
        self.rand_gen = props.rand_gen
        self.display_size = display_size
        self.state = props.state
        self.store = props.store

        self.left_move_title = True
        self.pos_x_title = 460

        self.title = TextBrush(64, "Мои рекорды", Colors.FOREGROUND, (self.pos_x_title, 48))

        self.buttons = []
        self.init_buttons()

    def init_buttons(self):
        h = 164
        self.buttons = []
        scores = self.store.get_scores()
        for it in scores:
            self.buttons.append(ButtonBrush(0, 42, it.score_str(), Colors.FOREGROUND, Colors.NORMAL, (460, h)))
            h += 128

        back_btn = ButtonBrush(BUTTON_ID_BACK, 42, "Назад", Colors.FOREGROUND, Colors.NORMAL, (460, h))
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
        self.buttons[-1].processing_hover(event.pos)

    def mouse_button_down(self, event: Event):
        self.buttons[-1].processing_press(event.pos)

    def mouse_button_up(self, event: Event):
        self.buttons[-1].processing_unpressed(event.pos)

    def click_button(self, event: Event):
        if event.btn_id == BUTTON_ID_BACK:
            pygame.event.post(new_event_change_page(Pages.MainMenu, True))

    def reset(self):
        self.init_buttons()
