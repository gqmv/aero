import pygame
from settings import *


class Bar(pygame.rect.Rect):
    def __init__(self, x, y, width, height, default_percentage):
        super().__init__(x, y, width, height)
        self.percentage = default_percentage

    def draw(self, surface):
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
        pygame.draw.rect(surface, rect=self, color=WHITE_COLOR, width=4)


class Object(pygame.sprite.Sprite):
    # Classe geral para todo objeto do jogo
    def __init__(self, image, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value


class Plane(Object):
    def __init__(self, img, img_left, img_right, x, y, *groups):
        super().__init__(img, x, y, *groups)
        self.img_left = pygame.image.load(img_left)
        self.img_right = pygame.image.load(img_right)
        self.img_default = pygame.image.load(img)
        self.gas = 0

    def movement(self, mouse):
        mouse_x = mouse[0]
        mouse_y = mouse[1]

        if (
            mouse_x > self.x + self.rect.width
            and self.x <= SCREEN_SIZE[0] - BORDER_MARGIN_SIDES - self.rect.width
        ):
            self.image = self.img_right
            self.x += MOVEMENT_SPEED

        elif mouse_x < self.x and self.x >= BORDER_MARGIN_SIDES:
            self.image = self.img_left
            self.x -= MOVEMENT_SPEED

        if (
            mouse_y > self.y + self.rect.height
            and self.y
            <= SCREEN_SIZE[1] - BORDER_MARGIN_TOP - BORDER_WIDTH - self.rect.height
        ):
            self.y += MOVEMENT_SPEED

        elif mouse_y < self.y and self.y >= BORDER_MARGIN_TOP + BORDER_WIDTH:
            self.y -= MOVEMENT_SPEED
