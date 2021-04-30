import pygame
from objects import *
from settings import *
from pygame import mixer


def menu(win, archive):
    state = 'start'
    sprites = pygame.sprite.Group()
    background = Object(MENU_ASSET, 0, 0, sprites)
    water = Object(MENU_WATER, 0, 550, sprites)
    start_key = Object(START_KEY_ASSET, 215, 550, sprites)
    highscore_key = Object(HIGHSCORE_KEY_ASSET, 215, 625, sprites)
    selector = Object(SELECTOR_ASSET, 190, 548, sprites)
    enter = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enter_sound = mixer.Sound('sounds/enter.wav')
                    enter_sound.play()
                    if state == 'start':
                        return True
                    else:
                        enter = True
                        highscore(win, archive)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selector_sound = mixer.Sound('sounds/selector_sound.wav')
                    selector_sound.play()
                    if state == 'start':
                        state = 'highscore'
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 623, sprites)

                    elif state == 'highscore':
                        state = 'start'
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 548, sprites)

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selector_sound = mixer.Sound('sounds/selector_sound.wav')
                    selector_sound.play()
                    if state == 'start':
                        state = 'highscore'
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 623, sprites)

                    elif state == 'highscore':
                        state = 'start'
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 548, sprites)

                elif event.key == pygame.K_ESCAPE:
                    enter_sound = mixer.Sound('sounds/enter.wav')
                    enter_sound.play()
                    if state == 'highscore':
                        state = 'start'
                        enter = False
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 548, sprites)

        if not enter:
            sprites.draw(win)
        pygame.display.update()


def game_over(win, score):
    state = 'restart'
    sprites = pygame.sprite.Group()
    background = Object(GAME_OVER_ASSET, 0, 0, sprites)
    restart_key = Object(RESTART_KEY_ASSET, 215, 550, sprites)
    restart_key.x = (SCREEN_SIZE[0] / 2) - (restart_key.rect.width / 2)
    quit_key = Object(QUIT_KEY_ASSET, 215, 625, sprites)
    quit_key.x = (SCREEN_SIZE[0] / 2) - (quit_key.rect.width / 2)
    selector = Object(SELECTOR_ASSET, 190, 548, sprites)
    enter = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enter_sound = mixer.Sound('sounds/enter.wav')
                    enter_sound.play()
                    if state == 'restart':
                        return True
                    else:
                        enter = True
                        return pygame.QUIT
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selector_sound = mixer.Sound('sounds/selector_sound.wav')
                    selector_sound.play()
                    if state == 'restart':
                        state = 'quit'
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 623, sprites)

                    elif state == 'quit':
                        state = 'restart'
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 548, sprites)

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selector_sound = mixer.Sound('sounds/selector_sound.wav')
                    selector_sound.play()
                    if state == 'restart':
                        state = 'quit'
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 623, sprites)

                    elif state == 'quit':
                        state = 'restart'
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 548, sprites)

                elif event.key == pygame.K_ESCAPE:
                    enter_sound = mixer.Sound('sounds/enter.wav')
                    enter_sound.play()
                    if state == 'quit':
                        state = 'quit'
                        enter = False
                        selector.kill()
                        selector = Object(SELECTOR_ASSET, 190, 548, sprites)

        if not enter:
            sprites.draw(win)
            text = Text(20, f"YOU SCORED {round(score)} POINTS", WHITE_COLOR)
            text.draw(win, (SCREEN_SIZE[0] / 2) - (text.render.get_width() / 2), 450)
        pygame.display.update()


def highscore(win, archive):
    sprites = pygame.sprite.Group()
    Object(HIGHSCORE_ASSET, 0, 0, sprites)
    sprites.draw(win)
    text = Text(60, 'Highscore', WHITE_COLOR)
    text.draw(win, SCREEN_SIZE[0]/2 - text.render.get_width()/2, 100)

    text = Text(60, update_archive(archive), WHITE_COLOR)
    text.draw(win, SCREEN_SIZE[0]/2 - text.render.get_width()/2, 300)

    text = Text(20, 'Press Esc to return', YELLOW_COLOR)
    text.draw(win, SCREEN_SIZE[0]/2 - text.render.get_width()/2, 550)


def check_archive(name):
    try:
        a = open(name, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def create_archive(name):
    a = open(name, 'wt+')
    a.write('0')
    a.close()


def update_archive(name, score=0):
    a = open(name, 'rt')
    number = a.read()
    if int(number) < score:
        a = open(name, 'w')
        a.write(str(score))
        number = str(score)
        a.close()
    a.close()
    return number