import pygame.draw
from pygame import Surface

from components.text_brush import TextBrush
from globals.colors import Colors
from pages.abstract_page import Props


class InfoPanel:
    def __init__(self, display_size: tuple[int, int], props: Props):
        self.display_size = display_size
        self.props = props

        self.panel = Surface((self.display_size[0], 64))
        self.rect = self.panel.get_rect()
        self.rect.topleft = 0, self.display_size[1] - self.rect.size[1]

        self.score_text = TextBrush(48, f'Счёт: {self.props.state.get_score()}',
                                    Colors.FOREGROUND, (800, 8))

        self.heart = pygame.image.load('./src/heart.png')
        self.heart = pygame.transform.scale(self.heart, (48, 38))

    def render(self):
        self.panel.fill(Colors.NORMAL)
        self.score_text.set_text(f'Счёт: {self.props.state.get_score()}')
        self.score_text.draw(self.panel)

        x = 16
        for i in range(self.props.state.get_heart_count()):
            self.panel.blit(self.heart, (x, 13, 48, 38))
            x += 64

    def draw(self, screen: Surface):
        self.render()
        screen.blit(self.panel, self.rect)
