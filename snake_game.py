import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
light_green = (170, 215, 81)
dark_green = (162, 209, 73)
blue = (0, 102, 255)
red = (255, 0, 0)
white = (255, 255, 255)

# Screen setup
block_size = 20
cols = 30
rows = 20
width = cols * block_size
height = rows * block_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("🐍 Snake Game by Sarthak")

# Font
font = pygame.font.SysFont("comicsansms", 25)

# Snake and food setup
clock = pygame.time.Clock()
snake = [(5, 5)]
snake_dir = (1, 0)
food = (random.randint(0, cols - 1), random.randint(0, rows - 1))

def draw_board():
    for row in range(rows):
        for col in range(cols):
            color = light_green if (row + col) % 2 == 0 else dark_green
            pygame.draw.rect(screen, color, (col * block_size, row * block_size, block_size, block_size))

def draw_snake():
    for i, (x, y) in enumerate(snake):
        rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
        pygame.draw.rect(screen, blue, rect, border_radius=10)

        if i == len(snake) - 1:
            # Draw eyes on the head based on direction
            cx = x * block_size + block_size // 2
            cy = y * block_size + block_size // 2
            eye_offset = 5
            eye_radius = 3

            dx, dy = snake_dir
            if dx == 1:  # right
                eye1 = (cx + eye_offset, cy - eye_offset)
                eye2 = (cx + eye_offset, cy + eye_offset)
            elif dx == -1:  # left
                eye1 = (cx - eye_offset, cy - eye_offset)
                eye2 = (cx - eye_offset, cy + eye_offset)
            elif dy == 1:  # down
                eye1 = (cx - eye_offset, cy + eye_offset)
                eye2 = (cx + eye_offset, cy + eye_offset)
            else:  # up
                eye1 = (cx - eye_offset, cy - eye_offset)
                eye2 = (cx + eye_offset, cy - eye_offset)

            pygame.draw.circle(screen, white, eye1, eye_radius)
            pygame.draw.circle(screen, white, eye2, eye_radius)

def draw_food():
    x, y = food
    pygame.draw.circle(screen, red, (x * block_size + block_size // 2, y * block_size + block_size // 2), block_size // 2 - 2)

def show_score():
    score_text = font.render(f"Score: {len(snake) - 1}", True, white)
    screen.blit(score_text, [10, 10])

def game_over():
    # Dark transparent overlay
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Game Over Text
    game_over_font = pygame.font.SysFont("comicsansms", 50, bold=True)
    info_font = pygame.font.SysFont("comicsansms", 28)

    game_text = game_over_font.render("GAME OVER", True, red)
    info_text = info_font.render("Press R to Restart or Q to Quit", True, white)

    game_rect = game_text.get_rect(center=(width // 2, height // 2 - 40))
    info_rect = info_text.get_rect(center=(width // 2, height // 2 + 20))

    screen.blit(game_text, game_rect)
    screen.blit(info_text, info_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_r:
                    return True

# Main game loop
running = True
while running:
    clock.tick(7)  # ← SLOWER speed here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Direction control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake_dir != (1, 0):
        snake_dir = (-1, 0)
    elif keys[pygame.K_RIGHT] and snake_dir != (-1, 0):
        snake_dir = (1, 0)
    elif keys[pygame.K_UP] and snake_dir != (0, 1):
        snake_dir = (0, -1)
    elif keys[pygame.K_DOWN] and snake_dir != (0, -1):
        snake_dir = (0, 1)

    # Move snake
    head = (snake[-1][0] + snake_dir[0], snake[-1][1] + snake_dir[1])
    if head in snake or not (0 <= head[0] < cols and 0 <= head[1] < rows):
        if not game_over():
            break
        else:
            snake = [(5, 5)]
            snake_dir = (1, 0)
            food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            continue

    snake.append(head)
    if head == food:
        food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
    else:
        snake.pop(0)

    # Drawing
    draw_board()
    draw_snake()
    draw_food()
    show_score()
    pygame.display.update()

pygame.quit()
