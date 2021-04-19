import pygame
from random import randint
from objects import *
from settings import *


pygame.init()

WINDOW = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_NAME)


def draw(sprites: pygame.sprite.Group, gas_bar: Bar, temp_bar: Bar):
    """
    :param sprites: Group of stripes
    :param gas_bar: The gas bar that will be drawn
    :param temp_bar: The temp_bar that will be drawn
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
    temp_bar.draw(WINDOW)


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


def generate_item(asset: str, spawn_chance: int, *groups: pygame.sprite.Group):
    """
    :param asset: The asset of the object that will be generated
    :param spawn_chance: A number between 1-1000 that will define the spawn chance
    :param groups: The sprite groups that the object should be added to

    This function generates a object if a random integer between 1 and 1000 is smaller than the spawn_chance
    The object has the following coordinates:
    x: A random integer within the bordered area.
    y: The top of the bordered area.
    """
    if randint(1, 1000) < spawn_chance:
        Object(
            asset,
            randint(
                BORDER_MARGIN_SIDES + BORDER_WIDTH,
                SCREEN_SIZE[0] - BORDER_WIDTH - BORDER_MARGIN_SIDES,
            ),
            BORDER_MARGIN_TOP_BOTTOM + BORDER_WIDTH,
            *groups
        )


def move_sprites(sprites: pygame.sprite.Group):
    """
    :param sprites: The sprite group that contains all sprites

    This function moves all sprites SCROLL_SPEED pixels down.
    """
    for sprite in sprites:
        sprite.y += SCROLL_SPEED

        if (
            sprite.y
            >= SCREEN_SIZE[1]
            - BORDER_MARGIN_TOP_BOTTOM
            - BORDER_WIDTH
            - sprite.rect.height
        ):
            sprite.kill()


def game_loop():
    """
    This function is the main game loop.
    """
    loop = True
    clock = pygame.time.Clock()

    gas_bar = Bar(
        x=10, y=80, width=25, height=400, default_percentage=1, color=RED_COLOR
    )
    temp_bar = Bar(
        x=560, y=80, width=25, height=400, default_percentage=1, color=BLUE_COLOR
    )
    gas_cans = pygame.sprite.Group()
    water_cans = pygame.sprite.Group()
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

        generate_item(GAS_ASSET, GAS_SPAWN_CHANCE, gas_cans, sprites)
        move_sprites(gas_cans)
        generate_item(WATER_ASSET, WATER_SPAWN_CHANCE, water_cans, sprites)
        move_sprites(water_cans)

        if plane.gas >= GAS_CONS_PER_FRAME:
            plane.gas -= GAS_CONS_PER_FRAME

        if check_collision(plane, gas_cans):
            plane.gas += GAS_PER_CAN

            if plane.gas > 1:
                plane.gas = 1

        if plane.temperature <= 1:
            plane.temperature += TEMP_CONS_PER_FRAME

        if check_collision(plane, water_cans):
            plane.temperature -= COOLING_PER_CAN

            if plane.temperature <= 0:
                plane.temperature = 0

        gas_bar.percentage = plane.gas
        temp_bar.percentage = plane.temperature
        draw(sprites, gas_bar, temp_bar)

        pygame.display.update()


if __name__ == "__main__":
    game_loop()
