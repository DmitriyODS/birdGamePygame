from random import Random

import pygame.image
from pygame.sprite import Sprite


class Heal(Sprite):
    def __init__(self, screen_size: tuple[int, int], rand_gen: Random):
        super().__init__()
        self.rand_gen = rand_gen
        self.screen_size = screen_size
        self.speed_x = 0
        self.speed_y = 0

        self.move_left = True

        self.image = pygame.image.load('./src/heal.png')
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.x, self.y = 0, 0
        self.gen_new_pos()

    def gen_new_pos(self):
        self.x = self.rand_gen.randint(16, self.screen_size[0])
        self.y = -self.rect.size[1]
        self.speed_x = self.rand_gen.randint(2, 8)
        self.speed_y = self.rand_gen.randint(4, 8)
        self.move_left = bool(self.rand_gen.randint(0, 1))

    def update(self):
        if self.x < -self.rect.size[0] or self.y > self.screen_size[1]:
            self.kill()
        else:
            if self.move_left:
                self.x -= self.speed_x
            else:
                self.x += self.speed_x

            self.y += self.speed_y

        self.rect.topleft = self.x, self.y
