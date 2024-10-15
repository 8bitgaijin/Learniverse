# -*- coding: utf-8 -*-
"""
@author: Alvadore Retro Technology
Learniverse
"""

import ctypes
from datetime import datetime, timedelta
import fractions
import json
import math
import noise
import os
import pygame
import pyttsx3
import random
import sqlite3
import sys
import time


###################################
### Constants and Configuration ###
###################################

# Set the title of the window
pygame.display.set_caption("Learniverse")

# Constants for display and opacity
DISPLAY_TIME = 2000  # Time for text at full opacity (in milliseconds)
FADE_SPEED = 1  # Controls the fade-in and fade-out speed

# Color Definitions
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
TRUNK_COLOR = (139, 69, 19)  # Brown for trunk and branches
LEAF_COLOR = (34, 139, 34)   # Green for leaves
LIGHTNING_COLOR = (255, 255, 255)
SKY_BLUE = (135, 206, 235)  # Sky blue background


# Student selectable color themes
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
    },
    "Solar ": {
        "text_color": (255, 69, 0),  # Fiery Red-Orange
        "shadow_color": (255, 165, 0),  # Bright Orange
        "screen_color": (255, 99, 71)  # Tomato Red
    },
    "Midnight": {
        "text_color": (173, 216, 230),  # Light Sky Blue
        "shadow_color": (0, 0, 128),  # Navy Blue
        "screen_color": (25, 25, 112)  # Midnight Blue
    },
    "Autumn": {
        "text_color": (210, 105, 30),  # Chocolate Brown
        "shadow_color": (255, 140, 0),  # Dark Orange
        "screen_color": (139, 69, 19)  # Saddle Brown
    },
    "Cyber": {
        "text_color": (57, 255, 20),  # Neon Green
        "shadow_color": (0, 255, 255),  # Neon Cyan
        "screen_color": (0, 0, 0)  # Black
    },
    "Retro": {
        "text_color": (255, 182, 193),  # Light Pink
        "shadow_color": (135, 206, 250),  # Light Sky Blue
        "screen_color": (255, 105, 180)  # Hot Pink
    },
    "Forest": {
        "text_color": (34, 139, 34),  # Forest Green
        "shadow_color": (107, 142, 35),  # Olive Drab
        "screen_color": (85, 107, 47)  # Dark Olive Green
    },
    "Aqua": {
        "text_color": (0, 255, 255),  # Aqua
        "shadow_color": (72, 209, 204),  # Medium Turquoise
        "screen_color": (0, 128, 128)  # Teal
    },
    "Firefly": {
        "text_color": (240, 255, 240),  # Honeydew (pale green)
        "shadow_color": (50, 205, 50),  # Lime Green
        "screen_color": (0, 0, 0)  # Black
    },
    "Berry": {
        "text_color": (255, 20, 147),  # Deep Pink
        "shadow_color": (138, 43, 226),  # Blue Violet
        "screen_color": (75, 0, 130)  # Indigo
    },
    "Sandstorm": {
        "text_color": (255, 222, 173),  # Navajo White
        "shadow_color": (210, 180, 140),  # Tan
        "screen_color": (244, 164, 96)  # Sandy Brown
    }
}

# Constants for lightning SFX
BOLT_SEGMENTS = 15
BOLT_SPREAD = 50
BOLT_LIFETIME = 0.2  # Lifetime of each lightning bolt in seconds
lightning_bolts = []  # Store lightning bolts

# Constants for clouds SFX
BASE_ALPHA = 220  # Higher base alpha for more visible clouds
NOISE_SCALE = 0.005  # Scale to control cloud pattern size
CLOUD_THRESHOLD = 0.05  # Lower threshold to make clouds more dense
ALPHA_MULTIPLIER = 2.5  # Control how quickly alpha ramps up for denser clouds
CLOUD_SPEED = 0.5  # Speed of the cloud movement (pixels per frame)
x_offset = 0  # Horizontal offset for cloud movement

# Global variable to store the last generated problem
last_problem = None

BASE_FONT_SIZE = 90  # Define a base font size 
current_font_name_or_path = "timesnewroman"  # Set to the default font initially
music_volume = 0.5  # Start at 50% volume
text_color = RED  # Set the initial text color to red
shadow_color = RED  # Set the initial shadow color to RED
screen_color = RED
current_student = None  # Global variable to store the currently selected student

# Icon will be loaded later, initialized as None for now
icon = None

# Japanese colors data
colors1 = {
  "quiz_title": "Colors 1",
  "questions": [
    {
      "furigana": "あか",
      "kanji": "赤",
      "translation": "red",
      "image": "GFX/colors/red.png"
    },
    {
      "furigana": "あお",
      "kanji": "青",
      "translation": "blue",
      "image": "GFX/colors/blue.png"
    },
    {
      "furigana": "しろ",
      "kanji": "白",
      "translation": "white",
      "image": "GFX/colors/white.png"
    },
    {
      "furigana": "くろ",
      "kanji": "黒",
      "translation": "black",
      "image": "GFX/colors/black.png"
    },
    {
      "furigana": "みどり",
      "kanji": "緑",
      "translation": "green",
      "image": "GFX/colors/green.png"
    }
  ]
}

colors2 = {
  "quiz_title": "Colors 2",
  "questions": [
    {
      "furigana": "きいろ",
      "kanji": "黄色",
      "translation": "yellow",
      "image": "GFX/colors/yellow.png"
    },
    {
      "furigana": "ちゃいろ",
      "kanji": "茶色",
      "translation": "brown",
      "image": "GFX/colors/brown.png"
    },
    {
      "furigana": "むらさき",
      "kanji": "紫",
      "translation": "purple",
      "image": "GFX/colors/purple.png"
    },
    {
      "furigana": "はいいろ",
      "kanji": "灰色",
      "translation": "gray",
      "image": "GFX/colors/gray.png"
    },
    {
      "furigana": "きんいろ",
      "kanji": "金色",
      "translation": "gold",
      "image": "GFX/colors/gold.png"
    }
  ]
}

colors3 = {
  "quiz_title": "Colors 3",
  "questions": [
    {
      "furigana": "だいだいいろ",
      "kanji": "橙色",
      "translation": "orange",
      "image": "GFX/colors/orange.png"
    },
    {
      "furigana": "ももいろ",
      "kanji": "桃色",
      "translation": "pink",
      "image": "GFX/colors/pink.png"
    },
    # {
    #   "furigana": "きんいろ",
    #   "kanji": "金色",
    #   "translation": "gold",
    #   "image": "GFX/colors/gold.png"
    # },
    {
      "furigana": "ぎんいろ",
      "kanji": "銀色",
      "translation": "silver",
      "image": "GFX/colors/silver.png"
    },
    {
      "furigana": "こんいろ",
      "kanji": "紺色",
      "translation": "navy blue",
      "image": "GFX/colors/navy_blue.png"
    }
  ]
}

colors4 = {
  "quiz_title": "Colors 4",
  "questions": [
    {
      "furigana": "みずいろ",
      "kanji": "水色",
      "translation": "light blue",
      "image": "GFX/colors/light_blue.png"
    },
    {
      "furigana": "しこう",
      "kanji": "紫紅",
      "translation": "crimson",
      "image": "GFX/colors/crimson.png"
    },
    {
      "furigana": "きみどり",
      "kanji": "黄緑",
      "translation": "yellow-green",
      "image": "GFX/colors/yellow_green.png"
    },
    {
      "furigana": "わかくさいろ",
      "kanji": "若草色",
      "translation": "light green",
      "image": "GFX/colors/light_green.png"
    },
    {
      "furigana": "あさぎいろ",
      "kanji": "浅葱色",
      "translation": "light blue-green",
      "image": "GFX/colors/light_blue_green.png"
    }
  ]
}

colors5 = {
  "quiz_title": "Colors 5",
  "questions": [
    {
      "furigana": "さくらいろ",
      "kanji": "桜色",
      "translation": "cherry blossom pink",
      "image": "GFX/colors/cherry_blossom_pink.png"
    },
    {
      "furigana": "れんがいろ",
      "kanji": "煉瓦色",
      "translation": "brick red",
      "image": "GFX/colors/brick_red.png"
    },
    {
      "furigana": "おうどいろ",
      "kanji": "黄土色",
      "translation": "ochre",
      "image": "GFX/colors/ochre.png"
    },
    {
      "furigana": "とびいろ",
      "kanji": "鳶色",
      "translation": "dark reddish-brown",
      "image": "GFX/colors/dark_reddish_brown.png"
    },
    {
      "furigana": "ぶどういろ",
      "kanji": "葡萄色",
      "translation": "grape color",
      "image": "GFX/colors/grape.png"
    }
  ]
}


##################################
# TODO
# CAN I REMOVE THESE TWO SOMEHOW?
REFERENCE_RESOLUTION = (1080, 1080)
BASE_RESOLUTION = (1080, 1080)
##################################

########################
### Helper Functions ###
########################

def create_log_message(message):
    """
    Create a log message with a current timestamp.

    This is a pure function that generates a string formatted with a timestamp 
    and the provided message. The timestamp is in the format YYYY-MM-DD HH:MM:SS.

    Parameters:
        message (str): The log message to be included after the timestamp.

    Returns:
        str: The log message formatted with a timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {message}"


def log_message(log_entry):
    """
    Log a message to both the console and the error_log.txt file.

    This function handles logging by printing the log entry to the console and 
    appending it to a file named 'error_log.txt'. It handles any file I/O errors 
    gracefully by logging the failure to the console.

    Parameters:
        log_entry (str): The log message to be printed and saved.

    Raises:
        Exception: If an error occurs while writing to the log file, an 
        exception is caught, and an error message is printed to the console.
    """
    try:
        # Print the log entry to the console
        print(log_entry)
        # Attempt to open the log file and write the log entry
        with open("error_log.txt", "a") as error_file:
            error_file.write(log_entry + "\n")
    except Exception as e:
        # If an error occurs, print an error message to the console
        print(f"Failed to log message: {e}")


def select_random_background(folder_path):
    """
    Select a random background image from the specified folder.

    This function scans the provided folder for image files with common image 
    extensions (such as .png, .jpg, .jpeg, and .bmp), selects one at random, 
    and returns the file path.

    Parameters:
        folder_path (str): The path to the folder containing background images.

    Returns:
        str: The file path of the randomly selected image, or None if no image 
        files are found or an error occurs during the selection process.

    Raises:
        FileNotFoundError: If no image files are found in the specified folder,
        a log message is generated, and the function returns None.
        
        Exception: For any other unexpected errors, a log message is generated, 
        and the function returns None.
    """
    try:
        # List all image files in the folder
        image_files = [f for f in os.listdir(folder_path) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

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


def center_window(width, height):
    """Center the Pygame window on the screen."""
    try:
        # Reset the environment variable to ensure it's not "sticking"
        if 'SDL_VIDEO_WINDOW_POS' in os.environ:
            del os.environ['SDL_VIDEO_WINDOW_POS']
    
        # Get screen size
        user32 = ctypes.windll.user32
        screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    
        # Calculate the centered position
        window_x = (screen_width - width) // 2
        window_y = (screen_height - height) // 2
        
        # Set window position before creating the window
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"

    except Exception as e:
        log_entry = create_log_message(f"Failed to center window: {e}")
        log_message(log_entry)
        

##############################################
### Pygame Initialization and Window Setup ###
##############################################

# Try to load and set the window icon from a specified file
try:
    icon = pygame.image.load('assets/images/LLRN.ico')
    pygame.display.set_icon(icon)
except FileNotFoundError as e:
    log_entry = create_log_message(f"Icon file not found: {e}")
    log_message(log_entry)
    print("Icon file not found, continuing without a custom icon.")
except pygame.error as e:
    log_entry = create_log_message(f"Failed to load icon: {e}")
    log_message(log_entry)
    print("Failed to load icon, continuing without a custom icon.")

# Pygame initialization
# Initialize Pygame's main modules. If there's an issue, log the error and exit.
try:
    pygame.init()
    pygame.mixer.init()
except pygame.error as e:
    log_entry = create_log_message(f"Error initializing Pygame: {e}")
    log_message(log_entry)
    sys.exit(1)

# Define available windowed resolutions
# This list contains the resolutions that can be used by the game in windowed mode.
WINDOWED_RESOLUTIONS = [
    (640, 640), (768, 768), (800, 800), (900, 900), (1000, 1000), (1080, 1080)
]

# Get the display information from the system
# MAX_DISPLAY_RESOLUTION will store the width and height of the current display, 
# allowing the game to adapt to the user's monitor.
info = pygame.display.Info() 
MAX_DISPLAY_RESOLUTION = (info.current_w, info.current_h)

# Filter available resolutions to match the current display
# The AVAILABLE_RESOLUTIONS list only includes resolutions smaller than or 
# equal to the user's maximum screen size, ensuring compatibility with 
# different displays.
AVAILABLE_RESOLUTIONS = [
    res for res in WINDOWED_RESOLUTIONS if res[0] <= MAX_DISPLAY_RESOLUTION[0] and res[1] <= MAX_DISPLAY_RESOLUTION[1]
]

# Try to load the current resolution index from options, else default 800x800
try:
    with open("options.json", "r") as file:
        options = json.load(file)
        current_resolution_index = options.get("current_resolution_index", AVAILABLE_RESOLUTIONS.index((800, 800)))
        WIDTH, HEIGHT = AVAILABLE_RESOLUTIONS[current_resolution_index]
except (FileNotFoundError, ValueError):
    # Default to 800x800 resolution if options.json is missing or invalid
    current_resolution_index = AVAILABLE_RESOLUTIONS.index((800, 800))
    WIDTH, HEIGHT = AVAILABLE_RESOLUTIONS[current_resolution_index]

# Center the window before creating the Pygame window
center_window(WIDTH, HEIGHT)

# Initialize in windowed mode
screen = pygame.display.set_mode((WIDTH, HEIGHT))  

# Create a clock object to manage the frame rate of the game
clock = pygame.time.Clock()

# Load background images for different menus
# These images are selected randomly from the specified folders and will be used
# as backgrounds for the main menu and options menu.
main_menu_background = select_random_background("assets/images/main_menu/")
options_background = select_random_background("assets/images/options/")

# Initialize Text to Speech
engine = pyttsx3.init()

##########################
### DATABASE FUNCTIONS ###
##########################

def check_database_initialization():
    """
    Check if the 'learniverse.db' database exists. If not, create it.
    Ensure the 'students', 'lessons', 'sessions', and 'session_lessons' tables are set up.
    Handle errors by logging them.
    """
    db_name = 'learniverse.db'
    
    try:
        # Check if the database file exists in the same directory as the script
        if not os.path.isfile(db_name):
            log_entry = create_log_message("Database not found, creating 'learniverse.db'...")
            log_message(log_entry)
            
            # Create the database and the necessary tables
            connection = sqlite3.connect(db_name)
            cursor = connection.cursor()
            _initialize_tables(cursor, connection)
        else:
            # log_entry = create_log_message("'learniverse.db' found, checking accessibility...")
            # log_message(log_entry)
            
            connection = sqlite3.connect(db_name)
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students';")
            result = cursor.fetchone()

            if result:
                log_entry = create_log_message("'students' table found. Database is ready.")
                log_message(log_entry)
            else:
                log_entry = create_log_message("'students' table not found. Initializing tables...")
                log_message(log_entry)
                _initialize_tables(cursor, connection)
                
            # Always check for lessons and insert if missing
            insert_lessons(cursor, connection)

        cursor.close()
        connection.close()

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Database error: {e}")
        log_message(log_entry)
        sys.exit(1)
    
    except Exception as e:
        log_entry = create_log_message(f"Unexpected error: {e}")
        log_message(log_entry)
        sys.exit(1)


def _initialize_tables(cursor, connection):
    """Initialize the required tables and insert lessons if they don't exist."""
    try:
        # Create the necessary tables if they don't already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                start_time TIMESTAMP,  -- No DEFAULT here
                end_time TIMESTAMP,
                total_time REAL,
                total_questions INTEGER,
                total_correct INTEGER,
                avg_time_per_question REAL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_lessons (
                session_lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                lesson_id INTEGER NOT NULL,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                total_time REAL,
                questions_asked INTEGER,
                questions_correct INTEGER,
                avg_time_per_question REAL,
                percent_correct REAL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
            )
        ''')

        # New table for tracking individual student levels per lesson
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_lesson_progress (
                student_lesson_progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                lesson_id INTEGER NOT NULL,
                student_level INTEGER DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
            )
        ''')

        # Insert lessons 
        insert_lessons(cursor, connection)

        # Commit the changes
        connection.commit()
        log_entry = create_log_message("Database tables initialized and lessons updated successfully.")
        log_message(log_entry)
    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error initializing tables: {e}")
        log_message(log_entry)
        connection.rollback()


def insert_lessons(cursor, connection):
    """Insert default lessons into the lessons table if they don't already exist."""
    lessons = [
        ("Rainbow Numbers", "A math game to master mental arithmetic"),
        ("Hiragana", "A lesson to master the Japanese hiragana characters"),
        ("Katakana", "A lesson to master the Japanese katakana characters"),
        ("Single Digit Addition", "Single Digit Addition"),
        ("Single Digit Subtraction", "Single Digit Subtraction"),
        ("Single Digit Multiplication", "Single Digit Multiplication"),
        ("Double Digit Addition", "Double Digit Addition"),
        ("Triple Digit Addition", "Triple Digit Addition"),
        ("Quad Digit Addition", "Quad Digit Addition"),
        ("Double Digit Subtraction", "Double Digit Subtraction"),
        ("Triple Digit Subtraction", "Triple Digit Subtraction"),
        ("Quad Digit Subtraction", "Quad Digit Subtraction"),
        ("Single by Double Digit Multiplication", "Single by Double Digit Multiplication"),
        ("Double Digit Multiplication", "Double Digit Multiplication"),
        ("Single Denominator Fraction Addition", "Single Denominator Fraction Addition"),
        ("Lowest Common Denominator", "Lowest Common Denominator"),
        ("Basic Geometric Shapes", "Basic Geometric Shapes"),
        ("Colors 1", "Quiz to master Colors 1"),
        ("Colors 2", "Quiz to master Colors 2"),
        ("Colors 3", "Quiz to master Colors 3"),
        ("Colors 4", "Quiz to master Colors 4"),
        ("Colors 5", "Quiz to master Colors 5")
    ]

    try:
        # log_entry = create_log_message(f"Lessons to process: {lessons}")
        # log_message(log_entry)

        for title, description in lessons:
            # log_entry = create_log_message(f"Checking if lesson exists: {title}")
            # log_message(log_entry)

            # Check if the lesson already exists, case-insensitive check
            cursor.execute('SELECT 1 FROM lessons WHERE LOWER(title) = ?', (title.lower(),))
            result = cursor.fetchone()

            if not result:  # If no result, insert the lesson
                log_entry = create_log_message(f"Inserting lesson: {title}")
                log_message(log_entry)

                cursor.execute('''
                    INSERT INTO lessons (title, description)
                    VALUES (?, ?)
                ''', (title, description))

                # Commit after every insert to ensure changes are saved
                connection.commit()

            #     log_entry = create_log_message(f"Lesson added: {title}.")
            # else:
            #     log_entry = create_log_message(f"Lesson already exists: {title}.")
            
            # log_message(log_entry)

        log_entry = create_log_message("Lesson insertion process completed.")
        log_message(log_entry)

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error inserting lessons: {e}")
        log_message(log_entry)


