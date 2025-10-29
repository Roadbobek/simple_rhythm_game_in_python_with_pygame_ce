import pygame
import sys

# Initialize Pygame
pygame.init()

# --- Configuration ---
# Set initial screen size (4:3 aspect ratio)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

# We use the DOUBLEBUF flag for potentially smoother drawing
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("WASD Sprite Movement (FPS and Size Independent)")

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Extra settings
FPS_CAP = 180  # Capping FPS, but movement speed is now independent of this value!

# --- Constants for Proportional Scaling ---
# The sprite size is 2.5% of the screen width
SPRITE_SIZE_PCT = 0.025
# The player should move 30% of the screen width per second
MOVEMENT_SPEED_PCT_PER_SEC = 0.30


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()

        # 1. Size Independence: Calculate size based on a percentage of the screen width
        size = screen_width * SPRITE_SIZE_PCT
        self.image = pygame.Surface([size, size])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # 2. Speed Independence: Define speed in Pixels Per Second (PPS)
        # Speed is 30% of the screen width per second (PPS)
        self.speed_pps = screen_width * MOVEMENT_SPEED_PCT_PER_SEC

        # Direction Multipliers: change_x/y now only hold -1, 0, or 1.
        self.dir_x = 0
        self.dir_y = 0

    def set_initial_position(self, screen_width, screen_height):
        """Sets the initial position after the sprite object is created."""
        self.rect.center = (screen_width // 2, screen_height // 2)

    def set_direction(self, x, y):
        """Used by the event handler to set the direction multiplier."""
        self.dir_x = x
        self.dir_y = y

    def update(self, dt, screen_width, screen_height):
        """
        Updates the player's position using Delta Time (dt) and clamps it to the screen size.
        """
        # Calculate the actual movement this frame: (Direction * Speed_PPS * dt)

        # Horizontal movement
        self.rect.x += self.dir_x * self.speed_pps * dt
        # Vertical movement
        self.rect.y += self.dir_y * self.speed_pps * dt

        # Keep sprite within screen boundaries (uses current screen_width/height)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height


# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()
player = PlayerSprite(SCREEN_WIDTH)
player.set_initial_position(SCREEN_WIDTH, SCREEN_HEIGHT)  # Set initial position
all_sprites.add(player)

# Game Loop Control
clock = pygame.time.Clock()
running = True
dt = 0.0  # Delta time initialization

# Main Game Loop
while running:
    # --- 1. Calculate Delta Time (FPS Independence) ---
    # clock.tick returns time since last call in ms. Divide by 1000.0 to get seconds.
    dt = clock.tick(FPS_CAP) / 1000.0

    # --- 2. Event Handling (Input) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key Down Events: Set direction multipliers
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.set_direction(player.dir_x, -1)
            elif event.key == pygame.K_s:
                player.set_direction(player.dir_x, 1)
            elif event.key == pygame.K_a:
                player.set_direction(-1, player.dir_y)
            elif event.key == pygame.K_d:
                player.set_direction(1, player.dir_y)

        # Key Up Events: Stop movement in the released axis
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.set_direction(player.dir_x, 0)
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player.set_direction(0, player.dir_y)

    # --- 3. Update ---
    # Pass dt and screen dimensions to the update function
    player.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)

    # --- 4. Drawing ---
    screen.fill(BLACK)  # Clear the screen with black
    all_sprites.draw(screen)  # Draw all sprites

    # --- 5. Display Update ---
    pygame.display.flip()

# Quit Pygame and exit the program
pygame.quit()
sys.exit()
