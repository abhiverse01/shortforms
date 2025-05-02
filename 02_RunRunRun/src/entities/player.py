import pygame
from src.settings import *

class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_HEIGHT - PLAYER_HEIGHT
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
        self.lane = 1  # 0: left, 1: middle, 2: right
        self.image = load_image("player.gif")
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Check ground collision
        if self.y >= GROUND_HEIGHT - self.height:
            self.y = GROUND_HEIGHT - self.height
            self.velocity_y = 0
            self.is_jumping = False
        
        # Update x position based on lane
        target_x = LANE_POSITIONS[self.lane]
        if self.x < target_x - 5:
            self.x += 5
        elif self.x > target_x + 5:
            self.x -= 5
        else:
            self.x = target_x
    
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
    
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
    
    def move_right(self):
        if self.lane < 2:
            self.lane += 1
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))