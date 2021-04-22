import pygame
from random import randint
from objects import *
from settings import *
from menu import *


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


def generate_item(cls: type, asset: str, spawn_chance: int, *groups: pygame.sprite.Group):
    """
    :param cls: The class fo the object that will be generated
    :param asset: The asset of the object that will be generated
    :param spawn_chance: A number between 1-1000 that will define the spawn chance
    :param groups: The sprite groups that the object should be added to

    This function generates a object if a random integer between 1 and 1000 is smaller than the spawn_chance
    The object has the following coordinates:
    x: A random integer within the bordered area.
    y: The top of the bordered area.
    """
    if randint(1, 1000) < spawn_chance:
        c = cls(
            asset,
            randint(
                BORDER_MARGIN_SIDES + BORDER_WIDTH,
                SCREEN_SIZE[0] - BORDER_WIDTH - BORDER_MARGIN_SIDES - 55,
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
    change_scene = False
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
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    menu = Menu("assets/menu.png")
    gameover = GameOver("assets/gameover.png")

    bg1 = Object(
        BACKGROUND_ASSET,
        0,
        0,
        sprites
    )

    bg2 = Object(
        BACKGROUND_ASSET,
        0,
        -750,
        sprites
    )

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

            if not menu.change_scene:
                menu.events(event)

            elif not change_scene:

                if event.type == pygame.MOUSEMOTION:
                    plane.x = pygame.mouse.get_pos()[0] - plane.rect.width / 2
                    plane.y = pygame.mouse.get_pos()[1] - plane.rect.height / 2

                    # Adding colisions with the edge

                    if plane.rect.right >= SCREEN_SIZE[0] - (BORDER_MARGIN_SIDES + BORDER_WIDTH):
                        plane.rect.right = SCREEN_SIZE[0] - (BORDER_MARGIN_SIDES + BORDER_WIDTH)

                    elif plane.rect.left <= (BORDER_MARGIN_SIDES + BORDER_WIDTH):
                        plane.rect.left = (BORDER_MARGIN_SIDES + BORDER_WIDTH)

                    if plane.rect.top <= BORDER_MARGIN_TOP_BOTTOM:
                        plane.rect.top = BORDER_MARGIN_TOP_BOTTOM

                    elif plane.rect.bottom >= SCREEN_SIZE[1] - BORDER_MARGIN_TOP_BOTTOM:
                        plane.rect.bottom = SCREEN_SIZE[1] - BORDER_MARGIN_TOP_BOTTOM

            else:
                gameover.events(event)

        if not menu.change_scene:
            menu.all_sprites.draw(WINDOW)

        elif not change_scene:
            generate_item(Object, GAS_ASSET, GAS_SPAWN_CHANCE, gas_cans, sprites)
            move_sprites(gas_cans)
            generate_item(Object, WATER_ASSET, WATER_SPAWN_CHANCE, water_cans, sprites)
            move_sprites(water_cans)
            generate_item(Enemy, ENEMY_ASSET, ENEMY_SPAWN_CHANCE, enemies, sprites)
            move_sprites(enemies)

            # Decreasing the level of gasoline

            if plane.gas >= GAS_CONS_PER_FRAME:
                plane.gas -= GAS_CONS_PER_FRAME

            # Collisions between plane and gas cans

            if check_collision(plane, gas_cans):
                plane.gas += GAS_PER_CAN

                if plane.gas > 1:
                    plane.gas = 1

            # Increasing the temperature

            if plane.temperature <= 1:
                plane.temperature += TEMP_CONS_PER_FRAME

            # Collisions between plane and water cans

            if check_collision(plane, water_cans):
                plane.temperature -= COOLING_PER_CAN

                if plane.temperature <= 0:
                    plane.temperature = 0

            # Collisions between plane and enemies

            if check_collision(plane, enemies):
                plane.gas = 0

                if plane.gas <= 0:
                    plane.gas = 0

            # Collisions between plane and bullets

            if check_collision(plane, bullets):
                plane.gas -= GAS_PER_CAN
                plane.temperature += COOLING_PER_CAN

                if plane.gas <= 0:
                    plane.gas = 0

                if plane.temperature >= 1:
                    plane.temperature = 1

            if plane.gas <= 0 or plane.temperature >= 1:
                change_scene = True
                gas_cans.empty()
                water_cans.empty()
                enemies.empty()
                sprites.empty()
                bullets.empty()

                bg1 = Object(
                    BACKGROUND_ASSET,
                    0,
                    0,
                    sprites
                )

                bg2 = Object(
                    BACKGROUND_ASSET,
                    0,
                    -750,
                    sprites
                )

                plane = Plane(
                    PLANE_ASSET,
                    PLANE_ASSET,
                    PLANE_ASSET,
                    SCREEN_SIZE[0] / 2,
                    SCREEN_SIZE[1] - 200,
                    sprites,
                )

            # Moving background

            bg1.y += 1
            bg2.y += 1
            if bg1.y >= 750:
                bg1.y = 0
            if bg2.y >= 0:
                bg2.y = -750

            gas_bar.percentage = plane.gas
            temp_bar.percentage = plane.temperature
            draw(sprites, gas_bar, temp_bar)

        elif not gameover.change_scene:
            gameover.all_sprites.draw(WINDOW)

        else:
            menu.change_scene = False
            change_scene = False
            gameover.change_scene = False
            plane.gas = 1
            plane.temperature = 0

        pygame.display.update()


if __name__ == "__main__":
    game_loop()
