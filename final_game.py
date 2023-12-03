import pygame
import sys
from pygame.locals import *
import time
import config
import pygame.sprite
import socket
import threading
from queue import Queue

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Constants for button width and height
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 50

# game variable
wall_thickness = 20
wall_thickness1 = 60

# Initialize pygame
pygame.init()

# Variable to keep the main loop running
second_player_count = 0
first_player_count = 0

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup the clock for a decent framerate
clock = pygame.time.Clock()



# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y):
        super(Player, self).__init__()
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.surf = pygame.Surface((w, h))
        self.surf.fill('Gray')
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y - self.rect.height)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):

        # First player's movement
        if pressed_keys == 'K_UP':
            first_player.rect.move_ip(0, -1)
        if pressed_keys == 'K_DOWN':
            first_player.rect.move_ip(0, 1)
        if pressed_keys == 'K_LEFT':
            first_player.rect.move_ip(-1, 0)
        if pressed_keys == 'K_RIGHT':
            first_player.rect.move_ip(1, 0) 

        # Second player's movement
        if pressed_keys == 'K_w':
            second_player.rect.move_ip(0, -1)
        if pressed_keys == 'K_s':
            second_player.rect.move_ip(0, 1)
        if pressed_keys == 'K_a':
            second_player.rect.move_ip(-1, 0)
        if pressed_keys == 'K_d': 
            second_player.rect.move_ip(1, 0)        

        # Keep player on the screen
        if first_player.rect.left < 0:
            first_player.rect.left = 0
        if first_player.rect.right > SCREEN_WIDTH/2:
            first_player.rect.right = SCREEN_WIDTH/2
        if first_player.rect.top <= 0:
            first_player.rect.top = 0
        if first_player.rect.bottom >= SCREEN_HEIGHT:
            first_player.rect.bottom = SCREEN_HEIGHT 
        if second_player.rect.left < SCREEN_WIDTH/2:
            second_player.rect.left = SCREEN_WIDTH/2
        if second_player.rect.right > 800:
            second_player.rect.right = 800
        if second_player.rect.top <= 0:
            second_player.rect.top = 0
        if second_player.rect.bottom >= SCREEN_HEIGHT:
            second_player.rect.bottom = SCREEN_HEIGHT 


        # First_player's reaction with block 
        for block in first_blocks:
            if first_player.rect.colliderect(block.rect):
                if pressed_keys == 'K_UP':
                    first_player.rect.top = block.rect.bottom
                if pressed_keys == 'K_DOWN':
                    first_player.rect.bottom = block.rect.top
                if pressed_keys == 'K_LEFT':
                    first_player.rect.left = block.rect.right 
                if pressed_keys == 'K_RIGHT':
                    first_player.rect.right = block.rect.left 

        # Second player's reaction with block 
        for block in second_blocks:
            if second_player.rect.colliderect(block.rect):
                if pressed_keys == 'K_w':    
                    second_player.rect.top = block.rect.bottom
                if pressed_keys == 'K_s':
                    second_player.rect.bottom = block.rect.top
                if pressed_keys == 'K_a':
                    second_player.rect.left = block.rect.right 
                if pressed_keys == 'K_d':
                    second_player.rect.right = block.rect.left            

class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, width, y, length, id):
        super(Block, self).__init__()
        self.color = color
        self.outline_color = 'white'
        self.x = x
        self.width = width
        self.y = y 
        self.length = length
        self.id = id
        # Create a rect attribute for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.length)

    def draw(self):
        self.block = pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.length))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.radius = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1     

    def update(self, id):
        global bullet_count
        global second_player_count
        global first_player_count

        if id == 1:
            self.rect.x += self.speed
            if self.rect.colliderect(second_player.rect):
                second_player_count += 1
                if second_player_count == 3:
                    config.first_player_win = True
                    win()
                    second_player.kill()

            for block in first_blocks:
                if self.rect.colliderect(block.rect) or self.rect.left > SCREEN_WIDTH:
                    self.kill()

            for block in second_blocks:
                if self.rect.colliderect(block.rect):
                    self.kill()
                    first_bullet_count[second_blocks.index(block)] = first_bullet_count[second_blocks.index(block)] + 1

                    if first_bullet_count[second_blocks.index(block)] > 10:
                        second_blocks[second_blocks.index(block)].kill()
                        second_blocks.pop(second_blocks.index(block))

        if id == 2:
            self.rect.x -= self.speed
            if self.rect.colliderect(first_player.rect):
                first_player_count += 1
                if first_player_count == 3:
                    config.second_player_win = True
                    win()
                    first_player.kill()

            for block in second_blocks:
                if self.rect.colliderect(block.rect) or self.rect.right < 0:
                    self.kill()

            for block in first_blocks:
                if self.rect.colliderect(block.rect):
                    self.kill()
                    second_bullet_count[first_blocks.index(block)] = second_bullet_count[first_blocks.index(block)] + 1

                    if second_bullet_count[first_blocks.index(block)] > 10:
                        first_blocks[first_blocks.index(block)].kill()
                        first_blocks.pop(first_blocks.index(block))  


