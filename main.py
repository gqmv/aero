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
    :param sprites: Group of sprites
    :param gas_bar: The gas bar that will be drawn
    :param temp_bar: The temp_bar will be drawn
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
                SCREEN_SIZE[0] - BORDER_WIDTH - BORDER_MARGIN_SIDES - 55,
            ),
            BORDER_MARGIN_TOP_BOTTOM + BORDER_WIDTH,
            sprites,
            gas_cans,
        )


def generate_water(sprites: pygame.sprite.Group, water_cans: pygame.sprite.Group):
    """
    :param sprites: The sprite group that contains all sprites
    :param water_cans: The sprite group that contains all water cans

    This function generates a gas can if a random integer between 1 and 1000 is smaller than the WATER_SPAWN_CHANCE
    constant, defined at settings.py.
    The gas can has the following coordinates:
    x: A random integer within the bordered area.
    y: The top of the bordered area.
    """
    if randint(1, 1000) < WATER_SPAWN_CHANCE:
        Object(
            WATER_ASSET,
            randint(
                BORDER_MARGIN_SIDES + BORDER_WIDTH,
                SCREEN_SIZE[0] - BORDER_WIDTH - BORDER_MARGIN_SIDES - 55,
            ),
            BORDER_MARGIN_TOP_BOTTOM + BORDER_WIDTH,
            sprites,
            water_cans,
        )


def generate_enemy(sprites: pygame.sprite.Group, enemies: pygame.sprite.Group):
    """
    :param sprites: The sprite group that contains all sprites
    :param enemies: The sprite group that contains all enemies

    This function generates a gas can if a random integer between 1 and 1000 is smaller than the ENEMY_SPAWN_CHANCE
    constant, defined at settings.py.
    The gas can has the following coordinates:
    x: A random integer within the bordered area.
    y: The top of the bordered area.
    """
    if randint(1, 1000) < ENEMY_SPAWN_CHANCE:
        Enemy(
            ENEMY_ASSET,
            randint(
                BORDER_MARGIN_SIDES + BORDER_WIDTH,
                SCREEN_SIZE[0] - BORDER_WIDTH - BORDER_MARGIN_SIDES - 55,
            ),
            BORDER_MARGIN_TOP_BOTTOM + BORDER_WIDTH,
            sprites,
            enemies,
        )


def move_gas(gas_cans: pygame.sprite.Group):
    """
    :param gas_cans: The sprite group that contains gas sprites

    This function moves all gas cans (stored at gas_cans) SCROLL_SPEED pixels down.
    """
    for can in gas_cans:
        can.y += SCROLL_SPEED

        if can.y >= SCREEN_SIZE[1] - BORDER_MARGIN_TOP_BOTTOM - BORDER_WIDTH - can.rect.height:
            can.kill()


def move_water(water_cans: pygame.sprite.Group):
    """
    :param water_cans: The sprite group that contains gas sprites

    This function moves all water cans (stored at water_cans) SCROLL_SPEED pixels down.
    """
    for can in water_cans:
        can.y += SCROLL_SPEED

        if can.y >= SCREEN_SIZE[1] - BORDER_MARGIN_TOP_BOTTOM - BORDER_WIDTH - can.rect.height:
            can.kill()


def enemy_move_and_shoot(sprites: pygame.sprite.Group, enemies: pygame.sprite.Group, bullets: pygame.sprite.Group):
    """
    :param sprites: This group contains all sprites
    :param enemies: This group contains all enemies
    :param bullets: This group contains all bullets

    This function moves the generated enemies, bullets and define your shots.
    """
    # The ticks variable is a type of stopwatch to give regular time to enemy shots
    global TICKS
    TICKS += 1
    for enemy in enemies:
        enemy.y += SCROLL_SPEED

        if enemy.y >= SCREEN_SIZE[1] - BORDER_MARGIN_TOP_BOTTOM - BORDER_WIDTH - enemy.rect.height:
            enemy.kill()

        if TICKS >= 30:
            Bullets(
                BULLET_ASSET,
                (enemy.x + enemy.rect.width / 2) - 2,
                enemy.rect.bottom,
                sprites,
                bullets
            )
            TICKS = 0

    for bullet in bullets:
        bullet.y += BULLETS_SPEED

        if bullet.y >= SCREEN_SIZE[1] - BORDER_MARGIN_TOP_BOTTOM - BORDER_WIDTH - bullet.rect.height:
            bullet.kill()


def game_loop():
    """
    This function is the main game loop.
    """
    loop = True
    change_scene = False
    clock = pygame.time.Clock()

    gas_bar = Bar(10, 80, 25, 400, 1)
    temp_bar = Bar(560, 80, 25, 400, 1)
    gas_cans = pygame.sprite.Group()
    water_cans = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
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
            generate_gas(sprites, gas_cans)
            move_gas(gas_cans)
            generate_water(sprites, water_cans)
            move_water(water_cans)
            generate_enemy(sprites, enemies)
            enemy_move_and_shoot(sprites, enemies, bullets)

            # Decreasing the level of gasoline

            if plane.gas >= GAS_CONS_PER_FRAME:
                plane.gas -= GAS_CONS_PER_FRAME

            # Collisions between plane and gas cans

            if check_collision(plane, gas_cans):
                plane.gas += GAS_PER_CAN

                if plane.gas > 1:
                    plane.gas = 1

            # Increasing the temperature

            if plane.temp <= 1:
                plane.temp += WATER_CONS_PER_FRAME

            # Collisions between plane and water cans

            if check_collision(plane, water_cans):
                plane.temp -= WATER_PER_CAN

                if plane.temp <= 0:
                    plane.temp = 0

            # Collisions between plane and enemies

            if check_collision(plane, enemies):
                plane.gas = 0

                if plane.gas <= 0:
                    plane.gas = 0

            # Collisions between plane and bullets

            if check_collision(plane, bullets):
                plane.gas -= GAS_PER_CAN
                plane.temp += WATER_PER_CAN

                if plane.gas <= 0:
                    plane.gas = 0

                if plane.temp >= 1:
                    plane.temp = 1

            if plane.gas <= 0:
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
            temp_bar.percentage = plane.temp
            draw(sprites, gas_bar, temp_bar)

        elif not gameover.change_scene:
            gameover.all_sprites.draw(WINDOW)

        else:
            menu.change_scene = False
            change_scene = False
            gameover.change_scene = False
            plane.gas = 1
            plane.temp = 0

        pygame.display.update()


if __name__ == "__main__":
    game_loop()