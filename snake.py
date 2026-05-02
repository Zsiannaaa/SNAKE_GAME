import pygame
import random
import sys

pygame.init()

CELL = 20
COLS, ROWS = 30, 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
FPS = 12

BLACK = (15, 15, 25)
DARK = (25, 25, 40)
GRID_COLOR = (30, 30, 50)
SNAKE_HEAD = (80, 220, 120)
SNAKE_BODY = (50, 180, 90)
FOOD_COLOR = (230, 70, 70)
WHITE = (240, 240, 240)
GRAY = (140, 140, 160)
DARK_OVERLAY = (0, 0, 0, 180)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font_large = pygame.font.SysFont("consolas", 48, bold=True)
font_med = pygame.font.SysFont("consolas", 24)
font_small = pygame.font.SysFont("consolas", 18)


def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_rounded_rect(surface, color, rect, radius=4):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h), border_radius=0)
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius), border_radius=0)
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)


def place_food(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos


def main():
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    food = place_food(snake)
    score = 0
    high_score = 0
    game_over = False
    input_queue = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        snake = [(COLS // 2, ROWS // 2)]
                        direction = (1, 0)
                        food = place_food(snake)
                        score = 0
                        game_over = False
                        input_queue.clear()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    continue

                key = event.key
                if key in (pygame.K_UP, pygame.K_w):
                    if len(input_queue) < 2:
                        input_queue.append((0, -1))
                elif key in (pygame.K_DOWN, pygame.K_s):
                    if len(input_queue) < 2:
                        input_queue.append((0, 1))
                elif key in (pygame.K_LEFT, pygame.K_a):
                    if len(input_queue) < 2:
                        input_queue.append((-1, 0))
                elif key in (pygame.K_RIGHT, pygame.K_d):
                    if len(input_queue) < 2:
                        input_queue.append((1, 0))
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if game_over:
            screen.fill(BLACK)
            draw_grid()

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(DARK_OVERLAY)
            screen.blit(overlay, (0, 0))

            go_text = font_large.render("GAME OVER", True, FOOD_COLOR)
            screen.blit(go_text, go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

            score_text = font_med.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 15)))

            high_text = font_med.render(f"Best: {high_score}", True, GRAY)
            screen.blit(high_text, high_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

            restart_text = font_small.render("Press SPACE to restart, ESC to quit", True, GRAY)
            screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 95)))

            pygame.display.flip()
            clock.tick(FPS)
            continue

        if input_queue:
            next_dir = input_queue.pop(0)
            if (next_dir[0] + direction[0], next_dir[1] + direction[1]) != (0, 0):
                direction = next_dir

        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        if (new_head[0] < 0 or new_head[0] >= COLS or
                new_head[1] < 0 or new_head[1] >= ROWS or
                new_head in snake):
            game_over = True
            if score > high_score:
                high_score = score
            continue

        snake.insert(0, new_head)

        if new_head == food:
            score += 10
            food = place_food(snake)
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_grid()

        fx, fy = food
        food_rect = pygame.Rect(fx * CELL + 2, fy * CELL + 2, CELL - 4, CELL - 4)
        pygame.draw.ellipse(screen, FOOD_COLOR, food_rect)

        for i, (sx, sy) in enumerate(snake):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            rect = pygame.Rect(sx * CELL + 1, sy * CELL + 1, CELL - 2, CELL - 2)
            draw_rounded_rect(screen, color, rect, radius=3)

        score_surf = font_med.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 8))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
