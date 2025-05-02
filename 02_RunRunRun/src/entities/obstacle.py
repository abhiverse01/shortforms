import pygame
from src.settings import *

class Obstacle:
    def __init__(self, x, lane, game_speed):
        self.x = x
        self.lane = lane
        self.width = OBSTACLE_WIDTH
        self.height = 60
        self.y = GROUND_HEIGHT - self.height
        self.game_speed = game_speed
        self.image = load_image("obstacle.gif")
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.x -= self.game_speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def collides_with(self, player):
        if player.lane != self.lane:
            return False
            
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Pixel-perfect collision
        offset_x = self.x - player.x
        offset_y = self.y - player.y
        return player.mask.overlap(self.mask, (offset_x, offset_y)) is not None