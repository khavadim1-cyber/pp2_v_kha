import pygame
import sys
import random
import time
import json
from pygame.locals import *

# --- INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 400, 600
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer: Turbo Edition")
clock = pygame.time.Clock()

# Colors
GRAY, WHITE, YELLOW = (50, 50, 50), (255, 255, 255), (255, 255, 0)
RED, BLUE, GREEN = (200, 0, 0), (0, 0, 200), (0, 255, 0)
BLACK, GOLD, PURPLE = (0, 0, 0), (255, 215, 0), (128, 0, 128)

# Fonts
font_small = pygame.font.SysFont("Verdana", 18)
font_medium = pygame.font.SysFont("Verdana", 25)
font_large = pygame.font.SysFont("Verdana", 40)

# --- OBJECT CLASSES ---

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED) # Enemy cars only
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        # Position the obstacle randomly above the screen
        self.rect.center = (random.randint(40, WIDTH-40), random.randint(-500, -50))

    def move(self, speed):
        self.rect.move_ip(0, speed)
        # Respawn if the obstacle goes off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.spawn()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.types = ["nitro", "shield", "repair"]
        self.current_type = random.choice(self.types)
        self.image = pygame.Surface((30, 30))
        colors = {"nitro": GREEN, "shield": BLUE, "repair": PURPLE}
        self.image.fill(colors[self.current_type])
        self.rect = self.image.get_rect()
        self.spawn_time = time.time()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(30, WIDTH-30), -100)
        self.spawn_time = time.time()

    def move(self, speed):
        self.rect.move_ip(0, speed)
        # Remove if off-screen or if 8 seconds have passed since spawn
        if self.rect.top > HEIGHT or time.time() - self.spawn_time > 8:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 70))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.reset_pos()
        self.shielded = False
       
    def reset_pos(self):
        self.rect.center = (WIDTH // 2, 520)

    def move(self):
        keys = pygame.key.get_pressed()
        speed = 7
        if self.rect.left > 0 and keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if self.rect.right < WIDTH and keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)

# --- GAME ENGINE ---

class Game:
    def __init__(self):
        self.state = "MENU"
        self.username = ""
        self.reset_session()

    def reset_session(self):
        """Resets the game state for a new session"""
        self.score = 0
        self.distance = 0
        self.base_speed = 5
        self.boost_timer = 0
        self.p1 = Player()
        self.enemies = pygame.sprite.Group([Obstacle() for _ in range(2)])
        self.powerups = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.p1, *self.enemies)

    def update(self):
        if self.state == "PLAYING":
            # Speed logic: add +5 if nitro boost is active
            current_speed = self.base_speed + (5 if self.boost_timer > 0 else 0)
            if self.boost_timer > 0: self.boost_timer -= 1
            
            self.distance += current_speed / 10
            self.p1.move()
            
            for e in self.enemies: e.move(current_speed)
            for p in self.powerups: p.move(current_speed)

            # Spawn power-ups randomly if none are currently present
            if random.random() < 0.005 and len(self.powerups) == 0:
                self.powerups.add(PowerUp())

            # Collision with enemies
            if pygame.sprite.spritecollide(self.p1, self.enemies, False):
                if self.p1.shielded:
                    self.p1.shielded = False
                    for e in self.enemies: e.spawn()
                else:
                    self.state = "GAME_OVER"

            # Collection of power-ups
            p_hit = pygame.sprite.spritecollideany(self.p1, self.powerups)
            if p_hit:
                if p_hit.current_type == "nitro": self.boost_timer = 180 # 3 seconds at 60 FPS
                elif p_hit.current_type == "shield": self.p1.shielded = True
                elif p_hit.current_type == "repair": self.score += 100
                p_hit.kill()

    def draw(self):
        DISPLAYSURF.fill(GRAY)
        
        if self.state == "MENU":
            self.draw_text("RACER: TURBO", font_large, GREEN, 150)
            self.draw_text("Press 1 to START", font_small, WHITE, 300)
        
        elif self.state == "NAME_ENTRY":
            self.draw_text("ENTER NAME:", font_medium, WHITE, 200)
            self.draw_text(self.username + "_", font_large, YELLOW, 250)

        elif self.state == "PLAYING":
            # Road markings animation
            for i in range(0, HEIGHT, 100):
                pygame.draw.rect(DISPLAYSURF, WHITE, (WIDTH//2 - 5, i + (self.distance % 100), 10, 50))
            
            self.all_sprites.draw(DISPLAYSURF)
            self.powerups.draw(DISPLAYSURF)
            
            # UI Text
            ui_txt = font_small.render(f"Dist: {int(self.distance)}m", True, WHITE)
            DISPLAYSURF.blit(ui_txt, (10, 10))
            
            # Visual shield indicator
            if self.p1.shielded:
                pygame.draw.circle(DISPLAYSURF, BLUE, self.p1.rect.center, 45, 2)

        elif self.state == "GAME_OVER":
            self.draw_text("CRASHED!", font_large, RED, 200)
            self.draw_text("Press R to Restart", font_small, WHITE, 300)

        pygame.display.update()

    def draw_text(self, text, font, color, y):
        """Helper to render horizontally centered text"""
        surf = font.render(text, True, color)
        DISPLAYSURF.blit(surf, (WIDTH//2 - surf.get_width()//2, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if self.state == "MENU" and event.key == K_1:
                    self.state = "NAME_ENTRY"
                    
                elif self.state == "NAME_ENTRY":
                    if event.key == K_RETURN and self.username:
                        self.reset_session()
                        self.state = "PLAYING"
                    elif event.key == K_BACKSPACE: self.username = self.username[:-1]
                    else: self.username += event.unicode
                    
                elif self.state == "GAME_OVER" and event.key == K_r:
                    self.reset_session()
                    self.state = "PLAYING"

# --- MAIN LOOP ---
game = Game()
while True:
    game.handle_events()
    game.update()
    game.draw()
    clock.tick(60)