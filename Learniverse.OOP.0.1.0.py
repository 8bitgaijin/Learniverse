###############################################################################
### Single Responsibility Principle! Class/functions should do one thing.   ###
###############################################################################


###############################################################################
### Avoid magic numbers! Use named constants for clarity in class Config.   ###
###############################################################################


###############################################################################
### No global variables! Keep variables encapsulated in functions/classes.  ###
###############################################################################


###############################################################################
### Follow PEP8: Stick to Python's official style guide.                    ###
###############################################################################


###############################################################################
### KISS (Keep It Simple, Stupid): Avoid overcomplicating the design.       ###
###############################################################################

# Standard library imports
import datetime
import os
import random
import sys
import time


# Third-party imports
import pygame


# Typing imports
from typing import List, Union


class Config:
    """A configuration class to store game settings."""
    
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 900
    FPS = 60
    SCREEN_TITLE = "OOP Demo"

    # Color definitions
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 128, 255)
    GREEN = (0, 255, 128)
    LIGHT_GREY = (169, 169, 169)
    DARK_GREY = (51, 51, 51)
    LIGHT_BLUE = (0, 136, 255)  # Commodore 64 Light Blue
    NAVY_BLUE = (0, 0, 170)  # Commodore 64 Navy Blue
    ROYAL_BLUE = (16, 83, 227)
    RED = (255, 0, 0)
    DARK_RED = (170, 0, 0)
    WARM_YELLOW = (255, 204, 0)  # A warm, non-gaudy yellow for text
    WARM_ORANGE = (255, 140, 0)  # A warm, non-gaudy orange for shadow
    WARM_RED = (204, 0, 0)  # A warm, deep red for the background
    LIGHT_GREEN = (175,203,70)  # A light green for text
    MEDIUM_GREEN = (121,170,109)  # A medium green for shadow
    FOREST_GREEN = (34,111,95)  # A forest green for screen
    LAVENDER = (230, 230, 250)  # A soft lavender for text
    DEEP_PURPLE = (75, 0, 130)  # A deep purple for shadow
    COOL_BLUE = (100, 149, 237)  # A cool blue for the background
    
    # Button constants
    DEFAULT_BUTTON_COLOR = BLUE
    DEFAULT_BUTTON_HOVER_COLOR = GREEN
    DEFAULT_BUTTON_PADDING = 10
    DEFAULT_BUTTON_ROUNDING = 15 # How much to round the button corners

    # Font constants
    DEFAULT_FONT_SIZE = 75  # Default font size
    DEFAULT_FONT_NAME = "Vivaldi"  # Default font name
    DEFAULT_TEXT_COLOR = WHITE  # Use WHITE as the default text color
    
    # Window constants
    DEFAULT_BACKGROUND_COLOR = BLACK  # Default background color
    LINE_HEIGHT_MULTIPLIER = 1.2  # Multiplier for line height spacing
    WRAP_WIDTH_MULTIPLIER = 0.95  # Used to determine the wrap width as 95% of screen width
    
    # Student selectable color themes
    COLOR_THEMES = {
        "dark": {
            "text_color": BLACK,
            "shadow_color": LIGHT_GREY,
            "screen_color": WHITE
        },
        "light": {
            "text_color": WHITE,
            "shadow_color": LIGHT_GREY,
            "screen_color": BLACK
        },
        "C64": {
            "text_color": LIGHT_BLUE,
            "shadow_color": DARK_GREY,
            "screen_color": NAVY_BLUE
        },
        "warm": {
            "text_color": WARM_YELLOW,
            "shadow_color": WARM_ORANGE,
            "screen_color": DARK_RED
        },
        "GB89": {
            "text_color": LIGHT_GREEN,
            "shadow_color": MEDIUM_GREEN,
            "screen_color": FOREST_GREEN
        },
        "cool": {
            "text_color": LAVENDER,
            "shadow_color": DEEP_PURPLE,
            "screen_color": COOL_BLUE
        }
    }


