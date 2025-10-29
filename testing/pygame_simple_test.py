import pygame
import sys
import colorsys

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WASD Sprite Movement")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


# Sprite Setup
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a simple red square surface for the sprite
        self.image = pygame.Surface([20, 20])

        # Initial hue
        self.hue = 0.0

        # Change colour
        self.set_colour(self.hue)

        self.rect = self.image.get_rect()

        # Initial position (center of the screen)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Movement attributes
        self.speed = 5
        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Apply movement changes
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Keep sprite within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Change colour
        self.hue += 0.01
        self.hue = round(self.hue, 2)
        self.hue %= 1
        self.set_colour(self.hue)

    def set_colour(self, hue):
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        self.rgb = (int(r * 255), int(g * 255), int(b * 255))
        self.image.fill(self.rgb)

# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()
player = PlayerSprite()
all_sprites.add(player)

# Game Loop Control
clock = pygame.time.Clock()
running = True

# Main Game Loop
while running:

    # Get hid input --
    key_input = pygame.key.get_pressed()

    # Event Handling (inputs) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Clean up code would go here

        # Escape to quit
        if key_input[pygame.K_ESCAPE]:
            running = False
            # Clean up code would go here, you could make a func

        # # Key Down Events (for continuous movement)
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w:
        #         player.change_y = -player.speed  # Move Up
        #     elif event.key == pygame.K_s:
        #         player.change_y = player.speed  # Move Down
        #     elif event.key == pygame.K_a:
        #         player.change_x = -player.speed  # Move Left
        #     elif event.key == pygame.K_d:
        #         player.change_x = player.speed  # Move Right
        #
        # # Key Up Events (to stop movement)
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_w or event.key == pygame.K_s:
        #         player.change_y = 0
        #     if event.key == pygame.K_a or event.key == pygame.K_d:
        #         player.change_x = 0


    if not (key_input[pygame.K_w] or key_input[pygame.K_s]):
        player.change_y = 0
    if not (key_input[pygame.K_a] or key_input[pygame.K_d]):
        player.change_x = 0

    if (key_input[pygame.K_w] or key_input[pygame.K_s] or key_input[pygame.K_a] or key_input[pygame.K_d]):

        # Upgraded movement system
        if key_input[pygame.K_w]:
            player.change_y = -player.speed  # Move Up
        if key_input[pygame.K_s]:
            player.change_y = player.speed  # Move Down
        if key_input[pygame.K_a]:
            player.change_x = -player.speed  # Move Left
        if key_input[pygame.K_d]:
            player.change_x = player.speed  # Move Right

    if key_input[pygame.K_SPACE]:
        screen.fill(BLACK)  # Clear the screen with black

    # Call each sprite's update
    all_sprites.update()

    # Drawing
    # screen.fill(BLACK)  # Clear the screen with black
    all_sprites.draw(screen)  # Draw all sprites

    # Display Update
    pygame.display.flip()

    # Control the frame rate (for example 60 frames per second)
    clock.tick(60)

# Quit Pygame and exit the program
pygame.quit()
sys.exit()