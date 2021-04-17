import os
import pygame


# Cores
RED_COLOR = pygame.Color("Red")
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
MOVEMENT_SPEED = 5
SCROLL_SPEED = 5
GAS_SPAWN_CHANCE = 10  # (0-1000)
GAS_PER_CAN = 0.1  # (0-1)
GAS_CONS_PER_FRAME = 0.0005  # (0-1)

# Assets
GAS_ASSET = os.path.join("assets", "gas.png")
PLANE_ASSET = os.path.join("assets", "plane.png")
