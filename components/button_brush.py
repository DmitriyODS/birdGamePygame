from enum import IntEnum

import pygame

from components.text_brush import TextBrush


def get_new_size(font_size: tuple[int, int]) -> tuple[int, int]:
    w = font_size[0] + 32
    h = font_size[1] + 32

    return w, h


class ButtonEvents(IntEnum):
    CLICK = pygame.event.custom_type()


class ButtonStates(IntEnum):
    STATE_NORMAL = 1
    STATE_HOVER = 2
    STATE_PRESSED = 3
    STATE_DISABLED = 4


class ButtonBrush:
    def __init__(self, btn_id: int, size_w: int, text: str, foreground: any, background: any,
                 pos: tuple[int, int] = (0, 0)):
        self.cur_state: ButtonStates = ButtonStates.STATE_NORMAL
        self.is_render = True
        self.btn_id = btn_id

        self.pos = pos
        self.size_w = size_w
        self.text = text
        self.foreground = {ButtonStates.STATE_NORMAL: foreground, ButtonStates.STATE_HOVER: foreground,
                           ButtonStates.STATE_PRESSED: foreground, ButtonStates.STATE_DISABLED: foreground}
        self.background = {ButtonStates.STATE_NORMAL: background, ButtonStates.STATE_HOVER: background,
                           ButtonStates.STATE_PRESSED: background, ButtonStates.STATE_DISABLED: background}

        self.btn_text = TextBrush(self.size_w, color=self.foreground[self.cur_state])
        self.surface_btn = None
        self.rect: pygame.rect.Rect | None = None

        self.render()

    def new_event_click_button(self) -> pygame.event.Event:
        return pygame.event.Event(ButtonEvents.CLICK, {"btn_id": self.btn_id})

    def processing_hover(self, mouse_pos: tuple[int, int]):
        if self.cur_state == ButtonStates.STATE_DISABLED:
            return

        if self.cur_state == ButtonStates.STATE_PRESSED:
            return

        if self.rect.collidepoint(mouse_pos):
            self.set_state_hover()
        else:
            self.set_state_normal()

    def processing_press(self, mouse_pos: tuple[int, int]):
        if self.cur_state == ButtonStates.STATE_DISABLED:
            return

        if self.rect.collidepoint(mouse_pos):
            self.set_state_pressed()

    def processing_unpressed(self, mouse_pos: tuple[int, int]):
        if self.cur_state != ButtonStates.STATE_PRESSED:
            return

        if self.rect.collidepoint(mouse_pos):
            pygame.event.post(self.new_event_click_button())

        self.cur_state = ButtonStates.STATE_NORMAL
        self.processing_hover(mouse_pos)

    def set_state_normal(self):
        self.cur_state = ButtonStates.STATE_NORMAL
        self.is_render = True

    def set_state_hover(self):
        self.cur_state = ButtonStates.STATE_HOVER
        self.is_render = True

    def set_state_pressed(self):
        self.cur_state = ButtonStates.STATE_PRESSED
        self.is_render = True

    def set_state_disabled(self):
        if self.cur_state == ButtonStates.STATE_DISABLED:
            return

        self.cur_state = ButtonStates.STATE_DISABLED
        self.is_render = True

    def set_text(self, text):
        self.text = text
        self.is_render = True

    def set_color_normal(self, foreground, background):
        self.foreground[ButtonStates.STATE_NORMAL] = foreground
        self.background[ButtonStates.STATE_NORMAL] = background
        self.is_render = True

    def set_color_hover(self, foreground, background):
        self.foreground[ButtonStates.STATE_HOVER] = foreground
        self.background[ButtonStates.STATE_HOVER] = background
        self.is_render = True

    def set_color_pressed(self, foreground, background):
        self.foreground[ButtonStates.STATE_PRESSED] = foreground
        self.background[ButtonStates.STATE_PRESSED] = background
        self.is_render = True

    def set_color_disabled(self, foreground, background):
        self.foreground[ButtonStates.STATE_DISABLED] = foreground
        self.background[ButtonStates.STATE_DISABLED] = background
        self.is_render = True

    def get_pos_text(self) -> tuple[int, int]:
        return self.pos[0] + 16, self.pos[1] + 16

    def set_pos(self, pos: tuple[int, int]):
        self.pos = pos
        self.is_render = True

    def render(self):
        if self.is_render:
            self.btn_text.set_text(self.text)
            self.btn_text.set_pos(self.get_pos_text())
            self.btn_text.set_color(self.foreground[self.cur_state])
            self.btn_text.render()

            size = self.btn_text.get_rect().size
            self.rect = pygame.rect.Rect(self.pos, get_new_size(size))

            self.is_render = False

    def draw(self, screen: pygame.surface.Surface):
        self.render()
        pygame.draw.rect(screen, self.background[self.cur_state], self.rect, 4)
        self.btn_text.draw(screen)
