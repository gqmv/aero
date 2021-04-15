import pygame
from game import Game


class Main:
    # Classe basse para o jogo

    pygame.init()

    def __init__(self):
        self.window = pygame.display.set_mode([600, 750])
        pygame.display.set_caption("Aero")

        self.loop = True
        self.fps = pygame.time.Clock()

        self.game = Game()
        self.lost_gas_length = 0

    def draw(self):
        # Desenha a classe Game e todos os seus objetos na tela
        self.window.fill([120, 172, 255])
        self.game.draw(self.window)
        self.game.update()
        pygame.draw.rect(self.window, (255, 255, 255), (60, 80, 480, 650), 4)

    def gas_progress_bar(self):
        # Desenha uma barra de gasolina (ajeitar para atribuir parametros para poder fazer uma barra para o nivel de
        # agua tbm)
        self.game.plane.full_gas += 0.6
        if self.game.plane.full_gas >= 395:
            self.game.plane.full_gas = 395
        pygame.draw.rect(self.window, (255, 0, 0), (10, 80, 25, 400))
        pygame.draw.rect(self.window, (255, 255, 255), (10, 80, 25, 400), 4)
        pygame.draw.rect(
            self.window, (120, 172, 255), (13, 81, 20, self.game.plane.full_gas)
        )

    def events(self):
        # Identifica todos os eventos na tela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.plane.get_gas(50)
            self.game.plane.events(event)

    def update(self):
        # Atualiza os eventos do jogo
        while self.loop:
            self.draw()
            self.events()
            self.fps.tick(60)
            self.gas_progress_bar()
            pygame.display.update()


Main().update()
