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
pygame.display.set_caption("WASD Sprite Movement (Polling, FPS and Size Independent)")

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Extra settings
FPS_CAP = 180  # Movement speed is independent of this value!
# NEW: Define a fixed time step for physics and game logic updates.
# This ensures movement speed is completely consistent (e.g., exactly 60 updates per second).
FIXED_FPS = 60
FIXED_DT = 1.0 / FIXED_FPS

# --- Constants for Proportional Scaling ---
# The sprite size is 2.5% of the screen width
SPRITE_SIZE_PCT = 0.025
# The player should move 30% of the screen width per second
MOVEMENT_SPEED_PCT_PER_SEC = 0.30


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()

        # 1. Size Independence: Calculate size based on a percentage of the screen width
        size = int(screen_width * SPRITE_SIZE_PCT)

        # Ensure size is at least 1 pixel
        if size < 1: size = 1

        self.image = pygame.Surface([size, size])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # 2. Speed Independence: Define speed in Pixels Per Second (PPS)
        # Speed is 30% of the screen width per second (PPS)
        self.speed_pps = screen_width * MOVEMENT_SPEED_PCT_PER_SEC

        # Direction Multipliers: change_x/y now only hold -1, 0, or 1.
        self.dir_x = 0
        self.dir_y = 0

        # Float position tracker for sub-pixel movement accuracy
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def set_initial_position(self, screen_width, screen_height):
        """Sets the initial position after the sprite object is created and initializes floats."""
        self.rect.center = (screen_width // 2, screen_height // 2)
        # Initialize float positions to match the initial center integer position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, dt, screen_width, screen_height):
        """
        Updates the player's position using Delta Time (dt, which is now FIXED_DT),
        applying movement to the float position, and then clamping and updating the integer rect.
        """
        # 1. Apply movement to the high-precision float coordinates (self.x, self.y)
        self.x += self.dir_x * self.speed_pps * dt
        self.y += self.dir_y * self.speed_pps * dt

        # 2. Clamping/Boundary Check (applied to the float coordinates)

        # Horizontal clamping
        if self.x < 0:
            self.x = 0
        elif self.x + self.rect.width > screen_width:
            self.x = screen_width - self.rect.width

        # Vertical clamping
        if self.y < 0:
            self.y = 0
        elif self.y + self.rect.height > screen_height:
            self.y = screen_height - self.rect.height

        # 3. Update the integer rect for drawing/collision using ROUNDING
        # This synchronizes the integer position with the float position smoothly
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)


# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()
player = PlayerSprite(SCREEN_WIDTH)
player.set_initial_position(SCREEN_WIDTH, SCREEN_HEIGHT)  # Set initial position
all_sprites.add(player)

# Game Loop Control
clock = pygame.time.Clock()
running = True
accumulator = 0.0  # Accumulator for tracking time that needs to be simulated

# Main Game Loop
while running:
    # --- 1. Calculate Real-time Delta Time and Accumulate ---
    # clock.tick returns time since last call in ms. Divide by 1000.0 to get seconds (raw_dt).
    # We use a cap (FPS_CAP) for the drawing loop speed, but raw_dt accurately tracks time passed.
    raw_dt = clock.tick(FPS_CAP) / 1000.0
    accumulator += raw_dt

    # --- 2. Real-time Event Handling & Input Polling (Variable FPS) ---
    # Events and input must be checked every single frame for maximum responsiveness.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # STATE POLLING: Check keys every frame
    keys = pygame.key.get_pressed()

    # Reset direction multipliers every frame
    player.dir_x = 0
    player.dir_y = 0

    # Calculate desired direction based on keys (Net Movement System)
    if keys[pygame.K_a]:
        player.dir_x -= 1  # -1
    if keys[pygame.K_d]:
        player.dir_x += 1  # 1
    if keys[pygame.K_w]:
        player.dir_y -= 1  # -1
    if keys[pygame.K_s]:
        player.dir_y += 1  # 1

    if keys[pygame.K_ESCAPE]:
        running = False

    # --- 3. Fixed Time Step Logic Update (Consistent Speed) ---
    # Run the update function in fixed slices of time until the accumulator is caught up.
    # The movement steps are always the same size, which guarantees consistent speed.
    while accumulator >= FIXED_DT:
        # Pass the FIXED_DT to the update method
        player.update(FIXED_DT, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Consume the time slice
        accumulator -= FIXED_DT

        # Note: If FPS drops very low, this loop might run multiple times in one frame,
        # ensuring the simulation speed never slows down.

    # --- 4. Drawing (Variable FPS) ---
    # The player's position is now updated based on fixed logic, so drawing is smooth.
    screen.fill(BLACK)  # Clear the screen with black
    all_sprites.draw(screen)  # Draw all sprites

    # --- 5. Display Update ---
    pygame.display.flip()

# Quit Pygame and exit the program
pygame.quit()
sys.exit()
