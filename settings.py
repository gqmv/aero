import os
import pygame
pygame.font.init()


# Cores
RED_COLOR = pygame.Color("Red")
BLUE_COLOR = pygame.Color("Blue")
WHITE_COLOR = pygame.Color("White")
YELLOW_COLOR = pygame.Color("Yellow")
BACKGROUND_COLOR = (120, 172, 255)

# Definições de janela
SCREEN_SIZE = (600, 750)
WINDOW_NAME = "Aero"

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

BULLET_GAS_DAMAGE = GAS_PER_CAN
BULLET_TEMP_DAMAGE = COOLING_PER_CAN

MISSILE_SPAWN_CHANCE = 5  # (0-1000)
MISSILE_GAS_DAMAGE = GAS_PER_CAN * 3
MISSILE_TEMP_DAMAGE = COOLING_PER_CAN * 3

# Assets
GAS_ASSET = os.path.join("assets", "gas.png")
PLANE_ASSET = os.path.join("assets", "plane.png")
WATER_ASSET = os.path.join("assets", "water.png")
ENEMY_ASSET = os.path.join("assets", "enemy.png")
BULLET_ASSET = os.path.join("assets", "bullet.png")
BACKGROUND_ASSET = os.path.join("assets", "background.png")
MENU_ASSET = os.path.join("assets", "menu.png")
START_KEY_ASSET = os.path.join("assets", "start_key.png")
HIGHSCORE_KEY_ASSET = os.path.join("assets", "highscore_key.png")
SELECTOR_ASSET = os.path.join("assets", "selector.png")
MENU_WATER = os.path.join("assets", "menu_water.png")
GAMEOVER_ASSET = os.path.join("assets", "gameover.png")
MISSILE_ASSET = os.path.join("assets", "rocket1.png")
MOTOR_STATUS_ASSET = os.path.join("assets", "motor_status.png")
GAS_STATUS_ASSET = os.path.join("assets", "gas_status.png")
HIGHSCORE_ASSET = os.path.join("assets", "highscore.png")
GAME_OVER_ASSET = os.path.join("assets", "gameover.png")
RESTART_KEY_ASSET = os.path.join("assets", "restart.png")
QUIT_KEY_ASSET = os.path.join("assets", "quit-game.png")
