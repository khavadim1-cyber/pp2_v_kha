import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("шар")

# Цвета (в формате RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

radius = 25
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
step = 20 

clock = pygame.time.Clock()

running = True

while running:
    clock.tick(60) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                if ball_x - radius - step >= 0:
                    ball_x -= step
                    
            elif event.key == pygame.K_RIGHT:
                if ball_x + radius + step <= WIDTH:
                    ball_x += step
                    
            elif event.key == pygame.K_UP:
                if ball_y - radius - step >= 0:
                    ball_y -= step
                    
            elif event.key == pygame.K_DOWN:
                if ball_y + radius + step <= HEIGHT:
                    ball_y += step

    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, (ball_x, ball_y), radius)
    
    pygame.display.flip()

pygame.quit()