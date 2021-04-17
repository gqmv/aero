import pygame
from random import randint
from objects import *
from settings import *


pygame.init()

WINDOW = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_NAME)


def draw(sprites: pygame.sprite.Group, gas_bar: Bar):
    """
    :param sprites: Group of stripes
    :param gas_bar: The gas bar that will be drawn

    This function renders all sprites, bars and borders.
    """
    WINDOW.fill(BACKGROUND_COLOR)
    sprites.draw(WINDOW)

    # Draws the border
    pygame.draw.rect(
        WINDOW,
        WHITE_COLOR,
        (
            BORDER_MARGIN_SIDES,
            BORDER_MARGIN_TOP_BOTTOM,
            SCREEN_SIZE[0] - 2 * BORDER_MARGIN_SIDES,
            SCREEN_SIZE[1] - 2 * BORDER_MARGIN_TOP_BOTTOM,
        ),
        BORDER_WIDTH,
    )

    gas_bar.draw(WINDOW)


def check_collision(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    """
    :param sprite: Sprite that will be used for collision checking
    :param group: The group of sprites that will be checked
    :return: bool

    This function checks if any sprites from group collide with sprite. If so, returns True. Otherwise, returns False.
    """
    if len(pygame.sprite.spritecollide(sprite, group, dokill=True)):
        return True
    return False


def generate_gas(sprites: pygame.sprite.Group, gas_cans: pygame.sprite.Group):
    """
    :param sprites: The sprite group that contains all sprites
    :param gas_cans: The sprite group that contains all gas cans

    This function generates a gas can if a random integer between 1 and 1000 is smaller than the GAS_SPAWN_CHANCE
    constant, defined at settings.py.
    The gas can has the following coordinates:
    x: A random integer within the bordered area.
    y: The top of the bordered area.
    """
    if randint(1, 1000) < GAS_SPAWN_CHANCE:
        Object(
            GAS_ASSET,
            randint(
                BORDER_MARGIN_SIDES + BORDER_WIDTH,
                SCREEN_SIZE[0] - BORDER_WIDTH - BORDER_MARGIN_SIDES,
            ),
            BORDER_MARGIN_TOP_BOTTOM + BORDER_WIDTH,
            sprites,
            gas_cans,
        )


def move_gas(gas_cans: pygame.sprite.Group):
    """
    :param gas_cans: The sprite group that contains all sprites

    This function moves all gas cans (stored at gas_cans) SCROLL_SPEED pixels down.
    """
    for can in gas_cans:
        can.y += SCROLL_SPEED

        if can.y >= SCREEN_SIZE[1] - BORDER_MARGIN_TOP_BOTTOM - BORDER_WIDTH - can.rect.height:
            can.kill()


def game_loop():
    """
    This function is the main game loop.
    """
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

        plane.handle_movement(mouse)

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