# Instantiate player1/ First player. Right now, this is just a rectangle.
first_player = Player(20, 20, 0, SCREEN_HEIGHT/3)
player1 = pygame.sprite.Group()
player1.add(first_player)

# Instantiate player2/ Second player. Right now, this is just a rectangle.
second_player = Player(20, 20, 780, 2 * SCREEN_HEIGHT/3)
player2 = pygame.sprite.Group()
player2.add(second_player)

first_bullet_group = pygame.sprite.Group()
second_bullet_group = pygame.sprite.Group()

# player1/ First player's safety block
first_block1 = Block('red',30, 20, 15, 20, 1)
first_block2 = Block('blue', 30, 20, 50, 20, 2)
first_block3 = Block('yellow', 50, 20, 70, 20, 3)
first_block4 = Block('yellow', 30, 20, 120, 20, 4)
first_block5 = Block('red',30, 20, 140, 20, 5)
first_block6 = Block('blue', 50, 20, 140, 20, 6)
first_block7 = Block('yellow', 30, 20, 190, 20, 7)
first_block8 = Block('green', 50, 20, 190, 20, 8)
first_block9 = Block('red',30, 20, 210, 20, 9)
first_block10 = Block('blue', 50, 20, 210, 20, 10)
first_block11 = Block('yellow', 30, 20, 230, 20, 11)
first_block12 = Block('green', 30, 20, 250, 20, 12)
first_block13 = Block('green', 50, 20, 300, 20, 13)
first_block14 = Block('blue', 90, 20, 300, 20, 14)
first_block15 = Block('red',30, 20, 350, 20, 15)
first_block16 = Block('blue', 50, 20, 390, 20, 16)
first_block17 = Block('yellow', 50, 20, 430, 20, 17)
first_block18 = Block('green', 70, 20, 430, 20, 18)
first_block19 = Block('red',30, 20, 450, 20, 19)
first_block20 = Block('blue', 50, 20, 500, 20, 20)
first_block21 = Block('yellow', 70, 20, 500, 20, 21)
first_block22 = Block('yellow', 70, 20, 540, 20, 22)
first_block23 = Block('green', 70, 20, 560, 20, 23)
first_block24 = Block('red', 90, 20, 560, 20, 24)
first_block25 = Block('green', 30, 20, 580, 20, 25)

# player2 / Second player's safety block
second_block1 = Block('red',750, 20, 15, 20, 1)
second_block2 = Block('blue', 750, 20, 50, 20, 2)
second_block3 = Block('yellow', 730, 20, 70, 20, 3)
second_block4 = Block('yellow', 750, 20, 120, 20, 4)
second_block5 = Block('red',750, 20, 140, 20, 5)
second_block6 = Block('blue', 730, 20, 140, 20, 6)
second_block7 = Block('yellow', 750, 20, 190, 20, 7)
second_block8 = Block('green', 730, 20, 190, 20, 8)
second_block9 = Block('red',750, 20, 210, 20, 9)
second_block10 = Block('blue', 730, 20, 210, 20, 10)
second_block11 = Block('yellow', 750, 20, 230, 20, 11)
second_block12 = Block('green', 750, 20, 250, 20, 12)
second_block13 = Block('green', 730, 20, 300, 20, 13)
second_block14 = Block('blue', 690, 20, 300, 20, 14)
second_block15 = Block('red',750, 20, 350, 20, 15)
second_block16 = Block('blue', 730, 20, 390, 20, 16)
second_block17 = Block('yellow', 730, 20, 430, 20, 17)
second_block18 = Block('green', 710, 20, 430, 20, 18)
second_block19 = Block('red',750, 20, 450, 20, 19)
second_block20 = Block('blue', 730, 20, 500, 20, 20)
second_block21 = Block('yellow', 710, 20, 500, 20, 21)
second_block22 = Block('yellow', 710, 20, 540, 20, 22)
second_block23 = Block('green', 710, 20, 560, 20, 23)
second_block24 = Block('red', 690, 20, 560, 20, 24)
second_block25 = Block('green', 750, 20, 580, 20, 25)


