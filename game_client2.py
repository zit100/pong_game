import pygame, sys, random, socket, select, threading


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
    global opponent_speed

    # Move opponent
    opponent.y += opponent_speed

    # Prevent collisions
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def opponent_ai():
    # Move opponent
    if opponent.top < ball.y:
        opponent.top += opponent_ai_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_ai_speed
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


def infiniteloop1():
    global opponent_speed

    while True:
        rlist, wlist, xlist = select.select([my_socket], [], [])
        if my_socket in rlist:
            opponent_speed = int(my_socket.recv(MAX_MSG_LENGTH).decode())


def infiniteloop2():
    while True:
        rlist, wlist, xlist = select.select([], [my_socket], [])
        for msg in messages_to_send:
            if my_socket in wlist:
                my_socket.send(msg.encode())
                messages_to_send.remove(msg)


# Network setup
MAX_MSG_LENGTH = 1024

my_socket = socket.socket()
my_socket.connect(("192.168.56.1", 5555))

messages_to_send = []
message = ""

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
opponent_speed = 0
opponent_ai_speed = 0

thread1 = threading.Thread(target=infiniteloop1)
thread1.start()

thread2 = threading.Thread(target=infiniteloop2)
thread2.start()

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
                messages_to_send.append(str(player_speed))
            if event.key == pygame.K_UP:
                player_speed -= 7
                messages_to_send.append(str(player_speed))
        # Key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
                messages_to_send.append(str(player_speed))
            if event.key == pygame.K_UP:
                player_speed += 7
                messages_to_send.append(str(player_speed))

    ball_animation()
    player_animation()
    opponent_animation()
    # opponent_ai()

    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)