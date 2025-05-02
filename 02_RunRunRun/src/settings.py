import pygame
import os

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 500
GRAVITY = 1
JUMP_STRENGTH = 20
INITIAL_GAME_SPEED = 5
LANE_POSITIONS = [150, 400, 650]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)

# Paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_PATH = os.path.join(BASE_PATH, 'assets')

def load_image(name, scale=1):
    path = os.path.join(ASSETS_PATH, 'images', name)
    image = pygame.image.load(path).convert_alpha()
    if scale != 1:
        size = image.get_size()
        image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
    return image

def load_sound(name):
    path = os.path.join(ASSETS_PATH, 'sounds', name)
    return pygame.mixer.Sound(path)