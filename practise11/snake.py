import pygame 
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
SNAKE_BLOCK = 10  
SPEED = 15
YELLOW = (255, 255, 102)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

font_style = pygame.font.SysFont("bahnschrift", 25)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Escape from KBTU')

clock = pygame.time.Clock()
game_started = False
record = 0

def show_score(current_score):
    value = font_style.render("Score: " + str(current_score), True, YELLOW)
    screen.blit(value, [10, 10])

def show_record(current_record):
    value = font_style.render("Record: " + str(current_record), True, YELLOW)
    screen.blit(value, [700, 10])

def show_timer(seconds_left):
    value = font_style.render(f"Food Timer: {seconds_left}s", True, WHITE)
    screen.blit(value, [WIDTH // 2 - 50, 10])

def spawn_food():
    fx = round(random.randrange(0, WIDTH - SNAKE_BLOCK * 2) / 10.0) * 10.0
    fy = round(random.randrange(40, HEIGHT - SNAKE_BLOCK * 2) / 10.0) * 10.0
    
    weight = random.choices([1, 3, 5], weights=[70, 20, 10])[0]
    spawn_time = pygame.time.get_ticks() 
    
    return fx, fy, weight, spawn_time

def run_game():
    current_speed = SPEED
    global record
    game_over = False
    game_close = False 
    score = 0
    
    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = 0, 0

    snake_list = []
    length_of_snake = 1
    
    food_x, food_y, food_weight, food_spawn_time = spawn_food()
    food_limit_ms = 10000

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            msg_text = "НОВЫЙ РЕКОРД!" if score >= record else "Ты остался на ретейк!"
            over_msg = font_style.render(f"{msg_text} h - Рестарт, g - Выход", True, RED)
            screen.blit(over_msg, [WIDTH / 4, HEIGHT / 2])
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g: 
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_h:
                        run_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change, y_change = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change, y_change = SNAKE_BLOCK, 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change, x_change = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change, x_change = SNAKE_BLOCK, 0

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True 
       
        x += x_change
        y += y_change
        screen.fill(BLACK)

        current_time = pygame.time.get_ticks()
        time_passed = current_time - food_spawn_time
        
        if time_passed > food_limit_ms:
            food_x, food_y, food_weight, food_spawn_time = spawn_food()
        
        seconds_left = max(0, (food_limit_ms - time_passed) // 1000)
        show_timer(seconds_left)

        food_color = RED
        if food_weight == 3: food_color = BLUE
        elif food_weight == 5: food_color = GOLD

        pygame.draw.circle(screen, food_color, [int(food_x), int(food_y)], SNAKE_BLOCK)

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True 

        for segment in snake_list:
            pygame.draw.circle(screen, GREEN, [segment[0], segment[1]], SNAKE_BLOCK)

        show_score(score)
        show_record(record)
        pygame.display.update()

        if abs(x - food_x) <= 15 and abs(y - food_y) <= 15:
            length_of_snake += food_weight 
            score += food_weight
            current_speed += 2
            
            if score > record:
                record = score
            
            food_x, food_y, food_weight, food_spawn_time = spawn_food()

        clock.tick(current_speed)

    pygame.quit()
    quit()

while not game_started:
    screen.fill(BLACK)
    start_msg = font_style.render("Нажми h для старта, g для выхода", True, GREEN)
    screen.blit(start_msg, [WIDTH / 3, HEIGHT / 2])
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                pygame.quit()
                quit()
            if event.key == pygame.K_h:
                game_started = True
                run_game()