import pygame
import time
import random
import json
import os
import psycopg2
from datetime import datetime

pygame.init()

# ── Constants ──────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 800, 800
SNAKE_BLOCK = 10

# INCREASED SPEED: Base speed is 25 for faster gameplay
BASE_SPEED = 25 
# MASSIVE EAT RADIUS: Snake can eat items from very far away (40px)
EAT_RADIUS = 40 

SETTINGS_FILE = "settings.json"

# Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
YELLOW     = (255, 255, 102)
GREEN      = (0,   200, 0)
RED        = (213, 50,  80)
DARK_RED   = (120, 0,   20)
BLUE       = (50,  153, 213)
GOLD       = (255, 215, 0)
PURPLE     = (180, 0,   255)
CYAN       = (0,   255, 220)
ORANGE     = (255, 140, 0)
GRAY       = (80,  80,  80)
DARK_GRAY  = (30,  30,  30)
LIGHT_GRAY = (180, 180, 180)

# Power-up type constants
PU_SPEED  = "speed_boost"
PU_SLOW   = "slow_motion"
PU_SHIELD = "shield"
PU_COLORS = {PU_SPEED: CYAN, PU_SLOW: PURPLE, PU_SHIELD: ORANGE}

# ── Fonts ──────────────────────────────────────────────────────────────────────
font_sm   = pygame.font.SysFont("bahnschrift", 20)
font_md   = pygame.font.SysFont("bahnschrift", 28)
font_lg   = pygame.font.SysFont("bahnschrift", 42)
font_xl   = pygame.font.SysFont("bahnschrift", 60)
font_input = pygame.font.SysFont("bahnschrift", 32)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape from KBTU")
clock = pygame.time.Clock()

# ── Settings ───────────────────────────────────────────────────────────────────
DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 0],
    "grid_overlay": False
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

settings = load_settings()

# ── Database ───────────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     os.getenv("DB_PORT",     "5432"),
    "dbname":   os.getenv("DB_NAME",     "snake_db"),
    "user":     os.getenv("DB_USER",     "vadimkha"),
    "password": os.getenv("DB_PASSWORD", "3141566261023"),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id       SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id            SERIAL PRIMARY KEY,
                player_id     INTEGER REFERENCES players(id),
                score         INTEGER   NOT NULL,
                level_reached INTEGER   NOT NULL,
                played_at     TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB] init error: {e}")
        return False

def get_or_create_player(username):
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;", (username,))
        conn.commit()
        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        pid = cur.fetchone()[0]
        cur.close(); conn.close()
        return pid
    except Exception as e:
        print(f"[DB] get_or_create error: {e}")
        return None

def save_game_session(player_id, score, level_reached):
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);",
            (player_id, score, level_reached)
        )
        conn.commit()
        cur.close(); conn.close()
    except Exception as e:
        print(f"[DB] save session error: {e}")

def get_personal_best(player_id):
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s;", (player_id,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return row[0] if row and row[0] is not None else 0
    except Exception as e:
        print(f"[DB] personal best error: {e}")
        return 0

