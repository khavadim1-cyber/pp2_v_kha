import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("рисовальня")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

current_color = BLACK
current_tool = 'brush'
drawing = False
start_pos = (0, 0)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont(None, 24)

def draw_ui():
    status = f"Инструмент: {current_tool} | Цвет: {current_color}"
    txt = font.render(status, True, BLACK)
    screen.blit(txt, (10, 10))

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0)) 
    
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: current_tool = 'brush'
            if event.key == pygame.K_2: current_tool = 'rect'
            if event.key == pygame.K_3: current_tool = 'circle'
            if event.key == pygame.K_4: current_tool = 'eraser'
            
            if event.key == pygame.K_r: current_color = RED
            if event.key == pygame.K_g: current_color = GREEN
            if event.key == pygame.K_b: current_color = BLUE
            if event.key == pygame.K_w: current_color = BLACK

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if current_tool == 'rect':
                    width = mouse_pos[0] - start_pos[0]
                    height = mouse_pos[1] - start_pos[1]
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], width, height), 2)
                
                elif current_tool == 'circle':
                    radius = int(((mouse_pos[0] - start_pos[0])**2 + (mouse_pos[1] - start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                
                drawing = False

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == 'brush':
                    pygame.draw.circle(canvas, current_color, event.pos, 3)
                elif current_tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, 15)

    if drawing:
        if current_tool == 'rect':
            width = mouse_pos[0] - start_pos[0]
            height = mouse_pos[1] - start_pos[1]
            pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], width, height), 2)
        
        elif current_tool == 'circle':
            radius = int(((mouse_pos[0] - start_pos[0])**2 + (mouse_pos[1] - start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, radius, 2)

    draw_ui()
    pygame.display.flip()

pygame.quit()