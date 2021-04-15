import pygame as pg


class Obj(pg.sprite.Sprite):
    # Classe geral para todo objeto do jogo
    def __init__(self, img, x, y, *groups):
        super().__init__(*groups)
        self.image = pg.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y


class Plane(Obj):
    def __init__(self, img, x, y, *groups):
        super().__init__(img, x, y, *groups)
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.full_gas = 0

    def events(self, event):
        # Identifica se o avião está se movendo
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                self.right = True
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                self.left = True
            if event.key == pg.K_w or event.key == pg.K_UP:
                self.up = True
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                self.down = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                self.right = False
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                self.left = False
            if event.key == pg.K_w or event.key == pg.K_UP:
                self.up = False
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                self.down = False

    def movement(self):
        # Movimenta o avião
        if self.right and self.rect.right < 530:
            self.rect[0] += 5
        if self.left and self.rect.left > 70:
            self.rect[0] -= 5
        if self.up and self.rect.top > 90:
            self.rect[1] -= 5
        if self.down and self.rect.bottom < 720:
            self.rect[1] += 5

    def get_gas(self, amount):
        # Ganha gasolina
        self.full_gas -= amount
        if self.full_gas <= 0:
            self.full_gas = 0

    def colision(self, group, name, kill):
        # Indetifica o grupo, nome e se quer destruir com a colisão
        colision = pg.sprite.spritecollide(self, group, kill)
        if name == 'Gasoline' and colision:
            self.get_gas(50)

    def update(self, *args):
        # Atualiza as funções do avião
        self.movement()