def get_leaderboard():
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC
            LIMIT 10;
        """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception as e:
        print(f"[DB] leaderboard error: {e}")
        return []

db_available = init_db()

# ── Helpers ────────────────────────────────────────────────────────────────────
def draw_text(text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)

def draw_button(text, rect, color, hover_color, font=font_md):
    mx, my = pygame.mouse.get_pos()
    col = hover_color if rect.collidepoint(mx, my) else color
    pygame.draw.rect(screen, col, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    draw_text(text, font, WHITE, rect.centerx, rect.centery, center=True)
    return rect.collidepoint(mx, my)

def draw_grid():
    for x in range(0, WIDTH, SNAKE_BLOCK):
        pygame.draw.line(screen, (25, 25, 25), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, SNAKE_BLOCK):
        pygame.draw.line(screen, (25, 25, 25), (0, y), (WIDTH, y))

def snap(v):
    return round(v / SNAKE_BLOCK) * SNAKE_BLOCK

def random_pos(exclude=None, margin_top=40):
    for _ in range(300):
        x = snap(random.randrange(0, WIDTH  - SNAKE_BLOCK))
        y = snap(random.randrange(margin_top, HEIGHT - SNAKE_BLOCK))
        if exclude is None or (x, y) not in exclude:
            return x, y
    return snap(WIDTH // 2), snap(HEIGHT // 2)

# ── Username input screen ──────────────────────────────────────────────────────
def username_screen():
    username = ""
    error    = ""
    cursor_visible = True
    cursor_timer   = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()
        if now - cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer   = now

        screen.fill(BLACK)
        draw_text("ESCAPE FROM KBTU", font_xl, YELLOW, WIDTH//2, 180, center=True)
        draw_text("Enter your username:", font_md, WHITE, WIDTH//2, 290, center=True)

        box = pygame.Rect(WIDTH//2 - 180, 330, 360, 48)
        pygame.draw.rect(screen, DARK_GRAY, box, border_radius=6)
        pygame.draw.rect(screen, YELLOW,    box, 2, border_radius=6)
        display_name = username + ("|" if cursor_visible else " ")
        draw_text(display_name, font_input, WHITE, box.x + 12, box.y + 8)

        if error:
            draw_text(error, font_sm, RED, WIDTH//2, 395, center=True)

        btn = pygame.Rect(WIDTH//2 - 100, 430, 200, 50)
        draw_button("START", btn, GRAY, GREEN)

        draw_text("Press ENTER or click START", font_sm, LIGHT_GRAY, WIDTH//2, 500, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = username.strip()
                    if len(name) < 1: error = "Username cannot be empty!"
                    elif len(name) > 50: error = "Username too long!"
                    else: return name
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 50 and event.unicode.isprintable():
                        username += event.unicode
                error = ""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event.pos):
                    name = username.strip()
                    if len(name) < 1: error = "Username cannot be empty!"
                    else: return name
        clock.tick(60)

# ── Main Menu ──────────────────────────────────────────────────────────────────
def main_menu():
    while True:
        screen.fill(BLACK)
        if settings.get("grid_overlay"): draw_grid()

        draw_text("ESCAPE FROM KBTU", font_xl, YELLOW, WIDTH//2, 140, center=True)

        btn_play  = pygame.Rect(WIDTH//2 - 120, 260, 240, 55)
        btn_lb    = pygame.Rect(WIDTH//2 - 120, 330, 240, 55)
        btn_set   = pygame.Rect(WIDTH//2 - 120, 400, 240, 55)
        btn_quit  = pygame.Rect(WIDTH//2 - 120, 470, 240, 55)

        draw_button("PLAY",        btn_play, GRAY, GREEN)
        draw_button("LEADERBOARD", btn_lb,   GRAY, BLUE)
        draw_button("SETTINGS",    btn_set,  GRAY, PURPLE)
        draw_button("QUIT",        btn_quit, GRAY, RED)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.collidepoint(event.pos):  return "play"
                if btn_lb.collidepoint(event.pos):    return "leaderboard"
                if btn_set.collidepoint(event.pos):   return "settings"
                if btn_quit.collidepoint(event.pos):  pygame.quit(); quit()
        clock.tick(60)

# ── Leaderboard screen ─────────────────────────────────────────────────────────
def leaderboard_screen():
    rows = get_leaderboard()
    while True:
        screen.fill(BLACK)
        draw_text("🏆  TOP 10 LEADERBOARD", font_lg, GOLD, WIDTH//2, 40, center=True)

        headers = ["#", "Username", "Score", "Level", "Date"]
        col_x   = [40, 100, 390, 490, 570]
        for i, h in enumerate(headers):
            draw_text(h, font_sm, YELLOW, col_x[i], 100)
        pygame.draw.line(screen, YELLOW, (30, 122), (770, 122), 1)

        if not rows:
            draw_text("No records yet.", font_md, LIGHT_GRAY, WIDTH//2, 300, center=True)
        else:
            for i, (uname, score, level, played_at) in enumerate(rows):
                y = 135 + i * 52
                col = [GOLD, LIGHT_GRAY, GRAY][min(i, 2)] if i < 3 else WHITE
                date_str = played_at.strftime("%Y-%m-%d") if isinstance(played_at, datetime) else str(played_at)[:10]
                draw_text(str(i+1), font_sm, col, col_x[0], y)
                draw_text(str(uname)[:18], font_sm, WHITE, col_x[1], y)
                draw_text(str(score), font_sm, WHITE, col_x[2], y)
                draw_text(str(level), font_sm, WHITE, col_x[3], y)
                draw_text(date_str, font_sm, WHITE, col_x[4], y)

        btn_back = pygame.Rect(WIDTH//2 - 100, 740, 200, 48)
        draw_button("BACK", btn_back, GRAY, RED)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos): return
        clock.tick(60)

# ── Settings screen ────────────────────────────────────────────────────────────
COLOR_PRESETS = [
    ("Green",   (0,   200, 0)),
    ("Cyan",    (0,   230, 220)),
    ("Yellow",  (255, 230, 0)),
    ("Orange",  (255, 140, 0)),
    ("White",   (240, 240, 240)),
]

def settings_screen():
    global settings
    local = settings.copy()
    selected_color_idx = 0
    for i, (_, c) in enumerate(COLOR_PRESETS):
        if list(c) == local["snake_color"]:
            selected_color_idx = i; break

    while True:
        screen.fill(BLACK)
        draw_text("SETTINGS", font_lg, YELLOW, WIDTH//2, 50, center=True)

        draw_text("Grid Overlay:", font_md, WHITE, 100, 160)
        btn_grid = pygame.Rect(440, 155, 130, 44)
        lbl_grid = "ON" if local["grid_overlay"] else "OFF"
        col_grid = GREEN if local["grid_overlay"] else RED
        draw_button(lbl_grid, btn_grid, col_grid, col_grid)

        draw_text("Snake Color:", font_md, WHITE, 100, 250)
        color_rects = []
        for i, (name, col) in enumerate(COLOR_PRESETS):
            r = pygame.Rect(100 + i * 120, 300, 100, 40)
            color_rects.append(r)
            pygame.draw.rect(screen, col, r, border_radius=6)
            if i == selected_color_idx:
                pygame.draw.rect(screen, WHITE, r, 3, border_radius=6)
            draw_text(name, font_sm, BLACK, r.centerx, r.centery, center=True)

        btn_save = pygame.Rect(WIDTH//2 - 130, 560, 260, 52)
        draw_button("SAVE & BACK", btn_save, GRAY, GREEN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_grid.collidepoint(event.pos):
                    local["grid_overlay"] = not local["grid_overlay"]
                for i, r in enumerate(color_rects):
                    if r.collidepoint(event.pos):
                        selected_color_idx = i
                        local["snake_color"] = list(COLOR_PRESETS[i][1])
                if btn_save.collidepoint(event.pos):
                    settings = local
                    save_settings(settings)
                    return
        clock.tick(60)

# ── Game Over screen ───────────────────────────────────────────────────────────
def game_over_screen(score, level, personal_best):
    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", font_xl, RED, WIDTH//2, 140, center=True)
        draw_text(f"Score: {score}", font_md, WHITE, WIDTH//2, 240, center=True)
        draw_text(f"Level: {level}", font_md, WHITE, WIDTH//2, 285, center=True)
        draw_text(f"Best:  {personal_best}", font_md, YELLOW, WIDTH//2, 330, center=True)

        btn_retry = pygame.Rect(WIDTH//2 - 220, 450, 200, 52)
        btn_menu  = pygame.Rect(WIDTH//2 + 20,  450, 200, 52)
        draw_button("RETRY", btn_retry, GRAY, GREEN)
        draw_button("MAIN MENU", btn_menu, GRAY, BLUE)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(event.pos): return "retry"
                if btn_menu.collidepoint(event.pos):  return "menu"
        clock.tick(60)

# ── Obstacle generation ────────────────────────────────────────────────────────
def generate_obstacles(level, snake_pos):
    # FEWER WALLS: Reduced base count and level multiplier
    count = 3 + (level * 2) 
    obstacles = set()
    sx, sy = snake_pos
    
    for _ in range(count * 20):
        # We add 4 blocks for every 1 wall (to make it a 20x20 block)
        if len(obstacles) >= count * 4: 
            break
            
        ox = snap(random.randrange(0, WIDTH - 20))
        oy = snap(random.randrange(40, HEIGHT - 20))
        
        # Keep walls away from the snake's spawn point
        if abs(ox - sx) <= 60 and abs(oy - sy) <= 60: 
            continue
            
        # Add a 2x2 block to make the wall larger (20x20)
        obstacles.add((ox, oy))
        obstacles.add((ox + SNAKE_BLOCK, oy))
        obstacles.add((ox, oy + SNAKE_BLOCK))
        obstacles.add((ox + SNAKE_BLOCK, oy + SNAKE_BLOCK))
        
    return obstacles

# ── Main game ──────────────────────────────────────────────────────────────────
def run_game(username, player_id, personal_best_ref):
    snake_color = tuple(settings["snake_color"])
    current_speed = BASE_SPEED
    score, level = 0, 1
    points_for_next_level = 10

    x, y = snap(WIDTH // 2), snap(HEIGHT // 2)
    x_change, y_change = 0, 0
    snake_list = [[x, y]]
    length_of_snake = 1
    obstacles = generate_obstacles(level, (x, y))

    def excluded(): return set(map(tuple, snake_list)) | obstacles

    def spawn_food():
        fx, fy = random_pos(excluded())
        w = random.choices([1, 3, 5], weights=[70, 20, 10])[0]
        return fx, fy, w, pygame.time.get_ticks()

    food_x, food_y, food_weight, food_spawn_time = spawn_food()
    
    # Fixed unpacking bug here
    px, py = random_pos(excluded())
    poison_x, poison_y, poison_spawn = px, py, pygame.time.get_ticks()

    pu_active = False
    pu_x, pu_y, pu_type, pu_spawn = 0, 0, PU_SPEED, 0
    active_effect, effect_start, shield_ready = None, 0, False

    running = True
    while running:
        now = pygame.time.get_ticks()

        if not pu_active and random.random() < 0.01:
            pu_x, pu_y = random_pos(excluded())
            pu_type = random.choice([PU_SPEED, PU_SLOW, PU_SHIELD])
            pu_spawn, pu_active = now, True

        if active_effect in (PU_SPEED, PU_SLOW) and (now - effect_start) > 5000:
            current_speed = BASE_SPEED + (level - 1) * 2
            active_effect = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT  and x_change == 0: x_change, y_change = -10, 0
                elif event.key == pygame.K_RIGHT and x_change == 0: x_change, y_change = 10, 0
                elif event.key == pygame.K_UP and y_change == 0: x_change, y_change = 0, -10
                elif event.key == pygame.K_DOWN and y_change == 0: x_change, y_change = 0, 10

        x += x_change
        y += y_change

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0 or (x, y) in obstacles:
            if shield_ready:
                if (x,y) in obstacles: x -= x_change; y -= y_change
                else: x = max(0, min(x, WIDTH-10)); y = max(0, min(y, HEIGHT-10))
                shield_ready = False
            else: break

        screen.fill(BLACK)
        if settings.get("grid_overlay"): draw_grid()
        
        # Drawing obstacles (they are generated in blocks of 4)
        for (ox, oy) in obstacles: 
            pygame.draw.rect(screen, GRAY, (ox, oy, 10, 10))

        if now - food_spawn_time > 10000: food_x, food_y, food_weight, food_spawn_time = spawn_food()
        pygame.draw.circle(screen, {1: RED, 3: BLUE, 5: GOLD}[food_weight], (food_x, food_y), 10)
        pygame.draw.circle(screen, DARK_RED, (poison_x, poison_y), 10)

        if pu_active:
            pygame.draw.rect(screen, PU_COLORS[pu_type], (pu_x, pu_y, 10, 10))
            if now - pu_spawn > 8000: pu_active = False

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake: del snake_list[0]

        for seg in snake_list[:-1]:
            if seg == snake_head:
                if shield_ready: shield_ready = False
                else: running = False

        for seg in snake_list: pygame.draw.circle(screen, snake_color, (seg[0], seg[1]), 10)

        draw_text(f"Score: {score}  Level: {level}", font_sm, YELLOW, 10, 10)
        if shield_ready: draw_text("🛡 SHIELD", font_sm, ORANGE, WIDTH-100, 10)

        pygame.display.update()

        # MASSIVE EAT RADIUS logic applied here for Food
        if abs(x - food_x) < EAT_RADIUS and abs(y - food_y) < EAT_RADIUS:
            score += food_weight; length_of_snake += food_weight
            if score >= points_for_next_level:
                level += 1; points_for_next_level += 20
                current_speed = BASE_SPEED + (level - 1) * 3  # Scales slightly faster
                obstacles = generate_obstacles(level, (x, y))
            food_x, food_y, food_weight, food_spawn_time = spawn_food()

        # MASSIVE EAT RADIUS logic applied here for Poison
        if abs(x - poison_x) < EAT_RADIUS and abs(y - poison_y) < EAT_RADIUS:
            length_of_snake = max(1, length_of_snake - 2)
            px, py = random_pos(excluded())
            poison_x, poison_y = px, py

        # MASSIVE EAT RADIUS logic applied here for Power-ups
        if pu_active and abs(x - pu_x) < EAT_RADIUS and abs(y - pu_y) < EAT_RADIUS:
            if pu_type == PU_SPEED: current_speed += 7; active_effect = PU_SPEED
            elif pu_type == PU_SLOW: current_speed = max(5, current_speed - 7); active_effect = PU_SLOW
            elif pu_type == PU_SHIELD: shield_ready = True
            effect_start, pu_active = now, False

        clock.tick(current_speed)
    return score, level

def main():
    username = username_screen()
    player_id = get_or_create_player(username) if db_available else None
    pb = [get_personal_best(player_id) if player_id else 0]

    while True:
        action = main_menu()
        if action == "leaderboard": leaderboard_screen()
        elif action == "settings": settings_screen()
        elif action == "play":
            while True:
                s, l = run_game(username, player_id, pb)
                if player_id:
                    save_game_session(player_id, s, l)
                    pb[0] = get_personal_best(player_id)
                if game_over_screen(s, l, pb[0]) == "menu": break

if __name__ == "__main__":
    main()