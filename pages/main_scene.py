import pygame
from pygame import Surface
from pygame.event import Event
from pygame.sprite import Group

from components.info_panel import InfoPanel
from pages.abstract_page import AbstractPage, Props
from sprites.airplane import Airplane
from sprites.heal import Heal
from sprites.player import Player
from state.state import new_event_change_page, Pages


class MainScene(AbstractPage):
    def __init__(self, display_size: tuple[int, int], props: Props):
        self.display_size = display_size
        self.props = props

        self.panel = InfoPanel(self.display_size, self.props)

        self.airplane_group = Group()
        self.init_airplanes()

        self.heals_group = Group()

        self.player = Player((self.display_size[0], self.display_size[1] - 64))

        self.sound_boom = pygame.mixer.Sound('./src/boom.mp3')
        self.sound_heap = pygame.mixer.Sound('./src/heap.mp3')

    def init_airplanes(self):
        self.airplane_group.empty()
        for i in range(3):
            new_airplane = Airplane(self.display_size, self.props.rand_gen)
            self.airplane_group.add(new_airplane)

    def gen_heals(self):
        if self.props.state.get_heart_count() < 3 and self.props.state.get_system_score() % 200 == 0:
            self.heals_group.add(Heal(self.display_size, self.props.rand_gen))

    def draw(self, screen: Surface):
        self.airplane_group.draw(screen)
        self.heals_group.draw(screen)
        self.panel.draw(screen)
        self.player.draw(screen)

    def render(self):
        res = pygame.sprite.spritecollide(self.player, self.airplane_group, True, pygame.sprite.collide_mask)
        if len(res) > 0:
            self.sound_boom.play()
            self.props.state.del_heart()

        res = pygame.sprite.spritecollide(self.player, self.heals_group, True, pygame.sprite.collide_mask)
        if len(res) > 0:
            self.sound_heap.play()
            self.props.state.add_heart()

        if self.props.state.get_heart_count() == 0:
            self.props.state.game_is_run = False
            pygame.event.post(new_event_change_page(Pages.GameOver, True))

        self.props.state.add_score()
        higher_speed = False
        if self.props.state.get_system_score() % 400 == 0:
            higher_speed = True
            new_airplane = Airplane(self.display_size, self.props.rand_gen)
            self.airplane_group.add(new_airplane)

        self.airplane_group.update(higher_speed)
        self.gen_heals()
        self.heals_group.update()
        self.player.update()

    def processing_keydown(self, event: Event):
        match event.key:
            case pygame.K_w | pygame.K_UP:
                self.player.set_move_up()
            case pygame.K_s | pygame.K_DOWN:
                self.player.set_move_down()
            case pygame.K_a | pygame.K_LEFT:
                self.player.set_move_left()
            case pygame.K_d | pygame.K_RIGHT:
                self.player.set_move_right()
            case pygame.K_ESCAPE:
                self.props.state.game_is_run = True
                pygame.event.post(new_event_change_page(Pages.MainMenu, True))

    def processing_keyup(self, event: Event):
        match event.key:
            case pygame.K_a | pygame.K_LEFT:
                self.player.set_stop_move_x()
            case pygame.K_d | pygame.K_RIGHT:
                self.player.set_stop_move_x()

    def mouse_motion(self, event: Event):
        pass

    def mouse_button_down(self, event: Event):
        pass

    def mouse_button_up(self, event: Event):
        pass

    def click_button(self, event: Event):
        pass

    def reset(self):
        self.props.state.reset_score()
        self.init_airplanes()
        self.heals_group.empty()
        self.player.reset()
