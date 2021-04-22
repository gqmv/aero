import os
import pygame
pygame.font.init()


# Cores
RED_COLOR = pygame.Color("Red")
BLUE_COLOR = pygame.Color("Blue")
WHITE_COLOR = pygame.Color("White")
BACKGROUND_COLOR = (120, 172, 255)

# Definições de janela
SCREEN_SIZE = (600, 750)
WINDOW_NAME = "Aero"
BORDER_MARGIN_SIDES = 80
BORDER_MARGIN_TOP_BOTTOM = 60
BORDER_WIDTH = 4

# Definições de jogabilidade
FPS = 60
MOVEMENT_SPEED = 10
SCROLL_SPEED = 5
BULLETS_SPEED = 10
SCORE_PER_SECOND = 2

GAS_SPAWN_CHANCE = 5  # (0-1000)
GAS_PER_CAN = 0.1  # (0-1)
GAS_CONS_PER_FRAME = 0.0005  # (0-1)

WATER_SPAWN_CHANCE = 5  # (0-1000)
COOLING_PER_CAN = 0.1  # (0-1)
TEMP_CONS_PER_FRAME = 0.0005  # (0-1)

ENEMY_SPAWN_CHANCE = 5  # (0-1000)
ENEMY_PER_CAN = 0.1  # (0-1)
ENEMY_CONS_PER_FRAME = 0.0005  # (0-1)

MISSILE_SPAWN_CHANCE = 5  # (0-1000)
MISSILE_PER_CAN = 0.1  # (0-1)
MISSILE_CONS_PER_FRAME = 0.0005  # (0-1)

FONT_SIZE = 20
FONT = pygame.font.SysFont('Comic Sans MS', 20)

# Assets
GAS_ASSET = os.path.join("assets", "gas.png")
PLANE_ASSET = os.path.join("assets", "plane.png")
WATER_ASSET = os.path.join("assets", "water.png")
ENEMY_ASSET = os.path.join("assets", "enemy.png")
BULLET_ASSET = os.path.join("assets", "bullet.png")
BACKGROUND_ASSET = os.path.join("assets", "bg1.png")
MENU_ASSET = os.path.join("assets", "menu.png")
GAMEOVER_ASSET = os.path.join("assets", "gameover.png")
MISSILE_ASSET = os.path.join("assets", "missile.png")