from random import Random

import pygame.image
from pygame.sprite import Sprite


class CloudSprite(Sprite):
    def __init__(self, screen_size: tuple[int, int], rand_gen: Random):
        super().__init__()
        self.rand_gen = rand_gen
        self.screen_size = screen_size
        self.speed_x = 0

        self.image = pygame.image.load('./src/cloud.png')
        self.image = pygame.transform.scale(self.image, (300, 200))
        self.rect = self.image.get_rect()

        self.x, self.y = 0, 0
        self.gen_new_pos()

    def gen_new_pos(self):
        self.x = self.screen_size[0]
        self.y = self.rand_gen.randint(- (self.rect.size[1] // 2), self.screen_size[1] - (self.rect.size[1] // 2))
        self.speed_x = self.rand_gen.randint(2, 8)

    def update(self):
        if self.x < -self.rect.size[0]:
            self.gen_new_pos()
        else:
            self.x -= self.speed_x

        self.rect.topleft = self.x, self.y
