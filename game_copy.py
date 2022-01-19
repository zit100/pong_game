import pygame, sys, random


def ball_animation():
    global ball_speed_x, ball_speed_y

    # Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Borders collison
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_restart()

    # Paddles collison
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def player_animation():
    # Move player
    player.y += player_speed

    # Prevent collisions
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    # Move opponent
    opponent.y += player_speed

    # Prevent collisions
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def opponent_ai():
    # Move opponent
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    # Prevent collisions
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y

    # Move ball to screen center
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 25, 25)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 100)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 100)

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Speeds of the ball
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
# Speeds of the paddles
player_speed = 0
opponent_speed = 10

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        # Key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_ai()

    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)