from random import Random

import pygame
from pygame import Surface

from globals.colors import Colors
from sprites.cloud import CloudSprite


class BackgroundLayout:
    def __init__(self, display_size: tuple[int, int], rand_gen: Random):
        self.display_size = display_size
        self.rand_gen = rand_gen

        self.clouds_group = pygame.sprite.Group()
        self.init_clouds()

    def init_clouds(self):
        for i in range(self.rand_gen.randint(8, 24)):
            new_cloud = CloudSprite(self.display_size, self.rand_gen)
            self.clouds_group.add(new_cloud)

    def update(self):
        self.clouds_group.update()

    def draw(self, screen: Surface):
        screen.fill(Colors.BACKGROUND)
        self.clouds_group.draw(screen)
