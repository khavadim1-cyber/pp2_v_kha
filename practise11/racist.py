import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 400, 600

GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer: Turbo Edition")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 40)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        pygame.draw.rect(self.image, BLACK, (5, 10, 30, 15))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH-40), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > HEIGHT):
            self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = 1
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        if random.random() > 0.8:
            self.weight = 5
            self.image.fill(GOLD)
            pygame.draw.circle(self.image, BLACK, (12, 12), 12, 2)
        else:
            self.weight = 1
            self.image.fill(YELLOW)
            pygame.draw.circle(self.image, BLACK, (12, 12), 12, 1)
        self.rect.center = (random.randint(30, WIDTH-30), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > HEIGHT):
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 70))
        self.image.fill(BLUE)
        pygame.draw.rect(self.image, YELLOW, (5, 5, 10, 5))
        pygame.draw.rect(self.image, YELLOW, (25, 5, 10, 5))
        pygame.draw.rect(self.image, WHITE, (5, 20, 30, 15))
        self.rect = self.image.get_rect()
        self.reset_pos()
       
    def reset_pos(self):
        self.rect.center = (WIDTH // 2, 520)

    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH and keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

SPEED = 5
SCORE = 0

def show_menu(title, color):
    DISPLAYSURF.fill(BLACK)
    line1 = font_large.render(title, True, color)
    line2 = font_small.render("Нажми H для старта", True, WHITE)
    line3 = font_small.render("Нажми G для выхода", True, WHITE)
    DISPLAYSURF.blit(line1, (WIDTH // 2 - line1.get_width() // 2, HEIGHT // 3))
    DISPLAYSURF.blit(line2, (WIDTH // 2 - line2.get_width() // 2, HEIGHT // 2))
    DISPLAYSURF.blit(line3, (WIDTH // 2 - line3.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.update()

def reset_game():
    global SPEED, SCORE
    SPEED = 5
    SCORE = 0
    P1.reset_pos()
    E1.spawn()
    C1.spawn()

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

game_active = False
game_over_state = False
line_y = 0 

while True:
    if not game_active:
        if game_over_state:
            show_menu("ТЫ РАЗБИЛСЯ!", RED)
        else:
            show_menu("RACER TURBO", GREEN)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_h:
                    reset_game()
                    game_active = True
                    game_over_state = False
                if event.key == K_g:
                    pygame.quit()
                    sys.exit()
    
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(GRAY)
        pygame.draw.rect(DISPLAYSURF, WHITE, (10, 0, 10, HEIGHT))
        pygame.draw.rect(DISPLAYSURF, WHITE, (WIDTH-20, 0, 10, HEIGHT))
        for i in range(-100, HEIGHT, 100):
            pygame.draw.rect(DISPLAYSURF, WHITE, (WIDTH//2 - 5, i + line_y, 10, 50))
        line_y = (line_y + SPEED) % 100

        score_text = font_small.render(f"Score: {SCORE}", True, WHITE)
        speed_text = font_small.render(f"Speed: {SPEED}", True, YELLOW)
        DISPLAYSURF.blit(score_text, (25, 10))
        DISPLAYSURF.blit(speed_text, (WIDTH - 120, 10))

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        if pygame.sprite.spritecollide(P1, coins, False):
            SCORE += C1.weight
            SPEED += 1
            C1.spawn()

        if pygame.sprite.spritecollideany(P1, enemies):
            game_active = False
            game_over_state = True
            time.sleep(0.5)

        pygame.display.update()
        clock.tick(60)