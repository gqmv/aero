import pygame
from random import randint
from objects import *
from settings import *
from menu import *

ticks = 0

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
    :param cls: The class of the object that will be generated
    :param asset: The asset of the object that will be generated
    :param spawn_chance: A number between 1-1000 that will define the spawn chance
    :param groups: The sprite groups that the object should be added to

    This function generates a object if a random integer between 1 and 1000 is smaller than the spawn_chance
    The object has the following coordinates:
    x: A random integer within the bordered area.
    y: The top of the bordered area.
    """
    if randint(1, 1000) < spawn_chance:
        cls(
            asset,
            randint(
                BORDER_MARGIN_SIDES + BORDER_WIDTH,
                SCREEN_SIZE[0] - BORDER_WIDTH - BORDER_MARGIN_SIDES - 55,
            ),
            BORDER_MARGIN_TOP_BOTTOM + BORDER_WIDTH,
            *groups
        )
        return True
    return False


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


def shoot(sprites: pygame.sprite.Group, enemies: pygame.sprite.Group, bullets: pygame.sprite.Group):
    global ticks
    ticks += 1
    for enemy in enemies:
        if ticks >= 30:
            Bullets(
                BULLET_ASSET,
                (enemy.x + enemy.rect.width / 2) - 2,
                enemy.rect.bottom,
                sprites,
                bullets
            )
            ticks = 0

    for bullet in bullets:
        bullet.y += BULLETS_SPEED

        if bullet.y >= SCREEN_SIZE[1] - BORDER_MARGIN_TOP_BOTTOM - BORDER_WIDTH - bullet.rect.height:
            bullet.kill()


def animation(sprites: pygame.sprite.Group, name: str, ticks: int, frames: int):
    for sprite in sprites:
        sprite.tick += 1
        if sprite.tick == ticks:
            sprite.tick = 0
            sprite.frame += 1
        if sprite.frame == frames:
            sprite.frame = 1
        sprite.image = pygame.image.load('assets/'f'{name}'f'{str(sprite.frame)}''.png')


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

    background = pygame.sprite.Group()
    gas_cans = pygame.sprite.Group()
    water_cans = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    missiles = pygame.sprite.Group()

    menu = Menu("assets/menu.png")
    gameover = GameOver("assets/gameover.png")

    bg = Object(
        BACKGROUND_ASSET,
        0,
        0,
        sprites,
        background
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
            shoot(sprites, enemies, bullets)
            generate_item(Missiles, MISSILE_ASSET, MISSILE_SPAWN_CHANCE, missiles, sprites)
            move_sprites(missiles)
            animation(background, 'bg', 10, 4)

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

            # Collisions between plane and missiles

            if check_collision(plane, missiles):
                plane.gas -= GAS_PER_CAN * 3
                plane.temperature += COOLING_PER_CAN * 3

                if plane.gas <= 0:
                    plane.gas = 0

                if plane.temperature >= 1:
                    plane.temperature = 1

            if plane.gas <= 0.0005 or plane.temperature >= 1:
                change_scene = True
                gas_cans.empty()
                water_cans.empty()
                enemies.empty()
                sprites.empty()
                bullets.empty()

                bg = Object(
                    BACKGROUND_ASSET,
                    0,
                    0,
                    sprites,
                    background
                )

                plane = Plane(
                    PLANE_ASSET,
                    PLANE_ASSET,
                    PLANE_ASSET,
                    SCREEN_SIZE[0] / 2,
                    SCREEN_SIZE[1] - 200,
                    sprites,
                )

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