class WindowManager:
    """Manages window settings and display."""
    
    def __init__(self, config: Config):
        """Initialize the window with settings from the Config class."""
        self.config = config  # Store reference to config
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, 
                                               config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.SCREEN_TITLE)
        self.resolutions = [
            (640, 640),
            (720, 720),
            (800, 800),
            (900, 900),
            (1024, 1024),
            (1080, 1080)
        ]
        # Set the current resolution index
        self.selected_resolution_index = self.find_resolution_index()

    def find_resolution_index(self):
        """Find the current resolution index based on the window size."""
        current_width = self.config.SCREEN_WIDTH
        current_height = self.config.SCREEN_HEIGHT
        for i, (width, height) in enumerate(self.resolutions):
            if current_width == width and current_height == height:
                return i
        return 0  # Fallback to first resolution if no match found

    def change_resolution(self, width: int, height: int) -> None:
        """Change the window resolution dynamically."""
        self.config.SCREEN_WIDTH = width
        self.config.SCREEN_HEIGHT = height
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, 
                                               self.config.SCREEN_HEIGHT))
        pygame.display.set_caption(self.config.SCREEN_TITLE)

    def increase_resolution(self):
        """Increase resolution to the next in the list."""
        self.selected_resolution_index = (self.selected_resolution_index + 1) % len(self.resolutions)
        new_width, new_height = self.resolutions[self.selected_resolution_index]
        self.change_resolution(new_width, new_height)

    def decrease_resolution(self):
        """Decrease resolution to the previous in the list."""
        self.selected_resolution_index = (self.selected_resolution_index - 1) % len(self.resolutions)
        new_width, new_height = self.resolutions[self.selected_resolution_index]
        self.change_resolution(new_width, new_height)

    def get_current_resolution(self):
        """Return the current resolution as a string."""
        return f"{self.config.SCREEN_WIDTH} x {self.config.SCREEN_HEIGHT}"

    def get_screen(self) -> pygame.Surface:
        """Return the screen surface."""
        return self.screen


class FontManager:
    """Handles font settings for the entire game."""

    def __init__(self, default_font: str = Config.DEFAULT_FONT_NAME, 
                 default_size: int = Config.DEFAULT_FONT_SIZE):
        """Initialize the font manager with a default font and size."""
        self.font_name = default_font
        self.font_size = default_size

    def get_font(self) -> pygame.font.Font:
        """Return the current font based on the font name and size."""
        return pygame.font.SysFont(self.font_name, self.font_size)

    def set_font(self, font_name: str, font_size: int) -> None:
        """Update the current font name and size."""
        self.font_name = font_name
        self.font_size = font_size
        

class TextRenderer:
    """Handles rendering text to the screen."""

    def __init__(self, font_manager: FontManager, color: tuple = Config.DEFAULT_TEXT_COLOR):
        self.font_manager = font_manager
        self.color = color

    def render_text(self, screen: pygame.Surface, text: str, x: int, y: int, 
                    centered: bool = False, wrap_width: int = None) -> None:
        """Render text at the specified position."""
        self._render_text_internal(screen, text, x, y, centered, wrap_width, 
                                   alpha=None)

    def render_text_with_alpha(self, screen: pygame.Surface, text: str, x: int, 
                               y: int, alpha: int, centered: bool = False, 
                               wrap_width: int = None) -> None:
        """Render text at the specified position with alpha transparency and optional word wrap."""
        self._render_text_internal(screen, text, x, y, centered, wrap_width, 
                                   alpha=alpha)

    def _render_text_internal(self, screen: pygame.Surface, text: str, x: int, 
                              y: int, centered: bool, wrap_width: int, 
                              alpha: int) -> None:
        """Internal method to render text with optional alpha transparency and word wrap."""
        font = self.font_manager.get_font()

        # Word wrap the text if wrap_width is provided
        if wrap_width:
            lines = self.wrap_text(text, font, wrap_width)
        else:
            lines = [text]

        # Render each line of text
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, self.color)

            # Set alpha if provided
            if alpha is not None:
                text_surface.set_alpha(alpha)

            text_rect = text_surface.get_rect()

            # Align text based on the centered flag
            if centered:
                text_rect.centerx = x
            else:
                text_rect.x = x

            # Set the vertical position, adjusting for multiple lines
            text_rect.y = y + i * font.get_height()

            # Render the text line by line
            screen.blit(text_surface, text_rect)

    def wrap_text(self, text: str, font: pygame.font.Font, wrap_width: int) -> List[str]:
        """Wrap text into lines that fit within the specified width."""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Check if the current line plus the next word exceeds the wrap width
            if font.size(current_line + word)[0] <= wrap_width:
                current_line += word + " "
            else:
                # If it does, store the current line and start a new one
                lines.append(current_line.strip())
                current_line = word + " "

        # Append the last line
        if current_line:
            lines.append(current_line.strip())

        return lines


