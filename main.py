import pygame
from random import randint
from objects import *
from settings import *


pygame.init()

WINDOW = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_NAME)


def draw(all_sprites, gas_bar):
    WINDOW.fill(BACKGROUND_COLOR)
    all_sprites.draw(WINDOW)

    pygame.draw.rect(
        WINDOW,
        WHITE_COLOR,
        (
            BORDER_MARGIN_SIDES,
            BORDER_MARGIN_TOP,
            SCREEN_SIZE[0] - 2 * BORDER_MARGIN_SIDES,
            SCREEN_SIZE[1] - 2 * BORDER_MARGIN_TOP,
        ),
        BORDER_WIDTH,
    )

    gas_bar.draw(WINDOW)


def check_collision(sprite, group):
    if len(pygame.sprite.spritecollide(sprite, group, dokill=True)):
        return True
    return False


def generate_gas(sprites, gas_cans):
    if randint(1, 1000) < GAS_SPAWN_CHANCE:
        Object(
            GAS_ASSET,
            randint(
                BORDER_MARGIN_SIDES + BORDER_WIDTH,
                SCREEN_SIZE[0] - BORDER_WIDTH - BORDER_MARGIN_SIDES,
            ),
            BORDER_MARGIN_TOP + BORDER_WIDTH,
            sprites,
            gas_cans,
        )


def move_gas(gas_cans):
    for can in gas_cans:
        can.y += 5

        if can.y >= SCREEN_SIZE[1] - BORDER_MARGIN_TOP:
            can.kill


def game_loop():
    loop = True
    clock = pygame.time.Clock()

    gas_bar = Bar(10, 80, 25, 400, 1)
    gas_cans = pygame.sprite.Group()

    sprites = pygame.sprite.Group()

    plane = Plane(
        PLANE_ASSET,
        PLANE_ASSET,
        PLANE_ASSET,
        SCREEN_SIZE[0] / 2,
        SCREEN_SIZE[1] - 200,
        sprites,
    )

    while loop:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                loop = False
                break

        mouse = pygame.mouse.get_pos()

        plane.movement(mouse)

        generate_gas(sprites, gas_cans)
        move_gas(gas_cans)

        if plane.gas >= GAS_CONS_PER_FRAME:
            plane.gas -= GAS_CONS_PER_FRAME

        if check_collision(plane, gas_cans):
            plane.gas += GAS_PER_CAN

            if plane.gas > 1:
                plane.gas = 1

        gas_bar.percentage = plane.gas
        draw(sprites, gas_bar)

        pygame.display.update()


if __name__ == "__main__":
    game_loop()