def add_student(name, age=None, email=None):
    """Add a new student to the database and return their ID."""
    try:
        connection = sqlite3.connect('learniverse.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO students (name, age, email)
            VALUES (?, ?, ?)
        ''', (name, age, email))
        connection.commit()
        student_id = cursor.lastrowid
        log_entry = create_log_message(f"Student '{name}' added with ID: {student_id}")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return student_id
    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error adding student '{name}': {e}")
        log_message(log_entry)
        return -1


def get_students():
    """Retrieve a list of students from the database."""
    try:
        connection = sqlite3.connect('learniverse.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        # log_entry = create_log_message(f"Retrieved {len(students)} students from database.")
        # log_message(log_entry)
        cursor.close()
        connection.close()
        return students
    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error retrieving students: {e}")
        log_message(log_entry)
        return []


def add_session_lesson(session_id, lesson_id, start_time, end_time, total_questions, questions_correct):
    """Add a new record to the session_lessons table with detailed lesson data and return its ID."""
    try:
        connection = sqlite3.connect('learniverse.db')
        cursor = connection.cursor()

        # Convert Unix timestamps to human-readable datetime strings
        start_time_str = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
        end_time_str = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")

        # Calculate total time and average time per question
        total_time = round(end_time - start_time, 1)
        avg_time_per_question = total_time / total_questions if total_questions > 0 else 0
        percent_correct = (questions_correct / total_questions) * 100 if total_questions > 0 else 0

        # Insert the lesson record into session_lessons
        cursor.execute('''
            INSERT INTO session_lessons (session_id, lesson_id, start_time, end_time, total_time, 
                                         questions_asked, questions_correct, avg_time_per_question, percent_correct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, lesson_id, start_time_str, end_time_str, total_time, total_questions, 
              questions_correct, avg_time_per_question, percent_correct))

        connection.commit()
        session_lesson_id = cursor.lastrowid

        log_entry = create_log_message(f"Session lesson record added with ID: {session_lesson_id}")
        log_message(log_entry)
        cursor.close()
        connection.close()

        return session_lesson_id
    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error adding session lesson record: {e}")
        log_message(log_entry)
        return -1