# dictionary of Blocks
first_blocks = [first_block1, first_block2, first_block3, first_block4, first_block5, first_block6, first_block7, first_block8,
          first_block9, first_block10, first_block11, first_block12, first_block13, first_block14, first_block15, 
          first_block16, first_block17, first_block18, first_block19, first_block20, first_block21, first_block22,
          first_block23, first_block24, first_block25]

second_blocks = [second_block1, second_block2, second_block3, second_block4, second_block5, second_block6, second_block7, second_block8,
          second_block9, second_block10, second_block11, second_block12, second_block13, second_block14, second_block15, 
          second_block16, second_block17, second_block18, second_block19, second_block20, second_block21, second_block22,
          second_block23, second_block24, second_block25]

first_block_group = pygame.sprite.Group()
second_block_group = pygame.sprite.Group()

for block in first_blocks:
    first_block_group.add(block)

for block in second_blocks:
    second_block_group.add(block)

first_bullet_count = [0 for _ in second_blocks]
second_bullet_count = [0 for _ in first_blocks]

################ functions
# Function to draw buttons
def print_text( x_pos, y_pos, text, color, size):
    x = x_pos
    y = y_pos
    t = text
    c = color
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(t, True, c)
    textRect = text.get_rect()
    textRect.center = (x , y)
    screen.blit(text, textRect)

def draw_button(x, y, width, height, text, color):
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def data_from_client(client_socket):
    try:
        while config.p_server:
            data = client_socket.recv(1024)
            if not data:
                break

            config.recieved_keys.put(data.decode())
            if data.decode() == 'quit':
                config.p_server = False

            if data.decode() == 'replay':
                config.replay_op = True

    except ConnectionResetError:
        config.p_server = False  

    finally:      
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # Binds to all available interfaces on port 5555
    server.listen(1)
    print('Server is listening...')
    conn, addr = server.accept()
    print(f'Connected to {addr}')
    config.running1 = True
    client_thread = threading.Thread(target=data_from_client, args=(conn,))
    client_thread.start()    

    while config.p_server:
        if not config.input_keys.empty():        
            message = config.input_keys.get()

            if message == 'quit':
                connection_lost()
                config.p_server = False
                break     

            conn.sendall(message.encode())      

    conn.close()


def data_from_server(client_socket):
    try:
        while config.p_client:
            data = client_socket.recv(1024)
            
            if not data:
                break

            config.recieved_keys.put(data.decode())
            if data.decode() == 'quit':
                config.p_client = False

            if data.decode() == 'replay':
                config.replay_op = True

    except ConnectionResetError:
        config.p_client = False    

    finally:      
        client_socket.close()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.0.118', 5555))  # Replace 'SERVER_IP' with the actual IP of the server
    config.running1 = True
    receive_thread = threading.Thread(target=data_from_server, args=(client,))
    receive_thread.start()

    while config.p_client:
        if not config.input_keys.empty():
            message = config.input_keys.get()

            if message == 'quit':
                config.p_client = False

            client.sendall(message.encode())

    client.close()


def first_player_data_convert(unprepared_data):
    ready_data = 'K_n' 

    if unprepared_data[K_UP]:
        ready_data = 'K_UP'
    if unprepared_data[K_DOWN]:
        ready_data = 'K_DOWN' 
    if unprepared_data[K_LEFT]:
        ready_data = 'K_LEFT'
    if unprepared_data[K_RIGHT]:
        ready_data = 'K_RIGHT' 

    return ready_data


