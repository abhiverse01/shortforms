import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 500
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
OBSTACLE_WIDTH = 40
COIN_WIDTH = 30
GRAVITY = 1
JUMP_STRENGTH = 20
GAME_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Temple Run")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_HEIGHT - PLAYER_HEIGHT
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
        self.lane = 1  # 0: left, 1: middle, 2: right
        self.lane_positions = [150, 400, 650]  # X positions for each lane
    
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
        target_x = self.lane_positions[self.lane]
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
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # Draw head
        pygame.draw.circle(screen, RED, (self.x + self.width // 2, self.y - 10), 15)

class Obstacle:
    def __init__(self, x, lane):
        self.x = x
        self.lane = lane
        self.width = OBSTACLE_WIDTH
        self.height = 60
        self.y = GROUND_HEIGHT - self.height
    
    def update(self):
        self.x -= GAME_SPEED
    
    def draw(self):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
    
    def collides_with(self, player):
        if player.lane != self.lane:
            return False
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(obstacle_rect)

class Coin:
    def __init__(self, x, lane):
        self.x = x
        self.lane = lane
        self.width = COIN_WIDTH
        self.height = COIN_WIDTH
        self.y = GROUND_HEIGHT - self.height - 100  # Floating above ground
        self.collected = False
    
    def update(self):
        self.x -= GAME_SPEED
    
    def draw(self):
        if not self.collected:
            pygame.draw.circle(screen, GOLD, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)
    
    def collides_with(self, player):
        if player.lane != self.lane or self.collected:
            return False
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        coin_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(coin_rect)

def game_loop():
    player = Player()
    obstacles = []
    coins = []
    score = 0
    obstacle_timer = 0
    coin_timer = 0
    game_over = False
    
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_r and game_over:
                    return  # Restart game
        
        if not game_over:
            # Update game state
            player.update()
            
            # Spawn obstacles
            obstacle_timer += 1
            if obstacle_timer >= random.randint(50, 150):
                lane = random.randint(0, 2)
                obstacles.append(Obstacle(SCREEN_WIDTH, lane))
                obstacle_timer = 0
            
            # Spawn coins
            coin_timer += 1
            if coin_timer >= random.randint(30, 100):
                lane = random.randint(0, 2)
                coins.append(Coin(SCREEN_WIDTH, lane))
                coin_timer = 0
            
            # Update obstacles
            for obstacle in obstacles[:]:
                obstacle.update()
                if obstacle.x < -obstacle.width:
                    obstacles.remove(obstacle)
                elif obstacle.collides_with(player):
                    game_over = True
            
            # Update coins
            for coin in coins[:]:
                coin.update()
                if coin.x < -coin.width:
                    coins.remove(coin)
                elif coin.collides_with(player):
                    coin.collected = True
                    score += 10
                    coins.remove(coin)
        
        # Drawing
        screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.rect(screen, GREEN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        # Draw player
        player.draw()
        
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw()
        
        # Draw coins
        for coin in coins:
            coin.draw()
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("Game Over! Press R to restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 18))
        
        pygame.display.flip()
        clock.tick(60)

# Main game loop
while True:
    game_loop()