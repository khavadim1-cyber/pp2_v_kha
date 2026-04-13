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
BLACK = (0, 0, 0)
font_style = pygame.font.SysFont("bahnschrift", 25)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Escape from KBTU')

clock = pygame.time.Clock()
game_started=False


def show_score(current_score):
    value = font_style.render("Score: " + str(current_score), True, YELLOW)
    screen.blit(value, [10, 10])
def show_record(current_record):
    value = font_style.render("Record: " + str(current_record), True, YELLOW)
    screen.blit(value, [700, 10])
record =0
def run_game():
    current_speed=SPEED

    global record
    game_over = False
    game_close = False 
    score = 0
    
    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = 0, 0

    snake_list = []
    length_of_snake = 1
    

    food_x = round(random.randrange(0, WIDTH - 70) / 15.0) * 15.0
    food_y = round(random.randrange(0, HEIGHT - 70) / 15.0) * 15.0
    
    while not game_over:
        while game_close == True and score < record:
            screen.fill(BLACK)
            over_msg = font_style.render("Ты остался на ретейк! h - Рестарт, g - Выход", True, RED)
            screen.blit(over_msg, [WIDTH / 4, HEIGHT / 2])
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g: 
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_h:
                        run_game()
        while game_close == True and score >= record:
            screen.fill(BLACK)
            over_msg = font_style.render("НОВЫЙ РЕКОРД! h - Рестарт, g - Выход", True, RED)
            screen.blit(over_msg, [WIDTH / 4, HEIGHT / 2])
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g: 
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_h: 
                        run_game() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -SNAKE_BLOCK 
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -SNAKE_BLOCK
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = SNAKE_BLOCK
                    x_change = 0

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True 
       
        x += x_change
        y += y_change
        screen.fill(BLACK)
        show_score(score)
        show_record(record)

        pygame.draw.circle(screen, RED, [int(food_x), int(food_y)], SNAKE_BLOCK )

        snake_head = [x, y]
        snake_list.append(snake_head)
        
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True # 

        for segment in snake_list:
            pygame.draw.circle(screen, GREEN, [segment[0], segment[1]], SNAKE_BLOCK)

        pygame.display.update()

        
        if abs(x - food_x) <= 25 and abs(y - food_y) <= 25:
            food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK * 2) / 10.0) * 10.0
            food_y = round(random.randrange(10, HEIGHT - SNAKE_BLOCK*2)  / 10.0) * 10.0

            length_of_snake += 1
            score +=1
            current_speed+=1


            if score > record:
                record = score

        clock.tick(current_speed)

    pygame.quit()
    quit()
while not game_started:
        screen.fill(BLACK)
        start_msg = font_style.render("Нажми h для старта g для выхода", True, GREEN)
        screen.blit(start_msg, [WIDTH / 3, HEIGHT / 2])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game_over = True
                    game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    run_game()
                    game_started=True