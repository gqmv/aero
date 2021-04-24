import pygame
from menus import *
from game import *


if __name__ == "__main__":
    pygame.init()

    WINDOW = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_NAME)

    result = menu(WINDOW)

    while True:

        result = game_loop(WINDOW)
        if result == pygame.QUIT:
            break

        result = game_over(WINDOW, result)
        if result == pygame.QUIT:
            break
