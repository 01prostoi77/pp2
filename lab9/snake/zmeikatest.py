import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# Colors
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE  = (255, 255, 255)
PINK   = (242, 94, 166)

width, height = 720, 480
cell_size = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Font settings
font = pygame.font.SysFont("Bahnschrift", 30)
font_small = pygame.font.SysFont("Bahnschrift", 15)

# Zmei setup
snake_pos = [width // 2, height // 2]
snake_body = [[width // 2, height // 2]]
direction = 'RIGHT'
change_to = direction

clock = pygame.time.Clock()
fps = 5
running = True
alive = True

#BAckground music
pygame.mixer_music.load(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\snake\snake_soundtrack.mp3")
pygame.mixer_music.play(-1)

# hgame variables
level = 1
score = 0
new_level_at = 3


# NEW: Food class with random weight and a lifetime timer

class Food:
    def __init__(self):
        # Generate random position on grid (не на краях)
        self.pos = [random.randrange(1, width // cell_size - 1) * cell_size,
                    random.randrange(1, height // cell_size - 1) * cell_size]
        # Create rect for collision and drawing
        self.rect = pygame.Rect(self.pos[0], self.pos[1], cell_size - 1, cell_size - 1)
        # Random weight between 1 and 3
        self.weight = random.randint(1, 3)
        # Record spawn time (в миллисекундах)
        self.spawn_time = pygame.time.get_ticks()
        # Lifetime in milliseconds (например, 5000 мс = 5 секунд)
        self.lifetime = 5000

    def draw(self, surface):
        # Draw food as a red square; можно изменить цвет или добавить надпись веса
        pygame.draw.rect(surface, RED, self.rect)

    def is_expired(self):
        # Если прошло больше времени, чем lifetime, еда считается просроченной
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

# Create initial food instance
food = Food()
# ----------------------------------------------------------

# Function to spawn new food (при исчезновении или сборе еды)
def spawn_food():
    return Food()

while running:
    
    clock.tick(fps)
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            # Change direction based on key press
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif not alive and event.key == pygame.K_SPACE:
                # Restart game if game over and SPACE pressed
                alive = True
                snake_pos = [width // 2, height // 2]
                snake_body = [[width // 2, height // 2]]
                direction = 'RIGHT'
                change_to = direction
                food = spawn_food()
                fps = 5
                score = 0
                new_level_at = 3
                level = 1
    
    direction = change_to
    if alive:
        # Move snake based on direction
        if direction == 'UP':
            snake_pos[1] -= cell_size
        elif direction == 'DOWN':
            snake_pos[1] += cell_size
        elif direction == 'RIGHT':
            snake_pos[0] += cell_size
        elif direction == 'LEFT':
            snake_pos[0] -= cell_size
        
        # Check collisions with boundaries or self
        if (snake_pos[0] < 0 or snake_pos[0] >= width or
                snake_pos[1] < 0 or snake_pos[1] >= height or
                snake_pos in snake_body):
            alive = False
        else:
            snake_body.insert(0, list(snake_pos))
            
            # Check if snake has eaten the food
            if snake_pos[0] == food.rect.x and snake_pos[1] == food.rect.y:
                # Increase score by 1 and add food weight to score if needed
                score += food.weight
                food = spawn_food()
            else:
                snake_body.pop()
    else:
        # Game Over screen
        text_gameover = font.render("Game Over!", True, WHITE)
        screen.blit(text_gameover, (width // 2 - 80, height // 2))
        text_restart = font.render("Press SPACE to restart", True, WHITE)
        screen.blit(text_restart, (width // 2 - 160, height // 2 + 30))
    
    # If food is expired, spawn new food
    if food.is_expired():
        food = spawn_food()
    
    # Draw snake and food
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], cell_size - 1, cell_size - 1))
    food.draw(screen)
    
    # Display score and level
    screen.blit(font.render(f"Score: {score}", True, WHITE), (5, 5))
    screen.blit(font.render(f"Level: {level}", True, YELLOW), (5, 30))
    
    # Level up logic
    if score >= new_level_at:
        level += 1
        new_level_at += 3
        fps += 1
        pygame.mixer.Sound(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\snake\bonus-points.mp3").play()
        text_new_level = font_small.render("New Level!", True, PINK)
        screen.blit(text_new_level, (width // 2 - 40, height // 2 + 30))
        text_speed_up = font_small.render("Speed + 1!", True, PINK)
        screen.blit(text_speed_up, (width // 2 - 40, height // 2 + 50))
        pygame.display.flip()
        time.sleep(0.5)
    
    pygame.display.flip()