def second_player_data_convert(unprepared_data):
    ready_data = 'K_n'

    if unprepared_data == 'K_UP':
        ready_data = 'K_w'
    if unprepared_data == 'K_DOWN':
        ready_data = 'K_s'
    if unprepared_data == 'K_LEFT':
        ready_data = 'K_a'
    if unprepared_data == 'K_RIGHT':
        ready_data = 'K_d' 

    return ready_data   


def connection_lost():
    run = True

    while run:
        screen.fill((0, 0, 0))
        draw_button(300, 150, BUTTON_WIDTH+150, BUTTON_HEIGHT, "connection Lost...", (0,153,0))
        draw_button(300, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "RETRY...", (0,153,0))
        draw_button(300, 350, BUTTON_WIDTH, BUTTON_HEIGHT, "CLOSE", (204, 0, 0))

        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN: 
                x, y = event.pos
                
                if 300 <= x <= 480 and 350 <= y <= 400:
                    config.running1 = False
                    config.running = False
                    run = False  

                elif 300 <= x <= 480 and 250 <= y <= 300:
                    config.running1 = False
                    run = False 

        pygame.display.flip()


def waiting_connection():

    while not config.running1:
        screen.fill((0, 0, 0))
        draw_button(300, 250, BUTTON_WIDTH+150, BUTTON_HEIGHT, "Waiting for opponent...", (0,153,0))
        draw_button(300, 350, BUTTON_WIDTH, BUTTON_HEIGHT, "CLOSE", (204, 0, 0))

        if config.replay_op == True and config.replay_self == True:
            config.running1 = True

        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN: 
                x, y = event.pos

                if 300 <= x <= 480 and 350 <= y <= 400:
                    config.running = False 
                    pygame.quit()

        pygame.display.flip()


def win():

    run = True
    while run:

        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN: 
                x, y = event.pos

                if 300 <= x <= 480 and 250 <= y <= 300:
                    config.running1 = False
                    reinitialize()
                    config.replay_self = True
                    config.input_keys.put('replay')
                    run = False

                elif 300 <= x <= 480 and 350 <= y <= 400:
                    config.running = False
                    config.running1 = False
                    config.p_client = False
                    config.p_server = False 
                    run = False 
                    pygame.quit()

        screen.fill((0, 0, 0))

        if config.first_player_win == True:
            draw_button(300, 150, BUTTON_WIDTH+150, BUTTON_HEIGHT, "Player1 Win!!", (0,153,0))

        if config.second_player_win == True:
            draw_button(300, 150, BUTTON_WIDTH+150, BUTTON_HEIGHT, "Player2 Win!!", (0,153,0))

        draw_button(300, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "REPLAY", (0,153,0))
        draw_button(300, 350, BUTTON_WIDTH, BUTTON_HEIGHT, "CLOSE", (204, 0, 0))
        pygame.display.flip()


def reinitialize():
    global first_player
    global player1
    global second_player
    global player2 
    global  first_bullet_group  
    global  second_bullet_group 
    global first_blocks
    global second_blocks
    global first_block_group
    global second_block_group
    global first_bullet_count
    global second_bullet_count
    global second_player_count
    global first_player_count
    second_player_count = 0
    first_player_count = 0
    first_bullet_count.clear()
    first_blocks.clear()
    second_bullet_count.clear()
    second_blocks.clear()

    config.second_player_win = False
    config.first_player_win = False

    first_player = Player(20, 20, 0, SCREEN_HEIGHT/3)
    player1 = pygame.sprite.Group()
    player1.add(first_player)

    second_player = Player(20, 20, 780, 2 * SCREEN_HEIGHT/3)
    player2 = pygame.sprite.Group()
    player2.add(second_player)

    first_bullet_group = pygame.sprite.Group()
    second_bullet_group = pygame.sprite.Group()    


    # dictionary of Blocks
    first_blocks = [first_block1, first_block2, first_block3, first_block4, first_block5, first_block6, first_block7, first_block8,
            first_block9, first_block10, first_block11, first_block12, first_block13, first_block14, first_block15, 
            first_block16, first_block17, first_block18, first_block19, first_block20, first_block21, first_block22,
            first_block23, first_block24, first_block25]
    
    second_blocks = [second_block1, second_block2, second_block3, second_block4, second_block5, second_block6, second_block7, second_block8,
            second_block9, second_block10, second_block11, second_block12, second_block13, second_block14, second_block15, 
            second_block16, second_block17, second_block18, second_block19, second_block20, second_block21, second_block22,
            second_block23, second_block24, second_block25]
    
    first_block_group = pygame.sprite.Group()
    second_block_group = pygame.sprite.Group()

    for block in first_blocks:
        first_block_group.add(block)

    for block in second_blocks:
        second_block_group.add(block)

    first_bullet_count = [0 for _ in second_blocks]
    second_bullet_count = [0 for _ in first_blocks]


