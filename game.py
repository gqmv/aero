import pygame
from objects import Obj, Plane
from random import randint


class Game:
    # Classe onde fica as funcionalidades gerais do jogo
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_gas = pygame.sprite.Group()
        self.plane = Plane("assets/plane.png", 290, 600, self.all_sprites)
        self.gasoline = Obj(
            "assets/gas.png", randint(82, 518), 104, self.all_sprites, self.all_gas
        )

    def draw(self, window):
        # Desenha na tela todas as sprites que fazem parte do grupo all_sprites
        self.all_sprites.draw(window)

    def update(self):
        # Atualiza sprites e funções do jogo
        self.all_sprites.update()
        self.move_gas()
        self.plane.colision(self.all_gas, "Gasoline", True)

    def move_gas(self):
        # Movimenta e elimina os galões de gasolina
        self.gasoline.rect[1] += 5
        if self.gasoline.rect[1] >= 715:
            self.gasoline.kill()
            self.gasoline = Obj(
                "assets/gas.png", randint(82, 518), 104, self.all_sprites, self.all_gas
            )
