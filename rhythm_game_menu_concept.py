# I genuinely rather blow my brains out than work with this fucking abomination of code, like yeah I understand what its doing but not how, i understand what the code does but not the paths it takes fuck this i am really close to killing myself again

import pygame
import sys
import os

# --- Misc Constants ---
TITLE = "PyRhythm"

# --- In-Game Settings Constants ---
SCREEN_RESOLUTIONS = ((2560, 1440), (1920, 1080), (1280, 720), (800, 600))
SCREEN_RESOLUTION_OPTIONS = \
    [
        "2560x1440",
        "1920x1080",
        "1280x720",
        "800x600"
    ]
WINDOW_TYPE_OPTIONS = ["Windowed", "Fullscreen", "Borderless"]

# --- Game States ---
STATE_MENU = 0
STATE_PLAYING = 1
STATE_OPTIONS = 2

# --- Colours ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
BLUE = (50, 50, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
ACCENT_COLOR = (50, 150, 255)


class Button:
    """A reusable class for creating clickable buttons."""

    def __init__(self, x, y, width, height, text, action, color, hover_color, font_size_ratio=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.hover_color = hover_color
        self.font_size = int(height * font_size_ratio)  # Scale font with button height
        self.font = pygame.font.Font(None, self.font_size)
        self.is_hovered = False

    def draw(self, screen):
        # Determine current color
        current_color = self.hover_color if self.is_hovered else self.color

        # Draw the button rectangle
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)

        # Render and center the text
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Update hover state
            self.is_hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                # Execute the button's action (which is usually setting the game state)
                return self.action
        return None

    def update_hover(self, mouse_pos):
        """Used to check hover state even without a MOUSEMOTION event."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)


class Dropdown:
    """A simple dropdown menu component, now integrated."""

    def __init__(self, x, y, w, h, font_size_ratio, options, callback, default_text="Dropdown"):
        self.color_menu = (100, 100, 100)  # Lighter Gray
        self.color_option = GRAY
        self.rect = pygame.Rect(x, y, w, h)
        self.font_size = int(h * font_size_ratio)
        self.font = pygame.font.Font(None, self.font_size)
        self.options = options
        self.expanded = False
        self.callback = callback  # Function to call when a selection is made

        self.selected_option = options[0] if options else default_text
        self.default_text = default_text
        self.option_rects = []
        for i, option in enumerate(options):
            option_rect = pygame.Rect(x, y + h * (i + 1), w, h)
            self.option_rects.append(option_rect)

    def get_selected_value(self):
        """Returns the currently selected option."""
        return self.selected_option

    def update_selected_from_game(self, current_value_string):
        """Updates the displayed text based on the game's actual current setting."""
        self.selected_option = current_value_string if current_value_string in self.options else self.default_text

    def handle_event(self, event):
        """Handles mouse clicks and updates the state/selection."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
            elif self.expanded:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_option = self.options[i]
                        self.expanded = False
                        # Call the callback function with the selected value
                        self.callback(self.selected_option)
                        break
                else:
                    # If clicked outside options, collapse the menu
                    self.expanded = False

    def draw(self, screen):
        """Draws the dropdown menu and its options."""

        # 1. Draw the main selection box
        pygame.draw.rect(screen, self.color_menu, self.rect, border_radius=5)
        pygame.draw.rect(screen, ACCENT_COLOR, self.rect, 2, border_radius=5)

        # Render selected text
        text_surf = self.font.render(self.selected_option, True, WHITE)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surf, text_rect)

        # 2. Draw the dropdown arrow
        arrow_size = int(self.rect.height * 0.3)  # Scale arrow size with dropdown height
        arrow_center_x = self.rect.right - 15
        arrow_center_y = self.rect.centery

        points = [
            (arrow_center_x - arrow_size // 2, arrow_center_y - arrow_size // 2),
            (arrow_center_x + arrow_size // 2, arrow_center_y - arrow_size // 2),
            (arrow_center_x, arrow_center_y + arrow_size // 2)
        ]

        if self.expanded:
            # Change arrow direction when expanded
            points = [(p[0], 2 * arrow_center_y - p[1]) for p in points]

        pygame.draw.polygon(screen, WHITE, points)

        # 3. Draw the options list if expanded
        if self.expanded:
            for i, option in enumerate(self.options):
                rect = self.option_rects[i]

                # Check for hover state on options
                if rect.collidepoint(pygame.mouse.get_pos()):
                    color = ACCENT_COLOR
                else:
                    color = self.color_option

                pygame.draw.rect(screen, color, rect, border_radius=5)

                option_surf = self.font.render(option, True, WHITE)
                option_rect = option_surf.get_rect(midleft=(rect.x + 10, rect.centery))
                screen.blit(option_surf, option_rect)

                pygame.draw.rect(screen, ACCENT_COLOR, rect, 2, border_radius=5)


class MenuScreen:
    """Manages the layout, drawing, and logic for the main menu state."""

    def __init__(self, game):
        self.game = game  # Reference to the main Game object
        self.title_font = None  # Will be set in recreate_ui
        self.buttons = []

    def recreate_ui(self):
        """Re-calculates button positions and sizes based on current screen dimensions."""
        self.buttons.clear()
        # Define button properties
        btn_width = self.game.screen_width * 0.15
        btn_height = self.game.screen_height * 0.07
        x_center = self.game.screen_width / 2 - btn_width / 2
        y_start = self.game.screen_height * 0.35
        y_spacing = btn_height * 1.5

        # Scale title font
        self.title_font = pygame.font.Font(None, int(self.game.screen_height * 0.08))

        # Play Button: Action is to change the game state to PLAYING
        play_btn = Button(
            x_center, y_start, btn_width, btn_height,
            "Play Game", lambda: self.game.change_state(STATE_PLAYING),
            GREEN, BRIGHT_GREEN, font_size_ratio=0.5
        )
        self.buttons.append(play_btn)

        # Options Button: Action is to change the game state to OPTIONS
        options_btn = Button(
            x_center, y_start + y_spacing, btn_width, btn_height,
            "Options", lambda: self.game.change_state(STATE_OPTIONS),
            BLUE, (100, 100, 255), font_size_ratio=0.5
        )
        self.buttons.append(options_btn)

        # Quit Button: Action is to run the game's quit method
        quit_btn = Button(
            x_center, y_start + y_spacing * 2, btn_width, btn_height,
            "Quit", lambda: self.game.quit_game(),
            RED, BRIGHT_RED, font_size_ratio=0.5
        )
        self.buttons.append(quit_btn)

    def handle_events(self, event):
        for button in self.buttons:
            # Buttons handle their own click events and return the desired action
            action = button.handle_event(event)
            if action:
                action()  # Execute the lambda function (state change or quit)
                return  # Stop processing events once an action is triggered

    def update(self):
        # Check hover state continually (especially important if using touch or non-click effects)
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update_hover(mouse_pos)

    def draw(self, screen):
        screen.fill(BLACK)

        # Draw Title
        title_surf = self.title_font.render(TITLE, True, WHITE)
        title_rect = title_surf.get_rect(center=(self.game.screen_width // 2, self.game.screen_height * 0.2))
        screen.blit(title_surf, title_rect)

        # Draw Buttons
        for button in self.buttons:
            button.draw(screen)


class OptionsScreen:
    """Manages the layout, drawing, and logic for the main menu state."""

    def __init__(self, game):
        self.game = game  # Reference to the main Game object
        self.title_font = None  # Will be set in recreate_ui
        self.body_font = None  # Will be set in recreate_ui
        self.buttons = []
        self.resolution_dropdown = None
        self.window_type_dropdown = None

    def set_resolution(self, res_string):
        """Callback function to apply the selected resolution."""
        self.game.apply_resolution(res_string)

    def set_window_type(self, window_type_string):
        """Callback function to apply the selected window type."""
        self.game.apply_window_type(window_type_string)

    def recreate_ui(self):
        """Re-calculates UI positions and sizes based on current screen dimensions."""
        self.buttons.clear()

        # Scale fonts
        self.title_font = pygame.font.Font(None, int(self.game.screen_height * 0.08))
        self.body_font = pygame.font.Font(None, int(self.game.screen_height * 0.03))

        # --- Setup the Dropdowns ---
        dropdown_width = self.game.screen_width * 0.15
        dropdown_height = self.game.screen_height * 0.05
        dropdown_x = self.game.screen_width * 0.5
        dropdown_y_res = self.game.screen_height * 0.35
        dropdown_y_win = dropdown_y_res + dropdown_height * 1.5

        self.resolution_dropdown = Dropdown(
            x=dropdown_x,
            y=dropdown_y_res,
            w=dropdown_width,
            h=dropdown_height,
            font_size_ratio=0.5,
            options=SCREEN_RESOLUTION_OPTIONS,
            callback=self.set_resolution,
            default_text="Resolution"
        )
        current_res_str = f"{self.game.screen_width}x{self.game.screen_height}"
        self.resolution_dropdown.update_selected_from_game(current_res_str)

        self.window_type_dropdown = Dropdown(
            x=dropdown_x,
            y=dropdown_y_win,
            w=dropdown_width,
            h=dropdown_height,
            font_size_ratio=0.5,
            options=WINDOW_TYPE_OPTIONS,
            callback=self.set_window_type,
            default_text="Window Type"
        )
        self.window_type_dropdown.update_selected_from_game(self.game.window_type)

        # Back Button: Go back to menu
        btn_width = self.game.screen_width * 0.15
        btn_height = self.game.screen_height * 0.07
        x_center = self.game.screen_width / 2 - btn_width / 2
        y_pos = self.game.screen_height * 0.7
        back_btn = Button(
            x_center, y_pos, btn_width, btn_height,
            "Back", lambda: self.game.change_state(STATE_MENU),
            RED, BRIGHT_RED, font_size_ratio=0.5
        )
        self.buttons.append(back_btn)

    def handle_events(self, event):
        self.resolution_dropdown.handle_event(event)
        self.window_type_dropdown.handle_event(event)

        for button in self.buttons:
            action = button.handle_event(event)
            if action:
                action()
                return

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update_hover(mouse_pos)

    def draw(self, screen):
        screen.fill(BLACK)

        title_surf = self.title_font.render("Options", True, WHITE)
        title_rect = title_surf.get_rect(center=(self.game.screen_width // 2, self.game.screen_height * 0.2))
        screen.blit(title_surf, title_rect)

        for button in self.buttons:
            button.draw(screen)

        res_label_surf = self.body_font.render("Resolution:", True, WHITE)
        res_label_rect = res_label_surf.get_rect(
            midright=(self.resolution_dropdown.rect.left - 20, self.resolution_dropdown.rect.centery))
        screen.blit(res_label_surf, res_label_rect)
        self.resolution_dropdown.draw(screen)

        win_label_surf = self.body_font.render("Window Type:", True, WHITE)
        win_label_rect = win_label_surf.get_rect(
            midright=(self.window_type_dropdown.rect.left - 20, self.window_type_dropdown.rect.centery))
        screen.blit(win_label_surf, win_label_rect)
        self.window_type_dropdown.draw(screen)


class Game:
    """The main game engine, managing the application loop and state."""

    def __init__(self):
        pygame.init()

        # --- In-Game Settings Values ---
        self.screen_width = 1920
        self.screen_height = 1080
        self.last_windowed_width = self.screen_width
        self.last_windowed_height = self.screen_height
        self.window_type = "Windowed"
        self.fps_cap = 60

        self.screen = None  # Will be set by recreate_display

        # --- State and Screen Management ---
        self.state = STATE_MENU
        self.menu = MenuScreen(self)
        self.playing_logic = None
        self.options_screen = OptionsScreen(self)
        self.current_screen = self.menu

        # Initial display setup after all components are initialized
        self.recreate_display()

        self.clock = pygame.time.Clock()

    def apply_resolution(self, res_string):
        """Parses a resolution string and resizes the window."""
        try:
            width, height = map(int, res_string.split('x'))
            self.screen_width = width
            self.screen_height = height
            if self.window_type == "Windowed":
                self.last_windowed_width = width
                self.last_windowed_height = height
            self.recreate_display()
        except ValueError:
            print(f"Error: Invalid resolution string format: {res_string}")

    def apply_window_type(self, window_type_string):
        """Applies the selected window type."""
        self.window_type = window_type_string
        self.recreate_display()

    def recreate_display(self):
        """Recreates the display surface with current settings."""
        info = pygame.display.Info()
        monitor_width = info.current_w
        monitor_height = info.current_h

        # --- Prepare settings for the new display mode ---
        flags = 0

        if self.window_type == "Borderless":
            os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
            size = (monitor_width, monitor_height)
            flags = pygame.NOFRAME

        elif self.window_type == "Fullscreen":
            size = (self.screen_width, self.screen_height)
            flags = pygame.FULLSCREEN

        else:  # "Windowed"
            win_x = (monitor_width - self.last_windowed_width) // 2
            win_y = (monitor_height - self.last_windowed_height) // 2
            os.environ['SDL_VIDEO_WINDOW_POS'] = f'{win_x},{win_y}'
            size = (self.last_windowed_width, self.last_windowed_height)
            flags = 0

        # --- Re-initialize and create the display ---
        # A more targeted re-initialization of only the display module
        pygame.display.quit()
        pygame.display.init()

        self.screen = pygame.display.set_mode(size, flags)
        pygame.display.set_caption(TITLE)

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.menu.recreate_ui()
        self.options_screen.recreate_ui()

    def change_state(self, new_state):
        """Method to switch between game states."""
        self.state = new_state

        if self.state == STATE_MENU:
            self.current_screen = self.menu
        elif self.state == STATE_PLAYING:
            self.current_screen = None
        elif self.state == STATE_OPTIONS:
            self.current_screen = self.options_screen

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if self.current_screen:
                    self.current_screen.handle_events(event)

                if self.state in (STATE_PLAYING, STATE_OPTIONS) and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_state(STATE_MENU)

            if self.current_screen:
                self.current_screen.update()

            elif self.state == STATE_PLAYING:
                self.screen.fill(BLACK)
                font_size = int(self.screen_height * 0.07)
                font = pygame.font.Font(None, font_size)
                text = font.render("RHYTHM GAME IS PLAYING!", True, GREEN)
                text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                self.screen.blit(text, text_rect)

                sub_font_size = int(self.screen_height * 0.025)
                sub_font = pygame.font.Font(None, sub_font_size)
                sub_text = sub_font.render("Press ESC to return to Menu", True, WHITE)
                sub_rect = sub_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + sub_font_size * 2))
                self.screen.blit(sub_text, sub_rect)

            if self.current_screen:
                self.current_screen.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps_cap)


if __name__ == '__main__':
    game = Game()
    game.run()
