import pygame
from settings import *
from pygame.math import Vector2


class Bar(pygame.rect.Rect):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        default_percentage: int,
        color: pygame.Color,
    ):
        super().__init__(x, y, width, height)
        self.percentage = default_percentage
        self.color = color

    def draw(self, surface: pygame.Surface):
        """
        :param surface: The surface to which the bar will be drawn.

        This function draws the bar's outline and it's current percentage.
        """

        # Fills the bar according to self.percentage
        pygame.draw.rect(
            surface,
            color=self.color,
            rect=(
                self.x,
                self.y,
                self.width * self.percentage,
                self.height,
            ),
        )

        # Draws the outline
        pygame.draw.rect(surface, rect=self, color=WHITE_COLOR, width=4)


class Object(pygame.sprite.Sprite):
    def __init__(self, image: str, x: int, y: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tick = 0
        self.frame = 1

    @property
    def x(self):
        """
        :return: The current x coordinate of self

        This property returns the x position of the Object
        """
        return self.rect.x

    @x.setter
    def x(self, value: int):
        """
        :param value: The x coordinate that will set

        This property sets the Object's x coordinate
        """
        self.rect.x = value

    @property
    def y(self):
        """
        :return: The current y coordinate of self

        This property returns the y position of the Object
        """
        return self.rect.y

    @y.setter
    def y(self, value: int):
        """
        :param value: The y coordinate that will set
        :return: This property sets the Object's y coordinate
        """
        self.rect.y = value


class Plane(Object):
    def __init__(self, img, x, y, *groups):
        super().__init__(img, x, y, *groups)
        self.bullets = pygame.sprite.Group()
        self.gas = 1
        self.temperature = 0

    def movement(self, mouse):
        if 0 < mouse[0] < SCREEN_SIZE[0]:
            self.x = mouse[0] - self.rect.width / 2

        if 0 < mouse[1] < SCREEN_SIZE[1]:
            self.y = mouse[1] - self.rect.height / 2

    def shoot(self, *groups: pygame.sprite.Group):

        bullet_1 = Bullets(
            BULLET_ASSET,
            (self.x + self.rect.width / 2) + 8,
            self.rect.top - 2,
            self.bullets,
            *groups
        )

        bullet_2 = Bullets(
            BULLET_ASSET,
            (self.x + self.rect.width / 2) - 16,
            self.rect.top - 2,
            self.bullets,
            *groups
        )

        bullet_1.image = pygame.transform.rotate(bullet_1.image, 180)
        bullet_2.image = pygame.transform.rotate(bullet_2.image, 180)

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.y -= BULLETS_SPEED
            if bullet.y <= 0:
                bullet.kill()


class Bullets(Object):
    def __init__(self, image: str, x: int, y: int, *groups: pygame.sprite.Group):
        super().__init__(image, x, y, *groups)


class Enemy(Object):
    def __init__(self, image: str, x: int, y: int, *groups: pygame.sprite.Group):
        super().__init__(image, x, y, *groups)
        self.bullets = pygame.sprite.Group()
        self.life = 1

    def shoot(self, *groups: pygame.sprite.Group):
        Bullets(
            BULLET_ASSET,
            (self.x + self.rect.width / 2) - 2,
            self.rect.bottom,
            self.bullets,
            *groups
        )


class Missiles(Object):
    def __init__(self, image: str, x: int, y: int, *groups: pygame.sprite.Group):
        super().__init__(image, x, y, *groups)
        self.image = pygame.image.load(image)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(x + 8.5, y + 20))
        self.position = Vector2((x + 8.5, y + 20))
        self.direction = Vector2(0, 1)  # A unit vector pointing downward.
        self.speed = 5
        self.angle_speed = 0
        self.angle = 0
        self.life = 1

    def update(self):
        if self.angle_speed != 0:
            # Rotate the direction vector and then the image.
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.rect.center = self.position

    def animations(self, image, ticks, frames):
        self.tick += 1
        if self.tick == ticks:
            self.tick = 0
            self.frame += 1
        if self.frame == frames:
            self.frame = 1
        self.original_image = pygame.image.load('assets/'f'{image}'f'{str(self.frame)}''.png')
        

class Text:
    def __init__(self, size, text, color):
        self.font = pygame.font.Font('font/8-BIT WONDER.TTF', size)
        self.render = self.font.render(text, True, color)

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))