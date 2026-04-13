import pygame
import os

pygame.init()
pygame.mixer.init() 

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Музыкальный плеер")

font_main = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

MUSIC_FOLDER = "music"
playlist = []
current_track_index = 0
status = "Остановлено" 
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)
    print(f"Папка '{MUSIC_FOLDER}' создана. Пожалуйста, добавьте туда музыку (MP3/WAV).")

for file in os.listdir(MUSIC_FOLDER):
    if file.lower().endswith(('.mp3', '.wav')):
        playlist.append(file)

def play_track(index):
    global status
    if not playlist:
        return
    
    track_path = os.path.join(MUSIC_FOLDER, playlist[index])
    try:
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        status = "Играет"
    except pygame.error as e:
        print(f"Ошибка загрузки трека: {e}")

def format_time(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def draw_ui():
    screen.fill(BLACK) 
    
    if not playlist:
        text = font_main.render("Папка 'music' пуста! Добавьте MP3/WAV.", True, RED)
        screen.blit(text, (20, HEIGHT // 2))
    else:
        track_name = playlist[current_track_index]
        title_text = font_main.render(f"Сейчас играет: {track_name}", True, WHITE)
        screen.blit(title_text, (20, 30))
        
        color = GREEN if status == "Играет" else (WHITE if status == "Пауза" else RED)
        status_text = font_main.render(f"Статус: {status}", True, color)
        screen.blit(status_text, (20, 80))
        
        if status in ["Играет", "Пауза"]:
            current_time = pygame.mixer.music.get_pos() 
            if current_time >= 0:
                time_text = font_main.render(f"Время: {format_time(current_time)}", True, WHITE)
                screen.blit(time_text, (20, 130))

    instructions = [
        "[P] - Играть / Пауза",
        "[S] - Стоп",
        "[N] - Следующий трек",
        "[B] - Предыдущий трек",
        "[Q] - Выход"
    ]
    
    y_offset = 220
    for line in instructions:
        inst_text = font_small.render(line, True, WHITE)
        screen.blit(inst_text, (20, y_offset))
        y_offset += 30

    pygame.display.flip() 

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                
            elif playlist: 
                if event.key == pygame.K_p:
                    if status == "Остановлено":
                        play_track(current_track_index)
                    elif status == "Играет":
                        pygame.mixer.music.pause()
                        status = "Пауза"
                    elif status == "Пауза":
                        pygame.mixer.music.unpause()
                        status = "Играет"
                        
                elif event.key == pygame.K_s:
                    pygame.mixer.music.stop()
                    status = "Остановлено"
                    
                elif event.key == pygame.K_n:
                    current_track_index = (current_track_index + 1) % len(playlist)
                    play_track(current_track_index)
                    
                elif event.key == pygame.K_b:
                    current_track_index = (current_track_index - 1) % len(playlist)
                    play_track(current_track_index)

    draw_ui()

pygame.mixer.quit()
pygame.quit()