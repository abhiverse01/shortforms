import pygame
import random
import sys
from src.settings import *
from src.entities.player import Player
from src.entities.obstacle import Obstacle
from src.entities.coin import Coin

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RunRunRun")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset()
        
    def reset(self):
        self.player = Player()
        self.obstacles = []
        self.coins = []
        self.score = 0
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.game_over = False
        self.game_speed = INITIAL_GAME_SPEED
        self.distance = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.player.jump()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()
    
    def update(self):
        if self.game_over:
            return
            
        self.distance += 1
        # Increase difficulty over time
        if self.distance % 1000 == 0:
            self.game_speed += 0.5
            
        self.player.update()
        
        # Spawn obstacles
        self.obstacle_timer += 1
        if self.obstacle_timer >= random.randint(50, 150):
            lane = random.randint(0, 2)
            self.obstacles.append(Obstacle(SCREEN_WIDTH, lane, self.game_speed))
            self.obstacle_timer = 0
        
        # Spawn coins
        self.coin_timer += 1
        if self.coin_timer >= random.randint(30, 100):
            lane = random.randint(0, 2)
            self.coins.append(Coin(SCREEN_WIDTH, lane, self.game_speed))
            self.coin_timer = 0
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.x < -obstacle.width:
                self.obstacles.remove(obstacle)
            elif obstacle.collides_with(self.player):
                self.game_over = True
        
        # Update coins
        for coin in self.coins[:]:
            coin.update()
            if coin.x < -coin.width:
                self.coins.remove(coin)
            elif coin.collides_with(self.player):
                coin.collected = True
                self.score += 10
                self.coins.remove(coin)
    
    def render(self):
        self.screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.rect(self.screen, GREEN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        # Draw entities
        self.player.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        for coin in self.coins:
            coin.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to restart", True, BLACK)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 18))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)