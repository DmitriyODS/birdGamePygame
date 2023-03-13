from random import Random

import pygame.image
from pygame import Surface
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, screen_size: tuple[int, int]):
        super().__init__()
        self.screen_size = screen_size

        self.image = pygame.image.load('./src/bird.png')
        self.image = pygame.transform.scale(self.image, (64, 48))
        self.rect = self.image.get_rect()
        self.x, self.y = 16, 360
        self.rect.topleft = self.x, self.y
        self.mask = pygame.mask.from_surface(self.image)

        self.speed_x = 0
        self.speed_y = 1

    def reset(self):
        self.speed_x = 0
        self.speed_y = 1
        self.x, self.y = 16, 360

    def update(self):
        if self.speed_x != 0:
            self.x += self.speed_x
            if self.speed_x > 0:
                self.speed_x += 1
            else:
                self.speed_x -= 1

        self.y += self.speed_y
        if self.speed_y > 0:
            self.speed_y += 1
        else:
            self.speed_y -= 1

        if self.x < 0:
            self.x = 0
        if self.x > self.screen_size[0] - 64:
            self.x = self.screen_size[0] - 64
        if self.y < 0:
            self.y = 0
        if self.y > self.screen_size[1] - 48:
            self.y = self.screen_size[1] - 48

        self.rect.topleft = self.x, self.y

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)

    def set_move_left(self):
        if self.speed_x > -1:
            self.speed_x = -1

    def set_move_right(self):
        if self.speed_x < 1:
            self.speed_x = 1

    def set_move_up(self):
        if self.speed_y > -1:
            self.speed_y = -1

    def set_move_down(self):
        if self.speed_y < 1:
            self.speed_y = 1

    def set_stop_move_x(self):
        self.speed_x = 0
