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
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill('yellow')
        self.rect = self.surf.get_rect()

        # initial position of the moving rectangle to bottom-left position
        self.rect.topleft = (0, SCREEN_HEIGHT - self.rect.height- wall_thickness1/2)

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
        # self.block = pygame.draw.rect(screen, self.color, pygame.Rect(self.x1, self.y1, self.x2, self.y2))
        self.block = pygame.Rect((self.x1, self.x2), (self.y1, self.y2))
    ##### update block
    # def update_block(self):  for future 

# Instantiate player. Right now, this is just a rectangle.
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# block1 = Block('red',30, 30, 20, 20, 1)
block1 = Block('red',30, 30, 20, 20, 1)
# block2 = Block('blue',90, 90, 160, 160, 2)
block2 = Block('blue', 90, 92, 160, 162, 2)
# # New rectangle with half the size
# half_width = (block1.x2 - block1.x1) // 2
# half_height = (block1.y2 - block1.y1) // 2
# block_half = Block('blue', block1.x1, block1.x1 + half_width, block1.y1, block1.y1 + half_height, 2)


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

# def draw_blocks(color, x1, x2, y1, y2):
#     # Drawing Rectangle
#     pygame.draw.rect(screen, color, pygame.Rect(x1, y1, x2, y2),  2)



def play_ground():
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
    
    # # Drawing Rectangle
    # block1 = draw_blocks('black',30, 30, 60, 60)


    # Instantiate player. Right now, this is just a rectangle.
    player = Player()
    # Create groups to hold ball sprites and all sprites
    # - all_sprites is used for rendering
    gball = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
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

        block1.draw()
        block2.draw()
        # block_half.draw()
        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        # Draw the player on the screen
        screen.blit(player.surf, player.rect)    

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