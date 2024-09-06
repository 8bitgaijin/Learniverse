# -*- coding: utf-8 -*-
"""
@author: Alvadore Retro Technology
Learniverse Lite: Rainbow Numbers
Very simplified "lite" version of Learniverse for a la carte purchase.
v2.1.12 Release version
9/5/2024 14:02 local time
"""

import datetime
import json
import os
import pygame
import random
import sys
import time

# Set the title of the window
pygame.display.set_caption("Learniverse Lite: Rainbow Numbers")

# Constants
DISPLAY_TIME = 2000  # Time to display the text at full opacity (in milliseconds)
FADE_SPEED = 1  # Controls the fade-in and fade-out speed

#COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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

# Define color themes. Theme name should reference TEXT color
color_themes = {
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

# Global variable to store the last generated problem
last_problem = None

# Global State
REFERENCE_RESOLUTION = (1366, 768)  # The resolution that fits the game assets best
BASE_RESOLUTION = (1920, 1080)
BASE_FONT_SIZE = 120  # Define a base font size for 1920x1080 resolution
current_font_name_or_path = "timesnewroman"  # Set to the default font initially
music_volume = 0.5  # Start at 50% volume
text_color = RED  # Set the initial text color to white
shadow_color = RED  # Set the initial shadow color to black
screen_color = RED

# New function to create the log message (more pure)
def create_log_message(message):
    """Creates a log message with a timestamp (pure function)."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {message}"

# New function to handle logging (impure, deals with I/O)
def log_message(log_entry):
    """Logs the message to both the console and the error_log.txt file (impure function)."""
    try:
        # Print the log entry to the console
        print(log_entry)

        # Attempt to open the log file and write the log entry
        with open("error_log.txt", "a") as error_file:
            error_file.write(log_entry + "\n")

    except Exception as e:
        # If an error occurs, print an error message to the console
        print(f"Failed to log message: {e}")

# Initialize the icon variable as None
icon = None

try:
    # Try to load your icon (PNG or ICO)
    icon = pygame.image.load('assets/images/LLRN.ico')
    # If successful, set the icon for the window and taskbar
    pygame.display.set_icon(icon)
except FileNotFoundError as e:
    # Log the error if the file is not found
    log_entry = create_log_message(f"Icon file not found: {e}")
    log_message(log_entry)
    print("Icon file not found, continuing without a custom icon.")
except pygame.error as e:
    # Log the error if Pygame has an issue loading the icon
    log_entry = create_log_message(f"Failed to load icon: {e}")
    log_message(log_entry)
    print("Failed to load icon, continuing without a custom icon.")

# Only set the icon if it was successfully loaded
if icon:
    pygame.display.set_icon(icon)

# Pygame Initialization
try:
    pygame.init()
    pygame.mixer.init()
except pygame.error as e:
    log_entry = create_log_message(f"Error initializing Pygame: {e}")
    log_message(log_entry)
    sys.exit(1)

# Resolutions
WINDOWED_RESOLUTIONS = [
    (640, 360), (854, 480), (1280, 720), (1366, 768), 
    (1600, 900), (1920, 1080), (2560, 1440), (3840, 2160)
]
info = pygame.display.Info()  # Get current display info
MAX_DISPLAY_RESOLUTION = (info.current_w, info.current_h)
AVAILABLE_RESOLUTIONS = [
    res for res in WINDOWED_RESOLUTIONS if res[0] <= MAX_DISPLAY_RESOLUTION[0] and res[1] <= MAX_DISPLAY_RESOLUTION[1]
]
current_resolution_index = AVAILABLE_RESOLUTIONS.index((1280, 720))  # Default to 1280x720

# Display and Resolution Setup
clock = pygame.time.Clock()
WIDTH, HEIGHT = AVAILABLE_RESOLUTIONS[current_resolution_index]
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize in windowed mode

# Function Definitions
def apply_theme(theme_name):
    global text_color, shadow_color, screen_color, current_theme
    
    if theme_name in color_themes:
        theme = color_themes[theme_name]
        text_color = theme["text_color"]
        shadow_color = theme["shadow_color"]
        screen_color = theme["screen_color"]
        current_theme = theme_name  # Update the global current_theme variable
    else:
        log_entry = create_log_message(f"Theme {theme_name} not found. Defaulting to light theme.")
        log_message(log_entry)
        apply_theme("light")

# Function to calculate dynamic font size based on resolution
def get_dynamic_font_size():
    # Calculate scaling factor based on resolution
    scale_factor = min(WIDTH / BASE_RESOLUTION[0], HEIGHT / BASE_RESOLUTION[1])
    # Adjust the font size
    dynamic_font_size = int(BASE_FONT_SIZE * scale_factor)
    return dynamic_font_size

# Initialize the font based on the dynamically calculated font size.
def init_fonts():
    font_size = get_dynamic_font_size()
    
    # Check if the current font path is a file.
    if os.path.isfile(current_font_name_or_path):
        return pygame.font.Font(current_font_name_or_path, font_size)  # Load the font from the specified file.
    else:
        return pygame.font.SysFont(current_font_name_or_path, font_size)  # Load the system font by name.

# Update positions and fonts dynamically
def update_positions():
    global start_text, options_text, exit_text, back_to_main_menu_text
    global volume_label_text, resolution_label_text, volume_percentage_text
    global start_rect, options_rect, exit_rect, back_to_main_menu_rect
    global volume_label_rect, volume_percentage_rect, minus_rect, plus_rect
    global resolution_label_rect, resolution_minus_rect, resolution_plus_rect
    global problem_rect, question_pos, input_pos

    # Update the font based on current resolution
    font = init_fonts()
    
    # Update text elements
    start_text = font.render("Start", True, text_color)
    options_text = font.render("Options", True, text_color)
    exit_text = font.render("X", True, RED)
    back_to_main_menu_text = font.render("Back to Main Menu", True, text_color)
    volume_label_text = font.render("Volume:", True, text_color)
    resolution_label_text = font.render("Resolution:", True, text_color)
    
    # Volume percentage display
    volume_percentage_text = font.render(f"{int(music_volume * 100)}%", True, text_color)
    
    # Calculate positions as percentages of the screen dimensions
    start_rect = start_text.get_rect(center=(WIDTH * 0.50, HEIGHT * 0.40))
    options_rect = options_text.get_rect(center=(WIDTH * 0.50, HEIGHT * 0.60))
    exit_rect = exit_text.get_rect(topright=(WIDTH - 20, 20))  # Keep exit button fixed in top-right
    
    back_to_main_menu_rect = back_to_main_menu_text.get_rect(center=(WIDTH * 0.50, HEIGHT * 0.70))
    
    # Volume Control Positions
    volume_label_rect = volume_label_text.get_rect(center=(WIDTH * 0.4, HEIGHT * 0.50))  # "Volume:" label
    volume_percentage_rect = volume_percentage_text.get_rect(center=(WIDTH * 0.62, HEIGHT * 0.50))  # Percentage display
    
    # Minus and Plus buttons for volume control
    minus_rect = font.render("-", True, text_color).get_rect(center=(WIDTH * 0.25, HEIGHT * 0.5))
    plus_rect = font.render("+", True, text_color).get_rect(center=(WIDTH * 0.75, HEIGHT * 0.5))
    
    # Resolution Control Positions
    resolution_label_rect = resolution_label_text.get_rect(center=(WIDTH * 0.4, HEIGHT * 0.60))
    resolution_minus_rect = font.render("-", True, text_color).get_rect(center=(WIDTH * 0.2, HEIGHT * 0.60))
    resolution_plus_rect = font.render("+", True, text_color).get_rect(center=(WIDTH * 0.85, HEIGHT * 0.60))
    
    # Update math problem positions
    question_pos = (WIDTH * 0.5, HEIGHT * 0.4)
    input_pos = (WIDTH * 0.5, HEIGHT * 0.6)
    problem_rect = font.render("?", True, text_color).get_rect(center=question_pos)

def load_options():
    global current_font_name_or_path, music_volume, current_resolution_index, current_theme
    
    try:
        with open("options.json", "r") as file:
            options = json.load(file)
        
        # Apply loaded settings
        current_font_name_or_path = options.get("font", "timesnewroman")
        music_volume = options.get("volume", 0.5)
        current_resolution_index = options.get("current_resolution_index", AVAILABLE_RESOLUTIONS.index((1280, 720)))
        current_theme = options.get("current_theme", "light")  # Load the theme, default to "light" if not found
        
    except FileNotFoundError:
        log_entry = create_log_message("Options file not found, using default settings.")
        log_message(log_entry)
        current_theme = "light"
    except Exception as e:
        log_entry = create_log_message(f"Error loading options: {e}")
        log_message(log_entry)
    
    apply_resolution()  # Apply resolution based on loaded settings
    apply_theme(current_theme)  # Apply the loaded theme
    pygame.mixer.music.set_volume(music_volume)
    font = init_fonts()
    update_positions()

def apply_resolution():
    global WIDTH, HEIGHT, screen, current_resolution_index
    
    current_windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
    screen = pygame.display.set_mode(current_windowed_resolution)
    WIDTH, HEIGHT = current_windowed_resolution

def draw_text(
    text, font, color, x, y, surface=None, max_width=None, center=False, 
    enable_shadow=False, shadow_color=None, x_shadow_offset=4, y_shadow_offset=4,
    return_rect=False):
    """
    Draw text on the given surface (or screen if no surface is provided) with optional drop shadow,
    word wrapping, centering, and optional rect return.

    Arguments:
    text -- The text to display.
    font -- The font to use for rendering.
    color -- The color of the text.
    x, y -- The top-left coordinates for drawing the text.
    surface -- The surface to draw the text on (defaults to screen if None).
    max_width -- The maximum width for word wrapping (optional).
    center -- Whether to center the text horizontally (optional).
    enable_shadow -- Whether to enable a drop shadow (optional).
    shadow_color -- The color of the drop shadow (optional, defaults to BLACK).
    x_shadow_offset -- The X offset for the drop shadow (optional, defaults to 2).
    y_shadow_offset -- The Y offset for the drop shadow (optional, defaults to 2).
    return_rect -- Whether to return the rect of the drawn text (optional).

    Returns:
    If return_rect is True, returns the rect of the first line of drawn text. Otherwise, returns None.
    """
    
    # Use the screen as the default surface if none is provided
    if surface is None:
        surface = screen

    # If shadow_color is not provided, use the passed shadow_color or global value
    if shadow_color is None:
        shadow_color = globals().get('shadow_color', BLACK)
    
    # Split text into lines based on max_width for word wrapping
    if max_width:
        lines = []
        words = text.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
    else:
        lines = [text]

    text_rect = None

    for i, line in enumerate(lines):
        if center:
            # Center the line horizontally within the given max_width
            text_width = font.size(line)[0]
            draw_x = (WIDTH - text_width) // 2
        else:
            draw_x = x
        
        if enable_shadow:
            # Draw the shadow with the correct shadow_color
            shadow_surface = font.render(line, True, shadow_color)
            surface.blit(shadow_surface, (draw_x + x_shadow_offset, y + y_shadow_offset))

        # Draw the main text
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (draw_x, y))
        
        # Calculate rect for the first line
        if i == 0 and return_rect:
            text_rect = pygame.Rect(draw_x, y, font.size(line)[0], font.size(line)[1])
        
        # Move down to the next line
        y += font.get_linesize()

    return text_rect if return_rect else None

def introduction(font):
    fade_text_in_and_out("Developed by:", "Alvadore Retro Technology", font)

def fade_text_in_and_out(line1, line2, font, max_width=None):
    alpha = 0
    fading_in = True
    text_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Surface with alpha channel
    
    while fading_in or alpha > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # Skip to the main menu

        # Clear the text surface
        text_surface.fill((0, 0, 0, 0))  # Fully transparent background

        # Adjust the alpha of the surface
        text_surface.set_alpha(alpha)

        # Draw the first line of text onto the transparent text surface
        draw_text(
            line1, font, text_color, 0, HEIGHT * 0.3, text_surface,
            max_width=WIDTH, center=True, enable_shadow=True
        )
        draw_text("Start", font, text_color, 0, HEIGHT * 0.55, screen, center=True, enable_shadow=True, return_rect=True)


        # Draw the second line of text onto the transparent text surface
        draw_text(
            line2, font, text_color, 0, HEIGHT * 0.6, text_surface,
            max_width=WIDTH, center=True, enable_shadow=True
        )

        # Fill the screen with black
        screen.fill(screen_color)

        # Blit the transparent text surface onto the main screen
        screen.blit(text_surface, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)

        # Handle the fade-in and fade-out logic
        if fading_in:
            alpha += FADE_SPEED
            if alpha >= 255:
                alpha = 255
                fading_in = False
                pygame.time.delay(DISPLAY_TIME)  # Wait for the set display time
        else:
            alpha -= FADE_SPEED

def credit_roll():
    # Load the cat sprite and initialize its position and direction
    try:
        cat_image = pygame.image.load("assets/images/sprites/cat01.png").convert_alpha()
        cat_rect = cat_image.get_rect()
        cat_rect.y = HEIGHT - cat_rect.height  # Position the cat at the bottom of the screen
        cat_speed = 4  # Set the speed of the cat
        cat_direction = 1  # 1 for right, -1 for left
        cat_loaded = True
    except (FileNotFoundError, pygame.error) as e:
        log_entry = create_log_message(f"Error loading cat sprite: {e}")
        log_message(log_entry)
        cat_loaded = False

    # Function to update and draw the cat sprite
    def draw_moving_cat(cat_image, cat_rect, cat_direction):
        nonlocal cat_speed

        cat_rect.x += cat_speed * cat_direction
        
        # Flip direction if the cat hits the edge of the screen
        if cat_rect.left <= 0 or cat_rect.right >= WIDTH:
            cat_direction *= -1
            cat_image = pygame.transform.flip(cat_image, True, False)
        
        screen.blit(cat_image, cat_rect)
        return cat_image, cat_direction

    # Override the fade_text_in_and_out function to include the moving cat
    def fade_text_in_and_out_with_cat(line1, line2, font, max_width=None):
        alpha = 0
        fading_in = True
        text_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pause_time = 2000  # Time in milliseconds to pause at full alpha
        pause_counter = 0

        while fading_in or alpha > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return  # Skip to the main menu

            # Clear the text surface
            text_surface.fill((0, 0, 0, 0))

            # Adjust the alpha of the surface
            text_surface.set_alpha(alpha)

            # Draw the first line of text onto the transparent text surface
            draw_text(
                line1, font, text_color, 0, HEIGHT * 0.3, text_surface,
                max_width=WIDTH, center=True, enable_shadow=True
            )

            # Draw the second line of text onto the transparent text surface
            draw_text(
                line2, font, text_color, 0, HEIGHT * 0.6, text_surface,
                max_width=WIDTH, center=True, enable_shadow=True
            )

            # Fill the screen with black
            screen.fill(screen_color)

            # Blit the transparent text surface onto the main screen
            screen.blit(text_surface, (0, 0))
            
            # Draw the moving cat sprite if it was successfully loaded
            if cat_loaded:
                nonlocal cat_image, cat_direction
                cat_image, cat_direction = draw_moving_cat(cat_image, cat_rect, cat_direction)

            pygame.display.flip()
            clock.tick(60)

            # Handle the fade-in and fade-out logic
            if fading_in:
                alpha += FADE_SPEED
                if alpha >= 255:
                    alpha = 255
                    fading_in = False
                    pause_counter = pause_time  # Start the pause counter
            else:
                if pause_counter > 0:
                    pause_counter -= clock.get_time()  # Decrease the counter based on elapsed time
                else:
                    alpha -= FADE_SPEED

    # Use the modified fade_text_in_and_out_with_cat function
    fade_text_in_and_out_with_cat("Developed by:", "Alvadore Retro Technology", font)
    fade_text_in_and_out_with_cat("Chief Executive Officer", "William Alexander Martins", font)
    fade_text_in_and_out_with_cat("Chief Financial Officer", "Mary Evangeline Martins", font)
    fade_text_in_and_out_with_cat("Chief Information Officer", "Shane William Martins", font)
    fade_text_in_and_out_with_cat("Chief Operations Officer", "Ethan Hunter Martins", font)
    fade_text_in_and_out_with_cat("Chief Technology Officer", "Jeffrey Matthew Neff Esq.", font)
    fade_text_in_and_out_with_cat("Made possible by:", "Supporters like you!", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "Guido van Rossum", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the PyInstaller team", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the Pygame team", font)
    fade_text_in_and_out_with_cat("Pygame is licensed under", "LGPL version 2.1", font)

def draw_exit_button():
    global current_font_name_or_path  # Ensure we're using the global variable

    # Update the dynamic font size for the exit button based on the current resolution
    exit_font_size = int(get_dynamic_font_size() * 0.8)  # Slightly smaller than the other fonts

    # Recreate the font with the new size using the current font name or path
    if os.path.isfile(current_font_name_or_path):
        # If it's a file path, load the font from the file
        exit_font = pygame.font.Font(current_font_name_or_path, exit_font_size)
    else:
        # If it's a system font, use the font name
        exit_font = pygame.font.SysFont(current_font_name_or_path, exit_font_size)

    # Calculate the position for the "X" to be at 95% across the screen width
    x_position = WIDTH *  0.95
    y_position = 20  # Keep the Y position at 20 pixels from the top

    # Use draw_text to render the exit button with a drop shadow and get its rect
    exit_rect = draw_text("X", exit_font, RED, x_position, y_position, screen, enable_shadow=True, return_rect=True)

    return exit_rect

def check_exit_click(mouse_pos, exit_rect):
    """Check if the 'X' exit button was clicked."""
    if exit_rect.collidepoint(mouse_pos):
        pygame.quit()
        sys.exit()

def select_random_background(folder_path):
    """Select a random background image from the given folder."""
    try:
        # List all image files in the folder
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

        # If no image files are found, raise an exception
        if not image_files:
            raise FileNotFoundError(f"No image files found in folder: {folder_path}")

        # Randomly select an image file
        selected_image = random.choice(image_files)
        image_path = os.path.join(folder_path, selected_image)
        
        return image_path
    except FileNotFoundError as e:
        log_entry = create_log_message(f"Error selecting background image: {e}")
        log_message(log_entry)
        return None
    except Exception as e:
        log_entry = create_log_message(f"Unexpected error selecting background image: {e}")
        log_message(log_entry)
        return None

def draw_background(image_path):
    """Load and draw the pre-selected background image scaled to fit the screen resolution."""
    try:
        if image_path:
            # Load the selected background image
            background_image = pygame.image.load(image_path).convert()

            # Define the base resolution (the original size of your art)
            base_width, base_height = 1920, 1080

            # Calculate the scaling factor based on the current screen resolution
            scale_factor_x = WIDTH / base_width
            scale_factor_y = HEIGHT / base_height

            # Scale the image to fit the current resolution
            scaled_background = pygame.transform.scale(
                background_image, (int(base_width * scale_factor_x), int(base_height * scale_factor_y))
            )

            # Blit the scaled background image onto the screen
            screen.blit(scaled_background, (0, 0))  # Draw it starting at the top-left corner
        else:
            raise FileNotFoundError("No valid background image path provided.")
    except (pygame.error, FileNotFoundError) as e:
        # Handle the missing file case or Pygame error
        log_entry = create_log_message(f"Error loading background image: {e}")
        log_message(log_entry)
        screen.fill(screen_color)  # Fallback to black if loading fails
    except Exception as e:
        log_entry = create_log_message(f"Unexpected error while drawing background: {e}")
        log_message(log_entry)
        screen.fill(screen_color)

def rainbow_numbers_explanation():
    # Define the folder path for the background images
    folder_path = "assets/images/explanation"

    # Select a random background image
    background_image_path = select_random_background(folder_path)

    # Define the text to display
    texts = [
        '''Unlock the power of 10 with "Rainbow Numbers." This fun, interactive game helps students master the building blocks of math.''',
        '''With young learners in mind, Rainbow Numbers teaches how to find the number needed to reach 10—a key skill in mental math.''',
        '''Why 10? The number 10 is a friendly and familiar number in math.''',
        '''Mastering 10 makes addition and subtraction easier, faster, and more intuitive, laying the groundwork for future math success.''',
        '''In Rainbow Numbers, students are challenged to find the "rainbow partner"—the number that makes 10 when added to the given number.''',
        '''This approach reinforces mental math skills, builds confidence, and makes learning engaging and enjoyable.''',
        '''When students master Rainbow Numbers, they aren't just learning to add—they’re building a core strategy for their entire math journey.''',
        '''By focusing on the number 10, we make math less intimidating, giving every student the tools they need to succeed.'''
    ]

    for text in texts:
        # Draw the background before displaying the text
        draw_background(background_image_path)

        # Display the text
        display_text_and_wait(text)

    return "main_menu"  # Return to the main menu after all texts are displayed

def display_text_and_wait(text):
    """Clears the screen, displays the given text, and waits for a mouse click."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        # screen.fill(screen_color)  # Clear the screen with the current theme's background color
        draw_text(text, font, text_color, WIDTH // 2, HEIGHT // 20, center=True, max_width=WIDTH * 0.95, enable_shadow=True)  # Display the text
        pygame.display.flip()

    pygame.time.delay(200)  # Optional: Delay to prevent accidental double clicks

def main_menu():
    global font  # Ensure we update the global font variable

    while True:
        # Recalculate the font size dynamically based on the current resolution
        font = pygame.font.SysFont(current_font_name_or_path, get_dynamic_font_size())  # Use the global font

        # Draw the background for the main menu
        draw_background(main_menu_background)
        
        # Draw the text options using the new draw_text function with rects for click detection
        draw_text("Learniverse: Rainbow Numbers", font, text_color, 0, HEIGHT * 0.2, screen, center=True, enable_shadow=True, return_rect=False, max_width=WIDTH)
        start_rect = draw_text("Start", font, text_color, 0, HEIGHT * 0.55, screen, center=True, enable_shadow=True, return_rect=True)
        options_rect = draw_text("Options", font, text_color, 0, HEIGHT * 0.7, screen, center=True, enable_shadow=True, return_rect=True)
        explanation_rect = draw_text("Rainbow numbers?", font, text_color, 0, HEIGHT * 0.85, screen, center=True, enable_shadow=True, return_rect=True)
        
        # Draw the exit button using the new draw_text function and get its rect for click detection
        exit_rect = draw_exit_button()
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if "Start" was clicked
                if start_rect and start_rect.collidepoint(mouse_pos):
                    return "start_game"  # Return to indicate starting the game
                # Check if "Options" was clicked
                elif options_rect and options_rect.collidepoint(mouse_pos):
                    return "options_menu"  # Return to indicate transitioning to options menu
                elif explanation_rect and explanation_rect.collidepoint(mouse_pos):
                    return "rainbow_numbers_explanation"  # Return to indicate transitioning to options menu
                # Check if "X" was clicked
                check_exit_click(mouse_pos, exit_rect)
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_b:  # Check if the 'b' key is pressed
            #         return "bonus_game"  # Skip directly to the bonus game for debug

        clock.tick(60)

def get_filtered_fonts():
    # List of known problematic fonts to exclude (only essential exclusions)
    excluded_fonts = {
        'wingdings', 'wingdings2', 'wingdings3', 'webdings', 'bookshelfsymbol7', 
        'symbol', 'segoeuiemoji', 'segoeuisymbol', 'holomdl2assets', 'codicon', 
        'fontawesome47webfont', 'fontawesome4webfont47', 'fontawesome5brandswebfont', 
        'fontawesome5brandswebfont5154', 'fontawesome5regularwebfont', 'fontawesome5regularwebfont5154', 'fontawesome5solidwebfont', 
        'fontawesome5solidwebfont5154', 'materialdesignicons5webfont', 'materialdesignicons5webfont5955', 
        'materialdesignicons6webfont', 'materialdesignicons6webfont6996', 'remixicon', 'remixicon250', 
        'opensymbol', 'widelatin', 'segmdl2', 'REFSPCL', 'segoemdl2assets', 'segoefluenticons',
        'sansserifcollection', 'msreferencespecialty', 'msoutlook', 'miriammonoclmbookoblique',
        'miriamclmbook', 'miriamclm', 'lucidasanstypewriterregular', 'lucidasanstypewriteroblique',
        'goudystout', 'extra', 'dejavumathtexgyreregular', 'amiriquranregular'
    }

    # List fonts available through Pygame
    pygame_fonts = pygame.font.get_fonts()
    
    filtered_fonts = []
    fallback_font = "arial"  # Define a safe fallback font
    
    for font_name in sorted(pygame_fonts):
        if font_name not in excluded_fonts:
            try:
                # Try rendering a sample text to verify the font works
                sample_font = pygame.font.SysFont(font_name, get_dynamic_font_size())
                # If the font renders successfully, add it to the filtered list
                filtered_fonts.append(font_name)
            except Exception as e:
                log_entry = create_log_message(f"Skipping font {font_name} due to error: {e}")
                log_message(log_entry)
    
    # Ensure we have at least one valid font, fallback to 'arial' if necessary
    if not filtered_fonts:
        log_entry = create_log_message("No valid fonts found, falling back to 'arial'.")
        log_message(log_entry)
        filtered_fonts = [fallback_font]

    return filtered_fonts

def options_menu():
    global music_volume, current_resolution_index, screen, WIDTH, HEIGHT, current_windowed_resolution, current_font_name_or_path, font, text_color, shadow_color, screen_color  # Access the global variables

    # Get the filtered fonts list
    filtered_fonts = get_filtered_fonts()

    # Fallback to a default font if no valid fonts are found
    if not filtered_fonts:
        filtered_fonts = ["arial"]
        log_entry = create_log_message("No valid fonts found, falling back to 'arial'.")
        log_message(log_entry)

    # Set the current font index to match the current_font_name_or_path
    if current_font_name_or_path in filtered_fonts:
        current_font_index = filtered_fonts.index(current_font_name_or_path)
    else:
        current_font_index = 0
        current_font_name_or_path = filtered_fonts[current_font_index]

    # Track the current theme index based on the current applied theme
    for theme_name, theme_values in color_themes.items():
        if (text_color == theme_values["text_color"] and
            shadow_color == theme_values["shadow_color"] and
            screen_color == theme_values["screen_color"]):
            current_theme_index = list(color_themes.keys()).index(theme_name)
            break
    else:
        current_theme_index = list(color_themes.keys()).index("light")  # Default to "light" if no match is found

    while True:
        font = pygame.font.SysFont(current_font_name_or_path, get_dynamic_font_size())  # Update the font based on current font
        update_positions()

        # Draw the background for the options menu
        draw_background(options_background)

        # Y positions for consistent alignment
        volume_y = HEIGHT * 0.1  # line for the volume
        resolution_y = HEIGHT * 0.25  # line for the resolution
        theme_y = HEIGHT * 0.4  # line for the theme
        font_y = HEIGHT * 0.55  # line for the font
        credits_y = HEIGHT * 0.70  # line for the credits
        back_to_main_y = HEIGHT * 0.85
        left_buffer = 0.05
        right_buffer = 0.95

        # Draw the options and get rects for click detection
        back_to_main_menu_rect = draw_text("Back to Main Menu", font, text_color, 0, back_to_main_y, screen, center=True, enable_shadow=True, return_rect=True)

        # Draw the volume label, percentage, and control buttons with shadows
        draw_text("Volume:", font, text_color, WIDTH * (left_buffer * 2), volume_y, screen, enable_shadow=True)
        draw_text(f"{int(music_volume * 100)}%", font, text_color, WIDTH * 0.5, volume_y, screen, enable_shadow=True)
        
        # Calculate rects for volume control buttons based on the size of the rendered text
        minus_rect = draw_text("<", font, text_color, WIDTH * left_buffer, volume_y, screen, enable_shadow=True, return_rect=True)
        plus_rect = draw_text(">", font, text_color, WIDTH * right_buffer, volume_y, screen, enable_shadow=True, return_rect=True)

        # Draw the resolution controls with shadows
        draw_text("Resolution:", font, text_color, WIDTH * (left_buffer * 2), resolution_y, screen, enable_shadow=True)
        resolution_text = f"{AVAILABLE_RESOLUTIONS[current_resolution_index][0]}x{AVAILABLE_RESOLUTIONS[current_resolution_index][1]}"
        draw_text(resolution_text, font, text_color, WIDTH * 0.5, resolution_y, screen, enable_shadow=True)
        
        # Calculate rects for resolution control buttons
        resolution_minus_rect = draw_text("<", font, text_color, WIDTH * left_buffer, resolution_y, screen, enable_shadow=True, return_rect=True)
        resolution_plus_rect = draw_text(">", font, text_color, WIDTH * right_buffer, resolution_y, screen, enable_shadow=True, return_rect=True)

        # Draw the theme controls with shadows
        draw_text("Theme:", font, text_color, WIDTH * (left_buffer * 2), theme_y, screen, enable_shadow=True)
        theme_name = list(color_themes.keys())[current_theme_index]
        draw_text(f"{theme_name.capitalize()}", font, text_color, WIDTH * 0.5, theme_y, screen, enable_shadow=True)
        
        # Calculate rects for theme control buttons
        theme_minus_rect = draw_text("<", font, text_color, WIDTH * left_buffer, theme_y, screen, enable_shadow=True, return_rect=True)
        theme_plus_rect = draw_text(">", font, text_color, WIDTH * right_buffer, theme_y, screen, enable_shadow=True, return_rect=True)

        # Display the current font in use with < and > buttons
        left_arrow_rect = draw_text("<", font, text_color, WIDTH * left_buffer, font_y, screen, enable_shadow=True, return_rect=True)
        draw_text(f"Font: {current_font_name_or_path}", font, text_color, WIDTH * 0.5, font_y, screen, center=True, enable_shadow=True)
        right_arrow_rect = draw_text(">", font, text_color, WIDTH * right_buffer, font_y, screen, enable_shadow=True, return_rect=True)

        # Draw the "Credits" option
        credits_rect = draw_text("Credits", font, text_color, 0, credits_y, screen, center=True, enable_shadow=True, return_rect=True)

        # Draw the exit button with a shadow
        exit_rect = draw_exit_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Check if "Back to Main Menu" was clicked
                if back_to_main_menu_rect and back_to_main_menu_rect.collidepoint(mouse_pos):
                    save_options()
                    return "main_menu"
                
                # Check if "-" button was clicked for volume
                elif minus_rect and minus_rect.collidepoint(mouse_pos):
                    decrease_volume()
                
                # Check if "+" button was clicked for volume
                elif plus_rect and plus_rect.collidepoint(mouse_pos):
                    increase_volume()

                # Check if "-" button was clicked for resolution
                if resolution_minus_rect and resolution_minus_rect.collidepoint(mouse_pos):
                    current_resolution_index = max(0, current_resolution_index - 1)
                    current_windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
                    screen = pygame.display.set_mode(current_windowed_resolution)
                    WIDTH, HEIGHT = current_windowed_resolution
                    update_positions()

                # Check if "+" button was clicked for resolution
                if resolution_plus_rect and resolution_plus_rect.collidepoint(mouse_pos):
                    current_resolution_index = min(len(AVAILABLE_RESOLUTIONS) - 1, current_resolution_index + 1)
                    current_windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
                    screen = pygame.display.set_mode(current_windowed_resolution)
                    WIDTH, HEIGHT = current_windowed_resolution
                    update_positions()
                
                # Check if "<" was clicked to go to the previous theme
                if theme_minus_rect and theme_minus_rect.collidepoint(mouse_pos):
                    current_theme_index = (current_theme_index - 1) % len(color_themes)
                    apply_theme(list(color_themes.keys())[current_theme_index])
                
                # Check if ">" was clicked to go to the next theme
                if theme_plus_rect and theme_plus_rect.collidepoint(mouse_pos):
                    current_theme_index = (current_theme_index + 1) % len(color_themes)
                    apply_theme(list(color_themes.keys())[current_theme_index])

                # Check if "<" was clicked to go to the previous font
                if left_arrow_rect and left_arrow_rect.collidepoint(mouse_pos):
                    current_font_index = (current_font_index - 1) % len(filtered_fonts)
                    current_font_name_or_path = filtered_fonts[current_font_index]
                
                # Check if ">" was clicked to go to the next font
                if right_arrow_rect and right_arrow_rect.collidepoint(mouse_pos):
                    current_font_index = (current_font_index + 1) % len(filtered_fonts)
                    current_font_name_or_path = filtered_fonts[current_font_index]

                # Check if "Credits" was clicked
                if credits_rect and credits_rect.collidepoint(mouse_pos):
                    credit_roll()  # Trigger the credit roll

                # Check if "X" was clicked
                check_exit_click(mouse_pos, exit_rect)

        clock.tick(60)

def save_options():
    """Save the current user options to a JSON file."""
    options = {
        "font": current_font_name_or_path,
        "volume": music_volume,
        "current_resolution_index": current_resolution_index,
        "current_theme": current_theme  # Save the currently selected theme
    }

    try:
        with open("options.json", "w") as file:
            json.dump(options, file)
    except Exception as e:
        log_entry = create_log_message(f"Error saving options: {e}")
        log_message(log_entry)

def generate_problem():
    global last_problem
    rainbow_numbers = [(0, 10), (1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (9, 1), (10, 0)]

    while True:
        num1, num2 = random.choice(rainbow_numbers)
        current_problem = (num1, num2)

        # Check if the current problem is the same as the last problem
        if current_problem != last_problem and current_problem[::-1] != last_problem:
            last_problem = current_problem
            break
    
    answer = num1 + num2
    return num1, num2, answer

def display_math_problem(num1, num2, user_input, first_input, line_length_factor=1.9):
    screen.fill(screen_color)
    
    # Dynamically calculate positions based on screen size
    right_x = WIDTH * 0.55  # Right edge for alignment
    num1_y = HEIGHT * 0.4
    num2_y = HEIGHT * 0.5
    line_y = HEIGHT * 0.57
    sum_y = HEIGHT * 0.63
    
    # Draw the first number (right-aligned)
    num1_surface = font.render(str(num1), True, text_color)
    num1_rect = num1_surface.get_rect(right=right_x, centery=num1_y)
    screen.blit(num1_surface, num1_rect)
    
    # Draw the plus sign (right-aligned with some offset)
    plus_sign_x = right_x - num1_surface.get_width() - WIDTH * 0.05
    plus_surface = font.render("+", True, text_color)
    plus_rect = plus_surface.get_rect(right=plus_sign_x, centery=num2_y)
    screen.blit(plus_surface, plus_rect)
    
    # Draw the second number placeholder or the input from the user (right-aligned)
    if first_input:
        input_text = "?"
    else:
        input_text = user_input
        
    input_surface = font.render(input_text, True, text_color)
    input_rect = input_surface.get_rect(right=right_x, centery=num2_y)
    screen.blit(input_surface, input_rect)
    
    # Calculate line width with a factor
    line_width = max(num1_surface.get_width(), input_surface.get_width(), font.size(str(num1 + num2))[0]) * line_length_factor
    pygame.draw.line(screen, text_color, (right_x - line_width, line_y), (right_x, line_y), 3)
    
    # Draw the sum (right-aligned)
    sum_surface = font.render(str(num1 + num2), True, text_color)
    sum_rect = sum_surface.get_rect(right=right_x, centery=sum_y)
    screen.blit(sum_surface, sum_rect)

    pygame.display.flip()

def start_game():
    running = True
    correct_answers = 0
    problem_count = 0
    total_questions = 10
    completion_times = []  # List to store time taken for each question

    # Frame rate limiting
    clock = pygame.time.Clock()
    
    stop_mp3()

    while running and problem_count < total_questions:
        num1, num2, answer = generate_problem()
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            # Clear the screen before drawing
            screen.fill(screen_color)
            
            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input)
            
            pygame.display.flip()  # Update the display
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Handle both the regular return key and the one on the numpad (10-key)
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        # Stop the timer when the answer is submitted
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)  # Round to nearest tenth of a second
                        completion_times.append(time_taken)
                        
                        if int(user_input) == num2:
                            correct_answers += 1
                            
                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats")
                            else:
                                display_result("CORRECT!", "assets/images/cats")
                        else:
                            display_result(f"Sorry, the answer is {num2}")
                        
                        # Clear the event queue to avoid queued inputs
                        pygame.event.clear()
        
                        problem_count += 1
                        question_complete = True  # Move to the next question
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 2:  # Limit input to two digits
                        user_input += event.unicode
                        first_input = False
        
            # Frame rate limiting
            clock.tick(60)

    # Calculate and print the average time taken
    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)

    # End of game display: show final score and average time
    screen.fill(screen_color)
    
    # Final score message
    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)
    
    # Average time per question message
    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.5, center=True, enable_shadow=True, max_width=WIDTH)
    
        # Perfect score check
        if correct_answers == total_questions:
            perfect_score_message = "Perfect score!"
            draw_text(perfect_score_message, font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
            # return "bonus_game"
    
            # Mastery check (perfect score + fast average time)
            if average_time < 3.0:
                mastery_message = "MASTERY!"
                draw_text(mastery_message, font, text_color, WIDTH // 2, HEIGHT * 0.75, center=True, enable_shadow=True)
    
    # Update the display with the final messages
    pygame.display.flip()
    
    # Show the final score and average time for 4 seconds
    time.sleep(4)

    if (correct_answers == total_questions):
        return "bonus_game"

    # After showing the final score, return to the main menu
    play_mp3()
    return "main_menu"

def bonus_game():
    # Check if the assets/images directory exists
    if not os.path.exists('assets/images'):
        # Log the error if needed
        log_entry = create_log_message("Assets folder 'assets/images' is missing. Returning to the main menu.")
        log_message(log_entry)
        return "main_menu"
    
    # Calculate scaling factors based on the current resolution
    scale_factor_x = WIDTH / REFERENCE_RESOLUTION[0]
    scale_factor_y = HEIGHT / REFERENCE_RESOLUTION[1]
    scale_factor = min(scale_factor_x, scale_factor_y)  # Maintain aspect ratio

    FALL_SPEED = 13 * scale_factor  # Base speed for falling platforms, scaled
    RESPAWN_RATE = 10  # Probability out of 100 for a new platform to spawn each frame
    PLATFORM_SPAWN_INTERVAL = 300  # Minimum time (milliseconds) between platform spawns
    PIRANHA_SPAWN_INTERVAL = 2000  # Time interval (milliseconds) between spawning additional piranhas
    
    running = True
    win = False
    game_over = False
    start_time = time.time()
    last_spawn_time = 0
    last_piranha_spawn_time = 0

    # Load images
    platform_img = pygame.image.load('assets/images/sprites/platform.jpg')
    bonus_mode_background = select_random_background("assets/images/bonus_mode")
    gameplay_background = select_random_background("assets/images/bonus_bkgs")

    # Load and scale the fat tuna image
    fat_tuna_img = pygame.image.load('assets/images/sprites/fat_tuna.png')
    fat_tuna_img = pygame.transform.scale(
        fat_tuna_img, 
        (int(fat_tuna_img.get_width() * scale_factor), int(fat_tuna_img.get_height() * scale_factor))
    )
    fat_tuna_rect = fat_tuna_img.get_rect(center=(WIDTH // 2, int(fat_tuna_img.get_height() * scale_factor) // 2))
    fat_tuna_speed = 5 * scale_factor  # Adjust speed based on scale
    fat_tuna_direction = -1  # Direction of movement, 1 is right, -1 is left

    # Load and scale the piranha image
    piranha_img = pygame.image.load('assets/images/sprites/piranha.png')
    piranha_img = pygame.transform.scale(
        piranha_img, 
        (int(piranha_img.get_width() * scale_factor), int(piranha_img.get_height() * scale_factor))
    )
    piranhas = [Piranha(piranha_img, 0, HEIGHT, 5 * scale_factor)]

    # Initialize platforms with the image
    platforms = [
        Platform(platform_img, int(100 * scale_factor), int(600 * scale_factor), int(200 * scale_factor), int(50 * scale_factor)),
        Platform(platform_img, int(400 * scale_factor), int(400 * scale_factor), int(200 * scale_factor), int(50 * scale_factor)),
        Platform(platform_img, int(700 * scale_factor), int(200 * scale_factor), int(200 * scale_factor), int(50 * scale_factor))
    ]
    
    # Scale the text positions and movements
    text_x, text_y = WIDTH // 2 - int(175 * scale_factor), HEIGHT // 2
    text_dx, text_dy = random.choice([-10, 10]), random.choice([-10, 10])
    text_dx *= scale_factor
    text_dy *= scale_factor

    # Initialize the cat
    player_img = pygame.image.load('assets/images/sprites/cat01.png')
    player_img = pygame.transform.scale(player_img, (int(player_img.get_width() * scale_factor), int(player_img.get_height() * scale_factor)))
    # Instantiate the Cat object with the correct scaling
    cat = Cat(player_img, WIDTH // 2, HEIGHT - player_img.get_rect().height, 25 * scale_factor, scale_factor)

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Load and play bonus game music
    bonus_music_directory = 'assets/music/bonus'
    random_mp3 = get_random_mp3(bonus_music_directory)
    
    if random_mp3:
        music_loaded = load_mp3(random_mp3)
        if music_loaded:
            play_mp3()  # Play only if the music was successfully loaded
            
    # Bonus Mode Display Phase
    while time.time() - start_time < 5 and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                pygame.quit()  # Ensure Pygame quits properly
                sys.exit()  # Exit the program
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    running = False
                    pygame.mixer.music.stop()
                    return

        # Draw the bonus mode background (or fallback to navy blue)
        if bonus_mode_background:
            draw_background(bonus_mode_background)
        else:
            screen.fill(screen_color)

        # Render the four lines of static text with drop shadows and centered
        draw_text("Controls:", font, text_color, 0, HEIGHT * 0.2, center=True, enable_shadow=True)
        draw_text("W = Jump", font, text_color, 0, HEIGHT * 0.4, center=True, enable_shadow=True)
        draw_text("A = Move Left", font, text_color, 0, HEIGHT * 0.6, center=True, enable_shadow=True)
        draw_text("D = Move Right", font, text_color, 0, HEIGHT * 0.8, center=True, enable_shadow=True)

        # Render the bouncing "Bonus Stage!" text
        text_surface = font.render("Bonus Stage!", True, text_color)
        text_width, text_height = text_surface.get_size()

        # Update text position
        text_x += text_dx
        text_y += text_dy

        # Check for collisions with the screen edges
        if text_x <= 0 or text_x >= WIDTH - text_width:
            text_dx = -text_dx
        if text_y <= 0 or text_y >= HEIGHT - text_height:
            text_dy = -text_dy

        # Draw the bouncing text at the new position
        screen.blit(text_surface, (text_x, text_y))
        pygame.display.flip()

        clock.tick(60)  # Control the frame rate

    try:
        # Gameplay Phase
        start_time = time.time()

        while running:
            elapsed_time = int(time.time() - start_time)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.mixer.music.stop()
                    pygame.quit()  # Ensure Pygame quits properly
                    sys.exit()  # Exit the program
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        running = False
                        pygame.mixer.music.stop()
                        return
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        cat.jump()

            cat.update(platforms)

            # Check for win condition
            if cat.rect.colliderect(fat_tuna_rect):
                win = True
                running = False

            # Check for game over condition
            for piranha in piranhas:
                if cat.rect.colliderect(piranha.rect):
                    game_over = True
                    running = False

            # Update piranhas positions
            for piranha in piranhas:
                piranha.update()

            # Update platform positions and remove them if they scroll off the bottom of the screen
            for platform in platforms[:]:
                platform.update(FALL_SPEED)
                if platform.rect.y > HEIGHT:
                    platforms.remove(platform)

            # Spawn new platforms at the top of the screen
            if current_time - last_spawn_time > PLATFORM_SPAWN_INTERVAL and random.randint(1, 100) <= RESPAWN_RATE:
                new_platform = Platform(
                    platform_img, 
                    random.randint(0, int(WIDTH - 200 * scale_factor)), 
                    -int(50 * scale_factor), 
                    int(200 * scale_factor), 
                    int(50 * scale_factor)
                )
                platforms.append(new_platform)
                last_spawn_time = current_time

            # Spawn new piranhas at the bottom of the screen
            if current_time - last_piranha_spawn_time > PIRANHA_SPAWN_INTERVAL:
                new_piranha = Piranha(piranha_img, 0, HEIGHT, 5 * scale_factor)
                piranhas.append(new_piranha)
                last_piranha_spawn_time = current_time

            # Move the fat tuna
            fat_tuna_rect.x += fat_tuna_speed * fat_tuna_direction
            if fat_tuna_rect.left <= 0 or fat_tuna_rect.right >= WIDTH:
                fat_tuna_direction *= -1  # Reverse direction when hitting the edge

            # Draw the gameplay background (or fallback to navy blue)
            if gameplay_background:
                draw_background(gameplay_background)
            else:
                screen.fill(screen_color)

            # Draw the platforms first
            for platform in platforms:
                platform.draw(screen)

            # Draw the piranhas
            for piranha in piranhas:
                piranha.draw(screen)

            # Draw the fat tuna
            screen.blit(fat_tuna_img, fat_tuna_rect.topleft)

            # Draw the cat on top of everything else
            cat.draw(screen)

            # Draw the timer on top of all elements
            draw_text(f"{elapsed_time}", font, text_color, WIDTH // 4, HEIGHT // 60)

            pygame.display.flip()
            clock.tick(24)  # Control the frame rate

    finally:
        # Ensure music stops and resources are freed if an exception occurs
        stop_mp3()

    if win:
        screen.fill(screen_color)
        draw_text(f"You caught the Fat Tuna in {elapsed_time} seconds!", font, text_color,  WIDTH // 2, HEIGHT // 3, center=True, max_width=WIDTH)
        pygame.display.flip()
        time.sleep(5)
    elif game_over:
        screen.fill(screen_color)
        draw_text("Game Over! You were eaten by the piranha.", font, text_color, WIDTH // 2, HEIGHT // 3, center=True, max_width=WIDTH)
        pygame.display.flip()
        time.sleep(5)
    
    # Re-do main menu music before returning
    main_menu_music_directory = "assets/music/main_menu"
    random_mp3 = get_random_mp3(main_menu_music_directory)
    if random_mp3:
        music_loaded = load_mp3(random_mp3)
        if music_loaded:
            play_mp3()  # Play only if the music was successfully loaded
    
    # Return to main menu
    return "main_menu"

def display_result(result_text, image_folder=None):
    """
    Display the result text and an optional image from the given folder.
    If an image is provided, display a particle effect over the image.
    """
    # Clear the event queue to avoid any unwanted inputs
    pygame.event.clear()

    # Initialize particle list
    particles = []

    if image_folder:
        image_path = select_random_background(image_folder)
        draw_background(image_path)

        # Generate particles for the effect
        for _ in range(500):  # Number of particles to generate
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = random.choice([NAVY_BLUE, (255, 255, 255), ROYAL_BLUE, LIGHT_BLUE])
            particles.append(Particle(x, y, color))
    
    else:
        # If no image folder is provided, fill the screen with the current screen color
        screen.fill(screen_color)
    
    # Display loop for particle effect
    for _ in range(50):  # Run the effect for 50 frames
        if image_folder:
            # Transparent fill to allow particles to fade
            screen.fill((0, 0, 0, 0))
            draw_background(image_path)

            # Update and draw each particle
            for particle in particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    particles.remove(particle)
                else:
                    particle.draw(screen)
        else:
            # For incorrect answers, just fill the screen with the current screen color
            screen.fill(screen_color)

        # Draw the result text on top of the particles or background
        draw_text(result_text, font, text_color, WIDTH // 2, HEIGHT // 2, center=True, enable_shadow=True)
        pygame.display.flip()
        # time.sleep(0.03)  # Small delay for animation timing
    
    # Final display and pause before exiting the function
    pygame.display.flip()
    time.sleep(1)  # Pause for 1 second

    # Clear the event queue again after displaying the result
    pygame.event.clear()

def get_random_mp3(directory):
    """Get a random MP3 file from the specified directory."""
    try:
        # List all MP3 files in the directory
        mp3_files = [f for f in os.listdir(directory) if f.endswith('.mp3')]
        
        if not mp3_files:
            log_entry = create_log_message("No MP3 files found in the directory.")
            log_message(log_entry)
            return None
        
        # Randomly select an MP3 file
        random_mp3 = random.choice(mp3_files)
        return os.path.join(directory, random_mp3)
    
    except Exception as e:
        log_entry = create_log_message(f"Error loading MP3 files from directory: {e}")
        log_message(log_entry)
        return None

def load_mp3(mp3):
    try:
        pygame.mixer.music.load(mp3)
        return True  # Indicate success
    except pygame.error as e:
        log_entry = create_log_message(f"Failed to load {mp3}: {e}")
        log_message(log_entry)
        return False  # Indicate failure
    except Exception as e:
        log_entry = create_log_message(f"Unexpected error loading {mp3}: {e}")
        log_message(log_entry)
        return False  # Indicate failure
    
def play_mp3(volume=None):
    global music_volume
    if volume is not None:
        music_volume = volume
    try:
        pygame.mixer.music.set_volume(music_volume)  # Set volume to current level
        pygame.mixer.music.play(-1)  # -1 loops the music indefinitely
    except pygame.error as e:
        log_entry = create_log_message(f"Failed to play music: {e}")
        log_message(log_entry)
    except Exception as e:
        log_entry = create_log_message(f"Unexpected error while playing music: {e}")
        log_message(log_entry)
        
def increase_volume(step=0.1):
    global music_volume
    music_volume = min(1.0, music_volume + step)  # Cap volume at 1.0 (100%)
    pygame.mixer.music.set_volume(music_volume)

def decrease_volume(step=0.1):
    global music_volume
    music_volume = max(0.0, music_volume - step)  # Floor volume at 0.0 (mute)
    pygame.mixer.music.set_volume(music_volume)
        
def stop_mp3():
    # Stop the music
    pygame.mixer.music.stop()

class Particle:
    """
    A class to represent a particle for visual effects.

    Attributes:
    -----------
    x : int
        The x-coordinate of the particle.
    y : int
        The y-coordinate of the particle.
    color : tuple
        The RGB color of the particle.
    size : int
        The size (radius) of the particle.
    lifetime : int
        The lifetime of the particle in frames.
    dx : int
        The horizontal speed of the particle.
    dy : int
        The vertical speed of the particle.

    Methods:
    --------
    update():
        Updates the particle's position and decreases its lifetime.
    draw(screen):
        Draws the particle on the given screen.
    """

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = random.randint(2, 8)
        self.color = color
        self.lifetime = random.randint(20, 50)
        self.dx = random.randint(-2, 2)
        self.dy = random.randint(-2, 2)

    def update(self):
        """Updates the particle's position and decreases its lifetime."""
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1

    def draw(self, screen):
        """Draws the particle on the given screen."""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

class Cat:
    def __init__(self, image, x, y, speed, scale_factor):
        """
        Initialize the Cat object.
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.gravity = 5 * scale_factor
        self.jump_speed = -50 * scale_factor  # Scale the jump speed based on resolution
        self.vertical_speed = 0
        self.is_jumping = False
        self.can_double_jump = True
        self.facing_left = False
        self.jump_angle = 0
        self.max_angle = 45
        self.particles = []
        self.rotated_image = self.image

    def handle_input(self):
        """Handles the player's input to move the cat."""
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0:
            self.rect.x -= self.speed
            if not self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_left = True
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_left = False

    def apply_gravity(self, platforms=None):
        """
        Applies gravity to the cat and handles platform collisions.
        """
        if self.is_jumping or self.rect.bottom < HEIGHT:
            self.vertical_speed += self.gravity
            self.rect.y += self.vertical_speed
    
            if platforms:
                for platform in platforms:
                    if self.rect.colliderect(platform.rect) and self.vertical_speed > 0 and self.rect.bottom <= platform.rect.top + self.vertical_speed:
                        self.rect.bottom = platform.rect.top
                        self.vertical_speed = 0
                        self.is_jumping = False
                        self.can_double_jump = True  # Reset double jump when landing on a platform
                        self.jump_angle = 0
    
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vertical_speed = 0
            self.is_jumping = False
            self.can_double_jump = True  # Reset double jump when landing on the ground
            self.jump_angle = 0

    def jump(self):
        """Makes the cat jump, emitting particles during the action."""
        if not self.is_jumping:
            # Normal jump from ground or platform
            self.vertical_speed = self.jump_speed
            self.is_jumping = True
            self.can_double_jump = True  # Allow double jump after the first jump
            for _ in range(10):
                self.particles.append(Particle(self.rect.centerx, self.rect.bottom, (255, 255, 255)))
        elif self.can_double_jump:
            # Double jump in mid-air
            self.vertical_speed = self.jump_speed
            self.can_double_jump = False  # Disable further jumps after the double jump
            for _ in range(10):
                self.particles.append(Particle(self.rect.centerx, self.rect.bottom, (255, 255, 255)))


    def update(self, platforms=None):
        """
        Updates the cat's position, handles input, applies gravity, and manages double jumping.
        """
        self.handle_input()
        self.apply_gravity(platforms)

        if self.is_jumping:
            if self.facing_left:
                self.jump_angle = max(-self.max_angle, min(self.max_angle, self.jump_angle + (-1 if self.vertical_speed < 0 else 1) * 10))
            else:
                self.jump_angle = max(-self.max_angle, min(self.max_angle, self.jump_angle + (1 if self.vertical_speed < 0 else -1) * 10))
            self.rotated_image = pygame.transform.rotate(self.image, self.jump_angle)
        else:
            self.rotated_image = self.image

        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        """
        Draws the cat and its particles on the provided screen.
        """
        screen.blit(self.rotated_image, self.rect.topleft)
        for particle in self.particles:
            particle.draw(screen)

class Piranha:
    def __init__(self, image, x, y, speed):
        """
        Initialize the Piranha object.

        Parameters:
            image (Surface): The image representing the piranha.
            x (int): The initial x-coordinate of the piranha.
            y (int): The initial y-coordinate of the piranha.
            speed (int): The speed at which the piranha moves horizontally.
        """
        self.image = image
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.speed = speed

    def update(self):
        """
        Update the piranha's position.

        The piranha moves horizontally and reverses direction when it hits the screen edges.
        """
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed = -self.speed

    def draw(self, screen):
        """
        Draw the piranha on the screen.

        Parameters:
            screen (Surface): The Pygame surface to draw the piranha on.
        """
        screen.blit(self.image, self.rect.topleft)
   
class Platform:
    def __init__(self, image, x, y, width, height):
        """
        Initialize the Platform object.

        Parameters:
            image (Surface): The image representing the platform.
            x (int): The x-coordinate of the platform.
            y (int): The y-coordinate of the platform.
            width (int): The width of the platform.
            height (int): The height of the platform.
        """
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def update(self, speed):
        """
        Update the platform's position based on the falling speed.

        Parameters:
            speed (int): The speed at which the platform falls.
        """
        self.rect.y += speed

    def draw(self, screen):
        """
        Draw the platform on the screen.

        Parameters:
            screen (Surface): The Pygame surface to draw the platform on.
        """
        screen.blit(self.image, self.rect.topleft)
   
main_menu_background = select_random_background("assets/images/main_menu/")
options_background = select_random_background("assets/images/options/")

# Main function that reads like a recipe
def main():
    # Load user options first to apply settings like font and resolution
    load_options()
    
    # Apply the desired theme at the start
    # apply_theme("light")
    
    # Initialize the font based on current settings
    global font  # Declare font as global to modify it
    font = init_fonts()  # Initialize the font here after loading options
    
    # Music setup
    main_menu_music_directory = "assets/music/main_menu"
    random_mp3 = get_random_mp3(main_menu_music_directory)
    
    if random_mp3:
        music_loaded = load_mp3(random_mp3)
        if music_loaded:
            play_mp3()  # Play only if the music was successfully loaded
    
    # Intro
    introduction(font)  # Pass the initialized font to the introduction function
    
    # Main menu
    current_state = "main_menu"
    
    while True:
        if current_state == "main_menu":
            current_state = main_menu()
        elif current_state == "options_menu":
            current_state = options_menu()
        elif current_state == "start_game":
            current_state = start_game()
        elif current_state == "rainbow_numbers_explanation":
            current_state = rainbow_numbers_explanation()
        elif current_state == "bonus_game":
            current_state = bonus_game()

if __name__ == "__main__":
    main()
