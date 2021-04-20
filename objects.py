import pygame
from settings import *


class Bar(pygame.rect.Rect):
    def __init__(
            self, x: int, y: int, width: int, height: int, default_percentage: int
    ):
        super().__init__(x, y, width, height)
        self.percentage = default_percentage

    def draw(self, surface: pygame.Surface):
        """
        :param surface: The surface to which the bar will be drawn.

        This function draws the bar's outline and it's current percentage.
        """

        # Fills the bar according to self.percentage
        pygame.draw.rect(
            surface,
            color=RED_COLOR,
            rect=(
                self.x,
                self.y + ((1 - self.percentage) * self.height),
                self.width,
                self.height * self.percentage,
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
        self.ticks = 0

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
    def __init__(self, img, img_left, img_right, x, y, *groups):
        super().__init__(img, x, y, *groups)
        self.img_left = pygame.image.load(img_left)
        self.img_right = pygame.image.load(img_right)
        self.img_default = pygame.image.load(img)
        self.gas = 1
        self.temp = 0


class Enemy(Object):
    def __init__(self, image: str, x: int, y: int, *groups: pygame.sprite.Group):
        super().__init__(image, x, y, *groups)


class Bullets(Object):
    def __init__(self, image: str, x: int, y: int, *groups: pygame.sprite.Group):
        super().__init__(image, x, y, *groups)
        self.spedd_y = BULLETS_SPEED
