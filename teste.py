import math
import pygame
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = x, y
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.right = True
            if event.key == pygame.K_a:
                self.left = True
            if event.key == pygame.K_w:
                self.up = True
            if event.key == pygame.K_s:
                self.down = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.right = False
            if event.key == pygame.K_a:
                self.left = False
            if event.key == pygame.K_w:
                self.up = False
            if event.key == pygame.K_s:
                self.down = False

    def move(self):
        if self.right:
            self.rect.x += 8
        if self.left:
            self.rect.x -= 8
        if self.up:
            self.rect.y -= 8
        if self.down:
            self.rect.y += 8


class Missile(pygame.sprite.Sprite):

    def __init__(self, pos=(420, 420)):
        super(Missile, self).__init__()
        self.image = pygame.image.load("assets/missile.png")
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)
        self.direction = Vector2(0, 1)  # A unit vector pointing downward.
        self.speed = 2
        self.angle_speed = 0
        self.angle = 0

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


pygame.init()
screen = pygame.display.set_mode((720, 720))
missile = Missile((360, 360))
player = Player(100, 100)
missilesprite = pygame.sprite.RenderPlain(missile)
playersprite = pygame.sprite.RenderPlain(player)


def find_angle():
    lista = []
    for num in range(2):
        vec = player.rect.center[num] - missile.rect.center[num]
        lista.append(vec)
    vector = pygame.math.Vector2(lista[0], lista[1])
    return pygame.math.Vector2.angle_to(missile.direction, vector)


def main():
    clock = pygame.time.Clock()
    done = False
    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            player.events(event)
        missilesprite.update()
        playersprite.update()

        screen.fill((0, 0, 0))
        player.move()
        missilesprite.draw(screen)
        playersprite.draw(screen)
        pygame.display.flip()
        print(find_angle())
        if find_angle() > 10 or find_angle() < -10:

            missile.angle_speed = 3
            print(find_angle())
        else:
            missile.angle_speed = 0
        if missile.rect.bottom >= 720:
            missile.position[1] = 700


if __name__ == '__main__':
    main()
    pygame.quit()
