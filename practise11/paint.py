import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Рисовальня")

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
    status = f"Tool: {current_tool} | Color: {current_color} | Keys: 1-8 (Tools), R/G/B/W (Colors)"
    txt = font.render(status, True, BLACK)
    screen.blit(txt, (10, 10))

def get_shape_data(start, end, tool):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    if tool == 'square':
        side = max(abs(dx), abs(dy))
        s_x = x1 if x2 > x1 else x1 - side
        s_y = y1 if y2 > y1 else y1 - side
        return (s_x, s_y, side, side)

    elif tool == 'right_tri':
        return [(x1, y1), (x1, y2), (x2, y2)]

    elif tool == 'equi_tri':
        height = dx * (math.sqrt(3) / 2)
        return [(x1, y2), (x2, y2), (x1 + dx/2, y2 - height)]

    elif tool == 'rhombus':
        return [
            (x1 + dx/2, y1), 
            (x2, y1 + dy/2), 
            (x1 + dx/2, y2),
            (x1, y1 + dy/2)  
        ]
    return None

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
            if event.key == pygame.K_5: current_tool = 'square'
            if event.key == pygame.K_6: current_tool = 'right_tri'
            if event.key == pygame.K_7: current_tool = 'equi_tri'
            if event.key == pygame.K_8: current_tool = 'rhombus'
            
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
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]), 2)
                elif current_tool == 'circle':
                    radius = int(math.hypot(mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                elif current_tool == 'square':
                    data = get_shape_data(start_pos, mouse_pos, 'square')
                    pygame.draw.rect(canvas, current_color, data, 2)
                elif current_tool in ['right_tri', 'equi_tri', 'rhombus']:
                    pts = get_shape_data(start_pos, mouse_pos, current_tool)
                    pygame.draw.polygon(canvas, current_color, pts, 2)
                
                drawing = False

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == 'brush':
                    pygame.draw.circle(canvas, current_color, event.pos, 3)
                elif current_tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, 15)

    if drawing:
        if current_tool == 'rect':
            pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]), 2)
        elif current_tool == 'circle':
            radius = int(math.hypot(mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
            pygame.draw.circle(screen, current_color, start_pos, radius, 2)
        elif current_tool == 'square':
            data = get_shape_data(start_pos, mouse_pos, 'square')
            pygame.draw.rect(screen, current_color, data, 2)
        elif current_tool in ['right_tri', 'equi_tri', 'rhombus']:
            pts = get_shape_data(start_pos, mouse_pos, current_tool)
            pygame.draw.polygon(screen, current_color, pts, 2)
    draw_ui()
    pygame.display.flip()
pygame.quit()