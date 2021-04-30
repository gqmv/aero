import pygame
from menus import *
from game import *
from pygame import mixer


if __name__ == "__main__":
    archive = "highscore.txt"
    if not check_archive(archive):
        create_archive(archive)

    pygame.init()

    WINDOW = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_NAME)
    mixer.music.load("sounds/game_music.wav")
    mixer.music.play(-1)

    if menu(WINDOW, archive) != pygame.QUIT:
        while True:
            result = game_loop(WINDOW)
            if result == pygame.QUIT:
                break
            else:
                update_archive(archive, int(result))

            result = game_over(WINDOW, result)
            if result == pygame.QUIT:
                break
