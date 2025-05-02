import pygame
from src.settings import *

class Coin:
    def __init__(self, x, lane, game_speed):
        self.x = x
        self.lane = lane
        self.width = COIN_WIDTH
        self.height = COIN_WIDTH
        self.y = GROUND_HEIGHT - self.height - 100
        self.game_speed = game_speed
        self.collected = False
        self.image = load_image("coin.gif")
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_frame = 0
    
    def update(self):
        self.x -= self.game_speed
        self.animation_frame = (self.animation_frame + 0.1) % 10
    
    def draw(self, screen):
        if not self.collected:
            # Add slight animation
            scale = 1 + 0.1 * abs(5 - self.animation_frame) / 5
            img = pygame.transform.scale(self.image, 
                (int(self.width * scale), int(self.height * scale)))
            screen.blit(img, (self.x - (img.get_width() - self.width)/2, 
                         self.y - (img.get_height() - self.height)/2))
    
    def collides_with(self, player):
        if player.lane != self.lane or self.collected:
            return False
            
        offset_x = self.x - player.x
        offset_y = self.y - player.y
        return player.mask.overlap(self.mask, (offset_x, offset_y)) is not None