class Button:
    """A dynamic button class for Pygame."""

    def __init__(
        self, 
        x: int, 
        y: int, 
        text: str, 
        text_renderer: TextRenderer, 
        action: callable = None, 
        # Use padding from Config
        padding: int = Config.DEFAULT_BUTTON_PADDING,  
        color: tuple = Config.DEFAULT_BUTTON_COLOR, 
        hover_color: tuple = Config.DEFAULT_BUTTON_HOVER_COLOR, 
        text_color: tuple = Config.DEFAULT_TEXT_COLOR,
        # Add a border radius for rounded corners
        border_radius: int = Config.DEFAULT_BUTTON_ROUNDING  
    ):
        """Initialize the button with dynamic sizing based on text."""
        self.text = text
        self.text_renderer = text_renderer
        self.action = action  # Function to call when button is clicked
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.padding = padding  # Padding around the text
        self.border_radius = border_radius  # Border radius for rounded corners
        
        # Get the size of the text to dynamically adjust button size
        font = self.text_renderer.font_manager.get_font()
        text_width, text_height = font.size(text)
        
        # Set the rect based on the text size and padding
        self.rect = pygame.Rect(x - (text_width // 2), y, 
                                text_width + self.padding * 2, 
                                text_height + self.padding * 2)

    def draw(self, screen: pygame.Surface):
        """Draw the button."""
        # Change color on hover
        if self.hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect, 
                             border_radius=self.border_radius)
        else:
            pygame.draw.rect(screen, self.color, self.rect, 
                             border_radius=self.border_radius)

        # Get the text dimensions to calculate proper centering
        font = self.text_renderer.font_manager.get_font()
        text_width, text_height = font.size(self.text)

        # Calculate offsets to ensure the text is centered within the button
        x_offset = self.rect.centerx - (text_width // 2)
        y_offset = self.rect.centery - (text_height // 2)

        # Draw the text centered within the button
        self.text_renderer.render_text(screen, self.text, x_offset, y_offset, 
                                       centered=False)

    def handle_event(self, event: pygame.event.Event):
        """Handle mouse events for the button."""
        if event.type == pygame.MOUSEMOTION:
            # Check if the mouse is hovering over the button
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the button is clicked
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()  # Perform the button's action


class ButtonManager:
    """Manages multiple buttons in a menu."""

    def __init__(self):
        self.buttons = []

    def add_button(self, button: Button) -> None:
        """Add a button to the manager."""
        self.buttons.append(button)

    def handle_events(self, events: List[pygame.event.Event]):
        """Delegate event handling to all buttons."""
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def draw(self, screen: pygame.Surface):
        """Draw all buttons."""
        for button in self.buttons:
            button.draw(screen)


class FadeEffect:
    """Handles fade-in, display, and fade-out effects with timing."""

    def __init__(self, fade_in_duration: int, display_duration: int, 
                 fade_out_duration: int):
        """Initialize the fade effect with durations in milliseconds."""
        self.fade_in_duration = fade_in_duration
        self.display_duration = display_duration
        self.fade_out_duration = fade_out_duration
        
        # Store the start time in milliseconds
        self.start_time = time.time() * 1000  
        self.total_duration = self.fade_in_duration + self.display_duration + self.fade_out_duration

    def update(self) -> int:
        """Update the fade effect and return the current alpha value."""
        # Get current time elapsed since start in ms
        current_time = (time.time() * 1000) - self.start_time  
        if current_time <= self.fade_in_duration:
            # Fade-in phase: calculate alpha based on fade-in progress
            alpha = (current_time / self.fade_in_duration) * 255
        elif current_time <= self.fade_in_duration + self.display_duration:
            # Display phase: alpha is fully opaque
            alpha = 255
        elif current_time <= self.total_duration:
            # Fade-out phase: calculate alpha based on fade-out progress
            alpha = 255 - ((current_time - self.fade_in_duration - self.display_duration) / self.fade_out_duration) * 255
        else:
            # Effect is done, return alpha as 0
            alpha = 0

        return int(alpha)

    def is_finished(self) -> bool:
        """Check if the entire fade effect has completed."""
        current_time = (time.time() * 1000) - self.start_time
        return current_time >= self.total_duration


class GameState:
    """Base class for game states. All specific game states will inherit from this."""
    
    def __init__(self, name: str):
        """Initialize the game state with a name."""
        self.name = name
    
    def handle_events(self, events: List[pygame.event.Event]) -> Union[str, None]:
        """Handle input events. Return 'EXIT' to signal quitting."""
        pass

    def update(self) -> None:
        """Update game logic."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Render the game state to the screen."""
        # Use default background color
        screen.fill(Config.DEFAULT_BACKGROUND_COLOR)  


class IntroState(GameState):
    """Introduction state for the game with fade-in, pause, and fade-out using FadeEffect."""

    def __init__(self, text_renderer: TextRenderer):
        super().__init__("IntroState")
        self.text_renderer = text_renderer  # Use the text renderer
        # Create a fade effect for intro with durations in milliseconds
        self.fade_effect = FadeEffect(fade_in_duration=2500, 
                                      display_duration=5000, fade_out_duration=1000)
        # Keep track if auto transition was triggered
        self.auto_transition_triggered = False  

    def handle_events(self, events: List[pygame.event.Event]) -> Union[str, None]:
        """Handle events specific to the intro state."""
        for event in events:
            if event.type == pygame.QUIT:
                return "EXIT"  # Signal to exit the game
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return "MAIN_MENU"  # Transition to main menu on any key press or mouse click

    def update(self) -> Union[str, None]:
        """Update intro state logic by updating the fade effect."""
        if self.fade_effect.is_finished() and not self.auto_transition_triggered:
            self.auto_transition_triggered = True  # Make sure this is only triggered once
            return "MAIN_MENU"  # Automatically transition after the fade effect finishes

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the intro state with fading effect."""
        super().draw(screen)  # Fill with default background color
        alpha = self.fade_effect.update()  # Get the current alpha

        # Render text with the current alpha transparency
        self.text_renderer.render_text_with_alpha(screen, 
                                                  "Developed by:", 
                                                  screen.get_width() // 2, 
                                                  screen.get_height() * 0.33, 
                                                  alpha, centered=True)
        self.text_renderer.render_text_with_alpha(screen, 
                                                  "Alvadore Retro Technology", 
                                                  screen.get_width() // 2, 
                                                  screen.get_height() * 0.66, 
                                                  alpha, centered=True)


    

class MainMenuState(GameState):
    """Main menu state for the game."""

    def __init__(self, config: Config, text_renderer: TextRenderer, 
                 switch_to_options: callable):
        """Initialize the main menu state."""
        super().__init__("MainMenuState")
        self.config = config  # Store the config for screen dimensions
        self.text_renderer = text_renderer
        self.button_manager = ButtonManager()

        # Create the options button and add it to the button manager
        self.options_button = Button(
            x=self.config.SCREEN_WIDTH // 2,  # X position
            y=self.config.SCREEN_HEIGHT * 0.5,  # Y position
            text="Go to Options",  # Dynamic text
            text_renderer=text_renderer,  # TextRenderer object
            action=switch_to_options  # Button action
        )

        # Add the options button to the button manager
        self.button_manager.add_button(self.options_button)

    def update_button_position(self):
        """Update the button's position dynamically based on screen size."""
        screen_width = self.config.SCREEN_WIDTH
        self.options_button.rect.x = int(screen_width // 2 - self.options_button.rect.width // 2)

    def handle_events(self, events: List[pygame.event.Event]) -> Union[str, None]:
        """Handle events specific to the main menu."""
        for event in events:
            if event.type == pygame.QUIT:
                return "EXIT"

        # Delegate button events to the ButtonManager
        self.button_manager.handle_events(events)

    def update(self) -> None:
        """Update main menu logic."""
        self.update_button_position()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the main menu state."""
        super().draw(screen)  # Fill with default background color
        
        # Draw the debug lines for positioning
        # pygame.draw.line(screen, (255, 0, 0), (screen.get_width() // 2, 0), (screen.get_width() // 2, screen.get_height()), 5)
        # pygame.draw.line(screen, (255, 0, 0), (screen.get_width() * 0.25, 0), (screen.get_width() * 0.25, screen.get_height()), 5)
        # pygame.draw.line(screen, (255, 0, 0), (screen.get_width() * 0.75, 0), (screen.get_width() * 0.75, screen.get_height()), 5)
        
        # Render the main menu title
        self.text_renderer.render_text(screen, "Main Menu", 
                                       screen.get_width() // 2, 
                                       screen.get_height() * 0.25, 
                                       centered=True)
        
        # Delegate button drawing to the ButtonManager
        self.button_manager.draw(screen)


class OptionsMenuState(GameState):
    """Options menu state for adjusting game settings like resolution, font, text color, and background color."""

    def __init__(self, window_manager: WindowManager, text_renderer: TextRenderer, switch_to_main_menu: callable, switch_to_credits: callable):
        """Initialize the options menu state."""
        super().__init__("OptionsMenuState")
        self.window_manager = window_manager
        self.text_renderer = text_renderer
        self.switch_to_main_menu = switch_to_main_menu
        self.switch_to_credits = switch_to_credits

        self.button_manager = ButtonManager()

        # Example list of available resolutions
        self.resolutions = [(640, 640), 
                            (720, 720), 
                            (800, 800), 
                            (900, 900), 
                            (1024, 1024), 
                            (1080, 1080)]
        
        # Find the closest match to the current window resolution
        current_width, current_height = self.window_manager.config.SCREEN_WIDTH, self.window_manager.config.SCREEN_HEIGHT
        self.selected_resolution_index = next(
            (i for i, (width, height) in enumerate(self.resolutions) if current_width == width and current_height == height),
            0
        )

        # Create resolution buttons (positions will be dynamically updated later)
        self.left_button = Button(
            x=0, y=200, text="<", text_renderer=text_renderer, action=self.window_manager.decrease_resolution
        )
        self.right_button = Button(
            x=0, y=200, text=">", text_renderer=text_renderer, action=self.window_manager.increase_resolution
        )
        self.main_menu_button = Button(
            x=0, y=0, text="Main Menu", text_renderer=text_renderer, action=self.switch_to_main_menu
        )
        self.credits_button = Button(
            x=0, y=0, text="Credits", text_renderer=text_renderer, action=self.switch_to_credits
        )

        # Add buttons to the ButtonManager
        self.button_manager.add_button(self.left_button)
        self.button_manager.add_button(self.right_button)
        self.button_manager.add_button(self.main_menu_button)
        self.button_manager.add_button(self.credits_button)

    def handle_events(self, events: List[pygame.event.Event]) -> Union[str, None]:
        """Handle input events for the options menu."""
        for event in events:
            if event.type == pygame.QUIT:
                return "EXIT"  # Signal to exit the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"  # Return to the main menu

        # Delegate button events to the ButtonManager
        self.button_manager.handle_events(events)

    def update_button_positions(self, screen: pygame.Surface) -> None:
        """Update the positions of the buttons dynamically based on screen size."""
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Reposition buttons based on the current screen size
        self.left_button.rect.x = int(screen_width * 0.2 - self.left_button.rect.width // 2)
        self.right_button.rect.x = int(screen_width * 0.8 - self.right_button.rect.width // 2)
        self.main_menu_button.rect.x = int(screen_width * 0.5 - self.main_menu_button.rect.width // 2)
        self.main_menu_button.rect.y = screen_height * 0.85  # 75% of the screen height
        self.credits_button.rect.x = int(screen_width * 0.5 - self.credits_button.rect.width // 2)
        self.credits_button.rect.y = screen_height * 0.70  # 85% of the screen height

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the options menu."""
        screen.fill(self.window_manager.config.DEFAULT_BACKGROUND_COLOR)

        # Update button positions before drawing them
        self.update_button_positions(screen)

        # Draw the options menu title
        self.text_renderer.render_text(screen, "Options Menu", screen.get_width() // 2, 50, centered=True)

        # Display the current resolution
        current_resolution = self.window_manager.get_current_resolution()
        self.text_renderer.render_text(screen, current_resolution, screen.get_width() // 2, 200, centered=True)

        # Draw the buttons via ButtonManager
        self.button_manager.draw(screen)


class CreditRollState(GameState):
    """Credit roll state for displaying credits with fade-in and fade-out effects, one at a time."""

    def __init__(self, text_renderer: TextRenderer, return_to_options: callable):
        super().__init__("CreditRollState")
        self.text_renderer = text_renderer  # Use the text renderer
        self.return_to_options = return_to_options  # Callable to return to options menu
        
        # Create a fade effect for credits with durations in milliseconds
        self.fade_effect = FadeEffect(fade_in_duration=2000, 
                                      display_duration=2000, fade_out_duration=2000)
        self.current_credit_index = 0  # Track which credit is currently being displayed
        self.auto_transition_triggered = False  # Track if auto transition was triggered

        # Credits content
        self.credits = [
        "Developed by: Alvadore Retro Technology",
        "Chief Executive Officer: William Alexander Martins",
        "Chief Financial Officer: Mary Evangeline Martins",
        "Chief Information Officer: Shane William Martins",
        "Chief Operations Officer: Ethan Hunter Martins",
        "Chief Technology Officer: Jeffrey Matthew Neff Esq.",
        "Made possible by: Supporters like you!",
        "Special thanks to: Guido van Rossum",
        "Special thanks to: Richard Stallman",
        "Special thanks to: the Blender team",
        "Special thanks to: the ChatGPT team",
        "Special thanks to: the Krita team",
        "Special thanks to: the PyInstaller team",
        "Special thanks to: the Pygame team",
        "Pygame is licensed under LGPL version 2.1",
        "Special thanks to: the Raspberry Pi team",
        "Special thanks to: the Stable Diffusion team",
        "Special thanks to: the Suno team",
        "Special thanks to: the Ubuntu team"
        ]


    def handle_events(self, events: List[pygame.event.Event]) -> Union[str, None]:
        """Handle events specific to the credit roll state."""
        for event in events:
            if event.type == pygame.QUIT:
                return "EXIT"  # Signal to exit the game
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.advance_to_next_credit()

    def advance_to_next_credit(self) -> None:
        """Advance to the next credit or return to options if credits are finished."""
        self.current_credit_index += 1
        if self.current_credit_index >= len(self.credits):
            self.return_to_options()  # Return to options menu when all credits are shown
        else:
            self.fade_effect.start_time = time.time() * 1000  # Reset the fade effect for the next credit

    def update(self) -> Union[str, None]:
        """Update the credit roll state logic by updating the fade effect."""
        if self.fade_effect.is_finished() and not self.auto_transition_triggered:
            self.advance_to_next_credit()  # Automatically transition to next credit after fade effect finishes

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current credit with fade-in, display, and fade-out effects."""
        super().draw(screen)  # Fill with default background color

        if self.current_credit_index < len(self.credits):
            alpha = self.fade_effect.update()  # Get the current alpha

            # Calculate a wrap width (e.g., 90% of the screen width)
            wrap_width = int(screen.get_width() * 0.9)

            # Render the current credit with word wrapping and the calculated alpha transparency
            self.text_renderer.render_text_with_alpha(
                screen,
                self.credits[self.current_credit_index],  # Show the current credit
                screen.get_width() // 2,
                screen.get_height() // 2,  # Center the credit text
                alpha,
                centered=True,
                wrap_width=wrap_width  # Pass the wrap width for word wrapping
            )


class GamePlayState(GameState):
    """The actual game of the game, handling player and NPC logic, sprite updates, and collision detection."""

    def __init__(self, text_renderer: TextRenderer, window_manager: WindowManager):
        """Initialize the game play state."""
        super().__init__("GamePlayState")
        self.text_renderer = text_renderer
        self.window_manager = window_manager

        # Initialize the SpriteManager
        self.sprite_manager = SpriteManager()

        # Create player and NPCs
        self.player = Player('assets/images/sprites/cat01.png', 100, 100)
        self.npc = NPC('assets/images/sprites/piranha.png', 200, 200)

        # Add them to the sprite manager
        self.sprite_manager.add_player(self.player)
        self.sprite_manager.add_npc(self.npc)

    def handle_events(self, events: List[pygame.event.Event]) -> Union[str, None]:
        """Handle events specific to gameplay."""
        for event in events:
            if event.type == pygame.QUIT:
                return "EXIT"  # Return 'EXIT' if the player wants to quit
            if event.type == pygame.KEYDOWN:
                # Add any player controls here, e.g., move the player
                pass

    def update(self) -> None:
        """Update the game state (sprite positions, collision detection, etc.)."""
        self.sprite_manager.update_sprites()

        # Check for collisions
        if self.sprite_manager.check_collisions(self.player):
            print("Player collided with an NPC!")

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current gameplay state."""
        screen.fill((0, 0, 0))  # Clear the screen with black
        self.sprite_manager.draw_sprites(screen)  # Draw all sprites




    

   


class StateManager:
    """Manages switching between different game states."""
    
    def __init__(self, initial_state: GameState, text_renderer: TextRenderer, window_manager: WindowManager, config: Config):
        """Initialize with the first state."""
        self.current_state = initial_state
        self.text_renderer = text_renderer
        self.window_manager = window_manager
        self.config = config

    def switch_state(self, new_state_name: str) -> None:
        """Switch to a new game state based on the state name."""
        if new_state_name == "MAIN_MENU":
            self.current_state = MainMenuState(self.config, self.text_renderer, self.switch_to_options)
        elif new_state_name == "GAMEPLAY":
            self.current_state = GamePlayState(self.text_renderer, self.window_manager)
        elif new_state_name == "OPTIONS_MENU":
            self.current_state = OptionsMenuState(self.window_manager, self.text_renderer, self.switch_to_main_menu, self.switch_to_credits)
        elif new_state_name == "CREDITS":
            self.current_state = CreditRollState(self.text_renderer, self.switch_back_to_options)

    def handle_events(self, events: List[pygame.event.Event]) -> Union[str, None]:
        """Delegate event handling to the current state."""
        result = self.current_state.handle_events(events)
        if result == "EXIT":
            return "EXIT"
        if result:
            self.switch_state(result)

    def update(self) -> None:
        """Delegate update logic to the current state and handle state transitions."""
        result = self.current_state.update()
        if result:
            self.switch_state(result)

    def draw(self, screen: pygame.Surface) -> None:
        """Delegate drawing to the current state."""
        self.current_state.draw(screen)

    def switch_to_gameplay(self) -> None:
        """Switch to gameplay state."""
        self.switch_state("GAMEPLAY")
        
    def switch_to_options(self) -> None:
        """Switch to the options menu."""
        self.switch_state("OPTIONS_MENU")

    def switch_to_credits(self) -> None:
        """Switch to the credits roll state."""
        self.switch_state("CREDITS")

    def switch_back_to_options(self) -> None:
        """Switch back to the options menu after the credits roll finishes."""
        self.switch_state("OPTIONS_MENU")

    def switch_to_main_menu(self) -> None:
        """Switch back to the main menu."""
        self.switch_state("MAIN_MENU")



class SpriteManager:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()

    def add_player(self, player):
        """Add a player sprite to the game."""
        self.all_sprites.add(player)
        self.player_group.add(player)

    def add_npc(self, npc):
        """Add an NPC sprite to the game."""
        self.all_sprites.add(npc)
        self.npc_group.add(npc)

    def update_sprites(self):
        """Update all sprites in the game."""
        self.all_sprites.update()

    def draw_sprites(self, screen):
        """Draw all sprites to the screen."""
        self.all_sprites.draw(screen)

    def check_collisions(self, player):
        """Check for collisions between player and NPCs."""
        return pygame.sprite.spritecollide(player, self.npc_group, False)


# Input and player management
class InputManager:
    """Handles player input like keyboard, mouse, or controller events."""


class Player(pygame.sprite.Sprite):
    """A player sprite that can move around."""
    def __init__(self, image_path, x, y):
        super().__init__()  # Call Sprite initializer
        self.image = pygame.image.load(image_path)  # Load the player's image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.x = x  # Initial X position
        self.rect.y = y  # Initial Y position

    def update(self):
        """Update the player's position."""
        keys = pygame.key.get_pressed()  # Check for key inputs
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5


class NPC(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Handle NPC-specific movement (e.g., random wandering)."""
        directions = [(5, 0), (-5, 0), (0, 5), (0, -5)]
        move = random.choice(directions)
        self.rect.x += move[0]
        self.rect.y += move[1]
        

# Sound and music management
class SoundManager:
    """Handles loading and playing sound effects and background music."""
    
    
class LogManger:
    """Manages creating, updating log files."""


class Game:
    """Main game class responsible for the game loop and rendering."""

    def __init__(self, config: Config):
        """Initialize the game window and game settings."""
        pygame.init()

        # Use the WindowManager to set up the window
        self.window_manager = WindowManager(config)

        # Create the FontManager to manage the current font settings
        self.font_manager = FontManager(default_font=config.DEFAULT_FONT_NAME, default_size=config.DEFAULT_FONT_SIZE)

        # Create a TextRenderer to handle all text drawing
        self.text_renderer = TextRenderer(self.font_manager)

        # Set up the clock for consistent frame rate
        self.clock = pygame.time.Clock()

        # Initialize the state manager with the intro state
        self.state_manager = StateManager(IntroState(self.text_renderer), self.text_renderer, self.window_manager, config)

        # Flag to control the game loop
        self.running = True

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            # Get all the events that have occurred since the last frame
            events = pygame.event.get()
    
            # Handle game state events
            result = self.state_manager.handle_events(events)
    
            # If the result is "EXIT", stop the game loop
            if result == "EXIT":
                self.running = False
    
            # Update the current game state
            self.state_manager.update()
    
            # Draw the current frame
            screen = self.window_manager.get_screen()
            self.state_manager.draw(screen)
    
            # Update the display
            pygame.display.flip()
    
            # Limit the frame rate to the configured FPS
            self.clock.tick(Config.FPS)
        
        # Quit the game when the loop ends
        self.quit_game()


    def quit_game(self) -> None:
        """Gracefully quit the game."""
        # Properly quit Pygame
        pygame.quit()
    
        # Terminate the Python process
        sys.exit()


# OOP approach: create a Game object and run it
if __name__ == "__main__":
    game = Game(Config)
    game.run()