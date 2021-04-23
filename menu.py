import pygame
from objects import Object
from settings import *


class Menu:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.key_group = pygame.sprite.Group()
        self.image = Object(MENU_ASSET, 0, 0, self.all_sprites)
        self.key = Object(KEY_ASSET, 0, 600, self.key_group)
        self.menu_water = Object(MENU_WATER, 0, 550, self.all_sprites)
        self.change_scene = False
        self.tick = 0

    def draw(self, window):
        self.all_sprites.draw(window)
        self.key_group.draw(window)

    def animation(self):
        self.tick += 1
        if self.tick <= 45:
            self.key = Object(KEY_ASSET, 0, 600, self.key_group)
        else:
            if self.tick > 90:
                self.tick = 0
            self.key_group.empty()

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.change_scene = True


class GameOver:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.image = Object(GAMEOVER_ASSET, 0, 0, self.all_sprites)
        self.change_scene = False

    def draw(self, window):
        self.all_sprites.draw(window)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.change_scene = True
