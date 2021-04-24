import pygame
from random import randint
from objects import *
from settings import *
from menu import *

pygame.init()

WINDOW = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(WINDOW_NAME)


def draw(sprites: pygame.sprite.Group, gas_bar: Bar, temp_bar: Bar, score: int):
    """
    :param sprites: Group of stripes
    :param gas_bar: The gas bar that will be drawn
    :param temp_bar: The temp_bar that will be drawn
    :param score: The current score
    This function renders all sprites, bars and borders.
    """
    WINDOW.fill(BACKGROUND_COLOR)
    sprites.draw(WINDOW)

    score_text = FONT.render(str(round(score)), True, WHITE_COLOR)
    WINDOW.blit(score_text, (SCREEN_SIZE[0] - score_text.get_width() - 20, 20))

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


def generate_item(
    cls: type, asset: str, spawn_chance: int, *groups: pygame.sprite.Group
):
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
        instance = cls(asset, 0, 0, *groups)

        instance.x = randint(0, SCREEN_SIZE[0] - instance.rect.width)


def move_sprites(sprites: pygame.sprite.Group):
    """
    :param sprites: The sprite group that contains all sprites

    This function moves all sprites SCROLL_SPEED pixels down.
    """
    for sprite in sprites:
        sprite.y += SCROLL_SPEED

        if sprite.y >= SCREEN_SIZE[1]:
            sprite.kill()


def shoot(enemies, bullets, *groups: pygame.sprite.Group):
    for enemy in enemies:
        enemy.tick += 1
        if enemy.tick >= 30:
            enemy.shoot(bullets, *groups)
            enemy.tick = 0

    for bullet in bullets:
        bullet.y += BULLETS_SPEED

        if bullet.y >= SCREEN_SIZE[1]:
            bullet.kill()


def animation(sprite: Object, ticks: int):
    sprite.tick += 1
    if sprite.tick == ticks:
        sprite.tick = 0

        sprite.image = pygame.transform.rotate(sprite.image, 180)


def find_angle(missiles: pygame.sprite.Group, player):
    missiles.update()
    for missile in missiles:
        lista = []
        for num in range(2):
            vec = player.rect.center[num] - missile.rect.center[num]
            lista.append(vec)
        vector = pygame.math.Vector2(lista[0], lista[1])
        clockwise = pygame.math.Vector2.angle_to(missile.direction, vector)
        if clockwise < 0:
            clockwise = 360 + clockwise
        anticlockwise = abs(360 - clockwise)
        if clockwise < anticlockwise:
            if clockwise > 10 or clockwise < -10:
                missile.angle_speed = 5
            else:
                missile.angle_speed = 0
        else:
            if anticlockwise > 10 or anticlockwise < -10:
                missile.angle_speed = -5
            else:
                missile.angle_speed = 0


def game_loop():
    """
    This function is the main game loop.
    """
    loop = True
    clock = pygame.time.Clock()

    gas_bar = Bar(
        x=60, y=10, width=250, height=25, default_percentage=1, color=RED_COLOR
    )
    temp_bar = Bar(
        x=60, y=40, width=250, height=25, default_percentage=1, color=BLUE_COLOR
    )

    gas_cans = pygame.sprite.Group()
    water_cans = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    missiles = pygame.sprite.Group()

    score = 0

    background = Object(BACKGROUND_ASSET, 0, 0, sprites)

    plane = Plane(
        PLANE_ASSET,
        SCREEN_SIZE[0] / 2,
        SCREEN_SIZE[1] - 200,
        sprites,
    )

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return pygame.QUIT

        score += SCORE_PER_SECOND / FPS

        mouse = pygame.mouse.get_pos()
        plane.movement(mouse)

        generate_item(Object, GAS_ASSET, GAS_SPAWN_CHANCE, gas_cans, sprites)
        move_sprites(gas_cans)
        generate_item(Object, WATER_ASSET, WATER_SPAWN_CHANCE, water_cans, sprites)
        move_sprites(water_cans)
        generate_item(Enemy, ENEMY_ASSET, ENEMY_SPAWN_CHANCE, enemies, sprites)
        move_sprites(enemies)
        shoot(enemies, bullets, sprites)
        generate_item(Missiles, MISSILE_ASSET, MISSILE_SPAWN_CHANCE, missiles, sprites)
        animation(background, 10)
        find_angle(missiles, plane)

        # Decreasing the level of gasoline

        plane.gas = max(plane.gas - GAS_CONS_PER_FRAME, 0)

        # Collisions between plane and gas cans

        if check_collision(plane, gas_cans):
            plane.gas = min(plane.gas + GAS_PER_CAN, 1)

        # Increasing the temperature

        plane.temperature = min(plane.temperature + TEMP_CONS_PER_FRAME, 1)

        # Collisions between plane and water cans

        if check_collision(plane, water_cans):
            plane.temperature = max(plane.temperature - COOLING_PER_CAN, 0)

        # Collisions between plane and enemies

        if check_collision(plane, enemies):
            return score

        # Collisions between plane and bullets

        if check_collision(plane, bullets):
            max(plane.gas - BULLET_GAS_DAMAGE, 0)
            plane.temperature = min(plane.temperature + BULLET_TEMP_DAMAGE, 1)


        # Collisions between plane and missiles

        if check_collision(plane, missiles):
            plane.gas = max(plane.gas - MISSILE_GAS_DAMAGE, 0)
            plane.temperature = min(plane.temperature + MISSILE_TEMP_DAMAGE, 1)

        # Loosing conditions

        if plane.gas <= 0 or plane.temperature >= 1:
            return score

        gas_bar.percentage = plane.gas
        temp_bar.percentage = plane.temperature
        draw(sprites, gas_bar, temp_bar, score)

        pygame.display.update()


if __name__ == "__main__":
    result = menu(WINDOW)

    while True:

        result = game_loop()
        if result == pygame.QUIT:
            break

        result = game_over(WINDOW, result)
        if result == pygame.QUIT:
            break
