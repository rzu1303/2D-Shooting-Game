import pygame
from pygame.locals import *
import time
import config
import pygame.sprite

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

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to keep the main loop running
running = True
running1 = False
paused = False
splayer_count = 0
fplayer_count = 0

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

        # initial position of the moving rectangle to bottom-left position
        # self.rect.topleft = (0, SCREEN_HEIGHT - self.rect.height- wall_thickness1/2)
        self.rect.topleft = (x, y - self.rect.height)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            f_player.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            f_player.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            f_player.rect.move_ip(-1, 0) 
        if pressed_keys[K_RIGHT]:
            f_player.rect.move_ip(1, 0) 

        #### s_player
        if pressed_keys[K_w]:
            s_player.rect.move_ip(0, -1)
        if pressed_keys[K_s]:
            s_player.rect.move_ip(0, 1)
        if pressed_keys[K_a]:
            s_player.rect.move_ip(-1, 0) 
        if pressed_keys[K_d]:
            s_player.rect.move_ip(1, 0)        

        # Keep player on the screen
        if f_player.rect.left < 0:
            f_player.rect.left = 0
        if f_player.rect.right > SCREEN_WIDTH/2:
            f_player.rect.right = SCREEN_WIDTH/2
        if f_player.rect.top <= 0:
            f_player.rect.top = 0
        if f_player.rect.bottom >= SCREEN_HEIGHT:
            f_player.rect.bottom = SCREEN_HEIGHT 
        if s_player.rect.left < SCREEN_WIDTH/2:
            s_player.rect.left = SCREEN_WIDTH/2
        if s_player.rect.right > 800:
            s_player.rect.right = 800
        if s_player.rect.top <= 0:
            s_player.rect.top = 0
        if s_player.rect.bottom >= SCREEN_HEIGHT:
            s_player.rect.bottom = SCREEN_HEIGHT 


        # f_player's reaction with block 
        for block in f_blocks:
            if f_player.rect.colliderect(block.rect):
                if pressed_keys[K_UP]:
                    f_player.rect.top = block.rect.bottom
                if pressed_keys[K_DOWN]:
                    f_player.rect.bottom = block.rect.top
                if pressed_keys[K_LEFT]:
                    f_player.rect.left = block.rect.right 
                if pressed_keys[K_RIGHT]:
                    f_player.rect.right = block.rect.left  
        # player's reaction with block 
        for block in s_blocks:
            if s_player.rect.colliderect(block.rect):
                if pressed_keys[K_w]:
                    s_player.rect.top = block.rect.bottom
                if pressed_keys[K_s]:
                    s_player.rect.bottom = block.rect.top
                if pressed_keys[K_a]:
                    s_player.rect.left = block.rect.right 
                if pressed_keys[K_d]:
                    s_player.rect.right = block.rect.left            

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

    # f_block1 = Block('red'(color),30(pos x), 20(width), 15(pos y), 20(legth), 1)
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
    # def draw(self):

    def update(self, id):
        global bullet_count
        global splayer_count
        global fplayer_count
        # self.rect.x += self.speed
        ############
        if id == 1:
            self.rect.x += self.speed
            if self.rect.colliderect(s_player.rect):
                splayer_count += 1
                if splayer_count == 3:
                    print("Win!!!")
                    s_player.kill()
                    ### closing the game. will check again for better soluation
                    config.running1 = False


            for block in f_blocks:
                if self.rect.colliderect(block.rect) or self.rect.left > SCREEN_WIDTH:
                    self.kill()

            for block in s_blocks:
                if self.rect.colliderect(block.rect):
                    self.kill()


                    # print(s_blocks.index(block))
                    fbullet_count[s_blocks.index(block)] = fbullet_count[s_blocks.index(block)] + 1

                    print(fbullet_count[s_blocks.index(block)])
                    if fbullet_count[s_blocks.index(block)] > 10:
                        # s_blocks.index(block).kill()

                        print(s_blocks.index(block))
                        s_blocks[s_blocks.index(block)].kill()
                        s_blocks.pop(s_blocks.index(block))

        if id == 2:
            self.rect.x -= self.speed
            if self.rect.colliderect(f_player.rect):
                fplayer_count += 1
                if fplayer_count == 3:
                    print("player 2 Win!!!")
                    f_player.kill()
                    ### closing the game. will check again for better soluation
                    config.running1 = False


            for block in s_blocks:
                if self.rect.colliderect(block.rect) or self.rect.right < 0:
                    self.kill()

            for block in f_blocks:
                if self.rect.colliderect(block.rect):
                    self.kill()

                    # print(s_blocks.index(block))
                    sbullet_count[f_blocks.index(block)] = sbullet_count[f_blocks.index(block)] + 1

                    print(sbullet_count[f_blocks.index(block)])
                    if sbullet_count[f_blocks.index(block)] > 10:
                        # s_blocks.index(block).kill()

                        print(f_blocks.index(block))
                        f_blocks[f_blocks.index(block)].kill()
                        f_blocks.pop(f_blocks.index(block))                            

