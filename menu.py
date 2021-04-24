import pygame
from objects import Object
from settings import *


def menu(win):
    sprites = pygame.sprite.Group()
    background = Object(MENU_ASSET, 0, 0, sprites)
    press_key_text = Object(KEY_ASSET, 0, 600, sprites)
    water = Object(MENU_WATER, 0, 550, sprites)

    tick = 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        tick += 1

        if tick == 70:
            press_key_text.kill()
        elif tick >= 120:
            tick = 0
            press_key_text = Object(KEY_ASSET, 0, 600, sprites)

        sprites.draw(win)
        pygame.display.update()


def game_over(win, score):
    sprites = pygame.sprite.Group()
    text = Object(GAMEOVER_ASSET, 0, 0, sprites)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        sprites.draw(win)
        pygame.display.update()