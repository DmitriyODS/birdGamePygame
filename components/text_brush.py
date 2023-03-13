import pygame

FONT_PATH = "./src/font.ttf"


class TextBrush:
    def __init__(self, size=24, text='', color='black', pos=(0, 0)):
        self.is_render = True

        self.font_size = size
        self.text = text
        self.color = color
        self.font_pos = pos

        self.font = pygame.font.Font(FONT_PATH, self.font_size)

        self.rect = None
        self.surface_font = None

    def set_text(self, text):
        self.text = text
        self.is_render = True

    def set_color(self, color: str):
        self.color = pygame.Color(color)
        self.is_render = True

    def set_pos(self, pos: tuple[int, int]):
        self.font_pos = pos
        self.is_render = True

    def get_rect(self) -> pygame.rect.Rect:
        return self.surface_font.get_rect()

    def render(self):
        if self.is_render:
            self.surface_font = self.font.render(self.text, True, self.color)
            self.rect = self.surface_font.get_rect()
            self.rect.topleft = self.font_pos

            self.is_render = False

    def draw(self, screen: pygame.surface.Surface):
        self.render()
        screen.blit(self.surface_font, self.rect)