# Instantiate player1. Right now, this is just a rectangle.
f_player = Player(20, 20, 0, SCREEN_HEIGHT/3)
p1 = pygame.sprite.Group()
p1.add(f_player)

# Instantiate player2. Right now, this is just a rectangle.
s_player = Player(20, 20, 780, 2 * SCREEN_HEIGHT/3)
p2 = pygame.sprite.Group()
p2.add(s_player)

fbullet_group = pygame.sprite.Group()
sbullet_group = pygame.sprite.Group()


# player1's safety block
f_block1 = Block('red',30, 20, 15, 20, 1)
f_block2 = Block('blue', 30, 20, 50, 20, 2)
f_block3 = Block('yellow', 50, 20, 70, 20, 3)
f_block4 = Block('yellow', 30, 20, 120, 20, 4)
f_block5 = Block('red',30, 20, 140, 20, 5)
f_block6 = Block('blue', 50, 20, 140, 20, 6)
f_block7 = Block('yellow', 30, 20, 190, 20, 7)
f_block8 = Block('green', 50, 20, 190, 20, 8)
f_block9 = Block('red',30, 20, 210, 20, 9)
f_block10 = Block('blue', 50, 20, 210, 20, 10)
f_block11 = Block('yellow', 30, 20, 230, 20, 11)
f_block12 = Block('green', 30, 20, 250, 20, 12)
f_block13 = Block('green', 50, 20, 300, 20, 13)
f_block14 = Block('blue', 90, 20, 300, 20, 14)
f_block15 = Block('red',30, 20, 350, 20, 15)
f_block16 = Block('blue', 50, 20, 390, 20, 16)
f_block17 = Block('yellow', 50, 20, 430, 20, 17)
f_block18 = Block('green', 70, 20, 430, 20, 18)
f_block19 = Block('red',30, 20, 450, 20, 19)
f_block20 = Block('blue', 50, 20, 500, 20, 20)
f_block21 = Block('yellow', 70, 20, 500, 20, 21)
f_block22 = Block('yellow', 70, 20, 540, 20, 22)
f_block23 = Block('green', 70, 20, 560, 20, 23)
f_block24 = Block('red', 90, 20, 560, 20, 24)
f_block25 = Block('green', 30, 20, 580, 20, 25)

# player2's safety block
s_block1 = Block('red',750, 20, 15, 20, 1)
s_block2 = Block('blue', 750, 20, 50, 20, 2)
s_block3 = Block('yellow', 730, 20, 70, 20, 3)
s_block4 = Block('yellow', 750, 20, 120, 20, 4)
s_block5 = Block('red',750, 20, 140, 20, 5)
s_block6 = Block('blue', 730, 20, 140, 20, 6)
s_block7 = Block('yellow', 750, 20, 190, 20, 7)
s_block8 = Block('green', 730, 20, 190, 20, 8)
s_block9 = Block('red',750, 20, 210, 20, 9)
s_block10 = Block('blue', 730, 20, 210, 20, 10)
s_block11 = Block('yellow', 750, 20, 230, 20, 11)
s_block12 = Block('green', 750, 20, 250, 20, 12)
s_block13 = Block('green', 730, 20, 300, 20, 13)
s_block14 = Block('blue', 690, 20, 300, 20, 14)
s_block15 = Block('red',750, 20, 350, 20, 15)
s_block16 = Block('blue', 730, 20, 390, 20, 16)
s_block17 = Block('yellow', 730, 20, 430, 20, 17)
s_block18 = Block('green', 710, 20, 430, 20, 18)
s_block19 = Block('red',750, 20, 450, 20, 19)
s_block20 = Block('blue', 730, 20, 500, 20, 20)
s_block21 = Block('yellow', 710, 20, 500, 20, 21)
s_block22 = Block('yellow', 710, 20, 540, 20, 22)
s_block23 = Block('green', 710, 20, 560, 20, 23)
s_block24 = Block('red', 690, 20, 560, 20, 24)
s_block25 = Block('green', 750, 20, 580, 20, 25)