def get_session_lessons(session_id):
    """Retrieve all lesson records for a specific session."""
    try:
        connection = sqlite3.connect('learniverse.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM session_lessons WHERE session_id = ?", (session_id,))
        session_lessons = cursor.fetchall()
        # log_entry = create_log_message(f"Retrieved {len(session_lessons)} session lessons for session ID {session_id}.")
        # log_message(log_entry)
        cursor.close()
        connection.close()
        return session_lessons
    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error retrieving session lessons for session ID {session_id}: {e}")
        log_message(log_entry)
        return []


def start_new_session(student_name):
    """Start a new session for the current student and return the session ID."""
    try:
        connection = sqlite3.connect('learniverse.db')
        cursor = connection.cursor()

        # Get the student's ID based on their name
        cursor.execute("SELECT id FROM students WHERE name = ?", (student_name,))
        student_id = cursor.fetchone()

        if student_id is None:
            log_entry = create_log_message(f"Error: Student '{student_name}' not found.")
            log_message(log_entry)
            return -1  # Return -1 if the student is not found
        else:
            student_id = student_id[0]

        # Get local time
        local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert a new session for the student with local time
        cursor.execute('''
            INSERT INTO sessions (student_id, start_time)
            VALUES (?, ?)
        ''', (student_id, local_time))
        connection.commit()

        # Get the ID of the newly created session
        session_id = cursor.lastrowid

        # Log the start of the session
        log_entry = create_log_message(f"New session started for student '{student_name}' with session ID {session_id}.")
        log_message(log_entry)

        cursor.close()
        connection.close()

        return session_id  # Return the session ID to track it later

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error starting session for student '{student_name}': {e}")
        log_message(log_entry)
        return -1


def end_session(session_id, total_questions, total_correct, overall_avg_time):
    """Update session with end time, total questions, correct answers, and avg time."""
    try:
        connection = sqlite3.connect('learniverse.db')
        cursor = connection.cursor()

        # Get the local end time
        session_end_time_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve the start_time from the database
        cursor.execute("SELECT start_time FROM sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()

        if result is None:
            log_entry = create_log_message(f"Session ID {session_id} not found.")
            log_message(log_entry)
            cursor.close()
            connection.close()
            return  # Or handle as appropriate

        start_time_str = result[0]

        # Parse the start_time string to a datetime object
        try:
            # Assuming the format is 'YYYY-MM-DD HH:MM:SS'
            start_time_dt = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            session_start_time = start_time_dt.timestamp()
        except ValueError as ve:
            log_entry = create_log_message(f"Invalid start_time format for session {session_id}: {ve}")
            log_message(log_entry)
            cursor.close()
            connection.close()
            return  # Or handle as appropriate

        # Calculate total time spent in session
        total_time = round(time.time() - session_start_time, 1)

        # Update session with overall stats using local end time
        cursor.execute('''
            UPDATE sessions
            SET end_time = ?,
                total_time = ?,
                total_questions = ?,
                total_correct = ?,
                avg_time_per_question = ?
            WHERE session_id = ?
        ''', (session_end_time_local, total_time, total_questions, total_correct, overall_avg_time, session_id))

        connection.commit()

        log_entry = create_log_message(f"Session {session_id} ended. Total questions: {total_questions}, "
                                       f"Total correct: {total_correct}, Overall avg time: {overall_avg_time}")
        log_message(log_entry)

        cursor.close()
        connection.close()

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Database error ending session {session_id}: {e}")
        log_message(log_entry)
    except Exception as e:
        log_entry = create_log_message(f"Unexpected error ending session {session_id}: {e}")
        log_message(log_entry)


def student_streak_query():
    global current_student  # Access global current_student
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()

    # First, get the student ID based on the current_student's name
    cursor.execute("SELECT id FROM students WHERE name = ?", (current_student,))
    result = cursor.fetchone()

    if not result:
        return 0  # No student found, no streak

    student_id = result[0]
    today = datetime.today().date()  # Get today's date

    streak = 0  # Initialize streak
    days_to_check = 1  # Start by checking yesterday

    # Step 1: Check if there is data for yesterday
    yesterday = today - timedelta(days=1)
    cursor.execute('''
        SELECT COUNT(*) FROM sessions 
        WHERE student_id = ? 
        AND date(start_time) = ?
    ''', (student_id, yesterday))

    result = cursor.fetchone()

    if result[0] == 0:
        return 0  # No session for yesterday, no streak

    # Step 2: There is data for yesterday, so streak starts at 1
    streak = 1

    # Step 3: Check further consecutive days before yesterday
    keep_checking = True
    while keep_checking:
        days_to_check += 1
        streak_day = today - timedelta(days=days_to_check)

        cursor.execute('''
            SELECT COUNT(*) FROM sessions 
            WHERE student_id = ? 
            AND date(start_time) = ?
        ''', (student_id, streak_day))

        result = cursor.fetchone()

        if result[0] > 0:
            # If there's data for this streak_day, increment the streak
            streak += 1
        else:
            # No session found for this streak_day, stop the check
            keep_checking = False

    cursor.close()
    connection.close()

    return streak


def get_student_progress(session_id, lesson_title):
    """Retrieves the student's current level for a specific lesson based on the session_id and lesson_title.
    If no entry exists for the lesson, it initializes progress with level 1 and returns 1."""
    try:
        # Connect to the database
        connection = sqlite3.connect('learniverse.db')
        cursor = connection.cursor()

        # Fetch student_id from the sessions table
        cursor.execute('''
            SELECT student_id
            FROM sessions
            WHERE session_id = ?
        ''', (session_id,))
        session_result = cursor.fetchone()

        if not session_result:
            raise ValueError(f"No session data found for session_id: {session_id}")

        student_id = session_result[0]

        # Fetch lesson_id from the lessons table based on the provided lesson title (e.g., 'Hiragana', 'Katakana')
        cursor.execute('''
            SELECT lesson_id
            FROM lessons
            WHERE title = ?
        ''', (lesson_title,))
        lesson_result = cursor.fetchone()

        if not lesson_result:
            raise ValueError(f"No lesson data found for {lesson_title} in the lessons table")

        lesson_id = lesson_result[0]

        # Query the student progress for the specific lesson
        cursor.execute('''
            SELECT student_level
            FROM student_lesson_progress
            WHERE student_id = ? AND lesson_id = ?
        ''', (student_id, lesson_id))
        progress_result = cursor.fetchone()

        if progress_result:
            # If progress exists, retrieve the current level
            student_level = progress_result[0]
        else:
            # If no progress exists for this lesson, insert a new entry with level 1
            cursor.execute('''
                INSERT INTO student_lesson_progress (student_id, lesson_id, student_level)
                VALUES (?, ?, 1)
            ''', (student_id, lesson_id))
            connection.commit()
            student_level = 1  # Default to level 1

        log_message(f"Fetched student progress: student_id={student_id}, lesson_id={lesson_id}, level={student_level}")
        return student_level

    except sqlite3.Error as e:
        log_message(f"Error retrieving student progress: {e}")
        raise  # Raise the error for proper handling upstream
    finally:
        cursor.close()
        connection.close()


def set_student_progress(session_id, lesson_title):
    """Updates the student_lesson_progress table for the given student and lesson based on session results."""
    try:
        # Connect to the database
        connection = sqlite3.connect('learniverse.db')
        cursor = connection.cursor()

        # Fetch student_id, lesson_id, questions_correct, and questions_asked from the session and session_lessons tables
        cursor.execute('''
            SELECT s.student_id, sl.lesson_id, sl.questions_correct, sl.questions_asked
            FROM session_lessons sl
            JOIN sessions s ON sl.session_id = s.session_id
            JOIN lessons l ON sl.lesson_id = l.lesson_id
            WHERE sl.session_id = ? AND l.title = ?
        ''', (session_id, lesson_title))
        result = cursor.fetchone()

        if not result:
            log_message(f"No session data found for session_id: {session_id}")
            return

        student_id, lesson_id, questions_correct, questions_asked = result

        # Calculate the student's current percentage correct
        percent_correct = (questions_correct / questions_asked) * 100 if questions_asked > 0 else 0
        log_message(f"Student {student_id} got {percent_correct}% in lesson {lesson_id} ({lesson_title}).")

        # Fetch or initialize the student's current level for the lesson
        cursor.execute('''
            SELECT student_level
            FROM student_lesson_progress
            WHERE student_id = ? AND lesson_id = ?
        ''', (student_id, lesson_id))
        progress_result = cursor.fetchone()

        if progress_result:
            current_level = progress_result[0]
        else:
            # Insert a new record for this student's progress at level 1 if no record exists
            cursor.execute('''
                INSERT INTO student_lesson_progress (student_id, lesson_id, student_level)
                VALUES (?, ?, 1)
            ''', (student_id, lesson_id))
            connection.commit()
            current_level = 1

        # Check if the student scored 100% and should level up
        if percent_correct == 100:
            new_level = current_level + 1
            log_message(f"Student {student_id} leveled up to {new_level} for lesson {lesson_id}.")
        else:
            new_level = current_level

        # Update the student's progress in the database
        cursor.execute('''
            UPDATE student_lesson_progress
            SET student_level = ?
            WHERE student_id = ? AND lesson_id = ?
        ''', (new_level, student_id, lesson_id))

        # Commit the changes
        connection.commit()

        # Log the successful update
        cursor.execute('SELECT * FROM student_lesson_progress WHERE student_id = ? AND lesson_id = ?', (student_id, lesson_id))
        log_message(f"Updated student progress: {cursor.fetchall()}")

    except sqlite3.Error as e:
        log_message(f"Error updating student progress: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


def fetch_lesson_id(lesson_title):
    """Fetches the lesson_id for a given lesson title."""
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", (lesson_title,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if result:
        return result[0]
    else:
        log_message(f"Lesson '{lesson_title}' not found in the database.")
        return None


######################
### Font Functions ###
######################

def get_dynamic_font_size():
    """
    Calculate the dynamic font size based on the current screen resolution.

    Returns:
        int: The adjusted font size based on the scaling factor.
    """
    # Calculate scaling factor based on resolution
    scale_factor = min(WIDTH / BASE_RESOLUTION[0], HEIGHT / BASE_RESOLUTION[1])
    # Adjust the font size
    dynamic_font_size = int(BASE_FONT_SIZE * scale_factor)
    
    return dynamic_font_size


def init_fonts():
    font_size = get_dynamic_font_size()  # Dynamically adjust the size

    # Initialize English font
    if os.path.isfile(current_font_name_or_path):
        english_font = pygame.font.Font(current_font_name_or_path, font_size)
    else:
        english_font = pygame.font.SysFont(current_font_name_or_path, font_size)

    # Initialize Japanese font (assuming MS Gothic for Japanese text)
    japanese_font = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", font_size)

    return english_font, japanese_font  # Return both fonts


def get_filtered_fonts():
    # List of known problematic fonts to exclude (alphabetized)
    excluded_fonts = {
        'amiriquranregular', 
        'bookshelfsymbol7', 
        'codicon', 
        'codicon0035', 
        'dejavumathtexgyreregular', 
        'elusiveicons', 
        'elusiveicons-webfont', 
        'elusiveicons-webfont-2.0', 
        'extra', 
        'fontawesome47webfont', 
        'fontawesome5brandswebfont', 
        'fontawesome5brandswebfont5154', 
        'fontawesome5regularwebfont', 
        'fontawesome5regularwebfont5154', 
        'fontawesome5solidwebfont', 
        'fontawesome5solidwebfont5154', 
        'goudystout', 
        'holomdl2assets', 
        'lucidasanstypewriteroblique', 
        'lucidasanstypewriterregular', 
        'materialdesignicons5webfont', 
        'materialdesignicons5webfont5955', 
        'materialdesignicons6webfont', 
        'materialdesignicons6webfont6996', 
        'miriamclm', 
        'miriamclmbook', 
        'miriammonoclmbookoblique', 
        'msoutlook', 
        'msreferencespecialty', 
        'opensymbol', 
        'phosphor', 
        'phosphor-1.3.0', 
        'playbill', 
        'pmingliuextb', 
        'remixicon', 
        'remixicon250', 
        'sansserifcollection', 
        'segoeuiemoji', 
        'segoeuisymbol', 
        'segoefluenticons', 
        'segoemdl2assets', 
        'segmdl2', 
        'symbol', 
        'webdings', 
        'widelatin', 
        'wingdings', 
        'wingdings2', 
        'wingdings3'
    }

    # List fonts available through Pygame
    pygame_fonts = pygame.font.get_fonts()
    
    filtered_fonts = []
    fallback_font = "arial"  # Define a safe fallback font
    
    for font_name in sorted(pygame_fonts):
        try:
            # Check if the font should be excluded based on the list
            if any(excluded in font_name for excluded in excluded_fonts):
                # print(f"Excluding font: {font_name}")
                continue

            # Attempt to use the font, which will validate if it's working
            pygame.font.SysFont(font_name, 12)  # Check font by loading it with small size
            filtered_fonts.append(font_name)
            # print(f"Including font: {font_name}")

        except FileNotFoundError:
            # Log error for missing font
            print(f"Font not found: {font_name}, excluding.")
            log_entry = create_log_message(f"Font not found and excluded: {font_name}")
            log_message(log_entry)

        except Exception as e:
            # Catch any other issues and log them without crashing
            log_entry = create_log_message(f"Skipping font {font_name} due to error: {e}")
            log_message(log_entry)
    
    # Ensure we have at least one valid font, fallback to 'arial' if necessary
    if not filtered_fonts:
        log_entry = create_log_message("No valid fonts found, falling back to 'arial'.")
        log_message(log_entry)
        filtered_fonts = [fallback_font]

    return filtered_fonts


###############################
### MP3 and Music Functions ###
###############################

def decrease_volume(step=0.1):
    global music_volume
    music_volume = max(0.0, music_volume - step)  # Floor volume at 0.0 (mute)
    pygame.mixer.music.set_volume(music_volume)


def increase_volume(step=0.1):
    global music_volume
    music_volume = min(1.0, music_volume + step)  # Cap volume at 1.0 (100%)
    pygame.mixer.music.set_volume(music_volume)


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
    
    
def stop_mp3():
    # Stop the music
    pygame.mixer.music.stop()    
    

###########
### SFX ###
###########

def draw_branch(screen, start_pos, end_pos, thickness, color):
    # Function to draw a branch segment
    pygame.draw.line(screen, color, start_pos, end_pos, thickness)


def grow_tree(screen, start_x, start_y, max_depth, max_branches):
    # Randomized recursive tree
    branches = [(start_x, start_y, -90)]  # Starting trunk (x, y, angle - 90 degrees pointing up)
    branch_thickness = 10  # Start thickness for the trunk
    
    for depth in range(max_depth):
        new_branches = []
        
        for branch in branches:
            x, y, angle = branch
            branch_length = random.randint(10, 40)  # Random length for variety
            
            # Calculate new branch endpoint
            end_x = x + math.cos(math.radians(angle)) * branch_length
            end_y = y + math.sin(math.radians(angle)) * branch_length
            
            # Draw the branch
            draw_branch(screen, (x, y), (end_x, end_y), branch_thickness, TRUNK_COLOR)
            
            # Randomly decide how many branches to grow from this segment
            num_new_branches = random.randint(1, max_branches)
            
            for _ in range(num_new_branches):
                new_angle = angle + random.randint(-40, 40)  # Random angle variation
                new_branches.append((end_x, end_y, new_angle))  # Append new branches

            # At the end of depth, we add leaves
            if depth == max_depth - 1:
                pygame.draw.circle(screen, LEAF_COLOR, (int(end_x), int(end_y)), 5)  # Leaves at the tips

        # Update for next depth
        branches = new_branches
        branch_thickness = max(1, branch_thickness - 1)  # Decrease thickness with each level

    
def draw_lightning(screen, start_pos, end_pos, background_image, font, text_color, correct_message="CORRECT!"):
    """
    Draws lightning bolts quickly flashing on the screen, clearing each frame of lightning
    while keeping the background image and 'CORRECT!' text intact, using the student's personalized settings.
    """
    # Prepare colors for the lightning
    start_color = (173, 216, 230)  # Light blue
    end_color = (255, 255, 255)    # White

    BOLT_SEGMENTS = 10  # Number of segments for each bolt
    FLASH_COUNT = 10    # Number of bolts per flash burst
    BOLT_FLASH_DURATION = 40  # Duration to display each flash (milliseconds)

    # Load the background image (which will always exist in this version)
    bg_image = pygame.image.load(background_image)

    # Resize the background image to fit the screen size
    bg_image = pygame.transform.scale(bg_image, (screen.get_width(), screen.get_height()))

    for _ in range(3):  # Number of flash bursts
        # Step 1: Redraw the background at the start of each frame to clear previous lightning bolts
        screen.blit(bg_image, (0, 0))

        # Step 2: Draw the "CORRECT!" message using the draw_text function
        draw_text(
            text=correct_message,
            font=font,
            color=text_color,
            x=0,  # X position is set to 0 for centering later
            y=screen.get_height() * 0.2,  # Y position places the text above the image
            center=True,
            enable_shadow=True,  # Optionally enable shadow
            shadow_color=(0, 0, 0),  # Shadow color, adjust if needed
        )

        # Step 3: Draw multiple lightning bolts in this frame
        for _ in range(FLASH_COUNT):
            current_pos = start_pos
            for i in range(BOLT_SEGMENTS):
                fraction = i / BOLT_SEGMENTS
                color = (
                    int(start_color[0] + (end_color[0] - start_color[0]) * fraction),
                    int(start_color[1] + (end_color[1] - start_color[1]) * fraction),
                    int(start_color[2] + (end_color[2] - start_color[2]) * fraction)
                )

                next_x = current_pos[0] + random.randint(-BOLT_SPREAD, BOLT_SPREAD)
                next_y = current_pos[1] + (end_pos[1] - start_pos[1]) // BOLT_SEGMENTS
                next_pos = (next_x, next_y)

                # Draw the segment of the lightning bolt
                pygame.draw.line(screen, color, current_pos, next_pos, 2)
                current_pos = next_pos

            # Draw the final segment of the bolt
            pygame.draw.line(screen, end_color, current_pos, end_pos, 2)

        # Step 4: Display the lightning on top of the background and "CORRECT!" message
        pygame.display.flip()

        # Step 5: Hold the lightning flash for a brief moment
        pygame.time.delay(BOLT_FLASH_DURATION)

        # Step 6: Clear the screen by redrawing the background and the "CORRECT!" message (erasing previous bolts)
        screen.blit(bg_image, (0, 0))
        draw_text(
            text=correct_message,
            font=font,
            color=text_color,
            x=0,  # X position is set to 0 for centering later
            y=screen.get_height() * 0.2,  # Y position places the text above the image
            center=True,
            enable_shadow=True,  # Optionally enable shadow
            shadow_color=(0, 0, 0),  # Shadow color, adjust if needed
        )

        # Step 7: Refresh the screen to apply the cleared frame
        pygame.display.flip()

        # Short delay before the next flash burst
        pygame.time.delay(20)

    # Step 8: Redraw the background and "CORRECT!" message after the lightning effect
    screen.blit(bg_image, (0, 0))
    draw_text(
        text=correct_message,
        font=font,
        color=text_color,
        x=0,  # X position is set to 0 for centering later
        y=screen.get_height() * 0.2,  # Y position places the text above the image
        center=True,
        enable_shadow=True,  # Optionally enable shadow
        shadow_color=(0, 0, 0),  # Shadow color, adjust if needed
    )
    pygame.display.flip()  # Final refresh with background and text intact


def generate_perlin_cloud(x_offset):
    # Function to generate a Perlin noise cloud mask with horizontal offset
    # Create a surface for the cloud with alpha
    cloud_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Generate a random seed offset for both x and y directions to create a different cloud pattern
    random_x_offset = random.uniform(0, 10000)  # Randomize X offset
    random_y_offset = random.uniform(0, 10000)  # Randomize Y offset

    # Generate Perlin noise for the entire screen
    for x in range(WIDTH):
        for y in range(HEIGHT):
            # Apply random offsets to both X and Y to randomize the cloud pattern
            noise_value = noise.pnoise2(
                (x + x_offset + random_x_offset) * NOISE_SCALE, 
                (y + random_y_offset) * NOISE_SCALE, 
                octaves=4
            )
            
            # If the noise value is higher than the threshold, draw a cloud pixel
            if noise_value > CLOUD_THRESHOLD:
                # Scale the alpha based on the noise value to make smoother cloud edges
                alpha = min(int((noise_value - CLOUD_THRESHOLD) * 255 * ALPHA_MULTIPLIER), BASE_ALPHA)
                pygame.draw.circle(cloud_surface, (*WHITE, alpha), (x, y), 3)  # Larger clouds
    
    return cloud_surface

    
###################################    
### 2. Display and UI Functions ###
###################################    

def apply_resolution():
    global WIDTH, HEIGHT, screen, current_resolution_index
    
    current_windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
    screen = pygame.display.set_mode(current_windowed_resolution)
    WIDTH, HEIGHT = current_windowed_resolution
    
    center_window(WIDTH, HEIGHT)


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


def check_continue_click(mouse_pos, continue_rect):
    """Check if the 'Continue...' button was clicked."""
    if continue_rect.collidepoint(mouse_pos):
        return True  # Indicate that the button was clicked
    return False


def draw_background(image_path):
    """Load and draw the pre-selected background image scaled to fit the screen 
    resolution."""
    try:
        if image_path:
            # Load the selected background image
            background_image = pygame.image.load(image_path).convert()

            # Define the base resolution (the original size of your art)
            base_width, base_height = 1080, 1080

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


def draw_continue_button():
    global current_font_name_or_path  # Ensure we're using the global variable for font

    # Update the dynamic font size for the continue button based on the current resolution
    continue_font_size = int(get_dynamic_font_size() * 0.8)  # Adjust the size as necessary

    # Recreate the font with the new size using the current font name or path
    if os.path.isfile(current_font_name_or_path):
        # If it's a file path, load the font from the file
        continue_font = pygame.font.Font(current_font_name_or_path, continue_font_size)
    else:
        # If it's a system font, use the font name
        continue_font = pygame.font.SysFont(current_font_name_or_path, continue_font_size)

    # Calculate the position for the "Continue..." text to be at 55% across the screen width
    x_position = WIDTH * 0.55
    y_position = HEIGHT * 0.90  # 90% down the screen

    # Use draw_text to render the continue button with a drop shadow and get its rect
    continue_rect = draw_text("Continue...", continue_font, text_color, x_position, y_position, screen, enable_shadow=True, shadow_color=shadow_color, return_rect=True)

    return continue_rect


def draw_and_wait_continue_button():
    """Draws the 'Continue...' button and waits for the student to click."""
    continue_rect = draw_continue_button()
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False
    return


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


def draw_text(
    text, font, color, x, y, surface=None, max_width=None, center=False, 
    enable_shadow=False, shadow_color=None, x_shadow_offset=2, y_shadow_offset=2,
    return_rect=False, use_japanese_font=False, font_override=None):
    """
    Draw text on the given surface (or screen if no surface is provided) with optional drop shadow,
    word wrapping, centering, and optional rect return. Optionally use Japanese font or override font size.
    This version respects explicit line breaks (\n).
    """

    # Use the screen as the default surface if none is provided
    if surface is None:
        surface = screen

    # If shadow_color is not provided, use the passed shadow_color or global value
    if shadow_color is None:
        shadow_color = globals().get('shadow_color', BLACK)

    # Select the font to use, prioritize font_override, then Japanese or default font
    selected_font = font_override if font_override else (j_font if use_japanese_font else font)

    # Split text into lines explicitly, using \n as a line break
    lines = text.split('\n')

    # Further split long lines into multiple lines if max_width is provided
    if max_width:
        wrapped_lines = []
        for line in lines:
            words = line.split(' ')
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if selected_font.size(test_line)[0] <= max_width:
                    current_line.append(word)
                else:
                    wrapped_lines.append(' '.join(current_line))
                    current_line = [word]
            wrapped_lines.append(' '.join(current_line))
        lines = wrapped_lines

    text_rect = None

    for i, line in enumerate(lines):
        if center:
            # Center the line horizontally within the given max_width
            text_width = selected_font.size(line)[0]
            draw_x = (WIDTH - text_width) // 2
        else:
            draw_x = x
        
        if enable_shadow:
            # Draw the shadow with the correct shadow_color
            shadow_surface = selected_font.render(line, True, shadow_color)
            surface.blit(shadow_surface, (draw_x + x_shadow_offset, y + y_shadow_offset))

        # Draw the main text
        text_surface = selected_font.render(line, True, color)
        surface.blit(text_surface, (draw_x, y))
        
        # Calculate rect for the first line (ensure it accounts for centering)
        if i == 0 and return_rect:
            text_rect = pygame.Rect(draw_x, y, selected_font.size(line)[0], selected_font.get_linesize())

        # Move down to the next line
        y += selected_font.get_linesize()

    return text_rect if return_rect else None




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


def update_positions():
    # Update positions and fonts dynamically
    global start_text, options_text, exit_text, back_to_main_menu_text
    global volume_label_text, resolution_label_text, volume_percentage_text
    global start_rect, options_rect, exit_rect, back_to_main_menu_rect
    global volume_label_rect, volume_percentage_rect, minus_rect, plus_rect
    global resolution_label_rect, resolution_minus_rect, resolution_plus_rect
    global font, j_font  

    # Update the font based on current resolution
    font, j_font = init_fonts()  

    # Update text elements using the English font
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


################################
### Text-to-Speech Functions ###
################################

def speak_english(text):
    """
    Set up the text-to-speech engine to use the English voice and speak the given text.

    Parameters:
    text (str): The text to speak out loud in English.
    """
    global engine  # Ensure we use the global engine

    # Set the voice to Zira (English) using the registry path
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0")
    
    # Optionally adjust the speech rate, for example, to slow down or speed up the voice
    engine.setProperty('rate', 150)  # 150 is the default rate, adjust as needed
    
    # Use the engine to say the given text
    engine.say(text)
    engine.runAndWait()  # Block while the speech finishes
    
    
def set_haruka_slow(engine):
    """
    Set the voice properties for the text-to-speech engine to use the 
    Haruka voice at a slow speaking rate.

    Parameters:
    engine (pyttsx3.Engine): The text-to-speech engine instance.
    """
    # Set the voice to Haruka (Japanese) using the registry path
    engine.setProperty(
        'voice', 
        "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_JA-JP_HARUKA_11.0"
    )
    
    # Set the speech rate to 100 (slow)
    engine.setProperty('rate', 100)
    
    
def speak_japanese(text):
    """
    Set up the text-to-speech engine to use the Japanese voice and speak the given text.

    Parameters:
    text (str): The text to speak out loud in Japanese.
    """
    global engine  # Ensure we use the global engine

    # Set the voice to Haruka (Japanese) and slow down the rate
    set_haruka_slow(engine)
    
    # Use the engine to say the given text
    engine.say(text)
    engine.runAndWait()  # Block while the speech finishes


############################
### Bonus Game Functions ###
############################

def bonus_game_fat_tuna():
    # Check if the assets/images directory exists
    if not os.path.exists('assets/images'):
        log_entry = create_log_message("Assets folder 'assets/images' is missing. Returning to the main menu.")
        log_message(log_entry)
        return "main_menu"
    
    # Calculate scaling factors based on the current resolution
    scale_factor_x = WIDTH / REFERENCE_RESOLUTION[0]
    scale_factor_y = HEIGHT / REFERENCE_RESOLUTION[1]
    scale_factor = min(scale_factor_x, scale_factor_y)

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
    cat = Cat(player_img, WIDTH // 2, HEIGHT - player_img.get_rect().height, 25 * scale_factor, scale_factor)

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Load and play bonus game music
    bonus_music_directory = 'assets/music/bonus'
    random_mp3 = get_random_mp3(bonus_music_directory)
    
    if random_mp3:
        music_loaded = load_mp3(random_mp3)
        if music_loaded:
            play_mp3()

    # Bonus Mode Display Phase (show controls and animated text)
    running = True
    controls_displayed = False
    start_time = time.time()

    while not controls_displayed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the bonus mode background (or fallback to navy blue)
        if bonus_mode_background:
            draw_background(bonus_mode_background)
        else:
            screen.fill(screen_color)

        # Render the controls
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

        # Draw the "Continue..." button below the controls
        continue_rect = draw_continue_button()
        pygame.display.flip()

        # Check for "Continue..." button click without stopping the animation
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    controls_displayed = True  # Exit the loop and continue to gameplay

        clock.tick(60)  # Keep the animation going at 60 FPS

    # Gameplay Phase
    try:
        start_time = time.time()
        while running:
            elapsed_time = int(time.time() - start_time)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
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

    # Game Over or Win Phase
    if win:
        screen.fill(screen_color)
        draw_text(f"You caught the Fat Tuna in {elapsed_time} seconds!", font, text_color, WIDTH // 2, HEIGHT // 3, center=True, max_width=WIDTH)
    elif game_over:
        screen.fill(screen_color)
        draw_text("Game Over! You were eaten by the piranha.", font, text_color, WIDTH // 2, HEIGHT // 3, center=True, max_width=WIDTH)

    # Draw the "Continue..." button after game completion message
    continue_rect = draw_continue_button()

    pygame.display.flip()

    # Wait for the player to click "Continue..." after the game ends
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False  # Continue after the "Continue..." button is clicked


##############################
### Math Problem Functions ###
##############################

def display_rainbow_math_problem(num1, num2, user_input, first_input, line_length_factor=1.9):
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


def display_result(result_text, image_folder=None, use_lightning=False):
    """
    Display the result text and an optional image from the given folder.
    If an image is provided and 'use_lightning' is True, show lightning instead of particles.
    If 'use_lightning' is False, show a particle effect.
    """
    # Clear the event queue to avoid any unwanted inputs
    pygame.event.clear()

    # Initialize particle list
    particles = []

    # Get the image path and set the background
    if image_folder:
        image_path = select_random_background(image_folder)
        draw_background(image_path)

        if not use_lightning:
            # Generate particles for the effect (only if use_lightning is False)
            for _ in range(500):  # Number of particles to generate
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                color = random.choice([NAVY_BLUE, (255, 255, 255), ROYAL_BLUE, LIGHT_BLUE])
                particles.append(Particle(x, y, color))

    else:
        # If no image folder is provided, fill the screen with the current screen color
        screen.fill(screen_color)
    
    # Display loop for particle effect or lightning effect
    if use_lightning:
        # Show lightning effect if the fast answer condition is met
        for _ in range(3):  # Increased number of lightning bolts for dramatic effect
            draw_lightning(screen, (random.randint(0, WIDTH), 0), (random.randint(0, WIDTH), HEIGHT), 
                           image_path, font, text_color, correct_message=result_text)
            pygame.display.flip()
            pygame.time.delay(150)  # Slight delay between lightning bolts
    else:
        # Show particle effect for slower answers
        for _ in range(50):  # Run the particle effect for 50 frames
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
            draw_text(result_text, 
                      font, 
                      text_color, 
                      WIDTH // 2, 
                      HEIGHT // 2, 
                      center=True, 
                      enable_shadow=True,
                      max_width=WIDTH)
            pygame.display.flip()
    
    # Final display and pause before exiting the function
    pygame.display.flip()
    time.sleep(1)  # Pause for 1 second

    # Clear the event queue again after displaying the result
    pygame.event.clear()


def generate_rainbow_number_problem():
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


def rainbow_numbers(session_id):
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Rainbow Numbers
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Rainbow Numbers',))
    result = cursor.fetchone()
    if result:
        rainbow_cats_lesson_id = result[0]
    else:
        log_entry = create_log_message("Rainbow Numbers lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return -1  # Or handle as appropriate
    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)  # Fill the screen with the background color
    draw_text(
        "Let's work on Rainbow Numbers!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,  # Wrap text within 95% of the screen width
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color  # Use the shadow color from the theme
    )

    # Draw the "Continue..." button before starting the lesson
    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    running = True
    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []  # List to store time taken for each question

    clock = pygame.time.Clock()

    while running and problem_count < total_questions:
        num1, num2, answer = generate_rainbow_number_problem()
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)  # Clear the screen before drawing

            # Draw the math problem
            display_rainbow_math_problem(num1, num2, user_input, first_input)

            pygame.display.flip()  # Update the display

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)  # Calculate time for the question
                        completion_times.append(time_taken)

                        if int(user_input) == num2:
                            correct_answers += 1

                            if time_taken < 3:
                                # Fast answer case: display fast_cats image and lightning bolts
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                # Slow answer case: display normal cat image and particle effects
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {num2}")

                        pygame.event.clear()  # Clear the event queue to avoid queued inputs
                        problem_count += 1
                        question_complete = True  # Move to the next question
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 2:  # Limit input to two digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)  # Frame rate limiting

    # End of lesson timer
    lesson_end_time = time.time()

    # Calculate the average time taken for each question
    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0  # Handle case where there were no completion times

    # Record the lesson performance in the database
    try:
        add_session_lesson(
            session_id,
            rainbow_cats_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        # Handle the exception as needed

    # Clear the screen with the background color from the theme/config
    screen.fill(screen_color)  # Use the configured background color before drawing the final score

    # Final score message
    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    # Average time per question message
    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

        if correct_answers == total_questions:
            perfect_score_message = "Perfect score!"
            draw_text(perfect_score_message, font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
            if average_time < 3.0:
                mastery_message = "MASTERY!"
                draw_text(mastery_message, font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    # Draw the "Continue..." button after displaying the final score
    draw_and_wait_continue_button()

    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    # Return the lesson results
    return total_questions, correct_answers, average_time


def generate_math_problem(min_val, max_val, operation="add"):
    """Generates two random numbers within the given range and returns the problem and the answer."""
    num1 = random.randint(min_val, max_val)
    num2 = random.randint(min_val, max_val)
    
    if operation == "sub" and num1 < num2:
        num1, num2 = num2, num1  # Ensure num1 is always larger to avoid negative answers
    
    if operation == "add":
        answer = num1 + num2
    elif operation == "sub":
        answer = num1 - num2
    elif operation == "mul":
        answer = num1 * num2
    else:
        raise ValueError("Unsupported operation. Use 'add', 'sub', or 'mul'.")
    
    return num1, num2, answer


def display_math_problem(num1, num2, user_input, first_input, operation="add", line_length_factor=1.9):
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
    
    # Draw the operator (right-aligned with some offset)
    if operation == "add":
        operator_sign = "+"
    elif operation == "sub":
        operator_sign = "-"
    elif operation == "mul":
        operator_sign = "×"
    else:
        raise ValueError("Unsupported operation. Use 'add', 'sub', or 'mul'.")
    
    operator_sign_x = right_x - num1_surface.get_width() - WIDTH * 0.05
    operator_surface = font.render(operator_sign, True, text_color)
    operator_rect = operator_surface.get_rect(right=operator_sign_x, centery=num2_y)
    screen.blit(operator_surface, operator_rect)
    
    # Draw the second number (right-aligned)
    num2_surface = font.render(str(num2), True, text_color)
    num2_rect = num2_surface.get_rect(right=right_x, centery=num2_y)
    screen.blit(num2_surface, num2_rect)
    
    # Calculate line width with a factor
    if operation == "add":
        line_width = max(num1_surface.get_width(), num2_surface.get_width(), font.size(str(num1 + num2))[0]) * line_length_factor
    elif operation == "sub":
        line_width = max(num1_surface.get_width(), num2_surface.get_width(), font.size(str(num1 - num2))[0]) * line_length_factor
    elif operation == "mul":
        line_width = max(num1_surface.get_width(), num2_surface.get_width(), font.size(str(num1 * num2))[0]) * line_length_factor
    else:
        raise ValueError("Unsupported operation. Use 'add', 'sub', or 'mul'.")
    
    pygame.draw.line(screen, text_color, (right_x - line_width, line_y), (right_x, line_y), 3)
    
    # Draw the sum placeholder or the input from the user (right-aligned)
    if first_input:
        input_text = "?"  # Show "?" as the sum the student needs to enter
    else:
        input_text = user_input
        
    input_surface = font.render(input_text, True, text_color)
    input_rect = input_surface.get_rect(right=right_x, centery=sum_y)
    screen.blit(input_surface, input_rect)

    pygame.display.flip()


def single_digit_addition(session_id):
    """Presents a single-digit addition quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Single Digit Addition
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single Digit Addition',))
    result = cursor.fetchone()
    
    if result:
        addition_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single Digit Addition lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Single-Digit Addition!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(1, 9)
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 2:  # Limit input to two digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            addition_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def double_digit_addition(session_id):
    """Presents a double-digit addition quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Double Digit Addition
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Double Digit Addition',))
    result = cursor.fetchone()
    
    if result:
        addition_lesson_id = result[0]
    else:
        log_entry = create_log_message("Double Digit Addition lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Double-Digit Addition!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(10, 99)
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 3:  # Limit input to three digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            addition_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def triple_digit_addition(session_id):
    """Presents a triple-digit addition quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Triple Digit Addition
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Triple Digit Addition',))
    result = cursor.fetchone()
    
    if result:
        addition_lesson_id = result[0]
    else:
        log_entry = create_log_message("Triple Digit Addition lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Triple-Digit Addition!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(100, 999)
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 4:  # Limit input to four digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            addition_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def quad_digit_addition(session_id):
    """Presents a four-digit addition quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Quad Digit Addition
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Quad Digit Addition',))
    result = cursor.fetchone()
    
    if result:
        addition_lesson_id = result[0]
    else:
        log_entry = create_log_message("Quad Digit Addition lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Four-Digit Addition!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(1000, 9999)
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 5:  # Limit input to five digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            addition_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def single_digit_subtraction(session_id):
    """Presents a single-digit subtraction quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Single Digit Subtraction
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single Digit Subtraction',))
    result = cursor.fetchone()
    
    if result:
        subtraction_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single Digit Subtraction lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Single-Digit Subtraction!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(1, 9, operation="sub")
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input, operation="sub")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 2:  # Limit input to two digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            subtraction_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def double_digit_subtraction(session_id):
    """Presents a double-digit subtraction quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Double Digit Subtraction
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Double Digit Subtraction',))
    result = cursor.fetchone()
    
    if result:
        subtraction_lesson_id = result[0]
    else:
        log_entry = create_log_message("Double Digit Subtraction lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Double-Digit Subtraction!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(10, 99, operation="sub")
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input, operation="sub")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 3:  # Limit input to three digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            subtraction_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def triple_digit_subtraction(session_id):
    """Presents a triple-digit subtraction quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Triple Digit Subtraction
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Triple Digit Subtraction',))
    result = cursor.fetchone()
    
    if result:
        subtraction_lesson_id = result[0]
    else:
        log_entry = create_log_message("Triple Digit Subtraction lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Triple-Digit Subtraction!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(100, 999, operation="sub")
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input, operation="sub")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 4:  # Limit input to four digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            subtraction_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def quad_digit_subtraction(session_id):
    """Presents a quad-digit subtraction quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Quad Digit Subtraction
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Quad Digit Subtraction',))
    result = cursor.fetchone()
    
    if result:
        subtraction_lesson_id = result[0]
    else:
        log_entry = create_log_message("Quad Digit Subtraction lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Quad-Digit Subtraction!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(1000, 9999, operation="sub")
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input, operation="sub")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 5:  # Limit input to five digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            subtraction_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def single_digit_multiplication(session_id):
    """Presents a single-digit multiplication quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Single Digit Multiplication
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single Digit Multiplication',))
    result = cursor.fetchone()
    
    if result:
        multiplication_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single Digit Multiplication lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Single-Digit Multiplication!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(1, 9, operation="mul")
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input, operation="mul")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 3:  # Limit input to three digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            multiplication_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def single_by_double_multiplication(session_id):
    """Presents a single-by-double-digit multiplication quiz and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Single by Double Digit Multiplication
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single by Double Digit Multiplication',))
    result = cursor.fetchone()
    
    if result:
        multiplication_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single by Double Digit Multiplication lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Single by Double-Digit Multiplication!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        # Generate the multiplication problem with one number in range 10-99 and the other in range 1-9
        num1 = random.randint(10, 99)
        num2 = random.randint(1, 9)
        answer = num1 * num2

        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input, operation="mul")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 4:  # Limit input to four digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            multiplication_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def double_digit_multiplication(session_id):
    """Presents a double-digit multiplication quiz and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Double Digit Multiplication
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Double Digit Multiplication',))
    result = cursor.fetchone()
    
    if result:
        multiplication_lesson_id = result[0]
    else:
        log_entry = create_log_message("Double Digit Multiplication lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Double-Digit Multiplication!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(10, 99, operation="mul")
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_math_problem(num1, num2, user_input, first_input, operation="mul")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and user_input.isdigit():
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        if int(user_input) == answer:
                            correct_answers += 1

                            if time_taken < 3:
                                display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                            else:
                                display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                        else:
                            display_result(f"Sorry, the answer is {answer}")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 5:  # Limit input to five digits
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    try:
        add_session_lesson(
            session_id,
            multiplication_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    screen.fill(screen_color)

    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def generate_fraction_problem(numerator_min, numerator_max, denominator):
    """Generates two fractions with the given denominator and returns the problem and the answer."""
    numerator1 = random.randint(numerator_min, numerator_max)
    numerator2 = random.randint(numerator_min, numerator_max)
    
    # The fractions will have the same denominator
    answer_numerator = numerator1 + numerator2

    return numerator1, numerator2, denominator, answer_numerator


def display_fraction_problem(numerator1, numerator2, denominator, user_input, first_input, line_length_factor=1.9):
    screen.fill(screen_color)
    
    # Dynamically calculate positions based on screen size
    right_x = WIDTH * 0.55  # Right edge for alignment
    num1_y = HEIGHT * 0.35
    num2_y = HEIGHT * 0.5
    line_y = HEIGHT * 0.57
    sum_y = HEIGHT * 0.63

    # Draw the first fraction (right-aligned)
    fraction1_str = f"{numerator1}/{denominator}"
    fraction1_surface = font.render(fraction1_str, True, text_color)
    fraction1_rect = fraction1_surface.get_rect(right=right_x, centery=num1_y)
    screen.blit(fraction1_surface, fraction1_rect)

    # Draw the plus sign (right-aligned with some offset)
    plus_sign_x = right_x - fraction1_surface.get_width() - WIDTH * 0.05
    plus_surface = font.render("+", True, text_color)
    plus_rect = plus_surface.get_rect(right=plus_sign_x, centery=num2_y)
    screen.blit(plus_surface, plus_rect)

    # Draw the second fraction (right-aligned)
    fraction2_str = f"{numerator2}/{denominator}"
    fraction2_surface = font.render(fraction2_str, True, text_color)
    fraction2_rect = fraction2_surface.get_rect(right=right_x, centery=num2_y)
    screen.blit(fraction2_surface, fraction2_rect)

    # Calculate line width with a factor
    answer_str = f"{numerator1 + numerator2}/{denominator}"
    line_width = max(fraction1_surface.get_width(), fraction2_surface.get_width(), font.size(answer_str)[0]) * line_length_factor
    pygame.draw.line(screen, text_color, (right_x - line_width, line_y), (right_x, line_y), 3)

    # Draw the answer placeholder or the input from the user (right-aligned)
    if first_input:
        input_text = "?"  # Show "?" as the answer the student needs to enter
    else:
        input_text = user_input

    input_surface = font.render(input_text, True, text_color)
    input_rect = input_surface.get_rect(right=right_x, centery=sum_y)
    screen.blit(input_surface, input_rect)

    pygame.display.flip()


def display_same_denominator_explanation():
    """
    Display a multi-step explanation for adding fractions with the same denominator and why it's an important first step.
    """
    explanation_lines = [
        "When adding fractions, they need to have the same denominator (bottom number).",
        "Fractions like 3/4 and 5/4 can be added because they have the same denominator.",
        "This lesson will help you practice adding fractions that already have the same denominator.",
        "Once you've mastered this, you'll be ready for the next challenge: finding the Lowest Common Denominator.",
        "This is an important step toward doing all fraction addition on your own!"
    ]
    
    for line in explanation_lines:
        screen.fill(screen_color)
        draw_text(line, font, text_color, x=0, y=HEIGHT * 0.4, max_width=WIDTH * 0.95, center=True, enable_shadow=True)
        pygame.display.flip()

        # Wait for a mouse click to move to the next explanation line
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False  # Move to the next line

    # After the explanation, return to the original introduction screen
    single_denominator_addition_intro()


def single_denominator_addition_intro():
    """
    Display the initial introduction for the Single Denominator Addition quiz with
    two clickable buttons: "What is Same Denominator?" and "Continue".
    """
    screen.fill(screen_color)

    # Draw the main instructional text
    draw_text(
        "Let's work on Fraction Addition!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Draw the "What is Same Denominator?" clickable text
    explanation_button_rect = draw_text(
        "What is Same Denominator?",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.8,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    # Draw the "Continue" button
    continue_button_rect = draw_text(
        "Continue",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.9,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    pygame.display.flip()

    # Wait for a click on either the explanation button or the Continue button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if explanation_button_rect.collidepoint(mouse_pos):
                    # Show the explanation if "What is Same Denominator?" is clicked
                    display_same_denominator_explanation()
                    waiting = False
                elif continue_button_rect.collidepoint(mouse_pos):
                    # Move to the next part of the quiz if "Continue" is clicked
                    waiting = False


def single_denominator_addition(session_id):
    """Presents an addition quiz of fractions with the same denominator and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Fraction Addition
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single Denominator Fraction Addition',))
    result = cursor.fetchone()
    
    if result:
        addition_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single Denominator Fraction Addition lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Start by displaying the introduction and clickable LCD explanation
    single_denominator_addition_intro()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()
    denominator = 10  # Fixed denominator for simplicity

    while problem_count < total_questions:
        numerator1, numerator2, denominator, answer_numerator = generate_fraction_problem(1, 9, denominator)
        user_input = ""
        first_input = True
        question_complete = False
        invalid_input = False  # Track if the input was invalid

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # If input was invalid, prompt the user again
            if invalid_input:
                display_result("Invalid input. Please try again.", None)
                invalid_input = False

            # Draw the math problem
            display_fraction_problem(numerator1, numerator2, denominator, user_input, first_input)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and "/" in user_input:
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        try:
                            # Split the input into numerator and denominator
                            num, denom = user_input.split("/")
                            
                            # Check if denominator is zero or missing
                            if denom == "" or int(denom) == 0:
                                raise ValueError("Invalid denominator")  # Trigger invalid input handling

                            # Convert the input to a Fraction and check the answer
                            user_fraction = fractions.Fraction(user_input)
                            if user_fraction == fractions.Fraction(answer_numerator, denominator):
                                correct_answers += 1
                                if time_taken < 3:
                                    display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                                else:
                                    display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                                question_complete = True  # Move on to the next question
                            else:
                                # Valid input but incorrect answer
                                display_result(f"Sorry, the answer is {answer_numerator}/{denominator}")
                                question_complete = True  # Move on to the next question

                        except (ValueError, ZeroDivisionError):
                            # Invalid input, prompt the user to try again
                            invalid_input = True  # Allow the student to try again without moving on

                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() or event.unicode == "/":  # Allow digits and '/'
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

        if question_complete:
            problem_count += 1  # Only increment after the question is fully processed

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    # Record the lesson performance in the database
    try:
        add_session_lesson(
            session_id,
            addition_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    # Display final score
    screen.fill(screen_color)
    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def generate_lcd_problem(numerator_min, numerator_max, denominator_min, denominator_max):
    """Generates two fractions with different denominators and returns the problem and the LCD."""
    numerator1 = random.randint(numerator_min, numerator_max)
    numerator2 = random.randint(numerator_min, numerator_max)
    denominator1 = random.randint(denominator_min, denominator_max)
    denominator2 = random.randint(denominator_min, denominator_max)

    # Ensure the denominators are different
    while denominator1 == denominator2:
        denominator2 = random.randint(denominator_min, denominator_max)

    # Find the lowest common denominator (LCD)
    lcd = math.lcm(denominator1, denominator2)

    return numerator1, denominator1, numerator2, denominator2, lcd


def display_lcd_problem(numerator1, denominator1, numerator2, denominator2, user_input, first_input, line_length_factor=1.9):
    screen.fill(screen_color)

    # Dynamically calculate positions based on screen size
    right_x = WIDTH * 0.55  # Right edge for alignment
    num1_y = HEIGHT * 0.35
    num2_y = HEIGHT * 0.5
    line_y = HEIGHT * 0.57
    sum_y = HEIGHT * 0.63

    # Draw the first fraction (right-aligned)
    fraction1_str = f"{numerator1}/{denominator1}"
    fraction1_surface = font.render(fraction1_str, True, text_color)
    fraction1_rect = fraction1_surface.get_rect(right=right_x, centery=num1_y)
    screen.blit(fraction1_surface, fraction1_rect)

    # Draw the plus sign (right-aligned with some offset)
    plus_sign_x = right_x - fraction1_surface.get_width() - WIDTH * 0.05
    plus_surface = font.render("+", True, text_color)
    plus_rect = plus_surface.get_rect(right=plus_sign_x, centery=num2_y)
    screen.blit(plus_surface, plus_rect)

    # Draw the second fraction (right-aligned)
    fraction2_str = f"{numerator2}/{denominator2}"
    fraction2_surface = font.render(fraction2_str, True, text_color)
    fraction2_rect = fraction2_surface.get_rect(right=right_x, centery=num2_y)
    screen.blit(fraction2_surface, fraction2_rect)

    # Draw the line (this can represent the denominator line if needed)
    line_width = max(fraction1_surface.get_width(), fraction2_surface.get_width()) * line_length_factor
    pygame.draw.line(screen, text_color, (right_x - line_width, line_y), (right_x, line_y), 3)

    # Draw the answer placeholder or the input from the student (right-aligned)
    if first_input:
        input_text = "?"  # Show "?" for the LCD answer the student needs to enter
    else:
        input_text = user_input

    input_surface = font.render(input_text, True, text_color)
    input_rect = input_surface.get_rect(right=right_x, centery=sum_y)
    screen.blit(input_surface, input_rect)

    pygame.display.flip()


def display_lcd_explanation():
    """
    Display a multi-step explanation of what the Lowest Common Denominator is and
    why it's important for adding fractions.
    """
    explanation_lines = [
        "The Lowest Common Denominator is the smallest number that two denominators divide into evenly.",
        "When adding fractions with different denominators, you need to find the LCD first.",
        "Once both fractions have the same denominator, you can add them more easily.",
        "The LCD helps simplify fraction addition and keeps the math easier to manage.",
        "Now that you know what LCD is, let's practice finding it!"
    ]
    
    for line in explanation_lines:
        screen.fill(screen_color)
        draw_text(line, font, text_color, x=0, y=HEIGHT * 0.4, max_width=WIDTH * 0.95, center=True, enable_shadow=True)
        pygame.display.flip()

        # Wait for a mouse click to move to the next explanation line
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False  # Move to the next line

    # After the explanation, return to the original introduction screen
    lowest_common_denominator_quiz_intro()


def lowest_common_denominator_quiz_intro():
    """
    Display the initial introduction for the Lowest Common Denominator quiz with
    two clickable buttons: "Lowest Common Denominator?" and "Continue".
    """
    screen.fill(screen_color)

    # Draw the main instructional text
    draw_text(
        "Let's work on finding the Lowest Common Denominator!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Draw the "Lowest Common Denominator?" clickable text
    lcd_button_rect = draw_text(
        "Lowest Common Denominator?",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.8,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    # Draw the "Continue" button
    continue_button_rect = draw_text(
        "Continue",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.9,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    pygame.display.flip()

    # Wait for a click on either the LCD button or the Continue button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if lcd_button_rect.collidepoint(mouse_pos):
                    # Show the LCD explanation if "Lowest Common Denominator?" is clicked
                    display_lcd_explanation()
                    waiting = False
                elif continue_button_rect.collidepoint(mouse_pos):
                    # Move to the next part of the quiz if "Continue" is clicked
                    waiting = False


def lowest_common_denominator_quiz(session_id):
    """Presents a quiz on solving for the lowest common denominator and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for LCD Problems
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Lowest Common Denominator',))
    result = cursor.fetchone()
    
    if result:
        lcd_lesson_id = result[0]
    else:
        log_entry = create_log_message("Lowest Common Denominator lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Start by displaying the introduction and clickable LCD explanation
    lowest_common_denominator_quiz_intro()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        numerator1, denominator1, numerator2, denominator2, lcd = generate_lcd_problem(1, 9, 2, 12)
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)

            # Draw the math problem
            display_lcd_problem(numerator1, denominator1, numerator2, denominator2, user_input, first_input)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                        end_time = time.time()
                        time_taken = round(end_time - start_time, 1)
                        completion_times.append(time_taken)

                        try:
                            user_answer = int(user_input)
                            if user_answer == lcd:
                                correct_answers += 1

                                if time_taken < 3:
                                    display_result("CORRECT!", "assets/images/fast_cats", use_lightning=True)
                                else:
                                    display_result("CORRECT!", "assets/images/cats", use_lightning=False)
                            else:
                                display_result(f"Sorry, the correct LCD is {lcd}")

                        except ValueError:
                            display_result("Invalid input, please try again")

                        pygame.event.clear()
                        problem_count += 1
                        question_complete = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit():
                        user_input += event.unicode
                        first_input = False

            clock.tick(60)

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    # Record the lesson performance in the database
    try:
        add_session_lesson(
            session_id,
            lcd_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    # Display final score
    screen.fill(screen_color)
    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def draw_shape(shape_type):
    """Draw a specific shape on the screen based on the shape type."""
    if shape_type == "circle":
        pygame.draw.circle(screen, text_color, (WIDTH // 2, HEIGHT // 2), 100, 5)
    elif shape_type == "oval":
        pygame.draw.ellipse(screen, text_color, (WIDTH // 3, HEIGHT // 3, 200, 100), 5)
    elif shape_type == "square":
        pygame.draw.rect(screen, text_color, (WIDTH // 3, HEIGHT // 3, 150, 150), 5)
    elif shape_type == "rectangle":
        pygame.draw.rect(screen, text_color, (WIDTH // 3, HEIGHT // 3, 200, 100), 5)
    elif shape_type == "triangle":
        pygame.draw.polygon(screen, text_color, [(WIDTH // 2, HEIGHT // 4), (WIDTH // 3, HEIGHT // 2), (2 * WIDTH // 3, HEIGHT // 2)], 5)
    elif shape_type == "pentagon":
        draw_regular_polygon(screen, text_color, (WIDTH // 2, HEIGHT // 2), 100, 5)  # Pentagon with 5 sides
    elif shape_type == "hexagon":
        draw_regular_polygon(screen, text_color, (WIDTH // 2, HEIGHT // 2), 100, 6)  # Hexagon with 6 sides
    elif shape_type == "parallelogram":
        pygame.draw.polygon(screen, text_color, [(WIDTH // 4, HEIGHT // 2), (WIDTH // 2, HEIGHT // 2), (3 * WIDTH // 4, HEIGHT // 3), (WIDTH // 2, HEIGHT // 3)], 5)
    elif shape_type == "rhombus":
        pygame.draw.polygon(screen, text_color, [
            (WIDTH // 2, HEIGHT // 4),           # Top vertex
            (WIDTH // 3, HEIGHT // 2),           # Left vertex
            (WIDTH // 2, 3 * HEIGHT // 4),       # Bottom vertex
            (2 * WIDTH // 3, HEIGHT // 2)        # Right vertex
        ], 5)
    elif shape_type == "trapezoid":
        pygame.draw.polygon(screen, text_color, [(WIDTH // 3, HEIGHT // 2), (2 * WIDTH // 3, HEIGHT // 2), (3 * WIDTH // 4, HEIGHT // 3), (WIDTH // 4, HEIGHT // 3)], 5)
    elif shape_type == "star":
        draw_star(screen, text_color, (WIDTH // 2, HEIGHT // 2), 100, 5)


def draw_regular_polygon(surface, color, center, radius, sides):
    """Draw a regular polygon with a specified number of sides."""
    points = []
    angle_step = 2 * math.pi / sides  # Full circle divided by number of sides

    for i in range(sides):
        angle = i * angle_step
        x = center[0] + radius * math.cos(angle)  # X coordinate
        y = center[1] + radius * math.sin(angle)  # Y coordinate
        points.append((x, y))

    pygame.draw.polygon(surface, color, points, 5)


def draw_star(surface, color, center, radius, points):
    """Draw a star with the specified number of points."""
    outer_points = []
    inner_points = []
    angle_step = 2 * math.pi / (2 * points)  # Angle between outer and inner points

    for i in range(2 * points):
        angle = i * angle_step
        if i % 2 == 0:
            # Outer point
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
        else:
            # Inner point, reduced radius
            x = center[0] + (radius / 2) * math.cos(angle)
            y = center[1] + (radius / 2) * math.sin(angle)
        outer_points.append((x, y))

    pygame.draw.polygon(surface, color, outer_points, 5)
    

def display_basic_shapes_explanation():
    """
    Display a multi-step explanation of basic geometric shapes and draw them on the screen.
    """
    explanation_steps = [
        ("A circle is a round shape where every point is the same distance from the center.", "circle"),
        ("An oval is a stretched-out circle, like an egg shape.", "oval"),
        ("A square has four equal sides and four right angles.", "square"),
        ("A rectangle also has four right angles, but two sides are longer than the other two.", "rectangle"),
        ("A triangle has three sides and three angles.", "triangle"),
        ("A pentagon has five equal sides and five angles.", "pentagon"),
        ("A hexagon has six sides and six angles.", "hexagon"),
        ("A parallelogram has opposite sides that are parallel.", "parallelogram"),
        ("A rhombus has all four sides of equal length, but with slanted angles.", "rhombus"),
        ("A trapezoid has one pair of parallel sides.", "trapezoid"),
        ("A star has five points and looks like a typical star shape.", "star"),
        ("Let's practice identifying these basic shapes!", None)
    ]

    for text, shape in explanation_steps:
        screen.fill(screen_color)
        draw_text(text, font, text_color, x=0, y=HEIGHT * 0.1, max_width=WIDTH * 0.95, center=True, enable_shadow=True)
        
        # Draw the shape if it's part of this step
        if shape:
            draw_shape(shape)

        pygame.display.flip()

        # Wait for a mouse click to move to the next explanation step
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False  # Move to the next step

    # After the explanation, return to the original introduction screen
    basic_shapes_quiz_intro()


def basic_shapes_quiz_intro():
    """
    Display the introduction for the basic geometric shapes quiz with
    two clickable buttons: "What are basic shapes?" and "Continue".
    """
    screen.fill(screen_color)

    # Draw the main instructional text
    draw_text(
        "Let's work on identifying basic geometric shapes!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Draw the "What are basic shapes?" clickable text
    explanation_button_rect = draw_text(
        "What are basic shapes?",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.8,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    # Draw the "Continue" button
    continue_button_rect = draw_text(
        "Continue",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.9,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    pygame.display.flip()

    # Wait for a click on either the explanation button or the Continue button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if explanation_button_rect.collidepoint(mouse_pos):
                    # Show the explanation if "What are basic shapes?" is clicked
                    display_basic_shapes_explanation()
                    waiting = False
                elif continue_button_rect.collidepoint(mouse_pos):
                    # Move to the next part of the quiz if "Continue" is clicked
                    waiting = False


def draw_shapes_for_quiz(correct_shape):
    """Draw multiple shapes on the screen for the student to choose from. Ensure the correct shape is drawn."""
    shapes = ["circle", "oval", "square", "rectangle", "triangle", "pentagon", "hexagon", "parallelogram", "rhombus", "trapezoid", "star"]
    
    # Remove the correct shape from the shapes list temporarily to avoid duplication
    shapes.remove(correct_shape)

    # Randomly select three shapes (not including the correct shape)
    random_shapes = random.sample(shapes, 3)

    # Add the correct shape to the list
    random_shapes.append(correct_shape)

    # Shuffle the shapes so the correct one appears in a random position
    random.shuffle(random_shapes)
    
    # Store rects for each shape for click detection
    shape_rects = {}

    # Define positions for each shape
    positions = [
        (WIDTH // 4, HEIGHT // 2),
        (3 * WIDTH // 4, HEIGHT // 2),
        (WIDTH // 4, 3 * HEIGHT // 4),
        (3 * WIDTH // 4, 3 * HEIGHT // 4)
    ]
    
    for i, shape in enumerate(random_shapes):
        x, y = positions[i]
        if shape == "circle":
            shape_rect = pygame.draw.circle(screen, text_color, (x, y), 50, 5)
        elif shape == "oval":
            shape_rect = pygame.draw.ellipse(screen, text_color, (x - 50, y - 25, 100, 50), 5)
        elif shape == "square":
            shape_rect = pygame.draw.rect(screen, text_color, (x - 50, y - 50, 100, 100), 5)
        elif shape == "rectangle":
            shape_rect = pygame.draw.rect(screen, text_color, (x - 75, y - 50, 150, 100), 5)
        elif shape == "triangle":
            shape_rect = pygame.draw.polygon(screen, text_color, [(x, y - 50), (x - 50, y + 50), (x + 50, y + 50)], 5)
        elif shape == "pentagon":
            shape_rect = pygame.draw.polygon(screen, text_color, [(x, y - 50), (x - 50, y), (x - 30, y + 50), (x + 30, y + 50), (x + 50, y)], 5)
        elif shape == "hexagon":
            shape_rect = pygame.draw.polygon(screen, text_color, [(x - 50, y), (x - 25, y - 50), (x + 25, y - 50), (x + 50, y), (x + 25, y + 50), (x - 25, y + 50)], 5)
        elif shape == "parallelogram":
            shape_rect = pygame.draw.polygon(screen, text_color, [(x - 50, y + 50), (x + 50, y + 50), (x + 25, y - 50), (x - 75, y - 50)], 5)
        elif shape == "rhombus":
            shape_rect = pygame.draw.polygon(screen, text_color, [(x, y - 50), (x - 50, y), (x, y + 50), (x + 50, y)], 5)
        elif shape == "trapezoid":
            shape_rect = pygame.draw.polygon(screen, text_color, [(x - 50, y + 50), (x + 50, y + 50), (x + 25, y - 50), (x - 25, y - 50)], 5)
        elif shape == "star":
            shape_rect = pygame.draw.polygon(screen, text_color, [(x, y - 50), (x - 20, y - 20), (x - 50, y), (x - 20, y + 20), (x, y + 50), (x + 20, y + 20), (x + 50, y), (x + 20, y - 20)], 5)

        # Store the rect for this shape for click detection
        shape_rects[shape] = shape_rect
    
    pygame.display.flip()
    
    return shape_rects


def basic_shapes_quiz(session_id):
    """
    Presents a quiz on identifying basic geometric shapes and updates the session results.
    The student will have to click on the correct shape.
    """
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Basic Geometric Shapes
    connection = sqlite3.connect('learniverse.db')
    cursor = connection.cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Basic Geometric Shapes',))
    result = cursor.fetchone()
    
    if result:
        shapes_lesson_id = result[0]
    else:
        log_entry = create_log_message("Basic Geometric Shapes lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, 0  # No questions asked, no correct answers, no time taken

    cursor.close()
    connection.close()

    # Start by displaying the introduction
    basic_shapes_quiz_intro()

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    # Define basic shapes for the quiz
    shapes = [
        {"name": "circle", "description": "Click the circle."},
        {"name": "oval", "description": "Click the oval."},
        {"name": "square", "description": "Click the square."},
        {"name": "rectangle", "description": "Click the rectangle."},
        {"name": "triangle", "description": "Click the triangle."},
        {"name": "pentagon", "description": "Click the pentagon."},
        {"name": "hexagon", "description": "Click the hexagon."},
        {"name": "parallelogram", "description": "Click the parallelogram."},
        {"name": "rhombus", "description": "Click the rhombus."},
        {"name": "trapezoid", "description": "Click the trapezoid."},
        {"name": "star", "description": "Click the star."}
    ]

    while problem_count < total_questions:
        # Select a random shape question
        shape_question = random.choice(shapes)
        correct_shape = shape_question["name"]

        # Draw the question
        screen.fill(screen_color)
        draw_text(
            shape_question['description'],
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.15,
            max_width=WIDTH * 0.95,
            center=True,
            enable_shadow=True
        )

        # Draw shapes and get rects for click detection
        shape_rects = draw_shapes_for_quiz(correct_shape)
        pygame.display.flip()

        question_complete = False

        while not question_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if the student clicked any shape
                    clicked_shape = None
                    for shape_name, rect in shape_rects.items():
                        if rect.collidepoint(mouse_pos):
                            clicked_shape = shape_name
                            break

                    # If they clicked a shape, check if it's correct or not
                    if clicked_shape:
                        if clicked_shape == correct_shape:
                            correct_answers += 1
                            display_result("CORRECT!", "assets/images/cats")
                        else:
                            display_result(f"Sorry, the correct answer was {correct_shape}")
                        
                        question_complete = True

            clock.tick(60)

        problem_count += 1

    # End of lesson timer
    lesson_end_time = time.time()

    if completion_times:
        average_time = round(sum(completion_times) / len(completion_times), 1)
    else:
        average_time = 0

    # Record the lesson performance in the database
    try:
        add_session_lesson(
            session_id,
            shapes_lesson_id,
            lesson_start_time,
            lesson_end_time,
            total_questions,
            correct_answers
        )
    except Exception as e:
        log_entry = create_log_message(f"Error recording session lesson: {e}")
        log_message(log_entry)
        return total_questions, correct_answers, average_time

    # Display final score
    screen.fill(screen_color)
    final_message = f"Final Score: {correct_answers}/{total_questions}"
    draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if completion_times:
        average_time_message = f"Average Time: {average_time} seconds"
        draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()

    return total_questions, correct_answers, average_time


def fibonacci_sequence(n):
    """Generates the Fibonacci sequence up to the nth term."""
    sequence = []
    a, b = 0, 1
    while len(sequence) < n:
        sequence.append(a)
        a, b = b, a + b
    return sequence


def show_fibonacci_explanation(COUNT_TO):
    """Displays Fibonacci explanation one sentence at a time."""
    fibonacci_explanation = [
        "Fibonacci numbers are a sequence of numbers starting with 0 and 1.",
        "Each number in the sequence is the sum of the two preceding ones.",
        "This sequence is found in nature, art, and architecture.",
        "Now, let's see how the Fibonacci sequence works!"
    ]
    
    sentence_index = 0
    while sentence_index < len(fibonacci_explanation):
        # Clear the screen and show the current explanation sentence
        screen.fill(screen_color)
        draw_text(fibonacci_explanation[sentence_index], font, text_color, x=0, y=HEIGHT * 0.4, 
                  center=True, enable_shadow=True, shadow_color=shadow_color, max_width=WIDTH)
        pygame.display.flip()

        # Wait for a mouse click to move to the next sentence
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False

        # Move to the next sentence
        sentence_index += 1

    # After the explanation, return to the intro screen
    skip_counting_fibonacci_intro(COUNT_TO)


def skip_counting_fibonacci_intro(COUNT_TO):
    """Displays the intro to Fibonacci counting with clickable 'Fibonacci numbers?' text."""
    screen.fill(screen_color)

    # Draw the main instructional text
    intro_message = f"Let's count using the Fibonacci sequence {COUNT_TO} times!"
    draw_text(
        intro_message,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        max_width=WIDTH
    )

    # Draw the "Fibonacci numbers?" clickable text and get its rect
    explanation_button_rect = draw_text(
        "Fibonacci numbers?",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.8,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    # Draw the "Continue" button and get its rect
    continue_button_rect = draw_text(
        "Continue",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.9,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    pygame.display.flip()

    # Wait for a click on either the explanation button or the Continue button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Use get_pos to ensure accurate click position
                if explanation_button_rect.collidepoint(mouse_pos):
                    # Show the explanation if "Fibonacci numbers?" is clicked
                    show_fibonacci_explanation(COUNT_TO)
                    waiting = False
                elif continue_button_rect.collidepoint(mouse_pos):
                    # Move to the next part if "Continue" is clicked
                    waiting = False


def skip_counting_fibonacci():
    """Displays Fibonacci sequence and equations, reads them aloud, and shows the number on screen."""
    global screen_color, text_color, shadow_color, current_font_name_or_path, font  # Access theme-related globals

    COUNT_TO = 10  # Number of Fibonacci iterations
    large_font_size = 150  # Adjust font size as necessary

    # Initialize the larger font based on whether the current font is a file or system font
    if os.path.isfile(current_font_name_or_path):
        large_font = pygame.font.Font(current_font_name_or_path, large_font_size)
    else:
        large_font = pygame.font.SysFont(current_font_name_or_path, large_font_size)

    # Show the intro screen with the "Fibonacci numbers?" button
    skip_counting_fibonacci_intro(COUNT_TO)

    # Get Fibonacci sequence up to COUNT_TO
    fibonacci_numbers = fibonacci_sequence(COUNT_TO)

    # Loop through the Fibonacci numbers and display each equation and result
    for i in range(2, len(fibonacci_numbers)):
        # Clear the screen before displaying each equation and number
        screen.fill(screen_color)

        # Get the equation and result for the current Fibonacci number
        a, b, result = fibonacci_numbers[i - 2], fibonacci_numbers[i - 1], fibonacci_numbers[i]
        equation_str = f"{a} + {b} = {result}"

        # Display the equation in the center of the screen using the larger font size
        draw_text(equation_str, large_font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

        # Update the screen before speaking
        pygame.display.flip()

        # Speak the equation aloud in English
        speak_english(equation_str)

        # Pause for a second before showing the next equation
        time.sleep(1)

    # After completing the Fibonacci sequence, show a completion message using the default font
    completion_message = f"Great job! You counted the Fibonacci sequence {COUNT_TO} times!"
    screen.fill(screen_color)
    draw_text(completion_message, font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

    # Update the screen before speaking
    pygame.display.flip()

    # Speak the completion message aloud
    speak_english(completion_message)
    
    # Draw the "Continue..." button after the completion message
    draw_and_wait_continue_button()


def generate_primes(n):
    """Generates the first n prime numbers."""
    primes = []
    candidate = 2  # Start with the first prime number
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


def show_prime_explanation(COUNT_TO):
    """Displays Prime Number explanation one sentence at a time."""
    prime_explanation = [
        "Prime numbers are numbers greater than 1 that have no divisors other than 1 and themselves.",
        "For example, 2 is prime because it can only be divided by 1 and 2.",
        "Prime numbers play a fundamental role in mathematics and are used in cryptography.",
        "Now, let's count some prime numbers!"
    ]
    
    sentence_index = 0
    while sentence_index < len(prime_explanation):
        # Clear the screen and show the current explanation sentence
        screen.fill(screen_color)
        draw_text(prime_explanation[sentence_index], font, text_color, x=0, y=HEIGHT * 0.4, 
                  center=True, enable_shadow=True, shadow_color=shadow_color, max_width=WIDTH)
        pygame.display.flip()

        # Wait for a mouse click to move to the next sentence
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False

        # Move to the next sentence
        sentence_index += 1

    # After the explanation, return to the intro screen
    skip_counting_primes_intro(COUNT_TO)


def skip_counting_primes_intro(COUNT_TO):
    """Displays the intro to prime number counting with clickable 'Prime numbers?' text."""
    screen.fill(screen_color)

    # Draw the main instructional text
    intro_message = f"Let's count the first {COUNT_TO} prime numbers!"
    draw_text(
        intro_message,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        max_width=WIDTH
    )

    # Draw the "Prime numbers?" clickable text and get its rect
    explanation_button_rect = draw_text(
        "Prime numbers?",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.8,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    # Draw the "Continue" button and get its rect
    continue_button_rect = draw_text(
        "Continue",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.9,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can check if it's clicked
    )

    pygame.display.flip()

    # Wait for a click on either the explanation button or the Continue button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Use get_pos to ensure accurate click position
                if explanation_button_rect.collidepoint(mouse_pos):
                    # Show the explanation if "Prime numbers?" is clicked
                    show_prime_explanation(COUNT_TO)
                    waiting = False
                elif continue_button_rect.collidepoint(mouse_pos):
                    # Move to the next part if "Continue" is clicked
                    waiting = False


def skip_counting_primes():
    """Displays prime numbers, reads them aloud, and shows the number on screen."""
    global screen_color, text_color, shadow_color, current_font_name_or_path, font  # Access theme-related globals

    COUNT_TO = 10  # Number of prime numbers to display
    large_font_size = 150  # Adjust font size as necessary

    # Initialize the larger font based on whether the current font is a file or system font
    if os.path.isfile(current_font_name_or_path):
        large_font = pygame.font.Font(current_font_name_or_path, large_font_size)
    else:
        large_font = pygame.font.SysFont(current_font_name_or_path, large_font_size)

    # Show the intro screen with the "Prime numbers?" button
    skip_counting_primes_intro(COUNT_TO)

    # Get prime numbers up to COUNT_TO
    prime_numbers = generate_primes(COUNT_TO)

    # Loop through the prime numbers and display each one
    for prime in prime_numbers:
        # Clear the screen before displaying each number
        screen.fill(screen_color)

        # Display the prime number in the center of the screen using the larger font size
        prime_str = str(prime)
        draw_text(prime_str, large_font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

        # Update the screen before speaking
        pygame.display.flip()

        # Speak the prime number aloud in English
        speak_english(prime_str)

        # Pause for a second before showing the next number
        time.sleep(1)

    # After completing the prime number counting, show a completion message
    completion_message = f"Great job! You counted the first {COUNT_TO} prime numbers!"
    screen.fill(screen_color)
    draw_text(completion_message, font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

    # Update the screen before speaking
    pygame.display.flip()

    # Speak the completion message aloud
    speak_english(completion_message)
    
    # Draw the "Continue..." button after the completion message
    draw_and_wait_continue_button()


def skip_counting():
    """Randomly selects a number between 2-9 and performs skip counting up to 100."""
    global screen_color, text_color, shadow_color, current_font_name_or_path, font  # Access theme-related globals

    # Define a larger size for the skip-counted numbers
    large_font_size = 200  # Adjust size as necessary

    # Initialize the larger font based on whether the current font is a file or system font
    if os.path.isfile(current_font_name_or_path):
        large_font = pygame.font.Font(current_font_name_or_path, large_font_size)
    else:
        large_font = pygame.font.SysFont(current_font_name_or_path, large_font_size)

    # Select a random number from 2-9
    skip_number = random.randint(2, 9)

    # Clear the screen and inform the student about the starting number
    screen.fill(screen_color)
    intro_message = f"Let's skip count by {skip_number}!"
    
    # Display the intro message and update the screen
    draw_text(intro_message, 
              font, 
              text_color, 
              x=0, 
              y=HEIGHT * 0.4, 
              center=True, 
              enable_shadow=True, 
              shadow_color=shadow_color,
              max_width=WIDTH)
    
    # Draw the "Continue..." button after intro message
    draw_and_wait_continue_button()

    # Start counting by the selected number, stopping at 100
    for i in range(skip_number, 101, skip_number):
        # Clear the screen before displaying each number
        screen.fill(screen_color)

        # Convert the number to string for display
        number_str = str(i)

        # Display the number in the center of the screen using the larger font size
        draw_text(number_str, large_font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

        # Update the screen after drawing the number
        pygame.display.flip()

        # Speak the number aloud in English
        speak_english(number_str)

        # Pause for a second before showing the next number
        time.sleep(1)

    # After completing the skip counting, show a completion message using the default font
    completion_message = "Great job!"
    screen.fill(screen_color)
    draw_text(completion_message, font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)
    
    # Draw the "Continue..." button after the completion message
    draw_and_wait_continue_button()
    
    
########################################
### 4. Menu and Navigation Functions ###
########################################

def introduction(font):
    fade_text_in_and_out("Developed by:", "Alvadore Retro Technology", font)


def load_options():
    """Load and apply saved options from JSON file. """
    global current_font_name_or_path, music_volume, current_resolution_index, current_theme
    
    try:
        with open("options.json", "r") as file:
            options = json.load(file)
        
        # Apply loaded settings
        current_font_name_or_path = options.get("font", "timesnewroman")
        music_volume = options.get("volume", 0.5)
        current_resolution_index = options.get("current_resolution_index", AVAILABLE_RESOLUTIONS.index((1080, 1080)))
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
    update_positions()


def main_menu():
    global font  # Ensure we update the global font variable
    
    # Check if music is currently playing
    if not pygame.mixer.music.get_busy():  # Returns False if no music is playing
        # If no music is playing, load and play a random MP3
        main_menu_music_directory = "assets/music/main_menu"
        random_mp3 = get_random_mp3(main_menu_music_directory)
        if random_mp3:
            music_loaded = load_mp3(random_mp3)
            if music_loaded:
                play_mp3()  # Start playing the random music if successfully loaded

    while True:
        # Recalculate the font size dynamically based on the current resolution
        font = pygame.font.SysFont(current_font_name_or_path, get_dynamic_font_size())  # Use the global font

        # Draw the background for the main menu
        draw_background(main_menu_background)
        
        # Draw the text options using the new draw_text function with rects for click detection
        draw_text("Learniverse", font, text_color, 0, HEIGHT * 0.2, screen, center=True, enable_shadow=True, return_rect=False, max_width=WIDTH)
        start_rect = draw_text("Start", font, text_color, 0, HEIGHT * 0.55, screen, center=True, enable_shadow=True, return_rect=True)
        options_rect = draw_text("Options", font, text_color, 0, HEIGHT * 0.7, screen, center=True, enable_shadow=True, return_rect=True)
        explanation_rect = draw_text("Learniverse?", font, text_color, 0, HEIGHT * 0.85, screen, center=True, enable_shadow=True, return_rect=True)
        
        # Draw the exit button using the new draw_text function and get its rect for click detection
        # exit_rect = draw_exit_button()
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if "Start" was clicked
                if start_rect and start_rect.collidepoint(mouse_pos):
                    return "student_select_menu"  # Return to indicate starting the game
                # Check if "Options" was clicked
                elif options_rect and options_rect.collidepoint(mouse_pos):
                    return "options_menu"  # Return to indicate transitioning to options menu
                elif explanation_rect and explanation_rect.collidepoint(mouse_pos):
                    return "learniverse_explanation"  # Return to indicate transitioning to options menu
                # Check if "X" was clicked
                # check_exit_click(mouse_pos, exit_rect)
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_b:  # Check if the 'b' key is pressed
            #         bonus_game_fat_tuna() # Skip directly to the bonus game for debug
            #     elif event.key == pygame.K_r:
            #         rainbow_numbers(45) # Fake session id to skip to rainbow numbers for testing
            #     elif event.key == pygame.K_s:
            #         skip_counting()

        clock.tick(60)


def student_select_menu():
    global font, current_student  # Make font and current_student global so they can be used across the function

    # Initial variables for text input
    input_active = False  # Whether the text input box is active
    student_input = ''  # The current input from the user

    while True:
        # Recalculate the font size dynamically based on the current resolution
        # font = pygame.font.SysFont(current_font_name_or_path, get_dynamic_font_size())  # Use the global font

        # Draw the background for the student select menu
        draw_background(main_menu_background)

        # Retrieve students from the database
        students = get_students()  # Fetch students from the database

        # Draw a title for the student selection menu
        draw_text("Select a Student", font, text_color, 0, HEIGHT * 0.1, screen, center=True, enable_shadow=True)

        # Display students as clickable text options
        student_rects = []  # List to hold rects for each student for click detection
        for index, student in enumerate(students):
            student_name = student[1]  # Assuming the student name is in the second column
            student_y = HEIGHT * (0.2 + 0.1 * index)  # Space out the student names vertically
            student_rect = draw_text(student_name, font, text_color, 0, student_y, screen, center=True, enable_shadow=True, return_rect=True)
            student_rects.append((student_rect, student_name))

        # Display the input box for adding new students
        input_box_rect = pygame.Rect(WIDTH * 0.55, HEIGHT * 0.74, WIDTH * 0.4, 80)  # The size of the input box
        pygame.draw.rect(screen, text_color, input_box_rect, 2)  # Draw the input box
        draw_text("New Student:", font, text_color, WIDTH * 0.05, HEIGHT * 0.75, screen, enable_shadow=True)
        draw_text(student_input, font, text_color, WIDTH * 0.56, HEIGHT * 0.74, screen, enable_shadow=True)

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if a student was clicked
                for rect, student_name in student_rects:
                    if rect.collidepoint(mouse_pos):
                        current_student = student_name  # Store the selected student's name
                        return "session_manager"  # Transition to the rainbow_numbers menu
                
                # Check if the input box is clicked to activate text input
                if input_box_rect.collidepoint(mouse_pos):
                    input_active = True

            elif event.type == pygame.KEYDOWN:
                if input_active:
                    # Handle text input for the new student name
                    if event.key == pygame.K_RETURN:  # Enter key to submit
                        if student_input.strip():  # Only add if the input is not empty
                            add_student(student_input.strip())  # Add the student to the database
                            student_input = ''  # Clear the input after submission
                            input_active = False  # Deactivate the text input
                    elif event.key == pygame.K_BACKSPACE:  # Handle backspace to delete characters
                        student_input = student_input[:-1]
                    else:
                        student_input += event.unicode  # Append new character to the input

        clock.tick(60)


def learniverse_explanation():
    # Define the folder path for the background images
    folder_path = "assets/images/explanation"

    # Select a random background image
    background_image_path = select_random_background(folder_path)

    # Define the text to display
    texts = [
        "What is Learniverse?",
        "Learniverse is an educational game designed to make learning fun!",
        "It helps students practice math skills through interactive gameplay.",
        "By integrating game elements, Learniverse aims to reduce the stress often associated with math.",
        "Students can choose their own pace and level, making learning personalized.",
        "The game provides instant feedback and rewards for progress.",
        "Learniverse covers fundamental math concepts that align with educational standards.",
        "Our goal is to turn learning into an engaging and enjoyable experience."
    ]

    for text in texts:
        # Draw the background before displaying the text
        draw_background(background_image_path)

        # Display the text
        display_text_and_wait(text)

    return "main_menu"  # Return to the main menu after all texts are displayed


def session_manager():
    global current_student  # Access global current_student

    # Step 1: Start the session and log in database
    session_id = start_new_session(current_student)

    # If session could not be started, return to main menu
    if session_id == -1:
        print(f"Error: Failed to start session for {current_student}.")
        return "main_menu"
    
    #####################################
    ### Step 2: Logic for lesson flow ###
    #####################################
    lessons_to_play = ["greet_student",                     #JP
                       # "rainbow_numbers",                   #Math
                       "japanese_colors1_quiz",             #JP
                       "streak_check",                      #ENG
                       "day_of_the_week",                   #JP
                       "month_of_the_year",                 #JP
                       "skip_counting",                     #Math
                       "hiragana_teach",                    #JP
                       "rainbow_numbers",                   #Math
                       "skip_counting_japanese",            #JP
                       "single_digit_addition",             #Math
                       "john_3_16",                         #ENG
                       "hiragana_quiz",                     #JP                      
                       "single_digit_subtraction",          #Math
                       "john_13_34",                        #ENG
                       "japanese_colors1_teach",            #JP
                       "single_digit_multiplication",       #Math
                       "hebrews_11_1",                      #ENG
                       "japanese_colors1_quiz",             #JP
                       "double_digit_subtraction",          #Math
                       "philippians_4_6",                   #ENG
                       "japanese_colors2_teach",            #JP
                       "double_digit_addition",             #Math
                       "ephesians_4_32",                    #ENG
                       "japanese_colors2_quiz",             #JP
                       "single_denominator_addition",       #Math
                       "japanese_colors3_teach",            #JP
                       "lowest_common_denominator_quiz",    #Math
                       "japanese_colors3_quiz",             #JP
                       "basic_shapes_quiz",                 #Math
                       "japanese_colors4_teach",            #JP
                       "single_by_double_multiplication",   #Math
                       "japanese_colors4_quiz",             #JP
                       "skip_counting_fibonacci",           #Math
                       "japanese_colors5_teach",            #JP
                       "skip_counting_primes",              #Math
                       "japanese_colors5_quiz",             #JP
                       "psalm_23",                          #ENG
                       
                       
                       
                       
                       
                       # "triple_digit_addition",
                       # "triple_digit_subtraction",
                       # "double_digit_multiplication",
                       # "quad_digit_addition",
                       # "quad_digit_subtraction",
                       ] 
    total_questions = 0
    total_correct = 0
    total_times = []  # List to track the average time across lessons

    # Loop through lessons
    for lesson in lessons_to_play:
        if lesson == "greet_student":
            greet_student()
        elif lesson == "streak_check":
            streak_check()
        elif lesson == "day_of_the_week":
            day_of_the_week()
        elif lesson == "month_of_the_year":
            month_of_the_year()
        elif lesson == "skip_counting":
            skip_counting()
        elif lesson == "skip_counting_fibonacci":
            skip_counting_fibonacci()
        elif lesson == "skip_counting_primes":
            skip_counting_primes()
        elif lesson == "john_3_16":
            john_3_16()
        elif lesson == "john_13_34":
            john_13_34()
        elif lesson == "psalm_23":
            psalm_23()
        elif lesson == "hebrews_11_1":
            hebrews_11_1()
        elif lesson == "philippians_4_6":
             philippians_4_6()
        elif lesson == "ephesians_4_32":
            ephesians_4_32()
        elif lesson == "hiragana_teach":
            hiragana_teach(session_id)
        elif lesson == "katakana_teach":
            katakana_teach(session_id)
        elif lesson == "rainbow_numbers":
            # Run the lesson, passing session_id
            lesson_result = rainbow_numbers(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            questions_asked, correct_answers, avg_time = lesson_result
            total_questions += questions_asked
            total_correct += correct_answers
            total_times.append(avg_time)
        elif lesson == "skip_counting_japanese":
            skip_counting_japanese()
        elif lesson == "hiragana_quiz":
            # Run the lesson, passing session_id
            lesson_result = hiragana_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            questions_asked, correct_answers, avg_time = lesson_result
            total_questions += questions_asked
            total_correct += correct_answers
            total_times.append(avg_time)
        elif lesson == "katakana_quiz":
            # Run the lesson, passing session_id
            lesson_result = katakana_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            questions_asked, correct_answers, avg_time = lesson_result
            total_questions += questions_asked
            total_correct += correct_answers
            total_times.append(avg_time)
        elif lesson == "single_digit_addition":
            print("Running single digit addition")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = single_digit_addition(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: single_digit_addition did not return a valid result.")
        elif lesson == "double_digit_addition":
            print("Running double digit addition")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = double_digit_addition(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: double_digit_addition did not return a valid result.")
        elif lesson == "triple_digit_addition":
            print("Running triple digit addition")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = triple_digit_addition(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: triple_digit_addition did not return a valid result.")
        elif lesson == "quad_digit_addition":
            print("Running quad digit addition")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = quad_digit_addition(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: quad_digit_addition did not return a valid result.")
        elif lesson == "single_digit_subtraction":
            print("Running single digit subtraction")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = single_digit_subtraction(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: single_digit_subtraction did not return a valid result.")
        elif lesson == "double_digit_subtraction":
            print("Running double digit subtraction")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = double_digit_subtraction(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: double_digit_subtraction did not return a valid result.")
        elif lesson == "triple_digit_subtraction":
            print("Running triple digit subtraction")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = triple_digit_subtraction(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: triple_digit_subtraction did not return a valid result.")
        elif lesson == "quad_digit_subtraction":
            print("Running quad digit subtraction")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = quad_digit_subtraction(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: quad_digit_subtraction did not return a valid result.")
        elif lesson == "single_digit_multiplication":
            print("Running single digit multiplication")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = single_digit_multiplication(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: single_digit_multiplication did not return a valid result.")
        # single_by_double_multiplication
        elif lesson == "single_by_double_multiplication":
            print("Running single by double digit multiplication")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = single_by_double_multiplication(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: single_by_double_multiplication did not return a valid result.")
        # double_digit_multiplication
        elif lesson == "double_digit_multiplication":
            print("Running double digit multiplication")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = double_digit_multiplication(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: double_digit_multiplication did not return a valid result.")
        # single_denominator_addition
        elif lesson == "single_denominator_addition":
            print("Running single_denominator_addition")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = single_denominator_addition(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: single_denominator_addition did not return a valid result.")
        # lowest_common_denominator_quiz
        elif lesson == "lowest_common_denominator_quiz":
            print("Running lowest_common_denominator_quiz")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = lowest_common_denominator_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: lowest_common_denominator_quiz did not return a valid result.")
        # basic_shapes_quiz
        elif lesson == "basic_shapes_quiz":
            print("Running basic_shapes_quiz")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = basic_shapes_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: basic_shapes_quiz did not return a valid result.")
        elif lesson == "japanese_colors1_teach":
            japanese_colors1_teach(session_id)
        elif lesson == "japanese_colors2_teach":
            japanese_colors2_teach(session_id)
        elif lesson == "japanese_colors3_teach":
            japanese_colors3_teach(session_id)
        elif lesson == "japanese_colors4_teach":
            japanese_colors4_teach(session_id)
        elif lesson == "japanese_colors5_teach":
            japanese_colors5_teach(session_id)
        elif lesson == "japanese_colors1_quiz":
            print("Running japanese_colors1_quiz")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = japanese_colors1_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: japanese_colors1_quiz did not return a valid result.")
        elif lesson == "japanese_colors2_quiz":
            print("Running japanese_colors2_quiz")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = japanese_colors2_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: japanese_colors2_quiz did not return a valid result.")
        elif lesson == "japanese_colors3_quiz":
            print("Running japanese_colors3_quiz")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = japanese_colors3_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: japanese_colors3_quiz did not return a valid result.")
        elif lesson == "japanese_colors4_quiz":
            print("Running japanese_colors4_quiz")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = japanese_colors4_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: japanese_colors4_quiz did not return a valid result.")
        elif lesson == "japanese_colors5_quiz":
            print("Running japanese_colors5_quiz")
            # Run the lesson, passing session_id, and capture the return values
            lesson_result = japanese_colors5_quiz(session_id)
            
            # Assuming lesson_result returns a tuple of (questions_asked, correct_answers, avg_time)
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: japanese_colors5_quiz did not return a valid result.")
        
        # Check if there's another lesson or handle lesson completion here
        # You can add more lessons to `lessons_to_play` and logic here
        

    # Step 3: Calculate total stats for the session
    if total_times:
        overall_avg_time = round(sum(total_times) / len(total_times), 1)
    else:
        overall_avg_time = 0

    # Step 4: End the session and log overall session stats
    end_session(session_id, total_questions, total_correct, overall_avg_time)

    # Return to main menu after all lessons are done
    return "main_menu"


def greet_student():
    global current_student  # Access global current_student
    global text_color, shadow_color, screen_color  # Access the theme-related globals
    
    stop_mp3()

    # Get the current time
    current_time = datetime.now().time()

    # Determine the appropriate greeting based on the time of day
    if current_time >= datetime.strptime("00:01", "%H:%M").time() and current_time < datetime.strptime("12:00", "%H:%M").time():
        # Morning greeting
        greeting_message_eng = f"Good morning, {current_student}! Welcome to your lesson."
        greeting_message_jp = "おはようございます。"  # Good morning in Japanese
    elif current_time >= datetime.strptime("12:00", "%H:%M").time() and current_time < datetime.strptime("17:00", "%H:%M").time():
        # Afternoon greeting
        greeting_message_eng = f"Hello, {current_student}! Welcome to your lesson."
        greeting_message_jp = "こんにちは。"  # Hello in Japanese
    else:
        # Evening greeting
        greeting_message_eng = f"Good evening, {current_student}! Welcome to your lesson."
        greeting_message_jp = "こんばんは。"  # Good evening in Japanese

    # Set a static sky blue background with Perlin clouds
    SKY_BLUE = (135, 206, 235)
    screen.fill(SKY_BLUE)  # Fill the screen with sky blue

    # Generate and blit Perlin clouds
    cloud_surface = generate_perlin_cloud(0)  # Use zero offset for static clouds
    screen.blit(cloud_surface, (0, 0))
    
    # Start growing tree from the exact bottom center
    grow_tree(screen, WIDTH * 0.25, HEIGHT, max_depth=10, max_branches=3)
    grow_tree(screen, WIDTH * 0.75, HEIGHT, max_depth=11, max_branches=3)

    # Draw the English greeting message
    draw_text(
        greeting_message_eng, 
        font, 
        text_color,  
        x=0, 
        y=HEIGHT * 0.20, 
        max_width=WIDTH * 0.95, 
        center=True,  
        enable_shadow=True,  
        shadow_color=shadow_color  
    )

    # Draw the Japanese greeting message and return its rect for click detection
    japanese_text_rect = draw_text(
        greeting_message_jp, 
        j_font,  
        text_color, 
        x=0, 
        y=HEIGHT * 0.60,  
        max_width=WIDTH * 0.95, 
        center=True,  
        enable_shadow=True,  
        shadow_color=shadow_color,
        return_rect=True  # Return the rect so we can detect clicks
    )
    
    # Draw the "Continue..." button wihtout draw_and_wait_continue_button()
    # As we do special stuff while waiting
    continue_rect = draw_continue_button()

    pygame.display.flip()  # Update the display

    # Use the reusable TTS function to speak the Japanese greeting aloud
    speak_japanese(greeting_message_jp)

    # Wait for the "Continue..." click or a click on the Japanese text to repeat TTS
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Correctly exit the program
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if the Japanese text is clicked
                if japanese_text_rect.collidepoint(mouse_pos):
                    speak_japanese(greeting_message_jp)  # Replay the Japanese greeting

                # Check if the "Continue..." button is clicked
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False  # Exit the loop when "Continue..." is clicked


def streak_check():
    global text_color, shadow_color, screen_color  # Access the theme-related globals

    # Fill the screen with the background color from the applied theme
    screen.fill(screen_color)

    # Query the student's streak
    streak_days = student_streak_query()

    # Check if the student is on a streak
    if streak_days > 1:
        message = f"Great job! You've been on a streak for {streak_days} days in a row!"
    elif streak_days == 1:
        message = "You're on a 1-day streak! Keep it up!"
    else:
        message = "Let's start a streak today! Keep it up!"

    # Display the message
    draw_text(
        message, 
        font, 
        text_color, 
        x=0, 
        y=HEIGHT * 0.25, 
        max_width=WIDTH * 0.8,  # Wrap text within 80% of the screen width
        center=True, 
        enable_shadow=True, 
        shadow_color=shadow_color
    )

    # Draw the "Continue..." button
    draw_and_wait_continue_button()


############################
### Jr. Church Functions ###
############################

def display_bible_verse(greeting_message, 
                        verse_title, 
                        verse_text, 
                        split_text=None):
    """Displays a Bible verse with an optional split for larger texts."""
    global screen_color, text_color, shadow_color, font
    
    # Define a larger font size for the Bible verse
    large_font_size = 60  # Adjust size as necessary
    large_font = pygame.font.Font(None, large_font_size)

    # Clear the screen and display the greeting message
    screen.fill(screen_color)
    draw_text(
        greeting_message,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        max_width=WIDTH
    )

    # Draw the "Continue" button and wait for the student to click
    draw_and_wait_continue_button()

    # If there is a split text (for long verses like Psalm 23), handle it in two parts
    if split_text:
        # Display and read the first part of the verse
        screen.fill(screen_color)
        draw_text(
            verse_title + "\n" + split_text[0],
            font,  
            text_color,
            x=0,
            y=HEIGHT * 0.1,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color,
            max_width=WIDTH * 0.95,
            font_override=large_font
        )

        # Update the screen before speaking
        pygame.display.flip()
        speak_english(verse_title + " " + split_text[0])

        # Draw the "Continue" button again and wait for the student to click
        draw_and_wait_continue_button()

        # Display and read the second part of the verse
        screen.fill(screen_color)
        draw_text(
            split_text[1],
            font,  
            text_color,
            x=0,
            y=HEIGHT * 0.1,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color,
            max_width=WIDTH * 0.95,
            font_override=large_font
        )

        # Update the screen before speaking
        pygame.display.flip()
        speak_english(split_text[1])

    else:
        # Display and read the entire verse if there's no split text
        screen.fill(screen_color)
        draw_text(
            verse_title + "\n" + verse_text,
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.1,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color,
            max_width=WIDTH * 0.95,
            font_override=large_font
        )

        # Update the screen before speaking
        pygame.display.flip()
        speak_english(verse_title + " " + verse_text)

    # Draw the "Continue" button again after displaying the verse
    draw_and_wait_continue_button()





def john_3_16():
    """Greets the student and introduces the Bible verse John 3:16 (NKJV)."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "John 3:16"
    verse_text = "For God so loved the world, that He gave His only begotten Son, that whosoever believeth in Him should not perish, but have everlasting life."
    display_bible_verse(greeting_message, verse_title, verse_text)


def john_13_34():
    """Greets the student and introduces the Bible verse John 13:34 (NKJV)."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "John 13:34"
    verse_text = "A new commandment I give to you, that you love one another; as I have loved you, that you also love one another."
    display_bible_verse(greeting_message, verse_title, verse_text)



def psalm_23():
    """Greets the student and introduces the Bible verse Psalm 23 (KJV) in two parts."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "Psalm 23"
    split_text = [
        "The Lord is my shepherd; I shall not want. He maketh me to lie down in green pastures: he leadeth me beside the still waters. He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake. Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me.",
        "Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over. Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the Lord for ever."
    ]
    display_bible_verse(greeting_message, verse_title, "", split_text)


def hebrews_11_1(): 
    """Greets the student and introduces the Bible verse Hebrews 11:1 (NKJV)."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "Hebrews 11:1"
    verse_text = "Now faith is the substance of things hoped for, the evidence of things not seen."
    display_bible_verse(greeting_message, verse_title, verse_text)


def philippians_4_6():
    """Greets the student and introduces the Bible verse Philippians 4:6 (NKJV)."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "Philippians 4:6"
    verse_text = "Be anxious for nothing, but in everything by prayer and supplication, with thanksgiving, let your requests be made known to God."
    display_bible_verse(greeting_message, verse_title, verse_text)


def ephesians_4_32():
    """Greets the student and introduces the Bible verse Ephesians 4:32 (NKJV)."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "Ephesians 4:32"
    verse_text = "And be kind to one another, tenderhearted, forgiving one another, even as God in Christ forgave you."
    display_bible_verse(greeting_message, verse_title, verse_text)






##########################
### Japanese Functions ###
##########################

def day_of_the_week():
    global text_color, shadow_color, screen_color  # Access the theme-related globals

    # Get today's day of the week (e.g., Monday, Tuesday, etc.)
    today_english = datetime.now().strftime("%A")  # Returns the full weekday name (e.g., "Wednesday")

    # Mapping English weekdays to Japanese equivalents (with hiragana)
    japanese_days = {
        "Monday": "月曜日",
        "Tuesday": "火曜日",
        "Wednesday": "水曜日", 
        "Thursday": "木曜日",
        "Friday": "金曜日",
        "Saturday": "土曜日",
        "Sunday": "日曜日"
    }

    today_japanese = japanese_days.get(today_english, today_english)  # Get the Japanese equivalent

    # Create the messages to display
    japanese_message = f"今日は {today_japanese} です。"  # In Japanese: "Today is (day) in Japanese"
    english_message = f"Today is {today_english}."  # In English

    # Fill the screen with the background color from the applied theme
    screen.fill(screen_color)

    # Display the Japanese message and capture its rect for click detection
    japanese_text_rect = draw_text(
        japanese_message, 
        j_font,  # Assuming you've set up a separate Japanese font
        text_color, 
        x=0, 
        y=HEIGHT * 0.25, 
        max_width=WIDTH * 0.95,  # Wrap text within 80% of the screen width
        center=True, 
        enable_shadow=True, 
        shadow_color=shadow_color,
        return_rect=True  # Return the rect for the Japanese text
    )

    # Display the English message right below the Japanese message
    draw_text(
        english_message, 
        font,  # Use the English font for this line
        text_color, 
        x=0, 
        y=HEIGHT * 0.45,  # Display slightly below the Japanese text
        max_width=WIDTH * 0.95,  # Wrap text within 80% of the screen width
        center=True, 
        enable_shadow=True, 
        shadow_color=shadow_color
    )

    # Draw the "Continue..." button
    continue_rect = draw_continue_button()

    pygame.display.flip()  # Update the display

    # Use the reusable TTS function to speak the Japanese message aloud
    speak_japanese(japanese_message)

    # Wait for the "Continue..." click or a click on the Japanese text to repeat TTS
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if the Japanese text is clicked
                if japanese_text_rect.collidepoint(mouse_pos):
                    speak_japanese(japanese_message)  # Replay the Japanese message

                # Check if the "Continue..." button is clicked
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False  # Exit the loop when "Continue..." is clicked


def month_of_the_year():
    global text_color, shadow_color, screen_color  # Access the theme-related globals

    # Get today's month of the year (e.g., January, February, etc.)
    current_month_english = datetime.now().strftime("%B")  # Returns the full month name (e.g., "January")

    # Mapping English months to Japanese equivalents (with hiragana)
    japanese_months = {
        "January": "1月",
        "February": "2月",
        "March": "3月",
        "April": "4月",
        "May": "5月",
        "June": "6月",
        "July": "7月",
        "August": "8月",
        "September": "9月",
        "October": "10月",
        "November": "11月",
        "December": "12月"
    }

    # Get the Japanese equivalent of the current month
    current_month_japanese = japanese_months.get(current_month_english, current_month_english)

    # Create the messages to display
    japanese_message = f"今月は {current_month_japanese} です。"  # In Japanese: "This month is (month) in Japanese"
    english_message = f"This month is {current_month_english}."  # In English

    # Fill the screen with the background color from the applied theme
    screen.fill(screen_color)

    # Display the Japanese message and capture its rect for click detection
    japanese_text_rect = draw_text(
        japanese_message, 
        j_font,  # Assuming you've set up a separate Japanese font
        text_color, 
        x=0, 
        y=HEIGHT * 0.25, 
        max_width=WIDTH * 0.95,  # Wrap text within 95% of the screen width
        center=True, 
        enable_shadow=True, 
        shadow_color=shadow_color,
        return_rect=True  # Return the rect for the Japanese text
    )

    # Display the English message right below the Japanese message
    draw_text(
        english_message, 
        font,  # Use the English font for this line
        text_color, 
        x=0, 
        y=HEIGHT * 0.45,  # Display slightly below the Japanese text
        max_width=WIDTH * 0.95,  # Wrap text within 95% of the screen width
        center=True, 
        enable_shadow=True, 
        shadow_color=shadow_color
    )

    # Draw the "Continue..." button
    continue_rect = draw_continue_button()

    pygame.display.flip()  # Update the display

    # Use the reusable TTS function to speak the Japanese message aloud
    speak_japanese(japanese_message)

    # Wait for the "Continue..." click or a click on the Japanese text to repeat TTS
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if the Japanese text is clicked
                if japanese_text_rect.collidepoint(mouse_pos):
                    speak_japanese(japanese_message)  # Replay the Japanese message

                # Check if the "Continue..." button is clicked
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False  # Exit the loop when "Continue..." is clicked


def skip_counting_japanese():
    """Performs skip counting in Arabic numerals from 1 to 30, while speaking the numbers in Japanese."""
    global screen_color, text_color, shadow_color, current_font_name_or_path, font  # Access theme-related globals

    # Define a larger size for the Arabic numerals
    large_font_size = 200  # Adjust size as necessary

    # Initialize the larger font based on whether the current font is a file or system font
    if os.path.isfile(current_font_name_or_path):
        large_font = pygame.font.Font(current_font_name_or_path, large_font_size)
    else:
        large_font = pygame.font.SysFont(current_font_name_or_path, large_font_size)

    # Clear the screen and inform the student about the activity
    screen.fill(screen_color)
    intro_message = "Let's count in Japanese!"
    
    # Display the intro message and update the screen using the default global font
    draw_text(intro_message, 
              font, 
              text_color, 
              x=0, 
              y=HEIGHT * 0.4, 
              center=True, 
              enable_shadow=True, 
              shadow_color=shadow_color,
              max_width=WIDTH)
    
    # Draw the "Continue..." button after the intro message
    draw_and_wait_continue_button()

    # Start counting from 1 to 30
    for i in range(1, 31):
        # Clear the screen before displaying each number
        screen.fill(screen_color)

        # Convert the number to string for display
        number_str = str(i)

        # Display the number in the center of the screen using the larger font size
        draw_text(number_str, large_font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

        # Update the screen after drawing the number
        pygame.display.flip()

        # Speak the number aloud in Japanese (using Haruka voice)
        speak_japanese(number_str)

        # Pause for a second before showing the next number
        time.sleep(1)

    # After completing the skip counting, show a completion message using the default font
    completion_message = "Great job!"
    screen.fill(screen_color)
    draw_text(completion_message, font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

    # Draw the "Continue..." button after the completion message
    draw_and_wait_continue_button()


def get_hiragana_subset_by_level(student_level, hiragana_list):
    """Returns the subset of Hiragana characters to teach or quiz based on the student's level."""
    max_characters = min(student_level * 5, len(hiragana_list))
    return hiragana_list[:max_characters]


def hiragana_teach(session_id):
    """Displays Hiragana characters one by one based on the student's current level and reads them aloud using Japanese TTS."""
    global screen_color, text_color, shadow_color  # Access theme-related globals
    
    # Retrieve the student's current level for the Hiragana lesson
    student_level = get_student_progress(session_id, 'Hiragana')

    # List of the 46 basic hiragana characters
    hiragana_list = [
        "あ", "い", "う", "え", "お", 
        "か", "き", "く", "け", "こ", 
        "さ", "し", "す", "せ", "そ", 
        "た", "ち", "つ", "て", "と", 
        "な", "に", "ぬ", "ね", "の", 
        "は", "ひ", "ふ", "へ", "ほ", 
        "ま", "み", "む", "め", "も", 
        "や", "ゆ", "よ", 
        "ら", "り", "る", "れ", "ろ", 
        "わ", "を", 
        "ん"
    ]

    # Get the subset of Hiragana to teach based on the student's current level
    hiragana_subset = get_hiragana_subset_by_level(student_level, hiragana_list)

    # Define a larger font for the hiragana characters
    large_japanese_font = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", 300)

    # Clear the screen and inform the student about the lesson
    screen.fill(screen_color)
    intro_message = f"Let's learn Hiragana! You are currently on level {student_level}."
    draw_text(intro_message, font, text_color, x=0, y=HEIGHT * 0.4, center=True, 
              enable_shadow=True, shadow_color=shadow_color, max_width=WIDTH)

    # Display "Continue..." button and wait for user input
    draw_and_wait_continue_button()

    # Loop through the subset of Hiragana and show each character
    for hiragana_char in hiragana_subset:
        screen.fill(screen_color)
        draw_text(hiragana_char, j_font, text_color, x=0, y=HEIGHT * 0.3, center=True, 
                  enable_shadow=True, shadow_color=shadow_color, font_override=large_japanese_font)
        pygame.display.flip()
        speak_japanese(hiragana_char)
        time.sleep(1)

    # Show completion message and wait for "Continue..."
    screen.fill(screen_color)
    draw_text("Great job!", font, text_color, x=0, y=HEIGHT * 0.4, center=True, 
              enable_shadow=True, shadow_color=shadow_color)
    draw_and_wait_continue_button()


def display_hiragana_quiz(screen, hiragana_char, options):
    screen.fill(NAVY_BLUE)

    # Draw the Hiragana on the screen using the updated draw_text function
    draw_text(
        hiragana_char,
        j_font,  # Assuming you have a separate Japanese font loaded
        WHITE,
        x=WIDTH // 2,
        y=HEIGHT // 3,
        center=True,
        enable_shadow=True,
        shadow_color=BLACK,
        use_japanese_font=True
    )

    # Draw the multiple-choice options
    option_rects = []
    y_pos = HEIGHT * 0.6
    answer_buffer = HEIGHT * 0.1

    for i, option in enumerate(options):
        option_rect = draw_text(
            option,
            font,  # Use your default or specific font here
            WHITE,
            x=WIDTH // 2,
            y=y_pos + i * answer_buffer,
            center=True,
            enable_shadow=True,
            shadow_color=BLACK,
            return_rect=True
        )
        option_rects.append((option_rect, option))

    pygame.display.flip()
    return option_rects


def hiragana_quiz(session_id):
    """Presents a quiz on Hiragana characters based on the student's level and updates their progress."""
    global screen_color, text_color, shadow_color  # Access theme-related globals

    # Retrieve the student's current level for the Hiragana lesson
    student_level = get_student_progress(session_id, 'Hiragana')

    # Fetch the Hiragana lesson ID
    hiragana_lesson_id = fetch_lesson_id('Hiragana')
    if hiragana_lesson_id is None:
        return -1  # Exit if lesson_id not found

    # Display the introductory message with the student's current level
    screen.fill(screen_color)
    draw_text(f"Hiragana quiz! You are currently on level {student_level}.", font, text_color,
              x=0, y=HEIGHT * 0.4, max_width=WIDTH * 0.95, center=True, enable_shadow=True, shadow_color=shadow_color)

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    # List of Hiragana characters
    hiragana_list = [
        ('あ', 'a'), ('い', 'i'), ('う', 'u'), ('え', 'e'), ('お', 'o'), ('か', 'ka'), 
        ('き', 'ki'), ('く', 'ku'), ('け', 'ke'), ('こ', 'ko'), ('さ', 'sa'), ('し', 'shi'), 
        ('す', 'su'), ('せ', 'se'), ('そ', 'so'), ('た', 'ta'), ('ち', 'chi'), ('つ', 'tsu'), 
        ('て', 'te'), ('と', 'to'), ('な', 'na'), ('に', 'ni'), ('ぬ', 'nu'), ('ね', 'ne'), 
        ('の', 'no'), ('は', 'ha'), ('ひ', 'hi'), ('ふ', 'fu'), ('へ', 'he'), ('ほ', 'ho'),
        ('ま', 'ma'), ('み', 'mi'), ('む', 'mu'), ('め', 'me'), ('も', 'mo'), ('や', 'ya'),
        ('ゆ', 'yu'), ('よ', 'yo'), ('ら', 'ra'), ('り', 'ri'), ('る', 'ru'), ('れ', 're'),
        ('ろ', 'ro'), ('わ', 'wa'), ('を', 'wo'), ('ん', 'n')
    ]

    # Adjust the number of Hiragana characters based on the student's level
    hiragana_subset = get_hiragana_subset_by_level(student_level, hiragana_list)
    random.shuffle(hiragana_subset)

    total_questions = 5  # Set the number of questions
    correct_answers = 0
    completion_times = []

    # Quiz loop
    for problem_count in range(total_questions):
        hiragana_char, correct_english = hiragana_subset[problem_count % len(hiragana_subset)]

        # Create multiple-choice options
        incorrect_answers = random.sample(
            [h[1] for h in hiragana_subset if h[1] != correct_english], 3)
        options = [correct_english] + incorrect_answers
        random.shuffle(options)

        # Display the quiz options and get option rects
        option_rects = display_hiragana_quiz(screen, hiragana_char, options)

        # Wait for student to click on an option
        start_time = time.time()
        question_complete = False
        while not question_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for rect, option in option_rects:
                        if rect.collidepoint(mouse_pos):
                            time_taken = round(time.time() - start_time, 1)
                            completion_times.append(time_taken)

                            if option == correct_english:
                                correct_answers += 1
                                display_result("Correct!", "assets/images/fast_cats", use_lightning=(time_taken < 3))
                            else:
                                display_result(f"Sorry, the correct answer is {correct_english}")
                            question_complete = True

            pygame.time.Clock().tick(60)

    # Final score and performance
    lesson_end_time = time.time()
    average_time = round(sum(completion_times) / len(completion_times), 1) if completion_times else 0
    add_session_lesson(session_id, hiragana_lesson_id, lesson_start_time, lesson_end_time, total_questions, correct_answers)

    # Display the final score and handle perfect scores
    screen.fill(screen_color)
    draw_text(f"Final Score: {correct_answers}/{total_questions}", font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)
    
    if correct_answers == total_questions:
        set_student_progress(session_id, 'Hiragana')  # Level up on perfect score
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()
    
    # Return the results of the quiz
    return total_questions, correct_answers, average_time


def katakana_teach(session_id):
    """Displays Katakana characters one by one based on the student's current level and reads them aloud using Japanese TTS."""
    global screen_color, text_color, shadow_color  # Access theme-related globals
    
    # Retrieve the student's current level for the Katakana lesson
    student_level = get_student_progress(session_id, 'Katakana')

    # List of the 46 basic katakana characters
    katakana_list = [
        "ア", "イ", "ウ", "エ", "オ", 
        "カ", "キ", "ク", "ケ", "コ", 
        "サ", "シ", "ス", "セ", "ソ", 
        "タ", "チ", "ツ", "テ", "ト", 
        "ナ", "ニ", "ヌ", "ネ", "ノ", 
        "ハ", "ヒ", "フ", "ヘ", "ホ", 
        "マ", "ミ", "ム", "メ", "モ", 
        "ヤ", "ユ", "ヨ", 
        "ラ", "リ", "ル", "レ", "ロ", 
        "ワ", "ヲ", "ン"
    ]

    # Get the subset of Katakana to teach based on the student's current level
    katakana_subset = get_hiragana_subset_by_level(student_level, katakana_list)

    # Define a larger font for the katakana characters
    large_japanese_font = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", 300)

    # Clear the screen and inform the student about the lesson
    screen.fill(screen_color)
    intro_message = f"Let's learn Katakana! You are currently on level {student_level}."
    draw_text(intro_message, font, text_color, x=0, y=HEIGHT * 0.4, center=True, 
              enable_shadow=True, shadow_color=shadow_color, max_width=WIDTH)

    draw_and_wait_continue_button()

    # Loop through the subset of Katakana and show each character
    for katakana_char in katakana_subset:
        screen.fill(screen_color)
        draw_text(katakana_char, j_font, text_color, x=0, y=HEIGHT * 0.3, center=True, 
                  enable_shadow=True, shadow_color=shadow_color, font_override=large_japanese_font)
        pygame.display.flip()
        speak_japanese(katakana_char)
        time.sleep(1)

    # Show completion message and wait for "Continue..."
    screen.fill(screen_color)
    draw_text("Great job!", font, text_color, x=0, y=HEIGHT * 0.4, center=True, 
              enable_shadow=True, shadow_color=shadow_color)
    draw_and_wait_continue_button()


def katakana_quiz(session_id):
    """Presents a quiz on Katakana characters based on the student's level and updates their progress."""
    global screen_color, text_color, shadow_color  # Access theme-related globals

    # Retrieve the student's current level for the Katakana lesson
    student_level = get_student_progress(session_id, 'Katakana')

    # Fetch the Katakana lesson ID
    katakana_lesson_id = fetch_lesson_id('Katakana')
    if katakana_lesson_id is None:
        return -1  # Exit if lesson_id not found

    # Display the introductory message with the student's current level
    screen.fill(screen_color)
    draw_text(f"Katakana quiz! You are currently on level {student_level}.", font, text_color,
              x=0, y=HEIGHT * 0.4, max_width=WIDTH * 0.95, center=True, enable_shadow=True, shadow_color=shadow_color)

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    # List of Katakana characters
    katakana_list = [
        ('ア', 'a'), ('イ', 'i'), ('ウ', 'u'), ('エ', 'e'), ('オ', 'o'),  # a, i, u, e, o
        ('カ', 'ka'), ('キ', 'ki'), ('ク', 'ku'), ('ケ', 'ke'), ('コ', 'ko'),  # ka, ki, ku, ke, ko
        ('サ', 'sa'), ('シ', 'shi'), ('ス', 'su'), ('セ', 'se'), ('ソ', 'so'),  # sa, shi, su, se, so
        ('タ', 'ta'), ('チ', 'chi'), ('ツ', 'tsu'), ('テ', 'te'), ('ト', 'to'),  # ta, chi, tsu, te, to
        ('ナ', 'na'), ('ニ', 'ni'), ('ヌ', 'nu'), ('ネ', 'ne'), ('ノ', 'no'),  # na, ni, nu, ne, no
        ('ハ', 'ha'), ('ヒ', 'hi'), ('フ', 'fu'), ('ヘ', 'he'), ('ホ', 'ho'),  # ha, hi, fu, he, ho
        ('マ', 'ma'), ('ミ', 'mi'), ('ム', 'mu'), ('メ', 'me'), ('モ', 'mo'),  # ma, mi, mu, me, mo
        ('ヤ', 'ya'), ('ユ', 'yu'), ('ヨ', 'yo'),  # ya, yu, yo
        ('ラ', 'ra'), ('リ', 'ri'), ('ル', 'ru'), ('レ', 're'), ('ロ', 'ro'),  # ra, ri, ru, re, ro
        ('ワ', 'wa'), ('ヲ', 'wo'), ('ン', 'n')  # wa, wo, n
    ]


    # Adjust the number of Katakana characters based on the student's level
    katakana_subset = get_hiragana_subset_by_level(student_level, katakana_list)
    random.shuffle(katakana_subset)

    total_questions = 5
    correct_answers = 0
    completion_times = []

    # Quiz loop (same as in hiragana_quiz)
    for problem_count in range(total_questions):
        katakana_char, correct_english = katakana_subset[problem_count % len(katakana_subset)]

        # Create multiple-choice options
        incorrect_answers = random.sample([k[1] for k in katakana_subset if k[1] != correct_english], 3)
        options = [correct_english] + incorrect_answers
        random.shuffle(options)

        # Display the quiz options and get option rects
        option_rects = display_hiragana_quiz(screen, katakana_char, options)

        # Wait for student to click on an option
        start_time = time.time()
        question_complete = False
        while not question_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for rect, option in option_rects:
                        if rect.collidepoint(mouse_pos):
                            time_taken = round(time.time() - start_time, 1)
                            completion_times.append(time_taken)

                            if option == correct_english:
                                correct_answers += 1
                                display_result("Correct!", "assets/images/fast_cats", use_lightning=(time_taken < 3))
                            else:
                                display_result(f"Sorry, the correct answer is {correct_english}")
                            question_complete = True

            pygame.time.Clock().tick(60)

    # Final score and performance
    lesson_end_time = time.time()
    average_time = round(sum(completion_times) / len(completion_times), 1) if completion_times else 0
    add_session_lesson(session_id, katakana_lesson_id, lesson_start_time, lesson_end_time, total_questions, correct_answers)

    # Display the final score and handle perfect scores
    screen.fill(screen_color)
    draw_text(f"Final Score: {correct_answers}/{total_questions}", font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)
    
    if correct_answers == total_questions:
        set_student_progress(session_id, 'Katakana')  # Level up on perfect score
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_fat_tuna()
    
    return total_questions, correct_answers, average_time


def japanese_colors1_teach(session_id):
    japanese_colors_teach(session_id, colors1)

    
def japanese_colors2_teach(session_id):
    japanese_colors_teach(session_id, colors2)


def japanese_colors3_teach(session_id):
    japanese_colors_teach(session_id, colors3)

    
def japanese_colors4_teach(session_id):
    japanese_colors_teach(session_id, colors4)

        
def japanese_colors5_teach(session_id):
    japanese_colors_teach(session_id, colors5)


def japanese_colors_teach(session_id, color_to_teach):
    """Displays Japanese colors (furigana, kanji, and translation) and reads them aloud using Japanese TTS."""
    global screen_color, text_color, shadow_color, WIDTH, HEIGHT  # Access theme-related globals

    # Define fonts for the furigana, kanji, and translation
    furigana_font = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", 100)
    kanji_font = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", 300)
    translation_font = pygame.font.Font(None, 50)

    # Clear the screen and inform the student about the lesson
    screen.fill(screen_color)
    intro_message = "Let's learn Japanese colors!"
    draw_text(intro_message, translation_font, text_color, x=0, y=HEIGHT * 0.2, center=True, 
              enable_shadow=True, shadow_color=shadow_color, max_width=WIDTH)

    # Display "Continue..." button and wait for user input
    draw_and_wait_continue_button()

    # Loop through the colors and display each one
    for color in color_to_teach['questions']:
        # Step 1: Show furigana, kanji, and translation, and read aloud
        screen.fill(screen_color)

        # Display furigana (above kanji)
        draw_text(color['furigana'], furigana_font, text_color, x=0, y=HEIGHT * 0.1, center=True, 
                  enable_shadow=True, shadow_color=shadow_color)

        # Display kanji (below furigana)
        draw_text(color['kanji'], kanji_font, text_color, x=0, y=HEIGHT * 0.3, center=True, 
                  enable_shadow=True, shadow_color=shadow_color)

        # Display English translation (below kanji)
        draw_text(color['translation'], translation_font, text_color, x=0, y=HEIGHT * 0.6, center=True, 
                  enable_shadow=True, shadow_color=shadow_color)

        pygame.display.flip()

        # Speak the furigana (the reading of the kanji)
        speak_japanese(color['furigana'])
        time.sleep(1)  # Wait for the audio to finish

        # Step 2: Try to show the color image, fallback to showing kanji, furigana, and translation if image is missing
        try:
            # Try to load and resize the color image to the current window size
            color_image = pygame.image.load(color['image'])
            color_image = pygame.transform.scale(color_image, (WIDTH, HEIGHT))

            # Blit the image on the screen
            screen.blit(color_image, (0, 0))  # Blit image at top left (fills entire screen)
            pygame.display.flip()

            # Speak the furigana again (in the background, no text)
            speak_japanese(color['furigana'])
            time.sleep(1)  # Wait for the audio to finish

        except FileNotFoundError:
            # If image is not found, display kanji, furigana, and translation again
            log_message(f"Image not found: {color['image']}. Displaying text instead.")
            screen.fill(screen_color)

            # Display furigana, kanji, and translation again as fallback
            draw_text(color['furigana'], furigana_font, text_color, x=0, y=HEIGHT * 0.1, center=True, 
                      enable_shadow=True, shadow_color=shadow_color)
            draw_text(color['kanji'], kanji_font, text_color, x=0, y=HEIGHT * 0.3, center=True, 
                      enable_shadow=True, shadow_color=shadow_color)
            draw_text(color['translation'], translation_font, text_color, x=0, y=HEIGHT * 0.6, center=True, 
                      enable_shadow=True, shadow_color=shadow_color)

            pygame.display.flip()

            # Speak the furigana again
            speak_japanese(color['furigana'])
            time.sleep(1)  # Wait for the audio to finish

    # Show completion message and wait for "Continue..."
    screen.fill(screen_color)
    completion_message = "Great job! You just learned Japanese colors!"
    draw_text(completion_message, translation_font, text_color, x=0, y=HEIGHT * 0.4, center=True, 
              enable_shadow=True, shadow_color=shadow_color)
    draw_and_wait_continue_button()





def display_result_with_image(result_text, image_file=None, use_lightning=False):
    """
    Display the result text and an optional image from a given file.
    If an image is provided and 'use_lightning' is True, show lightning instead of particles.
    If 'use_lightning' is False, show a particle effect.
    """
    # Clear the event queue to avoid any unwanted inputs
    pygame.event.clear()

    # Initialize particle list
    particles = []

    # Define a variable for particle delay (adjustable)
    PARTICLE_DELAY_MS = 20  # Delay in milliseconds between each frame of particle rendering

    # Attempt to load the image if provided
    bg_image = None
    if image_file:
        try:
            bg_image = pygame.image.load(image_file)
            # Resize the image to the screen dimensions
            bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        except FileNotFoundError:
            log_message(f"Image not found: {image_file}. Displaying text only.")
            # If the image is not found, bg_image remains None

    # If the image loaded successfully, blit it to the screen
    if bg_image:
        screen.blit(bg_image, (0, 0))

        if not use_lightning:
            # Generate particles for the effect (only if use_lightning is False)
            for _ in range(500):  # Number of particles to generate
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                color = random.choice([NAVY_BLUE, (255, 255, 255), ROYAL_BLUE, LIGHT_BLUE])
                particles.append(Particle(x, y, color))
    else:
        # If no image file is provided or failed to load, fill the screen with the current screen color
        screen.fill(screen_color)

    # Display loop for particle effect or lightning effect
    if use_lightning and bg_image:
        # Show lightning effect if the fast answer condition is met
        for _ in range(3):  # Increased number of lightning bolts for dramatic effect
            draw_lightning(screen, (random.randint(0, WIDTH), 0), (random.randint(0, WIDTH), HEIGHT), 
                           image_file, font, text_color, correct_message=result_text)
            pygame.display.flip()
            pygame.time.delay(150)  # Slight delay between lightning bolts
    else:
        # Show particle effect for slower answers or if no image is available
        for _ in range(50):  # Run the particle effect for 50 frames
            if bg_image:
                # Transparent fill to allow particles to fade
                screen.fill((0, 0, 0, 0))
                screen.blit(bg_image, (0, 0))

                # Update and draw each particle
                for particle in particles[:]:
                    particle.update()
                    if particle.lifetime <= 0:
                        particles.remove(particle)
                    else:
                        particle.draw(screen)

                # Add delay to control the speed of particle rendering
                pygame.time.delay(PARTICLE_DELAY_MS)
            else:
                # For incorrect answers or if no image is available, fill the screen with the current screen color
                screen.fill(screen_color)

            # Draw the result text on top of the particles or background
            draw_text(result_text, 
                      font, 
                      text_color, 
                      WIDTH // 2, 
                      HEIGHT // 2, 
                      center=True, 
                      enable_shadow=True,
                      max_width=WIDTH)
            pygame.display.flip()

    # Final display and pause before exiting the function
    pygame.display.flip()
    time.sleep(1)  # Pause for 1 second

    # Clear the event queue again after displaying the result
    pygame.event.clear()





def japanese_colors_quiz(session_id, color_data):
    """Presents a quiz on Japanese colors (furigana, kanji, and translation) and tracks performance."""
    global screen_color, text_color, shadow_color  # Access theme-related globals

    # Extract the quiz name from color_data
    quiz_name = color_data.get('quiz_title')
    if quiz_name is None:
        log_message("Error: quiz_title missing in color_data.")
        return -1  # Exit if quiz_title is missing

    # Fetch the unique lesson ID for the specific color quiz (e.g., "Colors 1")
    color_lesson_id = fetch_lesson_id(quiz_name)
    if color_lesson_id is None:
        log_message(f"Lesson '{quiz_name}' not found in the database.")
        return -1  # Exit if lesson_id not found

    # Start the lesson timer
    lesson_start_time = time.time()

    # Shuffle the questions
    color_questions = color_data['questions']
    random.shuffle(color_questions)

    total_questions = 5  # Set the number of questions
    correct_answers = 0
    completion_times = []

    # Quiz loop
    for problem_count in range(total_questions):
        question = color_questions[problem_count % len(color_questions)]
        correct_answer = question['translation']

        # Generate 3 incorrect answers
        incorrect_answers = random.sample(
            [q['translation'] for q in color_questions if q['translation'] != correct_answer], 3)

        # Create the multiple-choice options
        options = [correct_answer] + incorrect_answers
        random.shuffle(options)

        # Display the quiz options and get option rects
        kanji_rect, furigana_rect, option_rects = display_color_quiz(screen, question['kanji'], question['furigana'], options)

        # Update the screen before speaking the furigana
        pygame.display.flip()

        # Speak the furigana aloud in Japanese after drawing the screen
        speak_japanese(question['furigana'])

        # Wait for the student to click on an option or on the kanji/furigana to hear it again
        start_time = time.time()
        question_complete = False
        while not question_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # Check if the student clicked the kanji or furigana to replay the audio
                    if kanji_rect.collidepoint(mouse_pos) or furigana_rect.collidepoint(mouse_pos):
                        speak_japanese(question['furigana'])  # Replay the furigana audio
                        break  # Stay on the same question, wait for another click

                    # Check if an option was clicked
                    for rect, option in option_rects:
                        if rect.collidepoint(mouse_pos):
                            time_taken = round(time.time() - start_time, 1)
                            completion_times.append(time_taken)

                            if option == correct_answer:
                                correct_answers += 1
                                if time_taken < 3:
                                    display_result_with_image("Correct!", question['image'], use_lightning=True)
                                else:
                                    display_result_with_image("Correct!", question['image'])
                            else:
                                display_result_with_image(f"Sorry, the correct answer is {correct_answer}")
                            question_complete = True

            pygame.time.Clock().tick(60)

    # Final score and performance
    lesson_end_time = time.time()
    average_time = round(sum(completion_times) / len(completion_times), 1) if completion_times else 0
    add_session_lesson(session_id, color_lesson_id, lesson_start_time, lesson_end_time, total_questions, correct_answers)

    # Display the final score
    screen.fill(screen_color)
    draw_text(f"Final Score: {correct_answers}/{total_questions}", font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)
        set_student_progress(session_id, 'Japanese Colors')  # Level up on perfect score

    draw_and_wait_continue_button()

    if correct_answers == total_questions:
        bonus_game_fat_tuna()  # Trigger bonus game for perfect score

    # Return the results of the quiz
    return total_questions, correct_answers, average_time







def display_color_quiz(screen, kanji, furigana, options):
    """
    Draws the kanji, furigana, and multiple-choice options on the screen.
    Returns the rects for kanji, furigana, and the option rects for handling clicks.
    """
    screen.fill(NAVY_BLUE)

    # Draw the Kanji on the screen
    kanji_rect = draw_text(
        kanji,
        j_font,  # Assuming you have a separate kanji font loaded
        WHITE,
        x=WIDTH // 2,
        y=HEIGHT // 3,
        center=True,
        enable_shadow=True,
        shadow_color=BLACK,
        return_rect=True
    )

    # Draw the Furigana above the Kanji
    furigana_rect = draw_text(
        furigana,
        j_font,
        WHITE,
        x=WIDTH // 2,
        y=HEIGHT // 5,
        center=True,
        enable_shadow=True,
        shadow_color=BLACK,
        return_rect=True
    )

    # Draw the multiple-choice options
    option_rects = []
    y_pos = HEIGHT * 0.6
    answer_buffer = HEIGHT * 0.1

    for i, option in enumerate(options):
        option_rect = draw_text(
            option,
            font,  # Use your default or specific font here
            WHITE,
            x=WIDTH // 2,
            y=y_pos + i * answer_buffer,
            center=True,
            enable_shadow=True,
            shadow_color=BLACK,
            return_rect=True
        )
        option_rects.append((option_rect, option))

    pygame.display.flip()

    return kanji_rect, furigana_rect, option_rects


def japanese_colors1_quiz(session_id):
    japanese_colors_quiz(session_id, colors1)

def japanese_colors2_quiz(session_id):
    japanese_colors_quiz(session_id, colors2)

def japanese_colors3_quiz(session_id):
    japanese_colors_quiz(session_id, colors3)

def japanese_colors4_quiz(session_id):
    japanese_colors_quiz(session_id, colors4)

def japanese_colors5_quiz(session_id):
    japanese_colors_quiz(session_id, colors5)















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
        # update_positions()

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
        # exit_rect = draw_exit_button()

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
                    # Center the window
                    pygame.display.quit()
                    center_window(current_windowed_resolution[0], current_windowed_resolution[1])
                    screen = pygame.display.set_mode(current_windowed_resolution)
                    WIDTH, HEIGHT = current_windowed_resolution
                    update_positions()

                # Check if "+" button was clicked for resolution
                if resolution_plus_rect and resolution_plus_rect.collidepoint(mouse_pos):
                    current_resolution_index = min(len(AVAILABLE_RESOLUTIONS) - 1, current_resolution_index + 1)
                    current_windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
                    # Center the window
                    pygame.display.quit()
                    center_window(current_windowed_resolution[0], current_windowed_resolution[1])
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
                # check_exit_click(mouse_pos, exit_rect)

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
    fade_text_in_and_out_with_cat("Special thanks to:", "Richard Stallman", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the PyInstaller team", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the Pygame team", font)
    fade_text_in_and_out_with_cat("Pygame is licensed under", "LGPL version 2.1", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the Suno team", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the Blender team", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the Krita team", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the Stable Diffusion team", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the Ubuntu team", font)
    fade_text_in_and_out_with_cat("Special thanks to:", "the ChatGPT team", font)


class Cat:
    """
    A class to represent the player's cat character with jumping, movement, and particle effects.

    Attributes:
    -----------
    image : Surface
        The image representing the cat.
    rect : Rect
        The rectangle enclosing the cat for positioning and collision.
    speed : int
        The speed at which the cat moves horizontally.
    gravity : int
        The gravity applied to the cat during jumps and falls.
    jump_speed : int
        The speed applied to the cat when jumping.
    vertical_speed : int
        The current vertical speed of the cat (used for jumping and falling).
    is_jumping : bool
        Whether the cat is currently in the air.
    can_double_jump : bool
        Whether the cat can perform a double jump.
    facing_left : bool
        Whether the cat is facing left.
    jump_angle : int
        The rotation angle applied to the cat during jumps.
    max_angle : int
        The maximum rotation angle for the cat's jump.
    particles : list
        A list of particle objects emitted during jumps.

    Methods:
    --------
    handle_input():
        Handles player input for moving the cat.
    apply_gravity(platforms=None):
        Applies gravity to the cat and manages platform collisions.
    jump():
        Makes the cat jump and emits particles.
    update(platforms=None):
        Updates the cat's position, handles input, applies gravity, and manages jumping.
    draw(screen):
        Draws the cat and its particles on the provided screen.
    """
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


class Piranha:
    """
    A class to represent a piranha that moves horizontally across the screen.

    Attributes:
    -----------
    image : Surface
        The image representing the piranha.
    rect : Rect
        The rectangle enclosing the piranha, used for positioning and collision detection.
    speed : int
        The speed at which the piranha moves horizontally across the screen.

    Methods:
    --------
    update():
        Updates the piranha's position, reversing its direction when it hits the screen edges.
    draw(screen):
        Draws the piranha on the given Pygame surface.
    """
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
    """
    A class to represent a platform that can move or stay stationary on the screen.

    Attributes:
    -----------
    image : Surface
        The scaled image representing the platform.
    rect : Rect
        The rectangle defining the platform's position and dimensions.

    Methods:
    --------
    update(speed):
        Updates the platform's vertical position based on the given falling speed.
    draw(screen):
        Draws the platform on the given Pygame surface.
    """
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


#################
# Main function #
#################
def main():
    # Load user options first to apply settings like font and resolution
    load_options()
       
    # Check if the database is properly initialized before proceeding
    check_database_initialization()
    
    # Initialize the fonts based on current settings (both English and Japanese)
    global font, j_font  # Declare as global if you want to use these fonts throughout your project
    font, j_font = init_fonts()  # Initialize both English and Japanese fonts
    
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
        elif current_state == "rainbow_numbers":
            current_state = rainbow_numbers()
        elif current_state == "learniverse_explanation":
            current_state = learniverse_explanation()
        elif current_state == "student_select_menu":
            current_state = student_select_menu()
        elif current_state == "session_manager":
            current_state = session_manager()

if __name__ == "__main__":
    main()
