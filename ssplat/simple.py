# Simple pygame program
# Import and initialize the pygame library

# From https://realpython.com/pygame-a-primer/#basic-pygame-program
# Make a side scroller!
#   https://realpython.com/courses/pygame-primer/


import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

PHYSICS_UPDATE = pygame.USEREVENT + 1
time_step = 10 # 10 milliseconds, or .010 seconds
pygame.time.set_timer(PHYSICS_UPDATE, time_step) # Update physics every 10 ms

prt = print

prt = lambda v: None

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.a_y = -100 # negative is down

        self.v_x = 0
        self.v_y = 0

        self.drag_x = .002
        self.drag_y = .002

        self.rect.move_ip(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


    def update_v(self, pressed_keys):
        """Update the velocities"""

        dv = 20

        if pressed_keys[K_UP]:
            self.v_y += dv
        if pressed_keys[K_DOWN]:
            self.v_y -= dv
        if pressed_keys[K_LEFT]:
            self.v_x -= dv
        if pressed_keys[K_RIGHT]:
            self.v_x += dv

    def physics(self):
        dt = time_step/1000 # 50 ms

        # x = vt
        dx = self.v_x * dt
        dy = self.v_y * dt

        # v = at, for gravity
        self.v_y += self.a_y * dt

        # Drag
        self.v_x -= self.drag_x * self.v_x
        self.v_y -= self.drag_y * self.v_y

        self.rect.move_ip(dx, -dy)

        prt( f"move ({dx},{-dy}) @({self.rect.x, self.rect.y}) {self.v_x};{self.v_y}")

    def constrain(self):
        # Keep player on the screen

        if self.rect.left < 0:
            self.rect.left = 0
            self.v_x = -self.v_x
            prt("Bounce left")
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.v_x = -self.v_x
            prt("Bounce right")
        if self.rect.top <= 0:
            self.rect.top = 0
            self.v_y = -self.v_y
            prt("Bounce top")
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.v_y = -self.v_y
            prt("Bounce bottom")


player = Player()
# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Run until the user asks to quit
running = True
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
    # Did the user hit a key?

        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.

            if event.key == K_ESCAPE:
                running = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

        if event.type == PHYSICS_UPDATE:
            player.physics()

    pressed_keys = pygame.key.get_pressed()
    player.update_v(pressed_keys)
    player.constrain()

    # Fill the background with white
    screen.fill((0, 0, 0))

    screen.blit(player.surf,  player.rect)

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
