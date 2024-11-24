import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
paddle_speed = 7

# Ball settings
BALL_RADIUS = 10
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = 4 * random.choice([-1, 1])
ball_dy = -4

# Brick settings
BRICK_WIDTH = 60
BRICK_HEIGHT = 30
bricks = []

# Game clock
clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont("Arial", 24)

# Function to draw the paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw the ball
def draw_ball(x, y):
    pygame.draw.circle(screen, GREEN, (x, y), BALL_RADIUS)

# Function to create the bricks
def create_bricks():
    rows = 5
    cols = SCREEN_WIDTH // BRICK_WIDTH
    for row in range(rows):
        for col in range(cols):
            brick_x = col * BRICK_WIDTH
            brick_y = row * BRICK_HEIGHT
            brick_rect = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick_rect)

# Function to draw the bricks
def draw_bricks():
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

# Function to update the ball's position
def update_ball(x, y, dx, dy):
    x += dx
    y += dy
    return x, y

# Function to check for collision with the paddle
def check_paddle_collision(ball_rect, paddle_rect):
    return ball_rect.colliderect(paddle_rect)

# Function to check for collision with bricks
def check_brick_collision(ball_rect):
    global bricks
    for brick in bricks:
        if ball_rect.colliderect(brick):
            bricks.remove(brick)
            return True
    return False

# Function to draw the score
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Main game loop
def game_loop():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, bricks

    create_bricks()
    score = 0
    game_over = False

    while not game_over:
        screen.fill(BLACK)  # Clear screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed

        # Update ball position
        ball_x, ball_y = update_ball(ball_x, ball_y, ball_dx, ball_dy)

        # Ball-wall collision
        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= SCREEN_WIDTH:
            ball_dx = -ball_dx
        if ball_y - BALL_RADIUS <= 0:
            ball_dy = -ball_dy

        # Ball-paddle collision
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        if check_paddle_collision(ball_rect, paddle_rect):
            ball_dy = -ball_dy

        # Ball-brick collision
        if check_brick_collision(ball_rect):
            ball_dy = -ball_dy
            score += 10  # Increase score when a brick is broken

        # Check if ball falls below the paddle (game over)
        if ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
            game_over = True

        # Draw everything
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        draw_bricks()
        draw_score(score)

        # Check for win (if no bricks are left)
        if len(bricks) == 0:
            game_over = True
            score += 100  # Bonus for clearing all bricks

        pygame.display.update()  # Update display
        clock.tick(60)  # Limit frame rate

    # Game over screen
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(3000)  # Wait for 3 seconds before closing the game

    pygame.quit()


# Run the game
game_loop()
