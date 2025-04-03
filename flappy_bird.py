import pygame
import random

# Initialize Pygame
pygame.init()

# Load high score
def load_high_score():
    try:
        with open('high_score.txt', 'r') as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open('high_score.txt', 'w') as f:
        f.write(str(score))

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_SPAWN_TIME = 1500  # milliseconds
PIPE_GAP = 200

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Global variables
background = None  # Will be initialized in Game class

class Bird:
    def __init__(self):
        self.x = WINDOW_WIDTH // 3
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        try:
            self.sprite = pygame.image.load('images/bird.svg').convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (30, 30))
        except pygame.error as e:
            print(f"Error loading bird sprite: {e}")
            self.sprite = pygame.Surface((30, 30))
            self.sprite.fill(BLUE)
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
    
    def draw(self, screen):
        # Rotate bird based on velocity
        angle = max(-30, min(self.velocity * -3, 30))
        rotated_sprite = pygame.transform.rotate(self.sprite, angle)
        screen.blit(rotated_sprite, self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, WINDOW_HEIGHT - 150)
        self.top_pipe = pygame.Rect(x, 0, 50, self.height)
        self.bottom_pipe = pygame.Rect(x, self.height + PIPE_GAP, 50, WINDOW_HEIGHT)
        self.passed = False
    
    def update(self):
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_pipe)
        pygame.draw.rect(screen, GREEN, self.bottom_pipe)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Create a light blue background for sky effect
        global background
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background.fill((135, 206, 235))  # Light blue color for sky
        
        self.reset()
    
    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.high_score = load_high_score()
        self.last_pipe = pygame.time.get_ticks()
        self.game_over = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.bird.flap()
        return True
    
    def update(self):
        if not self.game_over:
            self.bird.update()
            
            # Spawn new pipes
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe > PIPE_SPAWN_TIME:
                self.pipes.append(Pipe(WINDOW_WIDTH))
                self.last_pipe = current_time
            
            # Update pipes and check collisions
            for pipe in self.pipes:
                pipe.update()
                if pipe.x + 50 < 0:
                    self.pipes.remove(pipe)
                if not pipe.passed and pipe.x < self.bird.x:
                    self.score += 1
                    pipe.passed = True
                if (pipe.top_pipe.colliderect(self.bird.rect) or
                    pipe.bottom_pipe.colliderect(self.bird.rect)):
                    self.game_over = True
                    if self.score > self.high_score:
                        self.high_score = self.score
                        save_high_score(self.high_score)
            
            # Check if bird hits the ground or ceiling
            if self.bird.y < 0 or self.bird.y > WINDOW_HEIGHT - 30:
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    save_high_score(self.high_score)
    
    def draw(self):
        # Draw background
        self.screen.blit(background, (0, 0))
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Draw score and high score
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 50))
        
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press SPACE to restart', True, (0, 0, 0))
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

# Start the game
if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()