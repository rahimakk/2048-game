import pygame
import random
import sys
import os
import json
from copy import deepcopy

pygame.init()

# Constants
SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH = SIZE * TILE_SIZE + (SIZE + 1) * MARGIN
HEIGHT = WIDTH + 150
TIMER_LIMIT = 180
FPS = 60

FONT = pygame.font.SysFont("arial", 36)
SMALL_FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 48)

THEMES = {
    "green": {
        "bg": (187, 173, 160),
        "text": (0, 0, 0),
        "tiles": {
            0: (45, 90, 60), 2: (102, 204, 153), 4: (76, 175, 80),
            8: (0, 150, 136), 16: (33, 150, 243), 32: (30, 136, 229),
            64: (25, 118, 210), 128: (0, 105, 92), 256: (0, 77, 64),
            512: (51, 105, 30), 1024: (85, 139, 47), 2048: (104, 159, 56)
        }
    },
    "blue": {
        "bg": (30, 30, 60),
        "text": (255, 255, 255),
        "tiles": {
            0: (20, 30, 60), 2: (70, 130, 180), 4: (100, 149, 237),
            8: (65, 105, 225), 16: (30, 144, 255), 32: (0, 191, 255),
            64: (0, 154, 205), 128: (25, 25, 112), 256: (0, 0, 128),
            512: (0, 0, 139), 1024: (72, 61, 139), 2048: (106, 90, 205)
        }
    }
}

theme = "green"
board = [[0] * SIZE for _ in range(SIZE)]
score = 0
undo_stack = []
paused = False
game_over = False
start_ticks = pygame.time.get_ticks()
last_time_left = TIMER_LIMIT

high_score_file = "highscore.txt"
save_file = "savefile.json"
high_score = int(open(high_score_file).read()) if os.path.exists(high_score_file) else 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

# Buttons
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30
button_color = (100, 100, 100)
button_text_color = (255, 255, 255)
buttons = {
    "Undo": pygame.Rect(10, 20, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Theme": pygame.Rect(10 + BUTTON_WIDTH + 10, 20, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Pause": pygame.Rect(10 + 2*(BUTTON_WIDTH + 10), 20, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Save": pygame.Rect(10 + 3*(BUTTON_WIDTH + 10), 20, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Load": pygame.Rect(10 + 4*(BUTTON_WIDTH + 10), 20, BUTTON_WIDTH, BUTTON_HEIGHT)
}



def draw_buttons():
    for text, rect in buttons.items():
        pygame.draw.rect(screen, button_color, rect, border_radius=5)
        label = SMALL_FONT.render(text, True, button_text_color)
        screen.blit(label, label.get_rect(center=rect.center))

def draw_board():
    screen.fill(THEMES[theme]["bg"])
    draw_buttons()
    for i in range(SIZE):
        for j in range(SIZE):
            val = board[i][j]
            color = THEMES[theme]["tiles"].get(val, (60, 58, 50))
            rect = pygame.Rect(
                j * TILE_SIZE + (j + 1) * MARGIN,
                i * TILE_SIZE + (i + 1) * MARGIN + 80,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(screen, color, rect, border_radius=8)
            if val != 0:
                text = FONT.render(str(val), True, THEMES[theme]["text"])
                screen.blit(text, text.get_rect(center=rect.center))

    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000 if not paused else 0
    time_left = max(0, TIMER_LIMIT - elapsed)
    screen.blit(SMALL_FONT.render(f"Score: {score}", True, (0, 0, 0)), (WIDTH - 200, HEIGHT - 60))
    screen.blit(SMALL_FONT.render(f"High Score: {high_score}", True, (0, 0, 0)), (WIDTH - 200, HEIGHT - 30))
    screen.blit(SMALL_FONT.render(f"Time Left: {time_left}s", True, (255, 0, 0)), (20, HEIGHT - 60))

    if paused:
        screen.blit(BIG_FONT.render("Paused", True, (255, 255, 255)),
                    (WIDTH // 2 - 80, HEIGHT // 2))

    if game_over or time_left <= 0:
        screen.blit(BIG_FONT.render("Game Over", True, (255, 0, 0)),
                    (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()

def add_tile():
    empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        board[i][j] = 2 if random.random() < 0.9 else 4

def can_move():
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                return True
            if j < SIZE - 1 and board[i][j] == board[i][j + 1]:
                return True
            if i < SIZE - 1 and board[i][j] == board[i + 1][j]:
                return True
    return False

def rotate(clockwise=True):
    return [[board[j][i] if clockwise else board[SIZE - 1 - j][i] for j in range(SIZE)] for i in range(SIZE)]

def move_left():
    global score
    moved = False
    for row in board:
        tight = [i for i in row if i != 0]
        merged = []
        skip = False
        for i in range(len(tight)):
            if skip:
                skip = False
                continue
            if i+1 < len(tight) and tight[i] == tight[i+1]:
                merged.append(tight[i]*2)
                score += tight[i]*2
                skip = True
            else:
                merged.append(tight[i])
        while len(merged) < SIZE:
            merged.append(0)
        if merged != row:
            moved = True
        row[:] = merged
    return moved

def save_state():
    undo_stack.append((deepcopy(board), score))

def save_game():
    with open(save_file, "w") as f:
        json.dump({"board": board, "score": score}, f)

def load_game():
    global board, score
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            data = json.load(f)
            board[:] = data["board"]
            score = data["score"]

# Game start
board = [[0]*SIZE for _ in range(SIZE)]
add_tile()
add_tile()

while True:
    clock.tick(FPS)
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open(high_score_file, "w") as f:
                f.write(str(max(score, high_score)))
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for name, rect in buttons.items():
                if rect.collidepoint(x, y):
                    if name == "Undo" and undo_stack:
                        board[:], score = undo_stack.pop()
                    elif name == "Theme":
                        theme = "blue" if theme == "green" else "green"
                    elif name == "Pause":
                        paused = not paused
                        if paused:
                            last_time_left = max(0, TIMER_LIMIT - (pygame.time.get_ticks() - start_ticks) // 1000)
                        else:
                            start_ticks = pygame.time.get_ticks() - (TIMER_LIMIT - last_time_left) * 1000
                    elif name == "Save":
                        save_game()
                    elif name == "Load":
                        load_game()

        elif event.type == pygame.KEYDOWN and not paused:
            moved = False
            save_state()
            if event.key == pygame.K_LEFT:
                moved = move_left()
            elif event.key == pygame.K_RIGHT:
                board[:] = rotate(True)
                board[:] = rotate(True)
                moved = move_left()
                board[:] = rotate(True)
                board[:] = rotate(True)
            elif event.key == pygame.K_UP:
                board[:] = rotate(False)
                moved = move_left()
                board[:] = rotate(True)
            elif event.key == pygame.K_DOWN:
                board[:] = rotate(True)
                moved = move_left()
                board[:] = rotate(False)

            if moved:
                add_tile()

    if not can_move() or (not paused and (pygame.time.get_ticks() - start_ticks) // 1000 >= TIMER_LIMIT):
        game_over = True
