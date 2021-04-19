import pygame
from settings import *


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
        self.temperature = 0

    def handle_movement(self, mouse: tuple):
        """
        :param mouse: The mouse position

        This function moves the plane depending on the mice position.
        """
        mouse_x = mouse[0]
        mouse_y = mouse[1]

        if (
            mouse_x
            > self.x
            + self.rect.width  # Checks if the mouse is to the right of the plane
            and self.x
            <= SCREEN_SIZE[0]
            - BORDER_MARGIN_SIDES
            - self.rect.width  # Checks if the plane isn't at the border
        ):
            self.image = (
                self.img_right
            )  # As the plane is moving right, set's the asset to self.img_right
            self.x += MOVEMENT_SPEED

        elif (
            mouse_x < self.x and self.x >= BORDER_MARGIN_SIDES
        ):  # Checks if the mouse is to the left of the plane and within the border
            self.image = (
                self.img_left
            )  # As the plane is moving left, set's the asset to self.img_left
            self.x -= MOVEMENT_SPEED

        if (
            mouse_y
            > self.y + self.rect.height  # Checks if the mouse is under the plane
            and self.y
            <= SCREEN_SIZE[1]
            - BORDER_MARGIN_TOP_BOTTOM
            - BORDER_WIDTH
            - self.rect.height
        ):  # Checks if the plane is at the border
            self.y += MOVEMENT_SPEED

        elif (
            mouse_y < self.y and self.y >= BORDER_MARGIN_TOP_BOTTOM + BORDER_WIDTH
        ):  # Checks if the mouse is above the plane and within the border
            self.y -= MOVEMENT_SPEED
