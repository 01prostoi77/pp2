import pygame
from pygame.locals import *
import random
import time
import math

pygame.init()
pygame.mixer.init()

fps = pygame.time.Clock()
fps.tick(60)

# Colors
BLUE = (0, 0, 255)
YELLOW = (242, 242, 10)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)

# Variables for program
width = 400
height = 600
SPEED = 5              # speed for enemy and coins
SCORE = 0
COINS = 0
# limit of coins, speed is increased if limit is achived
coin_threshold = 5     

screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)
pygame.display.set_caption("Racer")

background = pygame.image.load(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\racer\materials\AnimatedStreet.png")

# Actions for Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\racer\materials\Enemy.png")
        self.rect = self.image.get_rect()
        # начальное положение врага по случайной X и верхней Y
        self.rect.center = (random.randint(40, width - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        # если враг уходит за нижнюю границу, сбрасываем позицию и увеличиваем счет
        if self.rect.bottom > 600:
            SCORE += 100
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Actions for Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\racer\materials\Igrok.png")
        self.rect = self.image.get_rect()
        self.rect.center = (120, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < width:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Class for Coins
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\racer\materials\coin.gif")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        # монета появляется случайно по оси X и на фиксированной высоте
        self.rect.center = (random.randint(40, width - 40), 50)
        # случайный вес монеты: 1, 2 или 3
        self.weight = random.randint(1, 3)

    def move(self):
        self.rect.move_ip(0, SPEED)
        # если монета уходит за нижнюю границу, сбрасываем её позицию
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 50)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Setting up player, enemy and coin
P1 = Player()
E1 = Enemy()
C1 = Coin()
# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins_sprite = pygame.sprite.Group()
coins_sprite.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Event для увеличения базовой скорости через определённый интервал времени
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

pygame.mixer_music.load(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\racer\materials\background.wav")
pygame.mixer_music.play(-1)

running = True
while running:
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.15
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    # Отрисовка заднего фона
    screen.blit(background, (0, 0))

    # Отображение счета и количества монет
    screen.blit(font_small.render("Score:", True, BLACK), (10, 10))
    scores = font_small.render(str(SCORE), True, BLACK)
    screen.blit(scores, (80, 10))

    screen.blit(font_small.render("Coins:", True, BLACK), (10, 30))
    coins = font_small.render(str(COINS), True, YELLOW)
    screen.blit(coins, (80, 30))
    
    # Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
    
    # Проверка столкновения игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer_music.stop()
        pygame.mixer.Sound(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\racer\materials\crash.wav").play()
        time.sleep(0.5)

        # Game Over экран
        screen.fill(RED)
        screen.blit(game_over, (30, 250))
        time.sleep(0.4)

        screen.blit(font_medium.render("Total score:", True, BLACK), (30, 310))
        scores = font_medium.render(str(SCORE), True, BLACK)
        screen.blit(scores, (280, 310))
        time.sleep(0.4)

        screen.blit(font_medium.render("Total coins:", True, BLACK), (30, 360))
        scores = font_medium.render(str(COINS), True, YELLOW)
        screen.blit(scores, (280, 360))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()

    # проверка столкновения игрока с монетой
    if pygame.sprite.spritecollideany(P1, coins_sprite):
        pygame.mixer.Sound(r"C:\Users\Farkhat\Desktop\PP2\labworks\lab9\racer\materials\coin.mp3").play()
        # при сборе монеты добавляем значение её веса
        COINS += C1.weight
        C1.kill()
        # создаем новую монету
        C1 = Coin()
        coins_sprite.add(C1)
        all_sprites.add(C1)

        # если количество монет достигло порога, увеличиваем скорость врага и обновляем порог
        if COINS >= coin_threshold:
            SPEED += 1
            coin_threshold += 5  # следующий порог через каждые 5 монет

    pygame.display.update()
    fps.tick(60)
