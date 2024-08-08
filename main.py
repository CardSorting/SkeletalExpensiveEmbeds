import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Paddle
paddle_width, paddle_height = 100, 20
paddle = pygame.Rect(width // 2 - paddle_width // 2, height - 40, paddle_width, paddle_height)

# Ball
ball_size = 20
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)
ball_speed_x, ball_speed_y = 5, -5

# Bricks
brick_width, brick_height = 80, 30
bricks = [pygame.Rect(col * (brick_width + 5), row * (brick_height + 5), brick_width, brick_height) for row in range(5) for col in range(10)]

def reset_game():
    global paddle, ball, ball_speed_x, ball_speed_y, bricks
    paddle = pygame.Rect(width // 2 - paddle_width // 2, height - 40, paddle_width, paddle_height)
    ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)
    ball_speed_x, ball_speed_y = 5, -5
    bricks = [pygame.Rect(col * (brick_width + 5), row * (brick_height + 5), brick_width, brick_height) for row in range(5) for col in range(10)]

def show_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    continue_text = font.render("Press SPACE to play again or Q to quit", True, WHITE)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
    screen.blit(continue_text, (width // 2 - continue_text.get_width() // 2, height // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:
                    return False
    return False

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 7
    if keys[pygame.K_RIGHT] and paddle.right < width:
        paddle.x += 7

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball.bottom >= height:
        if show_game_over_screen():
            reset_game()
        else:
            running = False
        continue

    # Ball collision with paddle
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y = -ball_speed_y
        ball_speed_x += random.randint(-2, 2)

    # Ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
            break

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddle
    pygame.draw.rect(screen, BLUE, paddle)

    # Draw ball
    pygame.draw.rect(screen, WHITE, ball)

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()