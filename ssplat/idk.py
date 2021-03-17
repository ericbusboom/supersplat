# Simple pygame program
# Import and initialize the pygame library

# From https://realpython.com/pygame-a-primer/#basic-pygame-program
# Make a side scroller!
#   https://realpython.com/courses/pygame-primer/


import pygame
from pathlib import Path
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

PHYSICS_UPDATE = pygame.USEREVENT + 1
ENEMY_EXIT = pygame.USEREVENT + 2

time_step = 10 # 10 milliseconds, or .010 seconds
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

prt = print

images = Path(__file__).parent.joinpath('images')

#prt = lambda v: None

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super().__init__()
        self.surf = pygame.image.load(images.joinpath(image_name)).convert_alpha()
        self.rect = self.surf.get_rect()

        self.init_pos()

    def init_pos(self):
        self.rect.left = SCREEN_WIDTH
        self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        if self.rect.left < 0:
            pygame.event.post(pygame.event.Event(ENEMY_EXIT))

        self.rect.move_ip(-2,0)

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(images.joinpath('mario150.bmp')).convert_alpha()
        #self.surf = pygame.Surface((75, 25))
        #self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.a_y = -500 # negative is down
        self.dv_y = 400
        self.dt = time_step/1000

        self.dx = 2

        self.v_y = 0

        self.limit_left = 50
        self.limit_right = 400

        self.rect.move_ip(100, SCREEN_HEIGHT-35)

    def update(self, pressed_keys):
        """Update the velocities"""

        if pressed_keys[K_UP] and self.v_y == 0 and self.rect.bottom == SCREEN_HEIGHT:
            self.v_y += self.dv_y
            self.rect.move_ip(0, -1) # Kick off the bottom so constrain() doesnt set to zero

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.dx,0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.dx, 0)

    def physics(self):
        """Update physics, Y axis velocity"""

        self.v_y += self.a_y * self.dt # v =at
        dy = self.v_y * self.dt # x = vt
        self.rect.move_ip(0, -dy)

    def constrain(self):
        """Keep player on the screen"""

        if self.rect.right < self.limit_left:
            self.limit_left = 0

        if self.rect.right > self.limit_right:
            self.limit_right = self.limit_right

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.v_y = 0


pygame.init()

pygame.time.set_timer(PHYSICS_UPDATE, time_step) # Update physics every 10 ms

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

player = Player()

enemies = [ Enemy('Paratroopa.bmp'),Enemy('kujo.bmp')]

# Kick off the enemies
pygame.event.Event(ENEMY_EXIT)
enemy = None
enemy_pointer = 0

# Run until the user asks to quit
running = True
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
    # Did the user hit a key?

        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop

            if event.key == K_ESCAPE:
                running = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

        if event.type == KEYDOWN or event.type == KEYUP:
            pass

        if event.type == PHYSICS_UPDATE:
            player.physics()
            player.constrain()

            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)

            if enemy:
                enemy.update()

        if event.type == ENEMY_EXIT or enemy is None:
            enemy = enemies[enemy_pointer%len(enemies)]
            enemy_pointer += 1
            enemy.init_pos()

    screen.fill((0, 0, 0))

    screen.blit(player.surf,  player.rect)

    if enemy:
        screen.blit(enemy.surf, enemy.rect)

        if player.rect.colliderect(enemy.rect):
            pygame.event.post(pygame.event.Event(ENEMY_EXIT))

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
