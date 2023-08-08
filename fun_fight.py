 # Import the pygame module
import pygame
from pygame.locals import *
import time
import config

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

# Colors



################ functions

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
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0) 
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)   
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT  

class Block:
    def __init__(self, color, x1, x2, y1, y2, id):
        self.color = color
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.id = id

    def draw(self):
        self.block = pygame.draw.rect(screen, self.color, pygame.Rect(self.x1, self.y1, self.x2, self.y2))
        # self.block = pygame.Rect((self.x1, self.x2), (self.y1, self.y2))
    ##### update block
    # def update_block(self):  for future 

# Instantiate player1. Right now, this is just a rectangle.
player1 = Player(20, 20, 0, SCREEN_HEIGHT/2)
p1 = pygame.sprite.Group()
p1.add(player1)

# Instantiate player2. Right now, this is just a rectangle.
player2 = Player(20, 20, 780, SCREEN_HEIGHT/2)
p2 = pygame.sprite.Group()
p2.add(player2)

# (self, color, x1, x2, y1, y2, id)
# player1's safety block
block1 = Block('red',30, 20, 15, 20, 1)
block2 = Block('blue', 30, 20, 50, 20, 2)
block3 = Block('yellow', 50, 20, 70, 20, 3)
block4 = Block('yellow', 30, 20, 120, 20, 4)
block5 = Block('red',30, 20, 140, 20, 5)
block6 = Block('blue', 50, 20, 140, 20, 6)
block7 = Block('yellow', 30, 20, 190, 20, 7)
block8 = Block('green', 50, 20, 190, 20, 8)
block9 = Block('red',30, 20, 210, 20, 9)
block10 = Block('blue', 50, 20, 210, 20, 10)
block11 = Block('yellow', 30, 20, 230, 20, 11)
block12 = Block('green', 30, 20, 250, 20, 12)
block13 = Block('green', 50, 20, 300, 20, 13)
block14 = Block('blue', 90, 20, 300, 20, 14)
block15 = Block('red',30, 20, 350, 20, 15)
block16 = Block('blue', 50, 20, 390, 20, 16)
block17 = Block('yellow', 50, 20, 430, 20, 17)
block18 = Block('green', 70, 20, 430, 20, 18)
block19 = Block('red',30, 20, 450, 20, 19)
block20 = Block('blue', 50, 20, 500, 20, 20)
block21 = Block('yellow', 70, 20, 500, 20, 21)
block22 = Block('yellow', 70, 20, 540, 20, 22)
block23 = Block('green', 70, 20, 560, 20, 23)
block24 = Block('red', 90, 20, 560, 20, 24)
block25 = Block('green', 30, 20, 580, 20, 25)

# player2's safety block
blo1 = Block('red',750, 20, 15, 20, 1)
blo2 = Block('blue', 750, 20, 50, 20, 2)
blo3 = Block('yellow', 730, 20, 70, 20, 3)
blo4 = Block('yellow', 750, 20, 120, 20, 4)
blo5 = Block('red',750, 20, 140, 20, 5)
blo6 = Block('blue', 730, 20, 140, 20, 6)
blo7 = Block('yellow', 750, 20, 190, 20, 7)
blo8 = Block('green', 730, 20, 190, 20, 8)
blo9 = Block('red',750, 20, 210, 20, 9)
blo10 = Block('blue', 730, 20, 210, 20, 10)
blo11 = Block('yellow', 750, 20, 230, 20, 11)
blo12 = Block('green', 750, 20, 250, 20, 12)
blo13 = Block('green', 730, 20, 300, 20, 13)
blo14 = Block('blue', 690, 20, 300, 20, 14)
blo15 = Block('red',750, 20, 350, 20, 15)
blo16 = Block('blue', 730, 20, 390, 20, 16)
blo17 = Block('yellow', 730, 20, 430, 20, 17)
blo18 = Block('green', 710, 20, 430, 20, 18)
blo19 = Block('red',750, 20, 450, 20, 19)
blo20 = Block('blue', 730, 20, 500, 20, 20)
blo21 = Block('yellow', 710, 20, 500, 20, 21)
blo22 = Block('yellow', 710, 20, 540, 20, 22)
blo23 = Block('green', 710, 20, 560, 20, 23)
blo24 = Block('red', 690, 20, 560, 20, 24)
blo25 = Block('green', 750, 20, 580, 20, 25)

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

    # Instantiate player1. Right now, this is just a rectangle.
    player1 = Player(20, 20, 0, SCREEN_HEIGHT/2)
    p1 = pygame.sprite.Group()
    p1.add(player1)

    # Instantiate player2. Right now, this is just a rectangle.
    player2 = Player(20, 20, 780, SCREEN_HEIGHT/2)
    p2 = pygame.sprite.Group()
    p2.add(player2)
    global paused
  
    while config.running1: 

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    # game_over_screen(score)
                    config.running1 = False
                    # config.running = False

                elif event.key == K_p:
                    paused = True
                elif event.key == K_r:
                    paused = False 
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                # game_over_screen(score)
                # config.running = False
                config.running1 = False
                
        screen.fill((0, 0, 0))  # Fill the screen with black

        # player1's block
        block1.draw()
        block2.draw()
        block3.draw()
        block4.draw()
        block5.draw()
        block6.draw()
        block7.draw()
        block8.draw()
        block9.draw()
        block10.draw()
        block11.draw()
        block12.draw()
        block13.draw()
        block14.draw()
        block15.draw()
        block16.draw()
        block17.draw()
        block18.draw()
        block19.draw()
        block20.draw()
        block21.draw()
        block22.draw()
        block23.draw()
        block24.draw()
        block25.draw()
        # player2's block
        blo1.draw()
        blo2.draw()
        blo3.draw()
        blo4.draw()
        blo5.draw()
        blo6.draw()
        blo7.draw()
        blo8.draw()
        blo9.draw()
        blo10.draw()
        blo11.draw()
        blo12.draw()
        blo13.draw()
        blo14.draw()
        blo15.draw()
        blo16.draw()
        blo17.draw()
        blo18.draw()
        blo19.draw()
        blo20.draw()
        blo21.draw()
        blo22.draw()
        blo23.draw()
        blo24.draw()
        blo25.draw()

        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
        # Update the player sprite based on user keypresses
        player1.update(pressed_keys)
        # player2.update(pressed_keys)

        # Draw the player's on the screen
        screen.blit(player1.surf, player1.rect)  
        screen.blit(player2.surf, player2.rect)   

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

    # running1 = True
    # first_page()
    # Clear the screen
    # screen.fill((255, 255, 255))

    # Draw the buttons
    draw_button(300, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "START GAME", (0,153,0))
    draw_button(300, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "CLOSE", (204, 0, 0))

    pygame.display.flip()    
    
pygame.quit()  