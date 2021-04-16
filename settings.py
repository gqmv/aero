import os
import pygame

SCREEN_SIZE = (600, 750)
MOVEMENT_SPEED = 5
BACKGROUND_COLOR = (120, 172, 255)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = pygame.Color("RED")

WINDOW_NAME = "Aero"

BORDER_MARGIN_SIDES = 80
BORDER_MARGIN_TOP = 60
BORDER_WIDTH = 4

FPS = 60

GAS_ASSET = os.path.join("assets", "gas.png")
PLANE_ASSET = os.path.join("assets", "plane.png")

GAS_SPAWN_CHANCE = 10
GAS_PER_CAN = 0.1
GAS_CONS_PER_FRAME = 0.0005
