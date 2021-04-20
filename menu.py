import pygame
from objects import Object


class Menu:
    def __init__(self, image):
        self.all_sprites = pygame.sprite.Group()
        self.image = Object(image, 0, 0, self.all_sprites)
        self.change_scene = False

    def draw(self, window):
        self.all_sprites.draw(window)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.change_scene = True


class GameOver(Menu):
    def __init__(self, image):
        super().__init__(image)