# dictionary of Blocks
f_blocks = [f_block1, f_block2, f_block3, f_block4, f_block5, f_block6, f_block7, f_block8,
          f_block9, f_block10, f_block11, f_block12, f_block13, f_block14, f_block15, 
          f_block16, f_block17, f_block18, f_block19, f_block20, f_block21, f_block22,
          f_block23, f_block24, f_block25]
s_blocks = [s_block1, s_block2, s_block3, s_block4, s_block5, s_block6, s_block7, s_block8,
          s_block9, s_block10, s_block11, s_block12, s_block13, s_block14, s_block15, 
          s_block16, s_block17, s_block18, s_block19, s_block20, s_block21, s_block22,
          s_block23, s_block24, s_block25]
f_block_group = pygame.sprite.Group()
s_block_group = pygame.sprite.Group()
for block in f_blocks:
    f_block_group.add(block)

for block in s_blocks:
    s_block_group.add(block)

fbullet_count = [0 for _ in s_blocks]
sbullet_count = [0 for _ in f_blocks]

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
    # Create a font object
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


def play_ground():
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
    start_time = time.time()
  
    while config.running1: 
        screen.fill((0, 0, 0))  # Fill the screen with black
        # Inside the game loop, update and draw the bullets
        time1 = start_time
        time2 = time.time()

        if time2-time1 > .3:
            bullet = Bullet(f_player.rect.right, f_player.rect.centery)
            fbullet_group.add(bullet) 
            bullet = Bullet(s_player.rect.left, s_player.rect.centery)
            sbullet_group.add(bullet) 
            start_time = time.time()

        # bullet = Bullet(s_player.rect.left, s_player.rect.centery)
        # sbullet_group.add(bullet) 


        for block in f_block_group:
            block.draw()
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(block.x, block.y, block.width, block.length), 1)


        for block in s_block_group:
            block.draw()
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(block.x, block.y, block.width, block.length), 1)


        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    # game_over_screen(score)
                    config.running1 = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                config.running1 = False

        # # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
        # Update the player sprite based on user keypresses
        f_player.update(pressed_keys)
        s_player.update(pressed_keys)
        # player2.update(pressed_keys)

        # # Update and draw bullets
        # fbullet_group.update(1)
        # fbullet_group.draw(screen)
        # ######
        # sbullet_group.update(2)
        # sbullet_group.draw(screen)
        # Inside the update loop in play_ground function
        for bullet in fbullet_group:
            bullet.update(1)
        for bullet in sbullet_group:
            bullet.update(2)

        # Check for collisions between player 1's bullets and player 2's bullets
        for f_bullet in fbullet_group:
            for s_bullet in sbullet_group:
                if f_bullet.rect.colliderect(s_bullet.rect):  # Corrected attribute names
                    f_bullet.kill()
                    s_bullet.kill()

        # Drawing the bullets
        for bullet in fbullet_group:
            screen.blit(bullet.image, bullet.rect.topleft)  # Corrected attribute names
        for bullet in sbullet_group:
            screen.blit(bullet.image, bullet.rect.topleft)  # Corrected attribute names



        # Draw the player's on the screen
        screen.blit(f_player.surf, f_player.rect)  
        screen.blit(s_player.surf, s_player.rect)   

        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(250)  



config.running = True
# Main loop
while config.running:
    for event in pygame.event.get():
        if event.type == QUIT:
            config.running = False
        elif event.type == MOUSEBUTTONDOWN: 
            x, y = event.pos 
            if 300 <= x <= 480 and 150 <= y <= 200:
                
                config.running1 = True
                play_ground()
                config.running = False
                

            elif 300 <= x <= 480 and 250 <= y <= 300:
                # running = False 
                pygame.quit()

    # Draw the buttons
    draw_button(300, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "START GAME", (0,153,0))
    draw_button(300, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "CLOSE", (204, 0, 0))

    pygame.display.flip()    
    
pygame.quit()  
