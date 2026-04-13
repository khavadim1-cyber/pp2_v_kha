import pygame
import datetime
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("часы")

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)

font = pygame.font.SysFont(None, 48)

def get_coords(angle, length):
    theta = math.radians(angle - 90)
    x = CENTER[0] + length * math.cos(theta)
    y = CENTER[1] + length * math.sin(theta)
    return (x, y)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    h = now.hour % 12
    m = now.minute
    s = now.second

    screen.fill(WHITE)

    pygame.draw.circle(screen, BLACK, CENTER, RADIUS, 4)
    pygame.draw.circle(screen, BLACK, CENTER, 10)

    for i in range(12):
        angle = i * 30
        start = get_coords(angle, RADIUS - 10)
        end = get_coords(angle, RADIUS + 10)
        pygame.draw.line(screen, BLACK, start, end, 3)

    hour_angle = (h * 30) + (m * 0.5)
    pygame.draw.line(screen, BLACK, CENTER, get_coords(hour_angle, RADIUS * 0.5), 8)

    min_angle = m * 6
    pygame.draw.line(screen, BLACK, CENTER, get_coords(min_angle, RADIUS * 0.8), 5)

    sec_angle = s * 6
    pygame.draw.line(screen, RED, CENTER, get_coords(sec_angle, RADIUS * 0.9), 2)

    time_str = now.strftime("%H:%M:%S")
    time_text = font.render(time_str, True, GRAY)
    screen.blit(time_text, (WIDTH // 2 - 70, HEIGHT - 80))

    pygame.display.flip()
    clock.tick(1) 

pygame.quit()