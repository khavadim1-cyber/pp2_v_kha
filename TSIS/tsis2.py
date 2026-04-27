import pygame
import math
import datetime
from collections import deque

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Pygame Painter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# State Variables
current_color = BLACK
current_tool = 'pencil'
brush_size = 2
drawing = False
start_pos = (0, 0)
last_pos = (0, 0) # For smooth pencil lines

# Text Tool State
typing = False
text_buffer = ""
text_pos = (0, 0)

# Surfaces
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)
font = pygame.font.SysFont("Arial", 24)

def get_shape_data(start, end, tool):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1

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
        return [(x1 + dx/2, y1), (x2, y1 + dy/2), (x1 + dx/2, y2), (x1, y1 + dy/2)]
    return None

def flood_fill(surface, x, y, new_color):
    """Standard BFS Flood Fill algorithm"""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    queue = deque([(x, y)])
    width, height = surface.get_size()
    
    while queue:
        curr_x, curr_y = queue.popleft()
        if surface.get_at((curr_x, curr_y)) != target_color:
            continue
        
        surface.set_at((curr_x, curr_y), new_color)
        
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if surface.get_at((nx, ny)) == target_color:
                    queue.append((nx, ny))

def save_canvas(surface):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"drawing_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Saved as {filename}")

def draw_ui():
    info = f"Tool: {current_tool} | Size: {brush_size} | Color: {current_color}"
    controls = "Keys: 1-0 (Tools), T (Text), F1-F3 (Size), Ctrl+S (Save)"
    txt_info = font.render(info, True, (50, 50, 50))
    txt_ctrl = font.render(controls, True, (100, 100, 100))
    screen.blit(txt_info, (10, 10))
    screen.blit(txt_ctrl, (10, 35))

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Text 
        if typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Finalize text onto canvas
                    txt_surf = font.render(text_buffer, True, current_color)
                    canvas.blit(txt_surf, text_pos)
                    text_buffer = ""
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    text_buffer = ""
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    text_buffer += event.unicode
            continue # Skip other events while typing

        #  Keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            # Save Check
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                save_canvas(canvas)
            
            # Tool Selection
            if event.key == pygame.K_1: current_tool = 'pencil'
            if event.key == pygame.K_2: current_tool = 'line'
            if event.key == pygame.K_3: current_tool = 'rect'
            if event.key == pygame.K_4: current_tool = 'circle'
            if event.key == pygame.K_5: current_tool = 'eraser'
            if event.key == pygame.K_6: current_tool = 'square'
            if event.key == pygame.K_7: current_tool = 'right_tri'
            if event.key == pygame.K_8: current_tool = 'equi_tri'
            if event.key == pygame.K_9: current_tool = 'rhombus'
            if event.key == pygame.K_0: current_tool = 'fill'
            if event.key == pygame.K_t: current_tool = 'text'

            # Brush Sizes
            if event.key == pygame.K_F1: brush_size = 2
            if event.key == pygame.K_F2: brush_size = 5
            if event.key == pygame.K_F3: brush_size = 10

            # Color Selection
            if event.key == pygame.K_r: current_color = RED
            if event.key == pygame.K_g: current_color = GREEN
            if event.key == pygame.K_b: current_color = BLUE
            if event.key == pygame.K_w: current_color = BLACK

        # Mouse handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_tool == 'fill':
                flood_fill(canvas, event.pos[0], event.pos[1], current_color)
            elif current_tool == 'text':
                typing = True
                text_pos = event.pos
                text_buffer = ""
            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos
            
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                # Permanent drawing to canvas
                if current_tool == 'line':
                    pygame.draw.line(canvas, current_color, start_pos, mouse_pos, brush_size)
                elif current_tool == 'rect':
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]), brush_size)
                elif current_tool == 'circle':
                    radius = int(math.hypot(mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                elif current_tool == 'square':
                    data = get_shape_data(start_pos, mouse_pos, 'square')
                    pygame.draw.rect(canvas, current_color, data, brush_size)
                elif current_tool in ['right_tri', 'equi_tri', 'rhombus']:
                    pts = get_shape_data(start_pos, mouse_pos, current_tool)
                    pygame.draw.polygon(canvas, current_color, pts, brush_size)
                
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == 'pencil':
                pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                last_pos = event.pos
            elif current_tool == 'eraser':
                pygame.draw.circle(canvas, WHITE, event.pos, brush_size * 3)

    # Preview (Drawing on Screen, not Canvas)
    if drawing:
        if current_tool == 'line':
            pygame.draw.line(screen, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == 'rect':
            pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]), brush_size)
        elif current_tool == 'circle':
            radius = int(math.hypot(mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
            pygame.draw.circle(screen, current_color, start_pos, radius, brush_size)
        elif current_tool == 'square':
            data = get_shape_data(start_pos, mouse_pos, 'square')
            pygame.draw.rect(screen, current_color, data, brush_size)
        elif current_tool in ['right_tri', 'equi_tri', 'rhombus']:
            pts = get_shape_data(start_pos, mouse_pos, current_tool)
            pygame.draw.polygon(screen, current_color, pts, brush_size)

    # Text Preview
    if typing:
        preview_txt = font.render(text_buffer + "|", True, current_color)
        screen.blit(preview_txt, text_pos)

    draw_ui()
    pygame.display.flip()

pygame.quit()