def play_ground():
    start_time = time.time()
    reinitialize()
    config.replay_self = False 
    config.replay_op = False

    while config.running1: 

        screen.fill((0, 0, 0))  # Fill the screen with black
        # Inside the game loop, update and draw the bullets
        time1 = start_time
        time2 = time.time()

        if time2-time1 > .3:
            bullet = Bullet(first_player.rect.right, first_player.rect.centery)
            first_bullet_group.add(bullet) 
            bullet = Bullet(second_player.rect.left, second_player.rect.centery)
            second_bullet_group.add(bullet) 
            start_time = time.time()

        for block in first_block_group:
            block.draw()
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(block.x, block.y, block.width, block.length), 1)

        for block in second_block_group:
            block.draw()
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(block.x, block.y, block.width, block.length), 1)

        # for loop through the event queue
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    config.running1 = False

            elif event.type == QUIT:
                config.running1 = False

        recv_button  = 'K_n'
        input_button  = 'K_n'
        input_buttons = pygame.key.get_pressed()

        if config.p_server == True:
            input_button = first_player_data_convert(input_buttons)
            config.input_keys.put(input_button)
            first_player.update(input_button)

            if not config.recieved_keys.empty():
                recv_button = config.recieved_keys.get()

            second_player.update(recv_button)

        if config.p_client == True:
            input_button1 = first_player_data_convert(input_buttons)            
            input_button = second_player_data_convert(input_button1)
            config.input_keys.put(input_button)
            second_player.update(input_button)

            if not config.recieved_keys.empty():
                recv_button = config.recieved_keys.get() 

            first_player.update(recv_button)
                             
        if config.p_server == False and config.p_client == False:
            connection_lost()

        # Inside the update loop in play_ground function
        for bullet in first_bullet_group:
            bullet.update(1)
            
        for bullet in second_bullet_group:
            bullet.update(2)

        # Check for collisions between player 1's bullets and player 2's bullets
        for f_bullet in first_bullet_group:
            for s_bullet in second_bullet_group:
                if f_bullet.rect.colliderect(s_bullet.rect):  
                    f_bullet.kill()
                    s_bullet.kill()

        # Drawing the bullets
        for bullet in first_bullet_group:
            screen.blit(bullet.image, bullet.rect.topleft)  
        for bullet in second_bullet_group:
            screen.blit(bullet.image, bullet.rect.topleft)  


        # Draw the player's on the screen
        screen.blit(first_player.surf, first_player.rect)  
        screen.blit(second_player.surf, second_player.rect)   

        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(250) 

    screen.fill((0, 0, 0)) 



config.running = True
# Main loop
while config.running:
    for event in pygame.event.get():
        if event.type == QUIT:
            config.running = False
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN: 
            x, y = event.pos 

            if 300 <= x <= 480 and 150 <= y <= 200:                      
                game_update_server = threading.Thread(target=start_server,daemon=True, args=[])
                game_update_server.start()
                config.p_server = True

                while config.p_server:
                    waiting_connection()
                    play_ground()

            elif 300 <= x <= 480 and 250 <= y <= 300:
                game_update_client = threading.Thread(target=start_client,daemon=True, args=[])
                game_update_client.start()
                config.p_client = True

                while config.p_client:
                    waiting_connection()
                    play_ground()


            elif 300 <= x <= 480 and 350 <= y <= 400:
                config.running = False 
                pygame.quit()

    # Draw the buttons
    draw_button(300, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "PLAYER 1", (0,153,0))
    draw_button(300, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "PLAYER 2", (0,153,0))
    draw_button(300, 350, BUTTON_WIDTH, BUTTON_HEIGHT, "CLOSE", (204, 0, 0))

    pygame.display.flip() 
       
config.th_loop = False    
pygame.quit()  
