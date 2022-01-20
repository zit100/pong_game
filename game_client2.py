import pygame, sys, random, socket, select, threading


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    # Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Borders collison
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    # Player scored
    if ball.left <= 0:
        player_score += 1
        messages_to_send.append("goal")
        score_time = pygame.time.get_ticks()
    # Oponnent scored
    if ball.right >= screen_width:
        opponent_score += 1
        messages_to_send.append("goal")
        score_time = pygame.time.get_ticks()

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
    global ball_speed_x, ball_speed_y, score_time, start_count_ball, new_ball_speed_x, new_ball_speed_y

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    # Write 3 2 1 before new round starts
    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    # Wait till start next round
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        if start_count_ball:
            ball_speed_y = new_ball_speed_x
            ball_speed_x = new_ball_speed_y
            score_time = None
        else:
            start_count_ball = True
            ball_speed_x = start_ball_speed_x
            ball_speed_y = start_ball_speed_y
            score_time = None


def infiniteloop1():
    global opponent_speed, new_ball_speed_x, new_ball_speed_y

    while True:
        rlist, wlist, xlist = select.select([my_socket], [], [])
        if my_socket in rlist:
            msg = int(my_socket.recv(MAX_MSG_LENGTH).decode())
            if msg == 1317:
                new_ball_speed_x, new_ball_speed_y = -7, 7
            elif msg == 133:
                new_ball_speed_x, new_ball_speed_y = -7, -7
            elif msg == 2717:
                new_ball_speed_x, new_ball_speed_y = 7, 7
            elif msg == 273:
                new_ball_speed_x, new_ball_speed_y = 7, -7
            else:
                opponent_speed = msg


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
my_socket.connect(('192.168.1.110', 5555))

# Get ball first speed
data = my_socket.recv(1).decode()
if "-"  in data:
    start_ball_speed_x = -7
    ball_speed_x = -7
else:
    start_ball_speed_x = 7
    ball_speed_x = 7
data = my_socket.recv(1).decode()
if "-"  in data:
    start_ball_speed_y = -7
    ball_speed_y = -7
else:
    start_ball_speed_y = 7
    ball_speed_y = 7

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

# Text
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Speeds
player_speed = 0
opponent_speed = 0
opponent_ai_speed = 0
new_ball_speed_x = 0
new_ball_speed_y = 0

# Time
score_time = True
global start_count_ball
start_count_ball = False

thread1 = threading.Thread(target=infiniteloop1)
thread1.start()

thread2 = threading.Thread(target=infiniteloop2)
thread2.start()

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            my_socket.send("".encode())
            my_socket.close()
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

    if score_time:
        ball_restart()

    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (screen_width / 2 + 20, screen_height / 2 - 20))

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (screen_width / 2 - 30, screen_height / 2 - 20))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)