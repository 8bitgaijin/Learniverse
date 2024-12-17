# -*- coding: utf-8 -*-
"""
@author: Alvadore Retro Technology
Learniverse
"""

import colorsys  
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
from typing import Optional, List, Tuple
from unidecode import unidecode
import webbrowser


###################################
### Constants and Configuration ###
###################################

# Our database name
DB_NAME = 'learniverse.db'

# Format to get a human friendly date in the database
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Set the title of the window
pygame.display.set_caption("Learniverse")

# Constants for display and opacity
DISPLAY_TIME = 2000  # Time for text at full opacity (in milliseconds)
FADE_SPEED = 5  # Controls the fade-in and fade-out speed

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
DARK_BLUE = (10, 10, 40)

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

# Constants for monthly streak SFX
# Colors: Brown, Red, and Orange with intermediate shades
LEAF_COLORS = [
    (139, 69, 19),   # Brown
    (160, 82, 45),   # Light Brown
    (205, 92, 92),   # Rosy Brown
    (255, 69, 0),    # Red
    (255, 99, 71),   # Tomato
    (255, 140, 0),   # Dark Orange
    (255, 165, 0),   # Orange
    (255, 185, 15),  # Light Orange
    (218, 165, 32),  # Goldenrod
    (184, 134, 11)   # Dark Goldenrod
]

# Colors: Pink shades for sakura petals
SAKURA_COLORS = [
    (255, 182, 193),  # Light Pink
    (255, 192, 203),  # Pink
    (255, 105, 180),  # Hot Pink
    (250, 128, 114),  # Salmon Pink
]

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

DEFAULT_RESOLUTION = (800, 800)
WINDOWED_RESOLUTIONS = [
    (640, 640), (768, 768), (800, 800), (900, 900), (1000, 1000), (1080, 1080)
]


##################################
# TODO
# CAN I REMOVE THESE TWO SOMEHOW?
REFERENCE_RESOLUTION = (1080, 1080)
BASE_RESOLUTION = (1080, 1080)
##################################


# Japanese data
j_colors1 = {
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
    },
  ]
}

j_colors2 = {
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

j_colors3 = {
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

j_colors4 = {
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

j_colors5 = {
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

j_colors6 = {
  "quiz_title": "Color Sentences 1",
  "questions": [
    {
      "furigana": "あかいねこです",
      "kanji": "赤い猫です",
      "translation": "It is a red cat.",
      "image": "GFX/colors/red.png"
    },
    {
      "furigana": "あおいねこです",
      "kanji": "青い猫です",
      "translation": "It is a blue cat.",
      "image": "GFX/colors/blue.png"
    },
    {
      "furigana": "しろいねこです",
      "kanji": "白い猫です",
      "translation": "It is a white cat.",
      "image": "GFX/colors/white.png"
    },
    {
      "furigana": "くろいねこです",
      "kanji": "黒い猫です",
      "translation": "It is a black cat.",
      "image": "GFX/colors/black.png"
    },
    {
      "furigana": "みどりのねこです",
      "kanji": "緑の猫です",
      "translation": "It is a green cat.",
      "image": "GFX/colors/green.png"
    }
  ]
}

j_colors7 = {
  "quiz_title": "Color Sentences 2",
  "questions": [
    {
      "furigana": "きいろいねこです",
      "kanji": "黄色い猫です",
      "translation": "It is a yellow cat.",
      "image": "GFX/colors/yellow.png"
    },
    {
      "furigana": "ちゃいろいねこです",
      "kanji": "茶色い猫です",
      "translation": "It is a brown cat.",
      "image": "GFX/colors/brown.png"
    },
    {
      "furigana": "むらさきのねこです",
      "kanji": "紫の猫です",
      "translation": "It is a purple cat.",
      "image": "GFX/colors/purple.png"
    },
    {
      "furigana": "はいいろのねこです",
      "kanji": "灰色の猫です",
      "translation": "It is a gray cat.",
      "image": "GFX/colors/gray.png"
    },
    {
      "furigana": "きんいろのねこです",
      "kanji": "金色の猫です",
      "translation": "It is a gold cat.",
      "image": "GFX/colors/gold.png"
    }
  ]
}

j_colors8 = {
  "quiz_title": "Color Sentences 3",
  "questions": [
    {
      "furigana": "だいだいいろのねこです",
      "kanji": "橙色の猫です",
      "translation": "It is an orange cat.",
      "image": "GFX/colors/orange.png"
    },
    {
      "furigana": "ももいろのねこです",
      "kanji": "桃色の猫です",
      "translation": "It is a pink cat.",
      "image": "GFX/colors/pink.png"
    },
    {
      "furigana": "きんいろのねこです",
      "kanji": "金色の猫です",
      "translation": "It is a gold cat.",
      "image": "GFX/colors/gold.png"
    },
    {
      "furigana": "ぎんいろのねこです",
      "kanji": "銀色の猫です",
      "translation": "It is a silver cat.",
      "image": "GFX/colors/silver.png"
    },
    {
      "furigana": "こんいろのねこです",
      "kanji": "紺色の猫です",
      "translation": "It is a navy blue cat.",
      "image": "GFX/colors/navy_blue.png"
    }
  ]
}

j_colors9 = {
  "quiz_title": "Color Sentences 4",
  "questions": [
    {
      "furigana": "みずいろのねこです",
      "kanji": "水色の猫です",
      "translation": "It is a light blue cat.",
      "image": "GFX/colors/light_blue.png"
    },
    {
      "furigana": "しこうのねこです",
      "kanji": "紫紅の猫です",
      "translation": "It is a crimson cat.",
      "image": "GFX/colors/crimson.png"
    },
    {
      "furigana": "きみどりのねこです",
      "kanji": "黄緑の猫です",
      "translation": "It is a yellow-green cat.",
      "image": "GFX/colors/yellow_green.png"
    },
    {
      "furigana": "わかくさいろのねこです",
      "kanji": "若草色の猫です",
      "translation": "It is a light green cat.",
      "image": "GFX/colors/light_green.png"
    },
    {
      "furigana": "あさぎいろのねこです",
      "kanji": "浅葱色の猫です",
      "translation": "It is a light blue-green cat.",
      "image": "GFX/colors/light_blue_green.png"
    }
  ]
}

j_colors10 = {
  "quiz_title": "Color Sentences 5",
  "questions": [
    {
      "furigana": "さくらいろのねこです",
      "kanji": "桜色の猫です",
      "translation": "It is a cherry blossom pink cat.",
      "image": "GFX/colors/cherry_blossom_pink.png"
    },
    {
      "furigana": "れんがいろのねこです",
      "kanji": "煉瓦色の猫です",
      "translation": "It is a brick red cat.",
      "image": "GFX/colors/brick_red.png"
    },
    {
      "furigana": "おうどいろのねこです",
      "kanji": "黄土色の猫です",
      "translation": "It is an ochre cat.",
      "image": "GFX/colors/ochre.png"
    },
    {
      "furigana": "とびいろのねこです",
      "kanji": "鳶色の猫です",
      "translation": "It is a dark reddish-brown cat.",
      "image": "GFX/colors/dark_reddish_brown.png"
    },
    {
      "furigana": "ぶどういろのねこです",
      "kanji": "葡萄色の猫です",
      "translation": "It is a grape-colored cat.",
      "image": "GFX/colors/grape.png"
    }
  ]
}

j_body_parts1 = {
  "quiz_title": "Body Parts 1",
  "questions": [
    {
      "furigana": "みみ",
      "kanji": "耳",
      "translation": "ear",
      "image": "GFX/body_parts/ear.png"
    },
    {
      "furigana": "くち",
      "kanji": "口",
      "translation": "mouth",
      "image": "GFX/body_parts/mouth.png"
    },
    {
      "furigana": "て",
      "kanji": "手",
      "translation": "hand",
      "image": "GFX/body_parts/hand.png"
    },
    {
      "furigana": "あし",
      "kanji": "足",
      "translation": "foot",
      "image": "GFX/body_parts/foot.png"
    },
    {
      "furigana": "め",
      "kanji": "目",
      "translation": "eye",
      "image": "GFX/body_parts/eye.png"
    }
  ]
}

j_body_parts2 = {
  "quiz_title": "Body Parts 2",
  "questions": [
    {
      "furigana": "あたま",
      "kanji": "頭",
      "translation": "head",
      "image": "GFX/body_parts/head.png"
    },
    {
      "furigana": "はな",
      "kanji": "鼻",
      "translation": "nose",
      "image": "GFX/body_parts/nose.png"
    },
    {
      "furigana": "かみ",
      "kanji": "髪",
      "translation": "hair",
      "image": "GFX/body_parts/hair.png"
    },
    {
      "furigana": "かお",
      "kanji": "顔",
      "translation": "face",
      "image": "GFX/body_parts/face.png"
    },
    {
      "furigana": "ゆび",
      "kanji": "指",
      "translation": "finger",
      "image": "GFX/body_parts/finger.png"
    }
  ]
}

j_body_parts3 = {
  "quiz_title": "Body Parts 3",
  "questions": [
    {
      "furigana": "かた",
      "kanji": "肩",
      "translation": "shoulder",
      "image": "GFX/body_parts/shoulder.png"
    },
    {
      "furigana": "ひじ",
      "kanji": "",
      "translation": "elbow",
      "image": "GFX/body_parts/elbow.png"
    },
    {
      "furigana": "ひざ",
      "kanji": "",
      "translation": "knee",
      "image": "GFX/body_parts/knee.png"
    },
    {
      "furigana": "むね",
      "kanji": "胸",
      "translation": "chest",
      "image": "GFX/body_parts/chest.png"
    },
    {
      "furigana": "せなか",
      "kanji": "背中",
      "translation": "back",
      "image": "GFX/body_parts/back.png"
    }
  ]
}

j_body_parts4 = {
  "quiz_title": "Body Parts 4",
  "questions": [
    {
      "furigana": "くび",
      "kanji": "首",
      "translation": "neck",
      "image": "GFX/body_parts/neck.png"
    },
    {
      "furigana": "おなか",
      "kanji": "お腹",
      "translation": "stomach",
      "image": "GFX/body_parts/stomach.png"
    },
    {
      "furigana": "こし",
      "kanji": "腰",
      "translation": "waist",
      "image": "GFX/body_parts/waist.png"
    },
    {
      "furigana": "うで",
      "kanji": "腕",
      "translation": "arm",
      "image": "GFX/body_parts/arm.png"
    },
    {
      "furigana": "あご",
      "kanji": "顔",
      "translation": "chin",
      "image": "GFX/body_parts/chin.png"
    }
  ]
}

j_body_parts5 = {
  "quiz_title": "Body Parts 5",
  "questions": [
    {
      "furigana": "ほほ",
      "kanji": "",
      "translation": "cheek",
      "image": "GFX/body_parts/cheek.png"
    },
    {
      "furigana": "あごひげ",
      "kanji": "",
      "translation": "beard",
      "image": "GFX/body_parts/beard.png"
    },
    {
      "furigana": "まゆげ",
      "kanji": "",
      "translation": "eyebrow",
      "image": "GFX/body_parts/eyebrow.png"
    },
    {
      "furigana": "まつげ",
      "kanji": "",
      "translation": "eyelash",
      "image": "GFX/body_parts/eyelash.png"
    },
    {
      "furigana": "くちびる",
      "kanji": "",
      "translation": "lip",
      "image": "GFX/body_parts/lip.png"
    }
  ]
}

j_adjectives1 = {
  "quiz_title": "Simple Adjectives",
  "questions": [
    {
      "furigana": "おおきい",
      "kanji": "大きい",
      "translation": "large",
      "image": "GFX/adjectives/large.png"
    },
    {
      "furigana": "ちいさい",
      "kanji": "小さい",
      "translation": "small",
      "image": "GFX/adjectives/small.png"
    },
    {
      "furigana": "ながい",
      "kanji": "長い",
      "translation": "long",
      "image": "GFX/adjectives/long.png"
    },
    {
      "furigana": "みじかい",
      "kanji": "短い",
      "translation": "short",
      "image": "GFX/adjectives/short.png"
    },
    {
      "furigana": "はやい",
      "kanji": "速い",
      "translation": "fast",
      "image": "GFX/adjectives/fast.png"
    }
  ]
}

j_animals1 = {
  "quiz_title": "Animals",
  "questions": [
    {
      "kanji": "犬",
      "furigana": "いぬ",
      "translation": "dog",
      "image": "GFX/animals/dog.png"
    },
    {
      "kanji": "猫",
      "furigana": "ねこ",
      "translation": "cat",
      "image": "GFX/animals/cat.png"
    },
    {
      "kanji": "象",
      "furigana": "ぞう",
      "translation": "elephant",
      "image": "GFX/animals/elephant.png"
    },
    {
      "kanji": "魚",
      "furigana": "さかな",
      "translation": "fish",
      "image": "GFX/animals/fish.png"
    },
    {
      "kanji": "鶏",
      "furigana": "にわとり",
      "translation": "chicken",
      "image": "GFX/animals/chicken.png"
    }
  ]
}

j_animals2 = {
  "quiz_title": "Animals 2",
  "questions": [
    {
      "kanji": "馬",
      "furigana": "うま",
      "translation": "horse",
      "image": "GFX/animals/horse.png"
    },
    {
      "kanji": "鳥",
      "furigana": "とり",
      "translation": "bird",
      "image": "GFX/animals/bird.png"
    },
    {
      "kanji": "牛",
      "furigana": "うし",
      "translation": "cow",
      "image": "GFX/animals/cow.png"
    },
    {
      "kanji": "豚",
      "furigana": "ぶた",
      "translation": "pig",
      "image": "GFX/animals/pig.png"
    },
    {
      "kanji": "狐",
      "furigana": "きつね",
      "translation": "fox",
      "image": "GFX/animals/fox.png"
    }
  ]
}

j_animals3 = {
  "quiz_title": "Animals 3",
  "questions": [
    {
      "kanji": "亀",
      "furigana": "かめ",
      "translation": "turtle",
      "image": "GFX/animals/turtle.png"
    },
    {
      "kanji": "狼",
      "furigana": "おおかみ",
      "translation": "wolf",
      "image": "GFX/animals/wolf.png"
    },
    {
      "kanji": "鼠",
      "furigana": "ねずみ",
      "translation": "mouse/rat",
      "image": "GFX/animals/mouse.png"
    },
    {
      "kanji": "蛇",
      "furigana": "へび",
      "translation": "snake",
      "image": "GFX/animals/snake.png"
    },
    {
      "kanji": "鴨",
      "furigana": "かも",
      "translation": "duck",
      "image": "GFX/animals/duck.png"
    }
  ]
}

j_animals4 = {
  "quiz_title": "Animals 4",
  "questions": [
    {
      "kanji": "虎",
      "furigana": "とら",
      "translation": "tiger",
      "image": "GFX/animals/tiger.png"
    },
    {
      "kanji": "豹",
      "furigana": "ひょう",
      "translation": "leopard",
      "image": "GFX/animals/leopard.png"
    },
    {
      "kanji": "キリン",
      "furigana": "きりん",
      "translation": "giraffe",
      "image": "GFX/animals/giraffe.png"
    },
    {
      "kanji": "ラクダ",
      "furigana": "らくだ",
      "translation": "camel",
      "image": "GFX/animals/camel.png"
    },
    {
      "kanji": "パンダ",
      "furigana": "ぱんだ",
      "translation": "panda",
      "image": "GFX/animals/panda.png"
    }
  ]
}

j_animals5 = {
  "quiz_title": "Animals 5",
  "questions": [
    {
      "kanji": "ゴリラ",
      "furigana": "ごりら",
      "translation": "gorilla",
      "image": "GFX/animals/gorilla.png"
    },
    {
      "kanji": "ペンギン",
      "furigana": "ぺんぎん",
      "translation": "penguin",
      "image": "GFX/animals/penguin.png"
    },
    {
      "kanji": "シマウマ",
      "furigana": "しまうま",
      "translation": "zebra",
      "image": "GFX/animals/zebra.png"
    },
    {
      "kanji": "ハリネズミ",
      "furigana": "はりねずみ",
      "translation": "hedgehog",
      "image": "GFX/animals/hedgehog.png"
    },
    {
      "kanji": "イルカ",
      "furigana": "いるか",
      "translation": "dolphin",
      "image": "GFX/animals/dolphin.png"
    }
  ]
}

j_animals6 = {
  "quiz_title": "Animals 6",
  "questions": [
    {
      "kanji": "獅子",
      "furigana": "ライオン",
      "translation": "lion",
      "image": "GFX/animals/lion.png"
    },
    {
      "kanji": "烏",
      "furigana": "からす",
      "translation": "crow",
      "image": "GFX/animals/crow.png"
    },
    {
      "kanji": "鯨",
      "furigana": "くじら",
      "translation": "whale",
      "image": "GFX/animals/whale.png"
    },
    {
      "kanji": "烏賊",
      "furigana": "イカ",
      "translation": "squid",
      "image": "GFX/animals/squid.png"
    },
    {
      "kanji": "蛸",
      "furigana": "タコ",
      "translation": "octopus",
      "image": "GFX/animals/octopus.png"
    }
  ]
}

j_animals7 = {
  "quiz_title": "Animals 7",
  "questions": [
    {
      "kanji": "羊",
      "furigana": "ひつじ",
      "translation": "sheep",
      "image": "GFX/animals/sheep.png"
    },
    {
      "kanji": "鹿",
      "furigana": "しか",
      "translation": "deer",
      "image": "GFX/animals/deer.png"
    },
    {
      "kanji": "熊",
      "furigana": "くま",
      "translation": "bear",
      "image": "GFX/animals/bear.png"
    },
    {
      "kanji": "猿",
      "furigana": "さる",
      "translation": "monkey",
      "image": "GFX/animals/monkey.png"
    },
    {
      "kanji": "兎",
      "furigana": "うさぎ",
      "translation": "rabbit",
      "image": "GFX/animals/rabbit.png"
    }
  ]
}

j_animals8 = {
  "quiz_title": "Animals 8",
  "questions": [
    {
      "kanji": "カバ",
      "furigana": "かば",
      "translation": "hippopotamus",
      "image": "GFX/animals/hippopotamus.png"
    },
    {
      "kanji": "ワニ",
      "furigana": "わに",
      "translation": "crocodile",
      "image": "GFX/animals/crocodile.png"
    },
    {
      "kanji": "鷹",
      "furigana": "たか",
      "translation": "hawk",
      "image": "GFX/animals/hawk.png"
    },
    {
      "kanji": "フクロウ",
      "furigana": "ふくろう",
      "translation": "owl",
      "image": "GFX/animals/owl.png"
    },
    {
      "kanji": "コアラ",
      "furigana": "こあら",
      "translation": "koala",
      "image": "GFX/animals/koala.png"
    }
  ]
}

j_animals9 = {
  "quiz_title": "Animals 9",
  "questions": [
    {
      "kanji": "リス",
      "furigana": "りす",
      "translation": "squirrel",
      "image": "GFX/animals/squirrel.png"
    },
    {
      "kanji": "ハムスター",
      "furigana": "はむすたー",
      "translation": "hamster",
      "image": "GFX/animals/hamster.png"
    },
    {
      "kanji": "蟻",
      "furigana": "あり",
      "translation": "ant",
      "image": "GFX/animals/ant.png"
    },
    {
      "kanji": "蜂",
      "furigana": "はち",
      "translation": "bee",
      "image": "GFX/animals/bee.png"
    },
    {
      "kanji": "蛙",
      "furigana": "かえる",
      "translation": "frog",
      "image": "GFX/animals/frog.png"
    }
  ]
}

j_family1 = {
  "quiz_title": "Family Relations",
  "questions": [
    {
      "furigana": "はは",
      "kanji": "母",
      "translation": "my mother",
      "image": "GFX/family/mother.png"
    },
    {
      "furigana": "ちち",
      "kanji": "父",
      "translation": "my father",
      "image": "GFX/family/father.png"
    },
    {
      "furigana": "あに",
      "kanji": "兄",
      "translation": "my older brother",
      "image": "GFX/family/older_brother.png"
    },
    {
      "furigana": "おとうと",
      "kanji": "弟",
      "translation": "my younger brother",
      "image": "GFX/family/younger_brother.png"
    },
    {
      "furigana": "あね",
      "kanji": "姉",
      "translation": "my older sister",
      "image": "GFX/family/older_sister.png"
    },
    {
      "furigana": "いもうと",
      "kanji": "妹",
      "translation": "my younger sister",
      "image": "GFX/family/younger_sister.png"
    }
  ]
}

j_family2 = {
  "quiz_title": "Family Relations - Out-Group",
  "questions": [
    {
      "furigana": "おかあさん",
      "kanji": "お母さん",
      "translation": "your mother",
      "image": "GFX/family/mother.png"
    },
    {
      "furigana": "おとうさん",
      "kanji": "お父さん",
      "translation": "your father",
      "image": "GFX/family/father.png"
    },
    {
      "furigana": "おにいさん",
      "kanji": "お兄さん",
      "translation": "your older brother",
      "image": "GFX/family/older_brother.png"
    },
    {
      "furigana": "おとうとさん",
      "kanji": "弟さん",
      "translation": "your younger brother",
      "image": "GFX/family/younger_brother.png"
    },
    {
      "furigana": "おねえさん",
      "kanji": "お姉さん",
      "translation": "your older sister",
      "image": "GFX/family/older_sister.png"
    },
    {
      "furigana": "いもうとさん",
      "kanji": "妹さん",
      "translation": "your younger sister",
      "image": "GFX/family/younger_sister.png"
    }
  ]
}

j_family3 = {
  "quiz_title": "Family Relations 2",
  "questions": [
    {
      "furigana": "そふ",
      "kanji": "祖父",
      "translation": "my grandfather",
      "image": "GFX/family/grandfather.png"
    },
    {
      "furigana": "そぼ",
      "kanji": "祖母",
      "translation": "my grandmother",
      "image": "GFX/family/grandmother.png"
    },
    {
      "furigana": "おじ",
      "kanji": "叔父",
      "translation": "my uncle",
      "image": "GFX/family/uncle.png"
    },
    {
      "furigana": "おば",
      "kanji": "叔母",
      "translation": "my aunt",
      "image": "GFX/family/aunt.png"
    },
    {
      "furigana": "いとこ",
      "kanji": "従兄弟",
      "translation": "my cousin",
      "image": "GFX/family/cousin.png"
    }
  ]
}

j_family4 = {
  "quiz_title": "Family Relationships 2 - Outgroup",
  "questions": [
    {
      "furigana": "おじいさん",
      "kanji": "お祖父さん",
      "translation": "your grandfather",
      "image": "GFX/family/grandfather.png"
    },
    {
      "furigana": "おばあさん",
      "kanji": "お祖母さん",
      "translation": "your grandmother",
      "image": "GFX/family/grandmother.png"
    },
    {
      "furigana": "おじさん",
      "kanji": "叔父さん",
      "translation": "your uncle",
      "image": "GFX/family/uncle.png"
    },
    {
      "furigana": "おばさん",
      "kanji": "叔母さん",
      "translation": "your aunt",
      "image": "GFX/family/aunt.png"
    },
    {
      "furigana": "いとこさん",
      "kanji": "従兄弟さん",
      "translation": "your cousin",
      "image": "GFX/family/cousin.png"
    }
  ]
}

# Note: family relation 3 out group is the same as in group
j_family5 = {
  "quiz_title": "Family Relations 3",
  "questions": [
    {
      "furigana": "そうそふ",
      "kanji": "曽祖父",
      "translation": "my great-grandfather",
      "image": "GFX/family/great_grandfather.png"
    },
    {
      "furigana": "そうそぼ",
      "kanji": "曽祖母",
      "translation": "my great-grandmother",
      "image": "GFX/family/great_grandmother.png"
    },
    {
      "furigana": "ぎふ",
      "kanji": "義父",
      "translation": "my father-in-law",
      "image": "GFX/family/father_in_law.png"
    },
    {
      "furigana": "ぎぼ",
      "kanji": "義母",
      "translation": "my mother-in-law",
      "image": "GFX/family/mother_in_law.png"
    },
    {
      "furigana": "ぎけい",
      "kanji": "義兄",
      "translation": "my older brother-in-law",
      "image": "GFX/family/older_brother_in_law.png"
    },
    {
      "furigana": "ぎてい",
      "kanji": "義弟",
      "translation": "my younger brother-in-law",
      "image": "GFX/family/younger_brother_in_law.png"
    }
  ]
}

j_family6 = {
  "quiz_title": "Family Relations - 4",
  "questions": [
    {
      "furigana": "ぎし",
      "kanji": "義姉",
      "translation": "my older sister-in-law",
      "image": "GFX/family/older_sister_in_law.png"
    },
    {
      "furigana": "ぎまい",
      "kanji": "義妹",
      "translation": "my younger sister-in-law",
      "image": "GFX/family/younger_sister_in_law.png"
    },
    {
      "furigana": "おい",
      "kanji": "甥",
      "translation": "my nephew",
      "image": "GFX/family/nephew.png"
    },
    {
      "furigana": "めい",
      "kanji": "姪",
      "translation": "my niece",
      "image": "GFX/family/niece.png"
    },
    {
      "furigana": "おっと",
      "kanji": "夫",
      "translation": "my husband",
      "image": "GFX/family/husband.png"
    },
    {
      "furigana": "つま",
      "kanji": "妻",
      "translation": "my wife",
      "image": "GFX/family/wife.png"
    }
  ]
}

j_family7 = {
  "quiz_title": "Family Relations 4 - Out Group",
  "questions": [
    {
      "furigana": "おねえさん",
      "kanji": "お姉さん",
      "translation": "your older sister-in-law",
      "image": "GFX/family/older_sister_in_law.png"
    },
    {
      "furigana": "いもうとさん",
      "kanji": "妹さん",
      "translation": "your younger sister-in-law",
      "image": "GFX/family/younger_sister_in_law.png"
    },
    {
      "furigana": "おいごさん",
      "kanji": "甥御さん",
      "translation": "your nephew",
      "image": "GFX/family/nephew.png"
    },
    {
      "furigana": "めいごさん",
      "kanji": "姪御さん",
      "translation": "your niece",
      "image": "GFX/family/niece.png"
    },
    {
      "furigana": "ごしゅじん",
      "kanji": "ご主人",
      "translation": "your husband",
      "image": "GFX/family/husband.png"
    },
    {
      "furigana": "おくさん",
      "kanji": "奥さん",
      "translation": "your wife",
      "image": "GFX/family/wife.png"
    }
  ]
}

j_fruits1 = {
  "quiz_title": "Fruits",
  "questions": [
    {
      "kanji": "りんご",
      "furigana": "りんご",
      "translation": "apple",
      "image": "GFX/fruits/apple.png"
    },
    {
      "kanji": "みかん",
      "furigana": "みかん",
      "translation": "mandarin orange",
      "image": "GFX/fruits/mandarin_orange.png"
    },
    {
      "kanji": "ぶどう",
      "furigana": "ぶどう",
      "translation": "grape",
      "image": "GFX/fruits/grape.png"
    },
    {
      "kanji": "もも",
      "furigana": "もも",
      "translation": "peach",
      "image": "GFX/fruits/peach.png"
    },
    {
      "kanji": "柿",
      "furigana": "かき",
      "translation": "persimmon",
      "image": "GFX/fruits/persimmon.png"
    }
  ]
}

j_fruits2 = {
  "quiz_title": "Fruits 2",
  "questions": [
    {
      "kanji": "梨",
      "furigana": "なし",
      "translation": "pear",
      "image": "GFX/fruits/pear.png"
    },
    {
      "kanji": "スイカ",
      "furigana": "スイカ",
      "translation": "watermelon",
      "image": "GFX/fruits/watermelon.png"
    },
    {
      "kanji": "メロン",
      "furigana": "メロン",
      "translation": "melon",
      "image": "GFX/fruits/melon.png"
    },
    {
      "kanji": "バナナ",
      "furigana": "バナナ",
      "translation": "banana",
      "image": "GFX/fruits/banana.png"
    },
    {
      "kanji": "苺",
      "furigana": "いちご",
      "translation": "strawberry",
      "image": "GFX/fruits/strawberry.png"
    }
  ]
}

j_fruits3 = {
  "quiz_title": "Fruits 3",
  "questions": [
    {
      "kanji": "キウイ",
      "furigana": "キウイ",
      "translation": "kiwi",
      "image": "GFX/fruits/kiwi.png"
    },
    {
      "kanji": "パイナップル",
      "furigana": "パイナップル",
      "translation": "pineapple",
      "image": "GFX/fruits/pineapple.png"
    },
    {
      "kanji": "さくらんぼ",
      "furigana": "さくらんぼ",
      "translation": "cherry",
      "image": "GFX/fruits/cherry.png"
    },
    {
      "kanji": "柚子",
      "furigana": "ゆず",
      "translation": "yuzu",
      "image": "GFX/fruits/yuzu.png"
    },
    {
      "kanji": "ブルーベリー",
      "furigana": "ブルーベリー",
      "translation": "blueberry",
      "image": "GFX/fruits/blueberry.png"
    }
  ]
}

j_fruits4 = {
  "quiz_title": "Fruits 4",
  "questions": [
    {
      "kanji": "ライチ",
      "furigana": "ライチ",
      "translation": "lychee",
      "image": "GFX/fruits/lychee.png"
    },
    {
      "kanji": "アンズ",
      "furigana": "アンズ",
      "translation": "apricot",
      "image": "GFX/fruits/apricot.png"
    },
    {
      "kanji": "梅",
      "furigana": "うめ",
      "translation": "plum",
      "image": "GFX/fruits/plum.png"
    },
    {
      "kanji": "グレープフルーツ",
      "furigana": "グレープフルーツ",
      "translation": "grapefruit",
      "image": "GFX/fruits/grapefruit.png"
    },
    {
      "kanji": "ドラゴンフルーツ",
      "furigana": "ドラゴンフルーツ",
      "translation": "dragon fruit",
      "image": "GFX/fruits/dragon_fruit.png"
    }
  ]
}

j_fruits5 = {
  "quiz_title": "Fruits 5",
  "questions": [
    {
      "kanji": "パッションフルーツ",
      "furigana": "パッションフルーツ",
      "translation": "passion fruit",
      "image": "GFX/fruits/passion_fruit.png"
    },
    {
      "kanji": "いちじく",
      "furigana": "いちじく",
      "translation": "fig",
      "image": "GFX/fruits/fig.png"
    },
    {
      "kanji": "ザクロ",
      "furigana": "ザクロ",
      "translation": "pomegranate",
      "image": "GFX/fruits/pomegranate.png"
    },
    {
      "kanji": "びわ",
      "furigana": "びわ",
      "translation": "loquat",
      "image": "GFX/fruits/loquat.png"
    },
    {
      "kanji": "マンゴー",
      "furigana": "マンゴー",
      "translation": "mango",
      "image": "GFX/fruits/mango.png"
    }
  ]
}

j_greetings1 = {
  "quiz_title": "Greetings",
  "questions": [
    {
      "kanji": "お早う",
      "furigana": "おはよう",
      "translation": "Good morning",
      "image": ""
    },
    {
      "kanji": "今日は",
      "furigana": "こんにちは",
      "translation": "Good day",
      "image": ""
    },
    {
      "kanji": "今晩は",
      "furigana": "こんばんは",
      "translation": "Good evening",
      "image": ""
    },
    {
      "kanji": "お休み",
      "furigana": "おやすみ",
      "translation": "Good night",
      "image": ""
    },
    {
      "kanji": "頂きます",
      "furigana": "いただきます",
      "translation": "I humbly receive",
      "image": ""
    }
  ]
}

j_greetings2 = {
  "quiz_title": "Greetings 2",
  "questions": [
    {
      "kanji": "有難う",
      "furigana": "ありがとう",
      "translation": "Thank you",
      "image": ""
    },
    {
      "kanji": "さようなら",
      "furigana": "さようなら",
      "translation": "Goodbye",
      "image": ""
    },
    {
      "kanji": "お疲れ様",
      "furigana": "おつかれさま",
      "translation": "Thank you for your hard work",
      "image": ""
    },
    {
      "kanji": "行ってきます",
      "furigana": "いってきます",
      "translation": "I'm off (and will return)",
      "image": ""
    },
    {
      "kanji": "行ってらっしゃい",
      "furigana": "いってらっしゃい",
      "translation": "Please go and come back",
      "image": ""
    }
  ]
}

j_greetings3 = {
  "quiz_title": "Greetings 3",
  "questions": [
    {
      "kanji": "ただいま",
      "furigana": "ただいま",
      "translation": "I'm home",
      "image": ""
    },
    {
      "kanji": "お帰り",
      "furigana": "おかえり",
      "translation": "Welcome back",
      "image": ""
    },
    {
      "kanji": "ご馳走様",
      "furigana": "ごちそうさま",
      "translation": "Thank you for the meal (after eating)",
      "image": ""
    },
    {
      "kanji": "よろしくお願いします",
      "furigana": "よろしくおねがいします",
      "translation": "Please take care of this / Nice to meet you",
      "image": ""
    },
    {
      "kanji": "お元気ですか",
      "furigana": "おげんきですか",
      "translation": "How are you?",
      "image": ""
    }
  ]
}

j_one_piece1 = {
  "quiz_title": "One Piece",
  "questions": [
    {
      "furigana": "かいぞく",
      "kanji": "海賊",
      "translation": "pirate",
      "image": "GFX/one_piece/pirate.png"
    },
    {
      "furigana": "ふね",
      "kanji": "船",
      "translation": "ship",
      "image": "GFX/one_piece/ship.png"
    },
    {
      "furigana": "うみ",
      "kanji": "海",
      "translation": "ocean",
      "image": "GFX/one_piece/ocean.png"
    },
    {
      "furigana": "しま",
      "kanji": "島",
      "translation": "island",
      "image": "GFX/one_piece/island.png"
    },
    {
      "furigana": "ちず",
      "kanji": "地図",
      "translation": "map",
      "image": "GFX/one_piece/map.png"
    }
  ]
}

j_one_piece2 = {
  "quiz_title": "One Piece 2",
  "questions": [
    {
      "furigana": "たから",
      "kanji": "宝",
      "translation": "treasure",
      "image": "GFX/one_piece/treasure.png"
    },
    {
      "furigana": "ぼうけん",
      "kanji": "冒険",
      "translation": "adventure",
      "image": "GFX/one_piece/adventure.png"
    },
    {
      "furigana": "けん",
      "kanji": "剣",
      "translation": "sword",
      "image": "GFX/one_piece/sword.png"
    },
    {
      "furigana": "おれ",
      "kanji": "俺",
      "translation": "I/me (casual/rude)",
      "image": "GFX/one_piece/ore.png"
    },
    {
      "furigana": "まったく",
      "kanji": "全く",
      "translation": "jeez",
      "image": "GFX/one_piece/mattaku.png"
    }
  ]
}

j_one_piece3 = {
  "quiz_title": "One Piece 3",
  "questions": [
    {
      "furigana": "せんちょう",
      "kanji": "船長",
      "translation": "captain",
      "image": "GFX/one_piece/captain.png"
    },
    {
      "furigana": "のりくみいん",
      "kanji": "乗組員",
      "translation": "crew",
      "image": "GFX/one_piece/crew.png"
    },
    {
      "furigana": "なかま",
      "kanji": "仲間",
      "translation": "friend/companion",
      "image": "GFX/one_piece/friend.png"
    },
    {
      "furigana": "かいぐん",
      "kanji": "海軍",
      "translation": "navy",
      "image": "GFX/one_piece/navy.png"
    },
    {
      "furigana": "あくまのみ",
      "kanji": "悪魔の実",
      "translation": "Devil Fruit",
      "image": "GFX/one_piece/devil_fruit.png"
    }
  ]
}

j_one_piece4 = {
  "quiz_title": "One Piece 4",
  "questions": [
    {
      "furigana": "せんい",
      "kanji": "船医",
      "translation": "ship doctor",
      "image": "GFX/one_piece/ship_doctor.png"
    },
    {
      "furigana": "けんし",
      "kanji": "剣士",
      "translation": "swordsman",
      "image": "GFX/one_piece/swordsman.png"
    },
    {
      "furigana": "かいぞくおう",
      "kanji": "海賊王",
      "translation": "Pirate King",
      "image": "GFX/one_piece/pirate_king.png"
    },
    {
      "furigana": "ぼうけんしゃ",
      "kanji": "冒険者",
      "translation": "adventurer",
      "image": "GFX/one_piece/adventurer.png"
    },
    {
      "furigana": "たからのちず",
      "kanji": "宝の地図",
      "translation": "treasure map",
      "image": "GFX/one_piece/treasure_map.png"
    }
  ]
}

j_self_introduction1 = {
  "quiz_title": "Self-Introduction Vocabulary",
  "questions": [
    {
      "kanji": "私",
      "furigana": "わたし",
      "translation": "I (formal/polite)",
      "image": ""
    },
    {
      "kanji": "の",
      "furigana": "の",
      "translation": "possessive particle",
      "image": ""
    },
    {
      "kanji": "名前",
      "furigana": "なまえ",
      "translation": "name",
      "image": ""
    },
    {
      "kanji": "は",
      "furigana": "は",
      "translation": "topic marker particle",
      "image": ""
    },
    {
      "kanji": "です",
      "furigana": "です",
      "translation": "is/are",
      "image": ""
    },
    {
      "kanji": "から",
      "furigana": "から",
      "translation": "from",
      "image": ""
    }
  ]
}

j_self_introduction2 = {
  "quiz_title": "Self-Introduction Vocabulary",
  "questions": [
    {
      "kanji": "来ました",
      "furigana": "きました",
      "translation": "came (from)",
      "image": ""
    },
    {
      "kanji": "歳",
      "furigana": "さい",
      "translation": "years old",
      "image": ""
    },
    {
      "kanji": "趣味",
      "furigana": "しゅみ",
      "translation": "hobby",
      "image": ""
    },
    {
      "kanji": "どうぞ",
      "furigana": "どうぞ",
      "translation": "please",
      "image": ""
    },
    {
      "kanji": "よろしく",
      "furigana": "よろしく",
      "translation": "well",
      "image": ""
    },
    {
      "kanji": "お願いします",
      "furigana": "おねがいします",
      "translation": "please (polite request)",
      "image": ""
    }
  ]
}

j_self_introduction3 = {
  "quiz_title": "Self-Introduction",
  "questions": [
    {
      "kanji": "私の名前は___です",
      "furigana": "わたしのなまえは___です",
      "translation": "My name is ___",
      "image": ""
    },
    {
      "kanji": "___から来ました",
      "furigana": "___からきました",
      "translation": "I am from ___",
      "image": ""
    },
    {
      "kanji": "___歳です",
      "furigana": "___さいです",
      "translation": "I am ___ years old",
      "image": ""
    },
    {
      "kanji": "趣味は___です",
      "furigana": "しゅみは___です",
      "translation": "My hobby is ___",
      "image": ""
    },
    {
      "kanji": "どうぞよろしくお願いします",
      "furigana": "どうぞよろしくおねがいします",
      "translation": "Please take care of me / Nice to meet you",
      "image": ""
    }
  ]
}

j_self_introduction4 = {
  "quiz_title": "Self-Introduction 2 Vocabulary",
  "questions": [
    {
      "kanji": "住んでいます",
      "furigana": "すんでいます",
      "translation": "live (currently living)",
      "image": ""
    },
    {
      "kanji": "に",
      "furigana": "に",
      "translation": "location particle (in, at)",
      "image": ""
    },
    {
      "kanji": "で",
      "furigana": "で",
      "translation": "location particle (at, in; used for actions)",
      "image": ""
    },
    {
      "kanji": "働いています",
      "furigana": "はたらいています",
      "translation": "working (currently working)",
      "image": ""
    },
    {
      "kanji": "勉強しています",
      "furigana": "べんきょうしています",
      "translation": "studying (currently studying)",
      "image": ""
    }
  ]
}

j_self_introduction5 = {
  "quiz_title": "Self-Introduction 2 Vocabulary",
  "questions": [
    {
      "kanji": "家族",
      "furigana": "かぞく",
      "translation": "family",
      "image": ""
    },
    {
      "kanji": "人",
      "furigana": "にん",
      "translation": "people (counter for people)",
      "image": ""
    },
    {
      "kanji": "好きな",
      "furigana": "すきな",
      "translation": "favorite, liked",
      "image": ""
    },
    {
      "kanji": "食べ物",
      "furigana": "たべもの",
      "translation": "food",
      "image": ""
    }
  ]
}

j_self_introduction6 = {
  "quiz_title": "Self-Introduction 2",
  "questions": [
    {
      "kanji": "___に住んでいます",
      "furigana": "___にすんでいます",
      "translation": "I live in ___",
      "image": ""
    },
    {
      "kanji": "___で働いています",
      "furigana": "___ではたらいています",
      "translation": "I work at ___",
      "image": ""
    },
    {
      "kanji": "___を勉強しています",
      "furigana": "___をべんきょうしています",
      "translation": "I am studying ___",
      "image": ""
    },
    {
      "kanji": "家族は___人です",
      "furigana": "かぞくは___にんです",
      "translation": "There are ___ people in my family",
      "image": ""
    },
    {
      "kanji": "好きな食べ物は___です",
      "furigana": "すきなたべものは___です",
      "translation": "My favorite food is ___",
      "image": ""
    }
  ]
}

j_nouns1 = {
  "quiz_title": "Simple Nouns",
  "questions": [
    {
      "furigana": "やま",
      "kanji": "山",
      "translation": "mountain",
      "image": "GFX/nouns/mountain.png"
    },
    {
      "furigana": "かわ",
      "kanji": "川",
      "translation": "river",
      "image": "GFX/nouns/river.png"
    },
    {
      "furigana": "ひ",
      "kanji": "火",
      "translation": "fire",
      "image": "GFX/nouns/fire.png"
    },
    {
      "furigana": "いぬ",
      "kanji": "犬",
      "translation": "dog",
      "image": "GFX/nouns/dog.png"
    },
    {
      "furigana": "ひと",
      "kanji": "人",
      "translation": "person",
      "image": "GFX/nouns/person.png"
    }
  ]
}

j_nouns2 = {
  "quiz_title": "Simple Nouns - Part 2",
  "questions": [
    {
      "furigana": "いと",
      "kanji": "糸",
      "translation": "thread",
      "image": "GFX/nouns/thread.png"
    },
    {
      "furigana": "いし",
      "kanji": "石",
      "translation": "stone",
      "image": "GFX/nouns/stone.png"
    },
    {
      "furigana": "たけ",
      "kanji": "竹",
      "translation": "bamboo",
      "image": "GFX/nouns/bamboo.png"
    },
    {
      "furigana": "かい",
      "kanji": "貝",
      "translation": "shellfish",
      "image": "GFX/nouns/shellfish.png"
    },
    {
      "furigana": "くるま",
      "kanji": "車",
      "translation": "vehicle",
      "image": "GFX/nouns/vehicle.png"
    }
  ]
}

j_nouns3 = {
  "quiz_title": "Simple Nouns - Part 3",
  "questions": [
    {
      "furigana": "きん",
      "kanji": "金",
      "translation": "gold",
      "image": "GFX/nouns/gold_money.png"
    },
    {
      "furigana": "あめ",
      "kanji": "雨",
      "translation": "rain",
      "image": "GFX/nouns/rain.png"
    },
    {
      "furigana": "つき",
      "kanji": "月",
      "translation": "moon",
      "image": "GFX/nouns/moon.png"
    },
    {
      "furigana": "ひ",
      "kanji": "日",
      "translation": "sun",
      "image": "GFX/nouns/sun.png"
    },
    {
      "furigana": "みず",
      "kanji": "水",
      "translation": "water",
      "image": "GFX/nouns/water.png"
    },
    {
      "furigana": "つち",
      "kanji": "土",
      "translation": "earth",
      "image": "GFX/nouns/earth.png"
    }
  ]
}

j_nouns4 = {
  "quiz_title": "Simple Nouns 4",
  "questions": [
    {
      "furigana": "き",
      "kanji": "木",
      "translation": "tree",
      "image": "GFX/nouns/tree.png"
    },
    {
      "furigana": "た",
      "kanji": "田",
      "translation": "rice field",
      "image": "GFX/nouns/rice_field.png"
    },
    {
      "furigana": "はな",
      "kanji": "花",
      "translation": "flower",
      "image": "GFX/nouns/flower.png"
    },
    {
      "furigana": "むし",
      "kanji": "虫",
      "translation": "insect",
      "image": "GFX/nouns/insect.png"
    },
    {
      "furigana": "こ",
      "kanji": "子",
      "translation": "child",
      "image": "GFX/nouns/child.png"
    }
  ]
}

j_time1 = {
  "quiz_title": "Time 1",
  "questions": [
    {
      "furigana": "ことし",
      "kanji": "今年",
      "translation": "this year",
      "image": ""
    },
    {
      "furigana": "ねん",
      "kanji": "年",
      "translation": "year",
      "image": ""
    },
    {
      "furigana": "こんげつ",
      "kanji": "今月",
      "translation": "this month",
      "image": ""
    },
    {
      "furigana": "きょう",
      "kanji": "今日",
      "translation": "today",
      "image": ""
    },
    {
      "furigana": "じ",
      "kanji": "時",
      "translation": "hour",
      "image": ""
    },
    {
      "furigana": "ふん",
      "kanji": "分",
      "translation": "minute",
      "image": ""
    },
    {
      "furigana": "ごぜん",
      "kanji": "午前",
      "translation": "A.M.",
      "image": ""
    }
  ]
}

j_time2 = {
  "quiz_title": "Time 2",
  "questions": [
    {
      "furigana": "こんしゅう",
      "kanji": "今週",
      "translation": "this week",
      "image": ""
    },
    {
      "furigana": "せんしゅう",
      "kanji": "先週",
      "translation": "last week",
      "image": ""
    },
    {
      "furigana": "らいしゅう",
      "kanji": "来週",
      "translation": "next week",
      "image": ""
    },
    {
      "furigana": "せんげつ",
      "kanji": "先月",
      "translation": "last month",
      "image": ""
    },
    {
      "furigana": "らいげつ",
      "kanji": "来月",
      "translation": "next month",
      "image": ""
    }
  ]
}

j_time3 = {
  "quiz_title": "Time 3",
  "questions": [
    {
      "furigana": "きのう",
      "kanji": "昨日",
      "translation": "yesterday",
      "image": ""
    },
    {
      "furigana": "あした",
      "kanji": "明日",
      "translation": "tomorrow",
      "image": ""
    },
    {
      "furigana": "つき",
      "kanji": "月",
      "translation": "month",
      "image": ""
    },
    {
      "furigana": "ひ",
      "kanji": "日",
      "translation": "day",
      "image": ""
    },
    {
      "furigana": "ごご",
      "kanji": "午後",
      "translation": "P.M.",
      "image": ""
    }
  ]
}

j_time4 = {
  "quiz_title": "Time 4",
  "questions": [
    {
      "furigana": "あさって",
      "kanji": "明後日",
      "translation": "the day after tomorrow",
      "image": ""
    },
    {
      "furigana": "おととい",
      "kanji": "一昨日",
      "translation": "the day before yesterday",
      "image": ""
    },
    {
      "furigana": "まいにち",
      "kanji": "毎日",
      "translation": "every day",
      "image": ""
    },
    {
      "furigana": "まいしゅう",
      "kanji": "毎週",
      "translation": "every week",
      "image": ""
    },
    {
      "furigana": "まいつき",
      "kanji": "毎月",
      "translation": "every month",
      "image": ""
    },
    {
      "furigana": "まいとし",
      "kanji": "毎年",
      "translation": "every year",
      "image": ""
    }
  ]
}

j_time5 = {
  "quiz_title": "Time 5",
  "questions": [
    {
      "furigana": "しあさって",
      "kanji": "明明後日",
      "translation": "two days after tomorrow",
      "image": ""
    },
    {
      "furigana": "さきおととい",
      "kanji": "一昨昨日",
      "translation": "three days ago",
      "image": ""
    },
    {
      "furigana": "せんせんしゅう",
      "kanji": "先々週",
      "translation": "the week before last",
      "image": ""
    },
    {
      "furigana": "さらいしゅう",
      "kanji": "再来週",
      "translation": "the week after next",
      "image": ""
    }
  ]
}

j_time6 = {
  "quiz_title": "Time 6",
  "questions": [
    {
      "furigana": "とき",
      "kanji": "時",
      "translation": "time, moment, occasion",
      "image": ""
    },
    {
      "furigana": "じだい",
      "kanji": "時代",
      "translation": "era, period",
      "image": ""
    },
    {
      "furigana": "きかん",
      "kanji": "期間",
      "translation": "period, term, interval",
      "image": ""
    },
    {
      "furigana": "きげん",
      "kanji": "期限",
      "translation": "deadline, time limit",
      "image": ""
    },
    {
      "furigana": "きゅうじつ",
      "kanji": "休日",
      "translation": "holiday, day off",
      "image": ""
    }
  ]
}

j_time7 = {
  "quiz_title": "Time 7",
  "questions": [
    {
      "furigana": "しゅん",
      "kanji": "瞬",
      "translation": "moment",
      "image": ""
    },
    {
      "furigana": "しゅんかん",
      "kanji": "瞬間",
      "translation": "instant",
      "image": ""
    },
    {
      "furigana": "しゅんじ",
      "kanji": "瞬時",
      "translation": "immediate, in an instant",
      "image": ""
    },
    {
      "furigana": "しゅんかんてき",
      "kanji": "瞬間的",
      "translation": "momentary",
      "image": ""
    }
  ]
}

j_vegtables1 = {
  "quiz_title": "Vegetables",
  "questions": [
    {
      "kanji": "大根",
      "furigana": "だいこん",
      "translation": "daikon radish",
      "image": "GFX/vegetables/daikon.png"
    },
    {
      "kanji": "人参",
      "furigana": "にんじん",
      "translation": "carrot",
      "image": "GFX/vegetables/carrot.png"
    },
    {
      "kanji": "キャベツ",
      "furigana": "キャベツ",
      "translation": "cabbage",
      "image": "GFX/vegetables/cabbage.png"
    },
    {
      "kanji": "ほうれん草",
      "furigana": "ほうれんそう",
      "translation": "spinach",
      "image": "GFX/vegetables/spinach.png"
    },
    {
      "kanji": "茄子",
      "furigana": "なす",
      "translation": "eggplant",
      "image": "GFX/vegetables/eggplant.png"
    }
  ]
}

j_vegtables2 = {
  "quiz_title": "Vegetables 2",
  "questions": [
    {
      "kanji": "玉ねぎ",
      "furigana": "たまねぎ",
      "translation": "onion",
      "image": "GFX/vegetables/onion.png"
    },
    {
      "kanji": "じゃがいも",
      "furigana": "じゃがいも",
      "translation": "potato",
      "image": "GFX/vegetables/potato.png"
    },
    {
      "kanji": "ピーマン",
      "furigana": "ピーマン",
      "translation": "green pepper",
      "image": "GFX/vegetables/green_pepper.png"
    },
    {
      "kanji": "白菜",
      "furigana": "はくさい",
      "translation": "napa cabbage",
      "image": "GFX/vegetables/napa_cabbage.png"
    },
    {
      "kanji": "とうもろこし",
      "furigana": "とうもろこし",
      "translation": "corn",
      "image": "GFX/vegetables/corn.png"
    }
  ]
}

j_vegtables3 = {
  "quiz_title": "Vegetables 3",
  "questions": [
    {
      "kanji": "さつまいも",
      "furigana": "さつまいも",
      "translation": "sweet potato",
      "image": "GFX/vegetables/sweet_potato.png"
    },
    {
      "kanji": "しょうが",
      "furigana": "しょうが",
      "translation": "ginger",
      "image": "GFX/vegetables/ginger.png"
    },
    {
      "kanji": "れんこん",
      "furigana": "れんこん",
      "translation": "lotus root",
      "image": "GFX/vegetables/lotus_root.png"
    },
    {
      "kanji": "ネギ",
      "furigana": "ネギ",
      "translation": "green onion",
      "image": "GFX/vegetables/green_onion.png"
    },
    {
      "kanji": "きゅうり",
      "furigana": "きゅうり",
      "translation": "cucumber",
      "image": "GFX/vegetables/cucumber.png"
    }
  ]
}

j_vegtables4 = {
  "quiz_title": "Vegetables 4",
  "questions": [
    {
      "kanji": "ブロッコリー",
      "furigana": "ブロッコリー",
      "translation": "broccoli",
      "image": "GFX/vegetables/broccoli.png"
    },
    {
      "kanji": "カリフラワー",
      "furigana": "カリフラワー",
      "translation": "cauliflower",
      "image": "GFX/vegetables/cauliflower.png"
    },
    {
      "kanji": "アスパラガス",
      "furigana": "アスパラガス",
      "translation": "asparagus",
      "image": "GFX/vegetables/asparagus.png"
    },
    {
      "kanji": "かぼちゃ",
      "furigana": "かぼちゃ",
      "translation": "pumpkin",
      "image": "GFX/vegetables/pumpkin.png"
    },
    {
      "kanji": "ししとう",
      "furigana": "ししとう",
      "translation": "shishito pepper",
      "image": "GFX/vegetables/shishito_pepper.png"
    }
  ]
}

j_vegtables5 = {
  "quiz_title": "Vegetables 5",
  "questions": [
    {
      "kanji": "ごぼう",
      "furigana": "ごぼう",
      "translation": "burdock root",
      "image": "GFX/vegetables/burdock_root.png"
    },
    {
      "kanji": "にんにく",
      "furigana": "にんにく",
      "translation": "garlic",
      "image": "GFX/vegetables/garlic.png"
    },
    {
      "kanji": "さやえんどう",
      "furigana": "さやえんどう",
      "translation": "snow pea",
      "image": "GFX/vegetables/snow_pea.png"
    },
    {
      "kanji": "たけのこ",
      "furigana": "たけのこ",
      "translation": "bamboo shoot",
      "image": "GFX/vegetables/bamboo_shoot.png"
    },
    {
      "kanji": "春菊",
      "furigana": "しゅんぎく",
      "translation": "chrysanthemum greens",
      "image": "GFX/vegetables/chrysanthemum_greens.png"
    }
  ]
}

j_verbs1 = {
  "quiz_title": "Simple Verbs",
  "questions": [
    {
      "furigana": "たべる",
      "kanji": "食べる",
      "translation": "eat",
      "image": "GFX/verbs/eat.png"
    },
    {
      "furigana": "のむ",
      "kanji": "飲む",
      "translation": "drink",
      "image": "GFX/verbs/drink.png"
    },
    {
      "furigana": "みる",
      "kanji": "見る",
      "translation": "look",
      "image": "GFX/verbs/look.png"
    },
    {
      "furigana": "きく",
      "kanji": "聞く",
      "translation": "hear",
      "image": "GFX/verbs/hear.png"
    },
    {
      "furigana": "いう",
      "kanji": "言う",
      "translation": "say",
      "image": "GFX/verbs/say.png"
    }
  ]
}

j_song_sanpo1 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 1a)",
  "questions": [
    {
      "furigana": "あるこう　あるこう",
      "kanji": "歩こう 歩こう",
      "translation": "Let's walk, let's walk",
      "image": ""
    },
    {
      "furigana": "わたしはげんき",
      "kanji": "私は元気",
      "translation": "I'm feeling good",
      "image": ""
    },
    {
      "furigana": "あるくの　だいすき",
      "kanji": "歩くの 大好き",
      "translation": "I love walking",
      "image": ""
    },
    {
      "furigana": "どんどんいこう",
      "kanji": "どんどん行こう",
      "translation": "Let's keep going forward",
      "image": ""
    },
    {
      "furigana": "さかみち　トンネル",
      "kanji": "坂道 トンネル",
      "translation": "Uphill road, tunnel",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo2 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 1b)",
  "questions": [
    {
      "furigana": "くさっぱら",
      "kanji": "草っぱら",
      "translation": "Grassy field",
      "image": ""
    },
    {
      "furigana": "いっぽんばしに",
      "kanji": "一本橋に",
      "translation": "Single log bridge",
      "image": ""
    },
    {
      "furigana": "でこぼこじゃりみち",
      "kanji": "でこぼこ砂利道",
      "translation": "Bumpy gravel path",
      "image": ""
    },
    {
      "furigana": "くものすくぐって",
      "kanji": "蜘蛛の巣くぐって",
      "translation": "Passing through spider webs",
      "image": ""
    },
    {
      "furigana": "くだりみち",
      "kanji": "下り道",
      "translation": "Downhill road",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo3 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 2a)",
  "questions": [
    {
      "furigana": "くりかえし",
      "kanji": "繰り返し",
      "translation": "Repeat",
      "image": ""
    },
    {
      "furigana": "みつばち　ぶんぶん",
      "kanji": "蜜蜂 ブンブン",
      "translation": "Buzzing bees",
      "image": ""
    },
    {
      "furigana": "はなばたけ",
      "kanji": "花畑",
      "translation": "Flower field",
      "image": ""
    },
    {
      "furigana": "ひなたにとかげ",
      "kanji": "日向にトカゲ",
      "translation": "Lizards in the sunlight",
      "image": ""
    },
    {
      "furigana": "へびはひるね",
      "kanji": "蛇は昼寝",
      "translation": "Snake is napping",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo4 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 2b)",
  "questions": [
    {
      "furigana": "ばったがとんで",
      "kanji": "バッタが飛んで",
      "translation": "Grasshoppers flying",
      "image": ""
    },
    {
      "furigana": "まがりみち",
      "kanji": "曲がり道",
      "translation": "Winding road",
      "image": ""
    },
    {
      "furigana": "くりかえし",
      "kanji": "繰り返し",
      "translation": "Repeat",
      "image": ""
    },
    {
      "furigana": "きつねも　たぬきも",
      "kanji": "狐も 狸も",
      "translation": "Foxes and tanuki",
      "image": ""
    },
    {
      "furigana": "でておいで",
      "kanji": "出ておいで",
      "translation": "Come on out",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo5 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 3a)",
  "questions": [
    {
      "furigana": "きつねも　たぬきも",
      "kanji": "狐も 狸も",
      "translation": "Foxes and tanuki",
      "image": ""
    },
    {
      "furigana": "でておいで",
      "kanji": "出ておいで",
      "translation": "Come on out",
      "image": ""
    },
    {
      "furigana": "たんけんしよう",
      "kanji": "探検しよう",
      "translation": "Let's explore",
      "image": ""
    },
    {
      "furigana": "はやしのおくまで",
      "kanji": "林の奥まで",
      "translation": "Deep into the forest",
      "image": ""
    },
    {
      "furigana": "ともだちたくさん",
      "kanji": "友達たくさん",
      "translation": "Lots of friends",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo6 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 3b)",
  "questions": [
    {
      "furigana": "うれしいな!",
      "kanji": "嬉しいな!",
      "translation": "I'm so happy!",
      "image": ""
    },
    {
      "furigana": "ともだちたくさん",
      "kanji": "友達たくさん",
      "translation": "Lots of friends",
      "image": ""
    },
    {
      "furigana": "うれしいな!",
      "kanji": "嬉しいな!",
      "translation": "I'm so happy!",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_zou_san1 = {
  "quiz_title": "Zou-san Vocabulary (Part 1)",
  "questions": [
    {
      "furigana": "ぞうさん",
      "kanji": "象さん",
      "translation": "elephant",
      "image": ""
    },
    {
      "furigana": "おはな",
      "kanji": "お鼻",
      "translation": "nose, trunk",
      "image": ""
    },
    {
      "furigana": "かあさん",
      "kanji": "母さん",
      "translation": "mother",
      "image": ""
    },
    {
      "furigana": "ながい",
      "kanji": "長い",
      "translation": "long",
      "image": ""
    },
    {
      "furigana": "だれ",
      "kanji": "誰",
      "translation": "Who?",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=WguFpvqRSRY"  # Add URL here
}

j_song_zou_san2 = {
  "quiz_title": "Zou-san Vocabulary (Part 2)",
  "questions": [
    {
      "furigana": "すき",
      "kanji": "好き",
      "translation": "like, love",
      "image": ""
    },
    {
      "furigana": "あのね",
      "kanji": "あのね",
      "translation": "well, you see...",
      "image": ""
    },
    {
      "furigana": "そうよ",
      "kanji": "そうよ",
      "translation": "That's right!",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=WguFpvqRSRY"  # Add URL here
}




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
    Log a message to both the console and the error_log.txt file with UTF-8 encoding.

    This function handles logging by printing the log entry to the console and 
    appending it to a file named 'error_log.txt'. It handles any file I/O errors 
    gracefully by logging the failure to the console.

    Parameters:
        log_entry (str): The log message to be printed and saved.
    """
    # Print the log entry to the console
    print(log_entry)

    try:
        # Attempt to open the log file with UTF-8 encoding and write the log entry
        log_file_path = "error_log.txt"
        with open(log_file_path, "a", encoding="utf-8") as error_file:
            error_file.write(log_entry + "\n")
    except (IOError, OSError) as e:
        # If an error occurs, print an error message to the console
        print(f"Failed to log message to file '{log_file_path}': {e}")
        

def list_images_in_folder(folder_path):
    """
    List all image files in the specified folder.

    This function scans the provided folder for image files with common image 
    extensions (such as .png, .jpg, .jpeg, and .bmp) and returns a list of 
    matching file names.

    Parameters:
        folder_path (str): The path to the folder containing images.

    Returns:
        list: A list of image file names in the specified folder. Returns an 
        empty list if no image files are found.
    """
    try:
        # List all image files in the folder
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        image_files = [f for f in os.listdir(folder_path) 
                       if f.lower().endswith(image_extensions)]
        return image_files
    except OSError as e:
        # Log an error if there is an issue accessing the folder
        log_entry = create_log_message(f"File operation error while listing images: {e}")
        log_message(log_entry)
        return []


def select_random_image_from_list(image_list):
    """
    Select a random image from a provided list of image files.

    This function takes a list of image file names and selects one at random.

    Parameters:
        image_list (list): A list of image file names to select from.

    Returns:
        str: The randomly selected image file name, or None if the list is empty.
    """
    if not image_list:
        return None

    return random.choice(image_list)


def select_random_background(folder_path):
    """
    Select a random background image from the specified folder.

    This function lists the image files in the specified folder and selects 
    one at random. If no image files are found, it returns None.

    Parameters:
        folder_path (str): The path to the folder containing background images.

    Returns:
        str: The file path of the randomly selected image, or None if no image 
        files are found or an error occurs during the selection process.
    """
    # Get a list of all images in the folder
    image_files = list_images_in_folder(folder_path)

    # Select a random image from the list
    selected_image = select_random_image_from_list(image_files)

    if selected_image:
        return os.path.join(folder_path, selected_image)
    else:
        # Log an error if no image files were found
        log_entry = create_log_message(f"No image files found in folder: {folder_path}")
        log_message(log_entry)
        return None


def calculate_center_position(screen_width, screen_height, window_width, window_height):
    """Calculate the center position of a window given screen and window dimensions."""
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2
    return window_x, window_y


def center_window(width, height):
    """Centers the Pygame window on the screen.

    Parameters:
        width (int): The width of the window.
        height (int): The height of the window.

    This function sets the environment variable `SDL_VIDEO_WINDOW_POS` 
    to center the Pygame window on the user's screen.
    """
    try:
        # Clear existing window position to avoid residual settings
        if 'SDL_VIDEO_WINDOW_POS' in os.environ:
            del os.environ['SDL_VIDEO_WINDOW_POS']

        # Get screen dimensions
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        # Get calculated center position
        window_x, window_y = calculate_center_position(
            screen_width, screen_height, width, height
        )

        # Set environment variable for window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"

    except AttributeError as err:
        log_entry = create_log_message(f"Failed to center window: {err}")
        log_message(log_entry)

        
def bring_window_to_front():
    """Bring the Pygame window to the front of all other windows.
    
    This function works only on Windows platforms. It uses ctypes to interact
    with the Windows API to bring the Pygame window to the foreground and set focus.
    """
    # Platform check for Windows-specific functionality
    if sys.platform != "win32":
        log_entry = create_log_message("Bring to front is only supported on Windows.")
        log_message(log_entry)
        return

    try:
        # Get the Pygame window handle
        hwnd = pygame.display.get_wm_info().get('window')

        if hwnd is None:
            raise ValueError("Unable to get the window handle.")

        # Use ctypes to bring the window to the front
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        ctypes.windll.user32.SetFocus(hwnd)

    except (AttributeError, ValueError, ctypes.WinError) as e:
        # Handle AttributeError if 'window' info is missing
        # Handle ValueError if hwnd is None
        # Handle ctypes.WinError if ctypes call fails
        log_entry = create_log_message(f"Failed to bring window to front: {e}")
        log_message(log_entry)


def load_and_set_window_icon(icon_path):
    """
    Try to load and set the window icon from the specified file.

    Parameters:
        icon_path (str): Path to the icon file.
    """
    try:
        # Load the window icon
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
    except FileNotFoundError as e:
        log_entry = create_log_message(f"Icon file not found: {e}")
        log_message(log_entry)
    except pygame.error as e:
        log_entry = create_log_message(f"Failed to load icon: {e}")
        log_message(log_entry)
        
    
def initialize_pygame():
    """
    Initialize Pygame and its modules.

    This function initializes Pygame's main modules and handles any errors that occur,
    logging them and gracefully exiting the program if necessary.
    """
    try:
        pygame.init()
        pygame.mixer.init()
    except pygame.error as e:
        log_entry = create_log_message(f"Error initializing Pygame: {e}")
        log_message(log_entry)
        sys.exit(1)
        

def get_max_display_resolution():
    """Get the maximum display resolution from the system."""
    info = pygame.display.Info()
    return info.current_w, info.current_h


def filter_available_resolutions(max_resolution, resolutions):
    """
    Filter available resolutions to match the current display.

    Parameters:
        max_resolution (tuple): Maximum resolution of the user's display.
        resolutions (list): List of possible resolutions.

    Returns:
        list: A list of resolutions that fit within the user's display.
    """
    return [
        res for res in resolutions
        if res[0] <= max_resolution[0] and res[1] <= max_resolution[1]
    ]


def load_resolution_from_options(available_resolutions, default_resolution):
    """
    Load the current resolution from the options file if available.

    Parameters:
        available_resolutions (list): List of available resolutions.
        default_resolution (tuple): Default resolution to fall back on.

    Returns:
        tuple: The selected resolution (WIDTH, HEIGHT).
        int: The index of the selected resolution.
    """
    try:
        with open("options.json", "r") as file:
            options = json.load(file)
            current_resolution_index = options.get(
                "current_resolution_index",
                available_resolutions.index(default_resolution)
            )
            return available_resolutions[current_resolution_index], current_resolution_index
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        # Log error and default to the specified resolution
        log_entry = create_log_message(f"Error loading options.json: {e}")
        log_message(log_entry)
        default_index = available_resolutions.index(default_resolution)
        return default_resolution, default_index
        

##############################################
### Pygame Initialization and Window Setup ###
##############################################

load_and_set_window_icon('assets/images/Learniverse.ico')

initialize_pygame()

# Get the display information and filter available resolutions
max_display_resolution = get_max_display_resolution()
AVAILABLE_RESOLUTIONS = filter_available_resolutions(max_display_resolution, WINDOWED_RESOLUTIONS)

# Load the resolution, defaulting to 800x800 if no valid options are found
(WIDTH, HEIGHT), current_resolution_index = load_resolution_from_options(AVAILABLE_RESOLUTIONS, DEFAULT_RESOLUTION)

# Center the window before creating the Pygame window
center_window(WIDTH, HEIGHT)

# Initialize in windowed mode
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Now that we have a screen, bring it to the user's attention
bring_window_to_front()

# Create a clock object to manage the frame rate of the game
clock = pygame.time.Clock()

# Load random background images for menus
main_menu_background = select_random_background("assets/images/main_menu/")
options_background = select_random_background("assets/images/options/")

# Initialize Text to Speech
engine = pyttsx3.init()

# Initialize separate channels for different sounds
THUNDER_CHANNEL = pygame.mixer.Channel(1)
GREETING_CHANNEL = pygame.mixer.Channel(2)
pygame.mixer.set_num_channels(16)

##########################
### Database Functions ###
##########################

def check_database_initialization():
    """
    Check if the 'learniverse.db' database exists. If not, create it.
    Ensure the 'students', 'lessons', 'sessions', and 'session_lessons' tables are set up.
    Handle errors by logging them.
    """
    try:
        # Check if the database file exists; create if it doesn't
        if not os.path.isfile(DB_NAME):
            log_message(create_log_message(f"Database '{DB_NAME}' not found. Creating and initializing tables..."))
            create_database_and_initialize_tables()
        else:
            log_message(create_log_message(f"Database '{DB_NAME}' found. Verifying tables and inserting lessons..."))
            verify_and_initialize_database()

    except sqlite3.Error as e:
        log_message(create_log_message(f"Database error during initialization: {e}"))
        sys.exit(1)

    except Exception as e:
        log_message(create_log_message(f"Unexpected error during initialization: {e}"))
        sys.exit(1)


def create_database_and_initialize_tables():
    """
    Create the database and initialize tables if it doesn't exist.
    """
    try:
        connection, cursor = get_database_cursor()
        _initialize_tables(cursor, connection)
    finally:
        cursor.close()
        connection.close()


def verify_and_initialize_database():
    """
    Verify that the database tables are set up properly, and initialize them if not.
    Insert lessons if they are missing.
    """
    try:
        connection, cursor = get_database_cursor()

        # Check if 'students' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students';")
        if cursor.fetchone():
            log_message(create_log_message("'students' table found. Database is ready."))
        else:
            log_message(create_log_message("'students' table not found. Initializing tables..."))
            _initialize_tables(cursor, connection)

        # Ensure lessons are present in the 'lessons' table
        insert_lessons(cursor, connection)

    finally:
        cursor.close()
        connection.close()
        

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
        ("Subtraction Borrowing", "Subtraction Borrowing"),
        ("Japanese Colors", "Japanese Colors"),
        ("Japanese Body Parts", "Japanese Body Parts"),
        ("Japanese Adjectives", "Japanese Adjectives"),
        ("Japanese Animals", "Japanese Animals"),
        ("Japanese Family", "Japanese Family"),
        ("Japanese Fruits", "Japanese Fruits"),
        ("Japanese Greetings", "Japanese Greetings"),
        ("One Piece Vocab", "One Piece Vocab"),
        ("Japanese Self Introduction", "Japanese Self Introduction"),
        ("Japanese Nouns", "Japanese Nouns"),
        ("Japanese Time", "Japanese Time"),
        ("Japanese Vegtables", "Japanese Vegtables"),
        ("Japanese Verbs", "Japanese Verbs"),
        ("Japanese Song Sanpo", "Japanese Song Sanpo"),
        ("Japanese Song Zou-san", "Japanese Song Zou-san")
    ]

    try:
        for title, description in lessons:
            # Check if the lesson already exists, case-insensitive check
            cursor.execute('SELECT 1 FROM lessons WHERE LOWER(title) = ?', (title.lower(),))
            result = cursor.fetchone()

            if not result:  # If no result, insert the lesson
                cursor.execute('''
                    INSERT INTO lessons (title, description)
                    VALUES (?, ?)
                ''', (title, description))

                # Commit after every insert to ensure changes are saved
                connection.commit()

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error inserting lessons: {e}")
        log_message(log_entry)


def add_student(name: str, age: Optional[int] = None, email: Optional[str] = None) -> Optional[int]:
    """
    Add a new student to the database.

    This function inserts a new student into the 'students' table of the 'learniverse.db' database.
    It records the student's name, age, and email, and commits the transaction.

    Parameters:
        name (str): The name of the student. This is a required field and must be provided.
        age (Optional[int]): The age of the student. This is optional, and can be None if not provided.
        email (Optional[str]): The email address of the student. This is optional, and can be None if not provided.

    Returns:
        Optional[int]: The ID of the newly added student if the insertion was successful.
        Returns None if there was an error during the insertion.

    Logs:
        Logs an attempt to add the student, whether the addition was successful, and the student's ID.
        Logs any error encountered during the insertion process.

    Example:
        add_student("Alice", 10, "alice@example.com")
        -> Returns the ID of the new student, e.g., 1.

    In case of an error (e.g., database is unavailable or insertion fails), logs the error and returns None.
    """
    log_message(create_log_message(f"Attempting to add student '{name}'..."))
    
    try:
        with sqlite3.connect('learniverse.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO students (name, age, email)
                VALUES (?, ?, ?)
            ''', (name, age, email))

            student_id = cursor.lastrowid
            connection.commit()

            log_entry = create_log_message(f"Student '{name}' added with ID: {student_id}")
            log_message(log_entry)

            return student_id

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error adding student '{name}': {e}")
        log_message(log_entry)
        return None


def get_students() -> List[Tuple[int, str, int, str]]:
    """
    Retrieve a list of students from the database.

    Returns:
        List[Tuple[int, str, int, str]]: A list of tuples, each representing a student.
        The tuple structure is as follows:
            - int: Student ID (Primary Key)
            - str: Student name
            - int: Student age (can be None if not provided)
            - str: Student email (can be None if not provided)

    In case of an error, an empty list is returned.
    """

    try:
        with sqlite3.connect('learniverse.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students")
            student_list = cursor.fetchall()

        return student_list

    except sqlite3.Error as e:
        log_message(create_log_message(f"Error retrieving students: {e}"))
        return []


def convert_timestamp_to_string(timestamp: float) -> str:
    """Convert a Unix timestamp to a human-readable datetime string."""
    return datetime.fromtimestamp(timestamp).strftime(DATETIME_FORMAT)


def calculate_session_metrics(start_time: float, end_time: float, total_questions: int, questions_correct: int) -> Tuple[float, float, float]:
    """Calculate total time, average time per question, and percentage of correct answers."""
    total_time = round(end_time - start_time, 1)
    avg_time_per_question = total_time / total_questions if total_questions > 0 else 0
    percent_correct = (questions_correct / total_questions) * 100 if total_questions > 0 else 0
    return total_time, avg_time_per_question, percent_correct


def add_session_lesson(session_id: int, lesson_id: int, start_time: float, end_time: float, 
                       total_questions: int, questions_correct: int) -> Optional[int]:
    """
    Add a new record to the session_lessons table with detailed lesson data.

    Parameters:
        session_id (int): The ID of the session.
        lesson_id (int): The ID of the lesson.
        start_time (float): Unix timestamp representing the start time.
        end_time (float): Unix timestamp representing the end time.
        total_questions (int): The total number of questions asked in the lesson.
        questions_correct (int): The total number of correct answers.

    Returns:
        Optional[int]: The ID of the new session lesson record, or None if an error occurs.
    """
    log_message(create_log_message("Adding lesson to session in session_lessons table."))
    try:
        with sqlite3.connect('learniverse.db') as connection:
            cursor = connection.cursor()

            # Convert timestamps
            start_time_str = convert_timestamp_to_string(start_time)
            end_time_str = convert_timestamp_to_string(end_time)

            # Calculate metrics
            total_time, avg_time_per_question, percent_correct = calculate_session_metrics(
                start_time, end_time, total_questions, questions_correct
            )

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

            return session_lesson_id

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error adding session lesson record: {e}")
        log_message(log_entry)
        return None


def get_student_id_by_name(student_name: str) -> Optional[int]:
    """
    Retrieve the student ID based on the student's name.

    Parameters:
        student_name (str): The name of the student to search for.

    Returns:
        Optional[int]: The ID of the student if found, otherwise None.
    """
    try:
        with sqlite3.connect('learniverse.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM students WHERE name = ?", (student_name,))
            result = cursor.fetchone()

            if result is None:
                log_message(create_log_message(f"Error: Student '{student_name}' not found."))
                return None

            return result[0]

    except sqlite3.Error as e:
        log_message(create_log_message(f"Error retrieving student ID for '{student_name}': {e}"))
        return None


def insert_new_session(student_id: int) -> Optional[int]:
    """
    Insert a new session for the given student ID and return the session ID.

    Parameters:
        student_id (int): The ID of the student for whom the session is to be started.

    Returns:
        Optional[int]: The ID of the newly created session if successful, otherwise None.
    """
    local_time = datetime.now().strftime(DATETIME_FORMAT)

    try:
        with sqlite3.connect('learniverse.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO sessions (student_id, start_time)
                VALUES (?, ?)
            ''', (student_id, local_time))
            connection.commit()

            session_id = cursor.lastrowid
            # log_message(create_log_message(f"New session started for student ID {student_id} with session ID {session_id}."))

            return session_id

    except sqlite3.Error as e:
        log_message(create_log_message(f"Error inserting session for student ID {student_id}: {e}"))
        return None


def start_new_session(student_name: str) -> Optional[int]:
    """
    Start a new session for the current student and return the session ID.

    Parameters:
        student_name (str): The name of the student for whom the session is to be started.

    Returns:
        Optional[int]: The ID of the newly created session if successful, or None if an error occurs.

    Logs:
        Logs an attempt to start a session, any errors, and the session ID if successful.

    Example:
        start_new_session("Alice")
        -> Returns the session ID, e.g., 3, or None if an error occurs.
    """
    # log_message(create_log_message(f"Attempting to start a new session for student '{student_name}'..."))

    student_id = get_student_id_by_name(student_name)
    if student_id is None:
        return None

    return insert_new_session(student_id)


def get_database_cursor() -> sqlite3.Cursor:
    """Return a database cursor using a context manager for easier resource management."""
    connection = sqlite3.connect('learniverse.db')
    return connection, connection.cursor()


def get_session_start_time(session_id: int) -> Optional[float]:
    """
    Retrieve the start time of a session and convert it to a timestamp.

    Parameters:
        session_id (int): The ID of the session.

    Returns:
        Optional[float]: The start time in Unix timestamp if successful, otherwise None.
    """
    try:
        with sqlite3.connect('learniverse.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT start_time FROM sessions WHERE session_id = ?", (session_id,))
            result = cursor.fetchone()

            if result is None:
                log_message(create_log_message(f"Session ID {session_id} not found."))
                return None

            start_time_str = result[0]
            # Assuming the format is 'YYYY-MM-DD HH:MM:SS'
            start_time_dt = datetime.strptime(start_time_str, DATETIME_FORMAT)
            return start_time_dt.timestamp()

    except sqlite3.Error as e:
        log_message(create_log_message(f"Error retrieving start time for session {session_id}: {e}"))
        return None
    except ValueError as ve:
        log_message(create_log_message(f"Invalid start_time format for session {session_id}: {ve}"))
        return None


def calculate_total_time(start_time: float) -> float:
    """
    Calculate the total time spent in the session.

    Parameters:
        start_time (float): The start time in Unix timestamp.

    Returns:
        float: The total time spent in the session in seconds.
    """
    return round(time.time() - start_time, 1)


def end_session(session_id: int, total_questions: int, total_correct: int, overall_avg_time: float) -> None:
    """
    Update session with end time, total questions, correct answers, and avg time.

    Parameters:
        session_id (int): The ID of the session to be ended.
        total_questions (int): Total number of questions asked in the session.
        total_correct (int): Total number of questions answered correctly.
        overall_avg_time (float): The average time per question during the session.
    """
    log_message(create_log_message(f"Attempting to end session {session_id}..."))

    # Step 1: Get the start time for the session
    session_start_time = get_session_start_time(session_id)
    if session_start_time is None:
        return

    # Step 2: Calculate total time spent in the session
    total_time = calculate_total_time(session_start_time)

    # Step 3: Update the session in the database
    session_end_time_local = datetime.now().strftime(DATETIME_FORMAT)

    try:
        with sqlite3.connect('learniverse.db') as connection:
            cursor = connection.cursor()
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

            # Log the session end information
            log_message(create_log_message(f"Session {session_id} ended. Total questions: {total_questions}, "
                                           f"Total correct: {total_correct}, Overall avg time: {overall_avg_time}"))

    except sqlite3.Error as e:
        log_message(create_log_message(f"Database error ending session {session_id}: {e}"))
    except Exception as e:
        log_message(create_log_message(f"Unexpected error ending session {session_id}: {e}"))


def get_session_count(student_id: int, date_to_check) -> int:
    """
    Retrieve the count of sessions for a student on a specific date.

    Parameters:
        student_id (int): The ID of the student.
        date_to_check (datetime.date): The date to check for sessions.

    Returns:
        int: The count of sessions for the given student on the given date.
    """
    try:
        connection, cursor = get_database_cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM sessions 
            WHERE student_id = ? 
            AND date(start_time) = ?
        ''', (student_id, date_to_check))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            return result[0]
        return 0
    except sqlite3.Error as e:
        log_message(create_log_message(f"Error retrieving session count for student ID {student_id} on {date_to_check}: {e}"))
        return 0


def student_streak_query() -> int:
    """
    Query the current streak of consecutive days for a student based on session data.

    Parameters:
        student_name (str): The name of the student.

    Returns:
        int: The number of consecutive days the student has sessions.
    """
    global current_student  # Access global current_student
    
    student_id = get_student_id_by_name(current_student)
    if student_id is None:
        return 0  # No student found, no streak

    today = datetime.today().date()
    streak = 0
    days_to_check = 1

    # Step 1: Check if there is data for yesterday
    yesterday = today - timedelta(days=1)
    if get_session_count(student_id, yesterday) == 0:
        return 0  # No session for yesterday, no streak

    # Step 2: There is data for yesterday, so streak starts at 1
    streak = 1

    # Step 3: Check further consecutive days before yesterday
    while True:
        days_to_check += 1
        streak_day = today - timedelta(days=days_to_check)
        if get_session_count(student_id, streak_day) > 0:
            streak += 1
        else:
            break

    return streak


def get_student_id_by_session(session_id: int) -> Optional[int]:
    """Retrieve the student ID from the session ID."""
    try:
        connection, cursor = get_database_cursor()
        cursor.execute('''
            SELECT student_id
            FROM sessions
            WHERE session_id = ?
        ''', (session_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result[0] if result else None

    except sqlite3.Error as e:
        log_message(create_log_message(f"Error retrieving student ID for session_id {session_id}: {e}"))
        return None


def get_lesson_id_by_title(lesson_title: str) -> Optional[int]:
    """Retrieve the lesson ID from the lesson title."""
    try:
        connection, cursor = get_database_cursor()
        cursor.execute('''
            SELECT lesson_id
            FROM lessons
            WHERE title = ?
        ''', (lesson_title,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result[0] if result else None

    except sqlite3.Error as e:
        log_message(create_log_message(f"Error retrieving lesson ID for title '{lesson_title}': {e}"))
        return None


def get_student_progress(session_id: int, lesson_title: str) -> int:
    """
    Retrieve or initialize the student's progress for a specific lesson.

    Parameters:
        session_id (int): ID of the session.
        lesson_title (str): Title of the lesson.

    Returns:
        int: The student's current level for the lesson.
    """
    student_id = get_student_id_by_session(session_id)
    if student_id is None:
        raise ValueError(f"No session data found for session_id: {session_id}")

    lesson_id = get_lesson_id_by_title(lesson_title)
    if lesson_id is None:
        raise ValueError(f"No lesson data found for lesson_title: '{lesson_title}'")

    try:
        connection, cursor = get_database_cursor()
        cursor.execute('''
            SELECT student_level
            FROM student_lesson_progress
            WHERE student_id = ? AND lesson_id = ?
        ''', (student_id, lesson_id))
        result = cursor.fetchone()

        if result:
            student_level = result[0]
        else:
            cursor.execute('''
                INSERT INTO student_lesson_progress (student_id, lesson_id, student_level)
                VALUES (?, ?, 1)
            ''', (student_id, lesson_id))
            connection.commit()
            student_level = 1

        cursor.close()
        connection.close()

        log_message(create_log_message(f"Fetched student progress: student_id={student_id}, lesson_id={lesson_id}, level={student_level}"))
        return student_level

    except sqlite3.Error as e:
        log_message(create_log_message(f"Error retrieving or initializing progress for student_id={student_id}, lesson_id={lesson_id}: {e}"))
        raise  # Raise the error for proper handling upstream


def get_session_data(session_id: int, lesson_title: str) -> Optional[tuple]:
    """
    Retrieve the session data for a given session ID and lesson title.

    Parameters:
        session_id (int): The ID of the session.
        lesson_title (str): The title of the lesson.

    Returns:
        Optional[tuple]: A tuple of (student_id, lesson_id, questions_correct, questions_asked)
                         if data is found, otherwise None.
    """
    try:
        connection, cursor = get_database_cursor()
        cursor.execute('''
            SELECT s.student_id, sl.lesson_id, sl.questions_correct, sl.questions_asked
            FROM session_lessons sl
            JOIN sessions s ON sl.session_id = s.session_id
            JOIN lessons l ON sl.lesson_id = l.lesson_id
            WHERE sl.session_id = ? AND l.title = ?
        ''', (session_id, lesson_title))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        return result if result else None

    except sqlite3.Error as e:
        log_message(create_log_message(f"Error retrieving session data for session_id {session_id}: {e}"))
        return None


def set_student_progress(session_id: int, lesson_title: str):
    """
    Updates the student_lesson_progress table for the given student and lesson based on session results.

    Parameters:
        session_id (int): ID of the session.
        lesson_title (str): Title of the lesson.
    """
    # Fetch session data
    session_data = get_session_data(session_id, lesson_title)
    if session_data is None:
        log_message(f"No session data found for session_id: {session_id}")
        return

    student_id, lesson_id, questions_correct, questions_asked = session_data

    # Calculate percentage correct
    percent_correct = (questions_correct / questions_asked) * 100 if questions_asked > 0 else 0
    log_message(f"Student {student_id} got {percent_correct}% in lesson {lesson_id} ({lesson_title}).")

    # Fetch or initialize student progress using the existing get_student_progress function
    current_level = get_student_progress(session_id, lesson_title)

    # Determine if the student should level up
    new_level = current_level + 1 if percent_correct == 100 else current_level

    try:
        # Update student progress
        connection, cursor = get_database_cursor()
        cursor.execute('''
            UPDATE student_lesson_progress
            SET student_level = ?
            WHERE student_id = ? AND lesson_id = ?
        ''', (new_level, student_id, lesson_id))
        connection.commit()

        # Log the successful update
        cursor.execute('SELECT * FROM student_lesson_progress WHERE student_id = ? AND lesson_id = ?', (student_id, lesson_id))
        log_message(f"Updated student progress: {cursor.fetchall()}")

        cursor.close()
        connection.close()

    except sqlite3.Error as e:
        log_message(f"Error updating student progress: {e}")
        connection.rollback()


def fetch_lesson_id(lesson_title):
    """Fetches the lesson_id for a given lesson title."""
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", (lesson_title,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if result:
        return result[0]
    else:
        log_message(f"Lesson '{lesson_title}' not found in the database.")
        return None


def perfect_score_lesson_skip(student_name, lesson_name):
    """
    Check if a student achieved a perfect score on a specified lesson the previous day.
    Returns True if they did, False otherwise.
    """
    # Connect to the database
    connection, cursor = get_database_cursor()
    
    try:
        # Get student_id for the specified student name
        cursor.execute("SELECT id FROM students WHERE name = ?", (student_name,))
        student_result = cursor.fetchone()
        if not student_result:
            log_entry = create_log_message(f"Student '{student_name}' not found in the database.")
            log_message(log_entry)
            return False
        student_id = student_result[0]
        log_entry = create_log_message(f"Student ID for '{student_name}': {student_id}")
        log_message(log_entry)

        # Get lesson_id for the specified lesson name
        cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", (lesson_name,))
        lesson_result = cursor.fetchone()
        if not lesson_result:
            log_entry = create_log_message(f"Lesson '{lesson_name}' not found in the database.")
            log_message(log_entry)
            return False
        lesson_id = lesson_result[0]
        log_entry = create_log_message(f"Lesson ID for '{lesson_name}': {lesson_id}")
        log_message(log_entry)

        # Define date range for yesterday
        yesterday_start = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_end = yesterday_start.replace(hour=23, minute=59, second=59)
        log_entry = create_log_message(f"Date range for yesterday: {yesterday_start} to {yesterday_end}")
        log_message(log_entry)

        # Find session_id(s) for the student within the sessions table
        cursor.execute('''
            SELECT session_id
            FROM sessions
            WHERE student_id = ?
              AND start_time BETWEEN ? AND ?
        ''', (student_id, yesterday_start, yesterday_end))
        
        session_ids = [row[0] for row in cursor.fetchall()]
        if not session_ids:
            log_entry = create_log_message(f"No sessions found for student ID {student_id} on {yesterday_start.date()}")
            log_message(log_entry)
            return False
        log_entry = create_log_message(f"Session IDs for '{student_name}' on {yesterday_start.date()}: {session_ids}")
        log_message(log_entry)

        # Check session_lessons for perfect scores for this lesson within the sessions found
        cursor.execute('''
            SELECT percent_correct, end_time
            FROM session_lessons
            WHERE lesson_id = ?
              AND session_id IN ({seq})
              AND percent_correct = 100
        '''.format(seq=','.join(['?'] * len(session_ids))), (lesson_id, *session_ids))
        
        perfect_score_yesterday = cursor.fetchone()

        # Log the retrieved data 
        if perfect_score_yesterday:
            log_entry = create_log_message(f"Perfect score found for student ID {student_id} on lesson ID {lesson_id}: {perfect_score_yesterday}")
            log_message(log_entry)
        else:
            log_entry = create_log_message(f"No perfect score found for student ID {student_id} on lesson ID {lesson_id} on {yesterday_start.date()}.")
            log_message(log_entry)

        # Return True if a perfect score was achieved yesterday, otherwise False
        return bool(perfect_score_yesterday)

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Error checking perfect score: {e}")
        log_message(log_entry)
        return False
    finally:
        cursor.close()
        connection.close()
        

# TODO Finish implementing incomplete session logic and stuff
def was_last_session_incomplete_today(student_name):
    """Check if the last session started today for the student (by name) was incomplete (no end_time)."""
    try:
        # Connect to the database 
        connection, cursor = get_database_cursor()
        
        # Look up the student ID based on the name
        cursor.execute("SELECT id FROM students WHERE name = ?", (student_name,))
        result = cursor.fetchone()
        
        if result is None:
            log_message(f"Error: Student '{student_name}' not found.")
            cursor.close()
            connection.close()
            return False  # No student found with this name
        
        student_id = result[0]  # Extract the student ID

        # Get today's date in YYYY-MM-DD format
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        # Query for the latest session started today for this student
        cursor.execute('''
            SELECT session_id, start_time, end_time
            FROM sessions
            WHERE student_id = ? AND DATE(start_time) = ?
            ORDER BY start_time DESC
            LIMIT 1
        ''', (student_id, today_date))
        
        result = cursor.fetchone()
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        # Logging for fetched result
        if result:
            session_id, start_time, end_time = result
            log_message(f"Last session ID for today is {session_id}, start_time: {start_time}, end_time: {end_time}")
        else:
            log_message("No session found for today.")
            return False  # No session found for today means no incomplete session
        
        # Determine if the session is incomplete
        is_incomplete = end_time is None
        log_message(f"Session ID {session_id} is marked incomplete: {is_incomplete}")
        return is_incomplete

    except sqlite3.Error as e:
        log_entry = create_log_message(f"Database error checking last session for student '{student_name}': {e}")
        log_message(log_entry)
        return False  # Treat any database error as "no incomplete session" to prevent crash
    except Exception as e:
        log_entry = create_log_message(f"Unexpected error checking last session for student '{student_name}': {e}")
        log_message(log_entry)
        return False


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
                continue

            # Attempt to use the font, which will validate if it's working
            pygame.font.SysFont(font_name, 12)  # Check font by loading it with small size
            filtered_fonts.append(font_name)

        except FileNotFoundError:
            # Log error for missing font
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
    while keeping the background image and 'CORRECT!' text intact.
    """

    # Prepare colors for the lightning
    start_color = (173, 216, 230)  # Light blue
    end_color = (255, 255, 255)    # White

    BOLT_SEGMENTS = 10  # Number of segments for each bolt
    FLASH_COUNT = 10    # Number of bolts per flash burst
    BOLT_FLASH_DURATION = 40  # Duration to display each flash (milliseconds)

    # Load and scale the background image to fit the screen
    bg_image = pygame.image.load(background_image)
    bg_image = pygame.transform.scale(bg_image, (screen.get_width(), screen.get_height()))

    # Load the thunder sound effect
    thunder_sound = pygame.mixer.Sound('assets/SFX/loud-thunder-192165.wav')

    for _ in range(3):  # Number of flash bursts
        # Step 1: Redraw the background to clear previous lightning bolts
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
        )

        # Step 3: Play the thunder sound effect (automatically assigns channel)
        thunder_sound.play()

        # Step 4: Draw multiple lightning bolts in this frame
        for _ in range(FLASH_COUNT):
            current_pos = start_pos
            for i in range(BOLT_SEGMENTS):
                fraction = i / BOLT_SEGMENTS
                color = (
                    int(start_color[0] + (end_color[0] - start_color[0]) * fraction),
                    int(start_color[1] + (end_color[1] - start_color[1]) * fraction),
                    int(start_color[2] + (end_color[2] - start_color[2]) * fraction)
                )

                # Randomly vary the next segment position for a jagged effect
                next_x = current_pos[0] + random.randint(-BOLT_SPREAD, BOLT_SPREAD)
                next_y = current_pos[1] + (end_pos[1] - start_pos[1]) // BOLT_SEGMENTS
                next_pos = (next_x, next_y)

                # Draw the segment of the lightning bolt
                pygame.draw.line(screen, color, current_pos, next_pos, 2)
                current_pos = next_pos

            # Draw the final segment of the bolt
            pygame.draw.line(screen, end_color, current_pos, end_pos, 2)

        # Step 5: Display the lightning on top of the background and "CORRECT!" message
        pygame.display.flip()

        # Step 6: Hold the lightning flash for a brief moment
        pygame.time.delay(BOLT_FLASH_DURATION)

        # Step 7: Clear the screen by redrawing the background and "CORRECT!" message (erasing previous bolts)
        screen.blit(bg_image, (0, 0))
        draw_text(
            text=correct_message,
            font=font,
            color=text_color,
            x=0,  # X position is set to 0 for centering later
            y=screen.get_height() * 0.2,  # Y position places the text above the image
            center=True,
            enable_shadow=True,  # Optionally enable shadow
        )

        # Step 8: Refresh the screen to apply the cleared frame
        pygame.display.flip()

        # Short delay before the next flash burst
        pygame.time.delay(20)

    # Step 9: Redraw the background and "CORRECT!" message after the lightning effect
    screen.blit(bg_image, (0, 0))
    draw_text(
        text=correct_message,
        font=font,
        color=text_color,
        x=0,  # X position is set to 0 for centering later
        y=screen.get_height() * 0.2,  # Y position places the text above the image
        center=True,
        enable_shadow=True,  # Optionally enable shadow
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

    
### WIREFRAME CUBE ###
cube_vertices = [
    [-1, -1, -1],  # 0: Back-bottom-left
    [1, -1, -1],   # 1: Back-bottom-right
    [1, 1, -1],    # 2: Back-top-right
    [-1, 1, -1],   # 3: Back-top-left
    [-1, -1, 1],   # 4: Front-bottom-left
    [1, -1, 1],    # 5: Front-bottom-right
    [1, 1, 1],     # 6: Front-top-right
    [-1, 1, 1]     # 7: Front-top-left
]

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Back face edges
    (4, 5), (5, 6), (6, 7), (7, 4),  # Front face edges
    (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
]

# Rotation angle variables 
angle_x, angle_y, angle_z = 0, 0, 0  # Initial rotation angles

hue = 0.0  # Initial hue for color

# Projection function to convert 3D points to 2D
def project_3d_to_2d(point, center_x, center_y, fov=512, viewer_distance=10):
    """Project a 3D point onto a 2D plane (the screen) using perspective projection."""
    factor = fov / (viewer_distance + point[2])
    x = point[0] * factor + center_x
    y = -point[1] * factor + center_y  # Invert y-axis to match Pygame's coordinate system
    return (int(x), int(y))


# Functions to rotate 3D points around the axes
def rotate_x(point, angle):
    """Rotate a point around the X-axis."""
    y = point[1] * math.cos(angle) - point[2] * math.sin(angle)
    z = point[1] * math.sin(angle) + point[2] * math.cos(angle)
    return [point[0], y, z]


def rotate_y(point, angle):
    """Rotate a point around the Y-axis."""
    x = point[2] * math.sin(angle) + point[0] * math.cos(angle)
    z = point[2] * math.cos(angle) - point[0] * math.sin(angle)
    return [x, point[1], z]


def rotate_z(point, angle):
    """Rotate a point around the Z-axis."""
    x = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    y = point[0] * math.sin(angle) + point[1] * math.cos(angle)
    return [x, y, point[2]]


def draw_wireframe_cube(screen, center_x, center_y):
    global angle_x, angle_y, angle_z  # Use the global rotation variables

    # Rotate the cube's vertices
    rotated_vertices = []
    for vertex in cube_vertices:
        rotated = rotate_x(vertex, angle_x)
        rotated = rotate_y(rotated, angle_y)
        rotated = rotate_z(rotated, angle_z)
        rotated_vertices.append(rotated)

    # Project the 3D points to 2D
    projected_vertices = [
        project_3d_to_2d(vertex, center_x, center_y) for vertex in rotated_vertices
    ]

    # Convert HSV to RGB for dynamic color cycling
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    edge_color = (int(r * 255), int(g * 255), int(b * 255))

    # Draw the edges of the cube with the dynamic RGB color
    for edge in cube_edges:
        pygame.draw.line(screen, edge_color, projected_vertices[edge[0]], projected_vertices[edge[1]], 2)

    # Update the angles for continuous rotation
    angle_x += 0.01
    angle_y += 0.02
    angle_z += 0.015


def update_cube():
    global angle_x, angle_y, angle_z, hue  # Declare as global since they are being modified

    # Update the rotation angles for continuous animation
    angle_x += 0.01
    angle_y += 0.02
    angle_z += 0.015
    hue += 0.00833
    if hue > 1.0:
        hue -= 1.0

### SEASONAL SFX ###
# Colors: White to light blue
def random_snow_color():
    return (
        random.randint(200, 255),  # Red: High for white/light blue
        random.randint(200, 255),  # Green: High for white/light blue
        random.randint(255, 255)   # Blue: Max for light blue
    )


# Snowflake Particle class
class SnowflakeParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(-200, -10)  # Start above the screen
        self.color = random_snow_color()
        self.size = random.randint(5, 15)
        self.speed = random.uniform(1, 2)  # Vertical speed
        self.sway = random.uniform(0.5, 1.5)  # Horizontal sway
        self.sway_direction = random.choice([-1, 1])  # Left or right
        self.settled = False

    def update(self):
        if not self.settled:
            # Vertical falling
            self.y += self.speed
            # Horizontal swaying
            sway_offset = math.sin(pygame.time.get_ticks() / 500) * self.sway
            self.x += sway_offset * self.sway_direction

            # Keep within screen bounds
            self.x = max(0, min(WIDTH - 1, self.x))  # Clamp x to screen bounds

            # Check if snowflake hits the ground
            if self.y >= HEIGHT - 1:
                self.y = HEIGHT - 1  # Snap to the ground
                self.settled = True  # Mark as settled

    def draw(self, surface):
        for i in range(6):  # Six lines radiating from center
            angle = i * math.pi / 3  # 60 degrees between each line
            end_x = self.x + math.cos(angle) * self.size
            end_y = self.y + math.sin(angle) * self.size
            pygame.draw.line(surface, self.color, (self.x, self.y), (end_x, end_y), 1)


# Random color generator for sakura petals
def random_sakura_color():
    return random.choice(SAKURA_COLORS)


# Sakura Blossom Particle class
class SakuraBlossom:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(-200, -10)  # Start above the screen
        self.color = random_sakura_color()
        self.size = random.randint(10, 20)  # Blossom size
        self.speed = random.uniform(0.5, 1.5)  # Vertical speed
        self.sway = random.uniform(0.3, 1.0)  # Horizontal sway
        self.sway_direction = random.choice([-1, 1])  # Left or right
        self.settled = False

    def update(self):
        if not self.settled:
            # Vertical falling
            self.y += self.speed
            # Horizontal swaying
            sway_offset = math.sin(pygame.time.get_ticks() / 1000) * self.sway
            self.x += sway_offset * self.sway_direction

            # Keep within screen bounds
            self.x = max(0, min(WIDTH - 1, self.x))  # Clamp x to screen bounds

            # Check if blossom hits the ground
            if self.y >= HEIGHT - 1:
                self.y = HEIGHT - 1  # Snap to the ground
                self.settled = True  # Mark as settled

    def draw(self, surface):
        center_x, center_y = self.x, self.y
        petal_distance = self.size * 0.4  # Distance of petals from center (closer to center)
        petal_width = self.size * 0.7
        petal_height = self.size * 0.4

        for i in range(5):  # Draw five petals
            angle = i * (2 * math.pi / 5)  # Divide circle into 5 angles
            petal_x = center_x + math.cos(angle) * petal_distance
            petal_y = center_y + math.sin(angle) * petal_distance
            pygame.draw.ellipse(surface, self.color, (petal_x, petal_y, petal_width, petal_height))


# Random color generator for leaves
def random_leaf_color():
    return random.choice(LEAF_COLORS)


# Leaf Particle class
class LeafParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(-200, -10)  # Start above the screen
        self.color = random_leaf_color()
        self.width = random.randint(10, 20)  # Width of the oval
        self.height = random.randint(5, 10)  # Height of the oval
        self.speed = random.uniform(1, 2)  # Vertical speed
        self.sway = random.uniform(0.5, 1.5)  # Horizontal sway
        self.sway_direction = random.choice([-1, 1])  # Left or right
        self.settled = False

    def update(self):
        if not self.settled:
            # Vertical falling
            self.y += self.speed
            # Horizontal swaying
            sway_offset = math.sin(pygame.time.get_ticks() / 500) * self.sway
            self.x += sway_offset * self.sway_direction

            # Keep within screen bounds
            self.x = max(0, min(WIDTH - 1, self.x))  # Clamp x to screen bounds

            # Check if leaf hits the ground
            if self.y >= HEIGHT - 1:
                self.y = HEIGHT - 1  # Snap to the ground
                self.settled = True  # Mark as settled

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, (self.x, self.y, self.width, self.height))
        
        
################################
### Display and UI Functions ###
################################

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
    continue_font_size = int(get_dynamic_font_size() * 0.8)  

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
    continue_rect = draw_text("Continue...", continue_font, text_color, x_position, y_position, screen, enable_shadow=True, return_rect=True)

    return continue_rect


# TODO remove this entirely from teh project and only use draw_continue_button
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False
    return


def draw_skip_button(hovered_over=False):
    global current_font_name_or_path  # Ensure we're using the global font variable

    # Set font size for the skip button, similar to continue button
    skip_font_size = int(get_dynamic_font_size() * 0.8)

    # Create the font
    if os.path.isfile(current_font_name_or_path):
        skip_font = pygame.font.Font(current_font_name_or_path, skip_font_size)
    else:
        skip_font = pygame.font.SysFont(current_font_name_or_path, skip_font_size)

    # Position "Skip..." text on the lower left (at 10% width across the screen)
    x_position = WIDTH * 0.1
    y_position = HEIGHT * 0.90
    
    if (hovered_over == True):
        skip_button_color = shadow_color
    else:
        skip_button_color = text_color

    # Draw the "Skip..." text with a shadow and return the rectangle for click detection
    skip_rect = draw_text("Skip...", skip_font, skip_button_color, x_position, y_position, screen, enable_shadow=True, return_rect=True)
    return skip_rect


def display_text_and_wait(text):
    """Clears the screen, displays the given text, and waits for a left mouse click."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Only left-click
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
    use_japanese_font -- Whether to use the Japanese font (optional, defaults to False).
    font_override -- Optionally pass a different font for this draw call (optional).

    Returns:
    If return_rect is True, returns the rect of the first line of drawn text. Otherwise, returns None.
    """

    # Use the screen as the default surface if none is provided
    if surface is None:
        surface = screen

    # If shadow_color is not provided, use the passed shadow_color or global value
    if shadow_color is None:
        shadow_color = globals().get('shadow_color', BLACK)

    # Select the font to use, prioritize font_override, then Japanese or default font
    selected_font = font_override if font_override else (j_font if use_japanese_font else font)

    # First split text by \n to handle explicit new lines
    lines = text.split('\n')

    # Then handle word wrapping if max_width is provided
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
        
        # Calculate rect for the first line
        if i == 0 and return_rect:
            text_rect = pygame.Rect(draw_x, y, selected_font.size(line)[0], selected_font.size(line)[1])
        
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
    
    
def speak_japanese(text):
    """
    Attempt to play a pre-rendered WAV file for the given Japanese text.
    If the file does not exist or cannot be played, handle gracefully.

    Parameters:
    text (str): The Japanese text for which to play the corresponding WAV file.
    """
    # Convert Japanese text to a Romanized filename format
    romaji_filename = unidecode(text)[:50]  # Truncate for safety in filenames
    wav_file_path = f"assets/audio/{romaji_filename}.wav"

    try:
        # Check if the WAV file exists and play it
        if os.path.isfile(wav_file_path):
            sound = pygame.mixer.Sound(wav_file_path)
            sound.play()  # Play without specifying a channel, allowing automatic assignment
            # log_entry = create_log_message(f"Played audio file: {wav_file_path}")
            # log_message(log_entry)
        else:
            raise FileNotFoundError(f"No audio file found for '{text}' at '{wav_file_path}'")
    
    except Exception as e:
        # Log any error that occurs during file playback
        log_entry = create_log_message(f"Error playing audio for '{text}': {e}")
        log_message(log_entry)


############################
### Bonus Game Functions ###
############################

def bonus_game_selector():
    """
    Selects and launches a random bonus game.

    This function randomly chooses one of the available bonus games and initiates it.
    Each bonus game offers unique gameplay and objectives, providing variety for the player.
    Additional bonus games may be added to the selection list in the future.

    Returns:
        None
    """
    log_message(create_log_message("Selecting random bonus game."))
    bonus_games = [bonus_game_fat_tuna, 
                   bonus_game_no_fish, 
                   bonus_game_falling_fish,
                   bonus_game_cat_pong]
                    #, bonus_game_dolphin_dive, bonus_game_star_splash]
    selected_game = random.choice(bonus_games)
    selected_game()


def bonus_game_fat_tuna():
    """
    Runs the "Fat Tuna" bonus game.

    This function initializes the game environment, including background images,
    platforms, the player's cat character, piranhas, and the fat tuna target.
    The objective is to reach the fat tuna without colliding with any piranhas.
    The player can control the cat's movements to jump across platforms and avoid 
    obstacles.

    If the cat collides with the fat tuna, the game ends with a win message.
    If a piranha collides with the cat, the game ends with a game over message.

    Game Elements:
        - Scaling factors are used to adjust the size of sprites and movement speeds 
          based on the current resolution.
        - Platforms spawn and move downwards periodically.
        - The fat tuna moves horizontally and reverses direction when reaching 
          screen edges.
        - Piranhas spawn periodically and fall, presenting an obstacle to the player.

    Gameplay Phases:
        1. Control Display: Shows the control instructions and a bouncing "Bonus Stage!" 
           message until the player clicks "Continue...".
        2. Gameplay: Player controls the cat character to jump between platforms, avoid 
           piranhas, and reach the fat tuna. 
        3. End Phase: Displays a win or game over message based on the outcome.

    Returns:
        None
    """
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
    # player_img = pygame.image.load('assets/images/sprites/cat06.png')
    # Get the current month
    current_month = datetime.now().month
    
    # Conditional image loading
    player_img = pygame.image.load(
        'assets/images/sprites/cat06.png' if current_month == 12 
        else 'assets/images/sprites/cat01.png'
    )
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
        draw_text(f"You caught the Fat Tuna in {elapsed_time} seconds!", 
                  font, 
                  text_color, 
                  WIDTH // 2, 
                  HEIGHT // 3, 
                  center=True, 
                  enable_shadow=True,
                  max_width=WIDTH)
    elif game_over:
        screen.fill(screen_color)
        draw_text("Game Over! You were eaten by the piranha.", 
                  font, 
                  text_color, 
                  WIDTH // 2, 
                  HEIGHT // 3, 
                  center=True, 
                  enable_shadow=True,
                  max_width=WIDTH)

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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False  # Continue after the "Continue..." button is clicked


def bonus_game_no_fish():
    """
    Runs the "No Fish" bonus game.

    This game requires the player to control a cat character, avoiding obstacles and 
    surviving as long as possible by jumping across falling platforms and dodging 
    hazards like bombs and piranhas. The objective is to accumulate survival time 
    or a high score while avoiding collisions that would end the game.

    Game Elements:
        - Scaling factors adjust sprite sizes and movement speeds based on the 
          current screen resolution.
        - Platforms spawn periodically and scroll downwards.
        - Bombs and piranhas spawn at intervals and pose hazards for the player.

    Gameplay Phases:
        1. Control Display Phase: Shows control instructions and an animated 
           "Bonus Stage!" message until the player clicks "Continue...".
        2. Gameplay Phase: The player controls the cat, jumping between platforms 
           and avoiding bombs and piranhas. The game ends if the cat collides with 
           a bomb or piranha.
        3. Game Over Phase: Displays a game-over message indicating the cause of 
           death, either "hit by a bomb" or "eaten by a piranha."

    Returns:
        None
    """
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
    BOMB_SPAWN_INTERVAL = 1500  # Time interval (milliseconds) between bomb spawns
    BOMB_FALL_SPEED = 25 * scale_factor  # Speed for the falling bombs
    
    running = True
    game_over = False
    death_cause = None  # Variable to store the cause of death
    start_time = time.time()
    last_spawn_time = 0
    last_piranha_spawn_time = 0
    last_bomb_spawn_time = 0  # Track last bomb spawn time

    # Load images
    platform_img = pygame.image.load('assets/images/sprites/platform.jpg')
    bonus_mode_background = select_random_background("assets/images/bonus_mode")
    gameplay_background = select_random_background("assets/images/bonus_bkgs")

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
    
    # Load and scale the bomb image
    bomb_img = pygame.image.load('assets/images/sprites/bomb.png')
    bomb_img = pygame.transform.scale(bomb_img, (int(bomb_img.get_width() * scale_factor), int(bomb_img.get_height() * scale_factor)))
    bombs = []  # List to hold bombs

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

            # Check for game over condition (bomb or piranha collision)
            for bomb in bombs:
                if cat.rect.colliderect(bomb.rect):
                    death_cause = "bomb"
                    game_over = True
                    running = False

            for piranha in piranhas:
                if cat.rect.colliderect(piranha.rect):
                    death_cause = "piranha"
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

            # Spawn new bombs at the top of the screen
            if current_time - last_bomb_spawn_time > BOMB_SPAWN_INTERVAL:
                new_bomb = Bomb(bomb_img, random.randint(0, WIDTH - bomb_img.get_width()), 0, BOMB_FALL_SPEED)
                bombs.append(new_bomb)
                last_bomb_spawn_time = current_time

            # Update bombs positions
            for bomb in bombs:
                bomb.update()

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

            # Draw the bombs
            for bomb in bombs:
                bomb.draw(screen)

            # Draw the cat on top of everything else
            cat.draw(screen)

            # Draw the timer on top of all elements
            draw_text(f"{elapsed_time}", font, text_color, WIDTH // 4, HEIGHT // 60)

            pygame.display.flip()
            clock.tick(24)  # Control the frame rate

    finally:
        # Ensure music stops and resources are freed if an exception occurs
        stop_mp3()

    # Game Over Phase
    if game_over:
        screen.fill(screen_color)
        if death_cause == "bomb":
            death_message = "Game Over! You were hit by a bomb."
        elif death_cause == "piranha":
            death_message = "Game Over! You were eaten by a piranha."
        else:
            death_message = "Game Over!"

        draw_text(death_message, font, text_color, WIDTH // 2, HEIGHT // 3, center=True, enable_shadow=True, max_width=WIDTH)

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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False  # Continue after the "Continue..." button is clicked


def bonus_game_falling_fish():
    """
    Runs the "Falling Fish" bonus game with an additional special item (cat food) 
    that falls like fish for bonus points.
    """
    # Check if the assets/images directory exists
    if not os.path.exists('assets/images'):
        log_entry = create_log_message("Assets folder 'assets/images' is missing. Returning to the main menu.")
        log_message(log_entry)
        return "main_menu"
    
    try:
        # Scaling factors based on resolution
        scale_factor_x = WIDTH / REFERENCE_RESOLUTION[0]
        scale_factor_y = HEIGHT / REFERENCE_RESOLUTION[1]
        scale_factor = min(scale_factor_x, scale_factor_y)
        log_message(f"Scaling factors calculated: scale_factor_x={scale_factor_x}, scale_factor_y={scale_factor_y}, scale_factor={scale_factor}")

        # Game settings for items
        BOMB_SPAWN_INTERVAL = 600  # Time interval (milliseconds) between bomb spawns
        FISH_SPAWN_INTERVAL = 1000  # Time interval (milliseconds) between fish spawns
        CAT_FOOD_SPAWN_INTERVAL = 3000  # Time interval (milliseconds) between special item spawns
        BOMB_FALL_SPEED = 35 * scale_factor  # Speed for the falling bombs
        FISH_FALL_SPEED = 24 * scale_factor  # Speed for the falling fish
        CAT_FOOD_FALL_SPEED = 20 * scale_factor  # Speed for the falling cat food (special item)
        
        # Initialize variables
        running = True
        game_over = False
        death_cause = None
        score = 0
        # start_time = time.time()
        last_bomb_spawn_time = 0
        last_fish_spawn_time = 0
        last_cat_food_spawn_time = 0  # Special item spawn timer
        log_message("Game variables initialized")

        # Load images
        bonus_mode_background = select_random_background("assets/images/bonus_mode")
        gameplay_background = select_random_background("assets/images/bonus_bkgs")
        bomb_img = pygame.image.load('assets/images/sprites/bomb.png')
        bomb_img = pygame.transform.scale(bomb_img, (int(bomb_img.get_width() * scale_factor), int(bomb_img.get_height() * scale_factor)))
        bombs = []

        fish_dir = 'assets/images/sprites/fish'
        fish_images = [os.path.join(fish_dir, file) for file in os.listdir(fish_dir) if file.lower().endswith(('.jpg', '.png'))]
        fishes = []
        log_message(f"Fish images loaded from {fish_dir}: {len(fish_images)} images found")

        cat_food_img = pygame.image.load('assets/images/sprites/power_ups/cat_food.png')
        cat_food_img = pygame.transform.scale(cat_food_img, (int(cat_food_img.get_width() * scale_factor), int(cat_food_img.get_height() * scale_factor)))
        cat_food_items = []

        # Load and initialize the cat character
        player_img = pygame.image.load('assets/images/sprites/cat08.png')
        player_img = pygame.transform.scale(player_img, (int(player_img.get_width() * scale_factor * 2), int(player_img.get_height() * scale_factor * 2)))
        cat = Cat(player_img, WIDTH // 2, HEIGHT - player_img.get_rect().height, 25 * scale_factor, scale_factor)
        log_message("Cat character initialized")

        clock = pygame.time.Clock()

        # Load and play bonus game music
        bonus_music_directory = 'assets/music/bonus'
        random_mp3 = get_random_mp3(bonus_music_directory)
        if random_mp3:
            music_loaded = load_mp3(random_mp3)
            if music_loaded:
                play_mp3()
                log_message(f"Playing bonus music: {random_mp3}")
            else:
                log_message("Failed to load bonus music")
        
        # Bonus Mode Display Phase
        controls_displayed = False
        text_x, text_y = WIDTH // 2 - int(175 * scale_factor), HEIGHT // 2
        text_dx, text_dy = random.choice([-10, 10]), random.choice([-10, 10])
        text_dx *= scale_factor
        text_dy *= scale_factor
        log_message("Bonus Mode Display Phase started")

        while not controls_displayed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if bonus_mode_background:
                draw_background(bonus_mode_background)
            else:
                screen.fill(screen_color)

            draw_text("Controls:", font, text_color, 0, HEIGHT * 0.2, center=True, enable_shadow=True)
            draw_text("W = Jump", font, text_color, 0, HEIGHT * 0.4, center=True, enable_shadow=True)
            draw_text("A = Move Left", font, text_color, 0, HEIGHT * 0.6, center=True, enable_shadow=True)
            draw_text("D = Move Right", font, text_color, 0, HEIGHT * 0.8, center=True, enable_shadow=True)

            text_surface = font.render("Bonus Stage!", True, text_color)
            text_width, text_height = text_surface.get_size()

            text_x += text_dx
            text_y += text_dy

            if text_x <= 0 or text_x >= WIDTH - text_width:
                text_dx = -text_dx
            if text_y <= 0 or text_y >= HEIGHT - text_height:
                text_dy = -text_dy

            screen.blit(text_surface, (text_x, text_y))
            continue_rect = draw_continue_button()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if check_continue_click(pygame.mouse.get_pos(), continue_rect):
                        controls_displayed = True
                        log_message("Controls display completed, starting gameplay phase")

            clock.tick(60)

        # Gameplay Phase
        try:
            while running:
                current_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            running = False
                            pygame.mixer.music.stop()
                            return
                        elif event.key in [pygame.K_SPACE, pygame.K_w]:
                            cat.jump()
                            log_message("Cat jumped")

                cat.update()

                # Bomb collision check
                for bomb in bombs:
                    if cat.rect.colliderect(bomb.rect):
                        death_cause = "bomb"
                        game_over = True
                        running = False
                        log_message("Game Over: Cat collided with bomb")

                # Fish collision check
                for fish in fishes[:]:
                    if cat.rect.colliderect(fish.rect):
                        score += 1
                        fishes.remove(fish)
                        log_message(f"Score increased to {score} by collecting fish")

                # Cat food (special item) collision check
                for item in cat_food_items[:]:
                    if cat.rect.colliderect(item.rect):
                        score += 5
                        cat_food_items.remove(item)
                        log_message(f"Score increased to {score} by collecting cat food (special item)")

                # Bomb spawning
                if current_time - last_bomb_spawn_time > BOMB_SPAWN_INTERVAL:
                    new_bomb = Bomb(bomb_img, random.randint(0, WIDTH - bomb_img.get_width()), 0, BOMB_FALL_SPEED)
                    bombs.append(new_bomb)
                    last_bomb_spawn_time = current_time
                    log_message("New bomb spawned")

                # Fish spawning
                if current_time - last_fish_spawn_time > FISH_SPAWN_INTERVAL and fish_images:
                    fish_img = pygame.image.load(random.choice(fish_images))
                    fish_img = pygame.transform.scale(fish_img, (int(fish_img.get_width() * scale_factor), int(fish_img.get_height() * scale_factor)))
                    fishes.append(Fish(fish_img, random.randint(0, WIDTH - fish_img.get_width()), 0, FISH_FALL_SPEED))
                    last_fish_spawn_time = current_time
                    log_message("New fish spawned")

                # Cat food (special item) spawning
                if current_time - last_cat_food_spawn_time > CAT_FOOD_SPAWN_INTERVAL:
                    new_cat_food = Fish(cat_food_img, random.randint(0, WIDTH - cat_food_img.get_width()), 0, CAT_FOOD_FALL_SPEED)
                    cat_food_items.append(new_cat_food)
                    last_cat_food_spawn_time = current_time
                    log_message("New cat food (special item) spawned")

                # Update positions
                for bomb in bombs:
                    bomb.update()
                for fish in fishes:
                    fish.update()
                for item in cat_food_items:
                    item.update()

                if gameplay_background:
                    draw_background(gameplay_background)
                else:
                    screen.fill(screen_color)

                for bomb in bombs:
                    bomb.draw(screen)
                for fish in fishes:
                    fish.draw(screen)
                for item in cat_food_items:
                    item.draw(screen)

                cat.draw(screen)
                draw_text(f"Score: {score}", font, text_color, WIDTH // 4, HEIGHT // 60, enable_shadow=True)

                pygame.display.flip()
                clock.tick(24)

        finally:
            stop_mp3()
            log_message("Music stopped, exiting game")

    except Exception as e:
        log_message(f"Error in bonus_game_falling_fish: {str(e)}")
        pygame.quit()
        sys.exit()
    
    if game_over:
        screen.fill(screen_color)
        death_message = "Game Over! You were hit by a bomb." if death_cause == "bomb" else "Game Over!"
        draw_text(death_message, font, text_color, WIDTH // 2, HEIGHT // 3, center=True, enable_shadow=True, max_width=WIDTH)
        log_message(death_message)
        continue_rect = draw_continue_button()

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if check_continue_click(pygame.mouse.get_pos(), continue_rect):
                        waiting = False
                        log_message("Player continued after game over")


def bonus_game_cat_pong():
    """
    Runs the "Cat Pong" bonus game.

    This function launches a game where the player controls a cat character on 
    one side of the screen to bat a bomb back and forth with a computer-controlled 
    cat on the opposite side. The goal is to prevent the bomb from hitting the 
    player’s side while trying to make it past the computer-controlled cat.

    Game Elements:
        - Player Cat: Controlled by the player, moving up and down on the left side.
        - Computer Cat: Controlled by the AI, moving up and down on the right side 
          to intercept the bomb.
        - Bomb: Moves between the cats, with speed and direction changing upon contact 
          with the cats or screen edges.

    Gameplay Phases:
        1. Control Display Phase: Shows control instructions and an animated 
           "Bonus Stage!" message until the player clicks "Continue...".
        2. Gameplay Phase: The player controls the cat to prevent the bomb from 
           crossing the left boundary while the AI cat defends the right boundary.
        3. Game Over Phase: Displays a "Victory!" message if the bomb crosses 
           the AI’s side, or a "Game Over!" message if it crosses the player’s side.

    Returns:
        None
    """
    # Check if the assets/images directory exists
    if not os.path.exists('assets/images'):
        log_entry = create_log_message("Assets folder 'assets/images' is missing. Returning to the main menu.")
        log_message(log_entry)
        return "main_menu"

    # Calculate scaling factors based on the current resolution
    scale_factor_x = WIDTH / REFERENCE_RESOLUTION[0]
    scale_factor_y = HEIGHT / REFERENCE_RESOLUTION[1]
    scale_factor = min(scale_factor_x, scale_factor_y)

    BOMB_SPEED_X = 8 * scale_factor  # Initial horizontal speed of the bomb
    BOMB_SPEED_Y = 7 * scale_factor  # Initial vertical speed of the bomb
    # PLAYER_SPEED = 6 * scale_factor  # Slightly slower than the bomb’s initial speed
    AI_SPEED = 6.1 * scale_factor  # AI speed matches player speed
    PLAYER_SPEED = AI_SPEED * 1.2
    
    running = True
    game_over = False
    win = False  # Track if the player won or lost
    # start_time = time.time()

    # Load images
    background = select_random_background("assets/images/bonus_bkgs")

    # Load and double-scale the bomb image
    bomb_img = pygame.image.load('assets/images/sprites/bomb.png')
    bomb_img = pygame.transform.scale(bomb_img, (int(bomb_img.get_width() * 1.5 * scale_factor), int(bomb_img.get_height() * 1.5 * scale_factor)))
    bomb_rect = bomb_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    bomb_dx, bomb_dy = BOMB_SPEED_X, BOMB_SPEED_Y

    # Load and double-scale player cat
    player_cat_img = pygame.image.load('assets/images/sprites/cat01.png')
    player_cat_img = pygame.transform.scale(player_cat_img, (int(player_cat_img.get_width() * 2 * scale_factor), int(player_cat_img.get_height() * 2 * scale_factor)))
    player_cat_rect = player_cat_img.get_rect(midleft=(int(50 * scale_factor), HEIGHT // 2))

    # Load and double-scale AI cat
    ai_cat_img = pygame.image.load('assets/images/sprites/cat08.png')  # A second cat sprite
    ai_cat_img = pygame.transform.scale(ai_cat_img, (int(ai_cat_img.get_width() * 2 * scale_factor), int(ai_cat_img.get_height() * 2 * scale_factor)))
    ai_cat_img = pygame.transform.flip(ai_cat_img, True, False)  # Flip AI cat horizontally
    ai_cat_rect = ai_cat_img.get_rect(midright=(WIDTH - int(50 * scale_factor), HEIGHT // 2))


    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Load and play bonus game music
    bonus_music_directory = 'assets/music/bonus'
    random_mp3 = get_random_mp3(bonus_music_directory)
    
    if random_mp3:
        music_loaded = load_mp3(random_mp3)
        if music_loaded:
            play_mp3()

    # Control Display Phase
    controls_displayed = False

    while not controls_displayed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background
        if background:
            draw_background(background)
        else:
            screen.fill(screen_color)

        # Render the controls
        draw_text("Controls:", font, text_color, 0, HEIGHT * 0.2, center=True, enable_shadow=True)
        draw_text("W = Move Up", font, text_color, 0, HEIGHT * 0.4, center=True, enable_shadow=True)
        draw_text("S = Move Down", font, text_color, 0, HEIGHT * 0.6, center=True, enable_shadow=True)

        # Render the bouncing "Bonus Stage!" text
        text_surface = font.render("Bonus Stage!", True, text_color)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2))

        # Draw the "Continue..." button below the controls
        continue_rect = draw_continue_button()
        pygame.display.flip()

        # Check for "Continue..." button click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    controls_displayed = True

        clock.tick(60)

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
            # Move the player cat based on input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player_cat_rect.top > 0:
                player_cat_rect.y -= PLAYER_SPEED
            if keys[pygame.K_s] and player_cat_rect.bottom < HEIGHT:
                player_cat_rect.y += PLAYER_SPEED
    
            # AI cat movement logic
            if bomb_rect.centery < ai_cat_rect.centery and ai_cat_rect.top > 0:
                ai_cat_rect.y -= AI_SPEED
            elif bomb_rect.centery > ai_cat_rect.centery and ai_cat_rect.bottom < HEIGHT:
                ai_cat_rect.y += AI_SPEED
    
            # Update bomb position
            bomb_rect.x += bomb_dx
            bomb_rect.y += bomb_dy
    
            # Check for collisions with top/bottom screen boundaries
            if bomb_rect.top <= 0 or bomb_rect.bottom >= HEIGHT:
                bomb_dy = -bomb_dy
    
            # Check for collisions with player cat
            if bomb_rect.colliderect(player_cat_rect) and bomb_dx < 0:
                # Modify bounce angle based on contact point
                offset = (bomb_rect.centery - player_cat_rect.centery) / player_cat_rect.height
                bomb_dx = -bomb_dx  # Reverse direction horizontally
                bomb_dy += offset * 5  # Adjust vertical speed based on collision point
    
            # Check for collisions with AI cat
            if bomb_rect.colliderect(ai_cat_rect) and bomb_dx > 0:
                # Modify bounce angle based on contact point
                offset = (bomb_rect.centery - ai_cat_rect.centery) / ai_cat_rect.height
                bomb_dx = -bomb_dx  # Reverse direction horizontally
                bomb_dy += offset * 5  # Adjust vertical speed based on collision point
                
            # Check for win/loss state
            if bomb_rect.left <= 0:  # Player loses if bomb crosses the left edge
                game_over = True
                win = False
                running = False
            elif bomb_rect.right >= WIDTH:  # Player wins if bomb crosses the right edge
                game_over = True
                win = True
                running = False
    
            # Draw gameplay background
            if background:
                draw_background(background)
            else:
                screen.fill(screen_color)
    
            # Draw the cats and the bomb
            screen.blit(player_cat_img, player_cat_rect.topleft)
            screen.blit(ai_cat_img, ai_cat_rect.topleft)
            screen.blit(bomb_img, bomb_rect.topleft)
    
            pygame.display.flip()
            clock.tick(60)
    
    finally:
        stop_mp3()


    # Game Over Phase
    if game_over:
        screen.fill(screen_color)
        if win:
            message = "Victory!"
        else:
            message = "Game Over! The bomb passed your side."

        draw_text(message, font, text_color, WIDTH // 2, HEIGHT // 3, 
                  center=True, 
                  max_width=WIDTH,
                  enable_shadow=True)
        continue_rect = draw_continue_button()
        pygame.display.flip()

        # Wait for the player to click "Continue..."
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if check_continue_click(mouse_pos, continue_rect):
                        waiting = False  # Continue after the "Continue..." button is clicked


# TODO implement this, make it fun, this was William's idea        
# def bonus_game_tuna_tower():
#     # Check if the assets/images directory exists
#     if not os.path.exists('assets/images'):
#         log_entry = create_log_message("Assets folder 'assets/images' is missing. Returning to the main menu.")
#         log_message(log_entry)
#         return "main_menu"
    
#     # Calculate scaling factors based on the current resolution
#     scale_factor_x = WIDTH / REFERENCE_RESOLUTION[0]
#     scale_factor_y = HEIGHT / REFERENCE_RESOLUTION[1]
#     scale_factor = min(scale_factor_x, scale_factor_y)

#     GROUND_LEVEL = HEIGHT * 0.8  # Set the ground level

#     # Control display phase setup
#     running = True
#     controls_displayed = False

#     # Load tower tile image and scale it
#     tower_tile_img = pygame.image.load('assets/images/sprites/towertile01.png')
#     tower_tile_img = pygame.transform.scale(tower_tile_img, (int(64 * scale_factor), int(64 * scale_factor)))
    
#     # Load platform image and scale it
#     platform_img = pygame.image.load('assets/images/sprites/platform.jpg')
#     platform_img = pygame.transform.scale(platform_img, (int(200 * scale_factor), int(50 * scale_factor)))
    
#     # Load cat image and scale to double its original size
#     cat_img = pygame.image.load('assets/images/sprites/cat08.png')
#     cat_img = pygame.transform.scale(cat_img, (int(cat_img.get_width() * 2 * scale_factor), int(cat_img.get_height() * 2 * scale_factor)))
    
#     # Cat position and movement variables
#     cat_x = WIDTH // 2 - cat_img.get_width() // 2
#     cat_y = int(GROUND_LEVEL) - cat_img.get_height() - 100
#     cat_speed = 25 * scale_factor  # Speed for horizontal movement
#     cat_facing_right = True       # Track direction to manage flipping
#     is_falling = False            # Falling state to trigger upward scroll when off-platform
    
#     # Platform position and collision rect
#     platform_x = WIDTH // 2 - platform_img.get_width() // 2
#     platform_y = int(GROUND_LEVEL)
#     platform_rect = pygame.Rect(platform_x, platform_y, platform_img.get_width(), platform_img.get_height())

#     # Background scroll offset
#     scroll_offset = 0
#     base_scroll_speed = 20 * scale_factor  # Base speed for scrolling effect

#     # Jumping state variables
#     is_jumping = False
#     jump_start_time = 0
#     jump_duration = 1  # Duration of jump up phase (in seconds)

#     # Initialize bouncing text position and movement
#     text_x, text_y = WIDTH // 2 - int(175 * scale_factor), HEIGHT // 2
#     text_dx, text_dy = random.choice([-10, 10]), random.choice([-10, 10])
#     text_dx *= scale_factor
#     text_dy *= scale_factor

#     # Display control instructions
#     while not controls_displayed:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         screen.fill(screen_color)

#         # Render the controls text
#         draw_text("Controls:", font, text_color, 0, HEIGHT * 0.2, center=True, enable_shadow=True)
#         draw_text("W = Jump", font, text_color, 0, HEIGHT * 0.4, center=True, enable_shadow=True)
#         draw_text("A = Move Left", font, text_color, 0, HEIGHT * 0.6, center=True, enable_shadow=True)
#         draw_text("D = Move Right", font, text_color, 0, HEIGHT * 0.8, center=True, enable_shadow=True)

#         # Render the bouncing "Bonus Stage!" text
#         text_surface = font.render("Bonus Stage!", True, text_color)
#         text_width, text_height = text_surface.get_size()

#         # Update text position
#         text_x += text_dx
#         text_y += text_dy

#         # Check for collisions with the screen edges and reverse direction if needed
#         if text_x <= 0 or text_x >= WIDTH - text_width:
#             text_dx = -text_dx
#         if text_y <= 0 or text_y >= HEIGHT - text_height:
#             text_dy = -text_dy

#         # Draw the bouncing text at the updated position
#         screen.blit(text_surface, (text_x, text_y))

#         # Draw the "Continue..." button
#         continue_rect = draw_continue_button()
#         pygame.display.flip()

#         # Check for "Continue..." button click
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 mouse_pos = pygame.mouse.get_pos()
#                 if check_continue_click(mouse_pos, continue_rect):
#                     controls_displayed = True  # Exit the loop and move to gameplay

#         clock.tick(60)

#     # Gameplay Phase: Implement controls, jumping effect with easing, and scrolling background
#     try:
#         while running:
#             current_time = time.time()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                     pygame.quit()
#                     sys.exit()

#             keys = pygame.key.get_pressed()

#             # Handle left movement with "A" key
#             if keys[pygame.K_a]:
#                 cat_x -= cat_speed
#                 if cat_facing_right:
#                     cat_img = pygame.transform.flip(cat_img, True, False)  # Flip to face left
#                     cat_facing_right = False

#             # Handle right movement with "D" key
#             if keys[pygame.K_d]:
#                 cat_x += cat_speed
#                 if not cat_facing_right:
#                     cat_img = pygame.transform.flip(cat_img, True, False)  # Flip to face right
#                     cat_facing_right = True

#             # Initiate jump when "W" is pressed and cat is not already jumping
#             if keys[pygame.K_w] and not is_jumping and not is_falling:
#                 is_jumping = True
#                 jump_start_time = current_time

#             # Update cat's rect for collision detection
#             cat_rect = pygame.Rect(cat_x, cat_y, cat_img.get_width(), cat_img.get_height())

#             # Check if the cat is standing on the platform or falling
#             if not platform_rect.colliderect(cat_rect):
#                 is_falling = True
#             else:
#                 is_falling = False

#             # Jumping or falling logic with easing effect
#             if is_jumping:
#                 time_in_jump = current_time - jump_start_time
#                 if time_in_jump < jump_duration:
#                     scroll_speed = base_scroll_speed * (1 - time_in_jump / jump_duration)
#                     scroll_offset += scroll_speed
#                 elif time_in_jump < 2 * jump_duration:
#                     scroll_speed = base_scroll_speed * ((time_in_jump - jump_duration) / jump_duration)
#                     scroll_offset -= scroll_speed
#                 else:
#                     is_jumping = False
#                     scroll_offset = 0
#             elif is_falling:
#                 scroll_offset -= base_scroll_speed  # Scroll upward to simulate falling

#             # Ensure the cat doesn't move off-screen
#             if cat_x < 0:
#                 cat_x = 0
#             elif cat_x > WIDTH - cat_img.get_width():
#                 cat_x = WIDTH - cat_img.get_width()

#             # Fill the screen by tiling the tower tile image with a scrolling effect
#             for x in range(0, WIDTH, tower_tile_img.get_width()):
#                 for y in range(-tower_tile_img.get_height(), HEIGHT, tower_tile_img.get_height()):
#                     screen.blit(tower_tile_img, (x, y + scroll_offset % tower_tile_img.get_height()))
                    
#             # Draw the platform with scrolling effect
#             screen.blit(platform_img, (platform_x, platform_y + scroll_offset))

#             # Draw the cat at the updated position
#             screen.blit(cat_img, (cat_x, cat_y))

#             pygame.display.flip()
#             clock.tick(24)

#     finally:
#         stop_mp3()  # Ensure any music stops when exiting

#     # End Phase placeholder - can be used for displaying end-of-game messages
#     screen.fill(screen_color)
#     draw_text("Game Over!", font, text_color, WIDTH // 2, HEIGHT // 3, center=True, enable_shadow=True)
#     continue_rect = draw_continue_button()
#     pygame.display.flip()

#     # Wait for "Continue..." click after game ends
#     waiting = True
#     while waiting:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 mouse_pos = pygame.mouse.get_pos()
#                 if check_continue_click(mouse_pos, continue_rect):
#                     waiting = False
# def bonus_game_tuna_tower():
#     # Check if the assets/images directory exists
#     if not os.path.exists('assets/images'):
#         log_entry = create_log_message("Assets folder 'assets/images' is missing. Returning to the main menu.")
#         log_message(log_entry)
#         return "main_menu"
    
#     # Calculate scaling factors based on the current resolution
#     scale_factor_x = WIDTH / REFERENCE_RESOLUTION[0]
#     scale_factor_y = HEIGHT / REFERENCE_RESOLUTION[1]
#     scale_factor = min(scale_factor_x, scale_factor_y)

#     GROUND_LEVEL = HEIGHT * 0.8  # Set the ground level

#     # Load tower tile image and scale it
#     tower_tile_img = pygame.image.load('assets/images/sprites/towertile01.png')
#     tower_tile_img = pygame.transform.scale(tower_tile_img, (int(64 * scale_factor), int(64 * scale_factor)))
    
#     # Load platform image and scale it
#     platform_img = pygame.image.load('assets/images/sprites/platform.jpg')
#     platform_img = pygame.transform.scale(platform_img, (int(200 * scale_factor), int(50 * scale_factor)))
    
#     # Load cat image and scale to double its original size
#     cat_img = pygame.image.load('assets/images/sprites/cat08.png')
#     cat_img = pygame.transform.scale(cat_img, (int(cat_img.get_width() * 2 * scale_factor), int(cat_img.get_height() * 2 * scale_factor)))
    
#     # Cat position and movement variables
#     cat_x = WIDTH // 2 - cat_img.get_width() // 2
#     cat_y = HEIGHT * 0.8 - cat_img.get_height()  # Fixed cat vertical position, slightly above ground level
#     cat_speed = 25 * scale_factor  # Speed for horizontal movement
#     cat_facing_right = True       # Track direction to manage flipping
#     is_falling = True             # Assume the cat starts falling
#     scroll_offset = 0            # Background/platform scrolling offset
#     base_scroll_speed = 20 * scale_factor  # Base speed for scrolling effect
#     cat_velocity_y = 0           # Vertical movement placeholder for controlling scroll speed

#     # Platform position and collision rect
#     platform_x = WIDTH // 2 - platform_img.get_width() // 2
#     platform_y = int(GROUND_LEVEL)
#     platform_width = platform_img.get_width()
#     platform_height = platform_img.get_height()

#     # Background scroll offset
#     scroll_offset = 0
#     gravity = 1 * scale_factor
#     jump_strength = -20 * scale_factor
#     on_platform = False

#     # Jumping state variables
#     is_jumping = False
#     jump_start_time = 0
#     jump_duration = 1  # Duration of jump up phase (in seconds)

#     # Gameplay Phase: Implement controls, jumping effect with easing, and scrolling background
#     running = True
#     try:
#         while running:
#             current_time = time.time()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                     pygame.quit()
#                     sys.exit()

#             keys = pygame.key.get_pressed()

#             # Handle left movement with "A" key
#             if keys[pygame.K_a]:
#                 cat_x -= cat_speed
#                 if cat_facing_right:
#                     cat_img = pygame.transform.flip(cat_img, True, False)  # Flip to face left
#                     cat_facing_right = False

#             # Handle right movement with "D" key
#             if keys[pygame.K_d]:
#                 cat_x += cat_speed
#                 if not cat_facing_right:
#                     cat_img = pygame.transform.flip(cat_img, True, False)  # Flip to face right
#                     cat_facing_right = True

#             # Initiate jump when "W" is pressed and cat is on the platform
#             if keys[pygame.K_w] and on_platform:
#                 cat_velocity_y = jump_strength
#                 on_platform = False

#             # Apply gravity if the cat is falling
#             if not on_platform:
#                 cat_velocity_y += gravity
#                 scroll_offset -= cat_velocity_y

#             # Update platform Y position based on scroll offset
#             platform_y_on_screen = platform_y + scroll_offset
#             platform_rect = pygame.Rect(platform_x, platform_y_on_screen, platform_width, platform_height)

#             # Update cat's rect for collision detection
#             cat_rect = pygame.Rect(cat_x, cat_y, cat_img.get_width(), cat_img.get_height())

#             # Platform collision logic
#             if cat_rect.colliderect(platform_rect):
#                 # Check if cat is falling and lands on top of the platform
#                 if cat_velocity_y > 0 and cat_rect.bottom > platform_rect.top and cat_rect.bottom - cat_velocity_y <= platform_rect.top:
#                     # Place cat on top of the platform by stopping the scroll at the right position
#                     scroll_offset = platform_y - (cat_y + cat_img.get_height())
#                     cat_velocity_y = 0
#                     on_platform = True
#                 # If the cat walks off the platform, it should start falling
#                 elif cat_rect.right < platform_rect.left or cat_rect.left > platform_rect.right:
#                     on_platform = False

#             # Ensure the cat doesn't move off-screen horizontally
#             if cat_x < 0:
#                 cat_x = 0
#             elif cat_x > WIDTH - cat_img.get_width():
#                 cat_x = WIDTH - cat_img.get_width()

#             # Fill the screen by tiling the tower tile image with a scrolling effect
#             screen.fill(screen_color)  # Clear the screen before drawing
#             for x in range(0, WIDTH, tower_tile_img.get_width()):
#                 for y in range(-tower_tile_img.get_height(), HEIGHT, tower_tile_img.get_height()):
#                     screen.blit(tower_tile_img, (x, y + scroll_offset % tower_tile_img.get_height()))

#             # Draw the platform
#             screen.blit(platform_img, (platform_x, platform_y_on_screen))

#             # Draw the cat at the updated position
#             screen.blit(cat_img, (cat_x, cat_y))

#             pygame.display.flip()
#             clock.tick(24)

#     finally:
#         stop_mp3()  # Ensure any music stops when exiting

#     # End Phase placeholder - can be used for displaying end-of-game messages
#     screen.fill(screen_color)
#     draw_text("Game Over!", font, text_color, WIDTH // 2, HEIGHT // 3, center=True, enable_shadow=True)
#     continue_rect = draw_continue_button()
#     pygame.display.flip()

#     # Wait for "Continue..." click after game ends
#     waiting = True
#     while waiting:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 mouse_pos = pygame.mouse.get_pos()
#                 if check_continue_click(mouse_pos, continue_rect):
#                     waiting = False
def bonus_game_tuna_tower():
    # Check if the assets/images directory exists
    if not os.path.exists('assets/images'):
        log_entry = create_log_message("Assets folder 'assets/images' is missing. Returning to the main menu.")
        log_message(log_entry)
        return "main_menu"
    
    # Calculate scaling factors based on the current resolution
    scale_factor_x = WIDTH / REFERENCE_RESOLUTION[0]
    scale_factor_y = HEIGHT / REFERENCE_RESOLUTION[1]
    scale_factor = min(scale_factor_x, scale_factor_y)

    GROUND_LEVEL = HEIGHT * 0.8  # Set the ground level

    # Load tower tile image and scale it
    tower_tile_img = pygame.image.load('assets/images/sprites/towertile01.png')
    tower_tile_img = pygame.transform.scale(tower_tile_img, (int(64 * scale_factor), int(64 * scale_factor)))
    
    # Load platform image and scale it
    platform_img = pygame.image.load('assets/images/sprites/platform.jpg')
    platform_img = pygame.transform.scale(platform_img, (int(200 * scale_factor), int(50 * scale_factor)))
    
    # Load cat image and scale to double its original size
    cat_img = pygame.image.load('assets/images/sprites/cat05.png')
    cat_img = pygame.transform.scale(cat_img, (int(cat_img.get_width() * 2 * scale_factor), int(cat_img.get_height() * 2 * scale_factor)))
    
    # Cat position and movement variables
    cat_x = WIDTH // 2 - cat_img.get_width() // 2
    cat_y = HEIGHT * 0.8 - cat_img.get_height()  # Fixed cat vertical position, slightly above ground level
    cat_speed = 25 * scale_factor  # Speed for horizontal movement
    cat_facing_right = True       # Track direction to manage flipping
    scroll_offset = 0            # Background/platform scrolling offset
    cat_velocity_y = 0           # Vertical movement placeholder for controlling scroll speed

    # Gravity and jumping variables
    gravity = 1 * scale_factor
    jump_strength = -20 * scale_factor
    on_platform = False

    # Platform positions and properties
    platforms = [
        {"x": WIDTH // 2 - platform_img.get_width() // 2, "y": int(GROUND_LEVEL)},
        {"x": WIDTH // 2 + 150, "y": int(GROUND_LEVEL) - 150},  # New platform above and to the right
    ]

    # Gameplay Phase: Implement controls, jumping effect with easing, and scrolling background
    running = True
    try:
        while running:
            # current_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            # Handle left movement with "A" key
            if keys[pygame.K_a]:
                cat_x -= cat_speed
                if cat_facing_right:
                    cat_img = pygame.transform.flip(cat_img, True, False)  # Flip to face left
                    cat_facing_right = False

            # Handle right movement with "D" key
            if keys[pygame.K_d]:
                cat_x += cat_speed
                if not cat_facing_right:
                    cat_img = pygame.transform.flip(cat_img, True, False)  # Flip to face right
                    cat_facing_right = True

            # Initiate jump when "W" is pressed and cat is on the platform
            if keys[pygame.K_w] and on_platform:
                cat_velocity_y = jump_strength
                on_platform = False

            # Apply gravity if the cat is falling
            if not on_platform:
                cat_velocity_y += gravity
                scroll_offset -= cat_velocity_y

            # Update cat's rect for collision detection
            cat_rect = pygame.Rect(cat_x, cat_y, cat_img.get_width(), cat_img.get_height())

            # Platform collision detection phase
            platform_to_land_on = None
            for platform in platforms:
                platform_x = platform["x"]
                platform_y_on_screen = platform["y"] + scroll_offset
                platform_rect = pygame.Rect(platform_x, platform_y_on_screen, platform_img.get_width(), platform_img.get_height())

                # Check if the cat is falling and collides with a platform
                if cat_velocity_y > 0 and cat_rect.colliderect(platform_rect):
                    if cat_rect.bottom > platform_rect.top and cat_rect.bottom - cat_velocity_y <= platform_rect.top:
                        if platform_to_land_on is None or platform_y_on_screen < platform_to_land_on["y"]:
                            platform_to_land_on = {"x": platform_x, "y": platform_y_on_screen}

            # Landing phase (apply landing response)
            if platform_to_land_on:
                # Align the cat's bottom to the top of the platform smoothly
                scroll_offset = platform_to_land_on["y"] - (cat_y + cat_img.get_height())
                cat_velocity_y = 0
                on_platform = True
            else:
                on_platform = False

            # Ensure the cat doesn't move off-screen horizontally
            if cat_x < 0:
                cat_x = 0
            elif cat_x > WIDTH - cat_img.get_width():
                cat_x = WIDTH - cat_img.get_width()

            # Fill the screen by tiling the tower tile image with a scrolling effect
            screen.fill(screen_color)  # Clear the screen before drawing
            for x in range(0, WIDTH, tower_tile_img.get_width()):
                for y in range(-tower_tile_img.get_height(), HEIGHT, tower_tile_img.get_height()):
                    screen.blit(tower_tile_img, (x, y + scroll_offset % tower_tile_img.get_height()))

            # Draw all platforms
            for platform in platforms:
                platform_x = platform["x"]
                platform_y_on_screen = platform["y"] + scroll_offset
                screen.blit(platform_img, (platform_x, platform_y_on_screen))

            # Draw the cat at the updated position
            screen.blit(cat_img, (cat_x, cat_y))

            pygame.display.flip()
            clock.tick(24)

    finally:
        stop_mp3()  # Ensure any music stops when exiting

    # End Phase placeholder - can be used for displaying end-of-game messages
    screen.fill(screen_color)
    draw_text("Game Over!", font, text_color, WIDTH // 2, HEIGHT // 3, center=True, enable_shadow=True)
    continue_rect = draw_continue_button()
    pygame.display.flip()

    # Wait for "Continue..." click after game ends
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False


# TODO For later use
def bonus_game_generic():
    # Check if the assets/images directory exists
    if not os.path.exists('assets/images'):
        log_entry = create_log_message("Assets folder 'assets/images' is missing. Returning to the main menu.")
        log_message(log_entry)
        return "main_menu"
    
    # Calculate scaling factors based on the current resolution
    scale_factor_x = WIDTH / REFERENCE_RESOLUTION[0]
    scale_factor_y = HEIGHT / REFERENCE_RESOLUTION[1]
    scale_factor = min(scale_factor_x, scale_factor_y)

    # GROUND_LEVEL = HEIGHT * 0.8  # Set the ground level

    # Control display phase setup
    running = True
    controls_displayed = False
    # start_time = time.time()

    # Load any background and platform images if needed (placeholder for future customization)
    bonus_mode_background = select_random_background("assets/images/bonus_mode")

    # Display control instructions
    while not controls_displayed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background (or fallback to navy blue)
        if bonus_mode_background:
            draw_background(bonus_mode_background)
        else:
            screen.fill(screen_color)

        # Render the controls text
        draw_text("Controls:", font, text_color, 0, HEIGHT * 0.2, center=True, enable_shadow=True)
        draw_text("W = Jump", font, text_color, 0, HEIGHT * 0.4, center=True, enable_shadow=True)
        draw_text("A = Move Left", font, text_color, 0, HEIGHT * 0.6, center=True, enable_shadow=True)
        draw_text("D = Move Right", font, text_color, 0, HEIGHT * 0.8, center=True, enable_shadow=True)

        # Render the bouncing "Bonus Stage!" text
        text_x, text_y = WIDTH // 2 - int(175 * scale_factor), HEIGHT // 2
        text_dx, text_dy = random.choice([-10, 10]), random.choice([-10, 10])
        text_dx *= scale_factor
        text_dy *= scale_factor
        text_surface = font.render("Bonus Stage!", True, text_color)
        screen.blit(text_surface, (text_x, text_y))

        # Draw the "Continue..." button
        continue_rect = draw_continue_button()
        pygame.display.flip()

        # Check for "Continue..." button click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    controls_displayed = True  # Exit the loop and move to gameplay

        clock.tick(60)

    # Placeholder for Gameplay Phase - can be customized as needed
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        running = False
                        return

            # Minimal gameplay phase setup - this can be replaced with future gameplay logic
            screen.fill(screen_color)  # Just a solid color background for now
            pygame.display.flip()
            clock.tick(24)

    finally:
        stop_mp3()  # Ensure any music stops when exiting

    # End Phase placeholder - can be used for displaying end-of-game messages
    screen.fill(screen_color)
    draw_text("Game Over!", font, text_color, WIDTH // 2, HEIGHT // 3, center=True, enable_shadow=True)
    continue_rect = draw_continue_button()
    pygame.display.flip()

    # Wait for "Continue..." click after game ends
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if check_continue_click(mouse_pos, continue_rect):
                    waiting = False


######################
## English section ###
######################

# def random_quote_display():
#     """
#     Selects a random quote, displays it on the screen, reads it aloud, 
#     and shows a 'Continue...' button with hover effects.
#     """
#     # Define a list of quotes
#     quotes = [
#         "The only limit to our realization of tomorrow is our doubts of today.",
#         "Success is not final, failure is not fatal: it is the courage to continue that counts."
#     ]
    
#     # Choose a random quote
#     selected_quote = random.choice(quotes)

#     # Clear the screen with the background color
#     screen.fill(screen_color)

#     # Draw the selected quote on the screen
#     draw_text(
#         selected_quote,
#         font,
#         text_color,
#         x=0,
#         y=HEIGHT * 0.4,
#         max_width=WIDTH * 0.9,
#         center=True,
#         enable_shadow=True,
#         shadow_color=shadow_color
#     )

#     # Update the display to show the quote
#     pygame.display.flip()

#     # Read the selected quote aloud using TTS
#     speak_english(selected_quote)

#     # Prepare for the "Continue..." button
#     button_font_size = int(get_dynamic_font_size() * 0.8)
#     if os.path.isfile(current_font_name_or_path):
#         button_font = pygame.font.Font(current_font_name_or_path, button_font_size)
#     else:
#         button_font = pygame.font.SysFont(current_font_name_or_path, button_font_size)

#     button_text = "Continue..."
#     hover_particles = []  # To store active hover particles
#     particle_count = 3
#     particle_lifetime = 30

#     # Initialize button_rect to avoid UnboundLocalError
#     button_rect = pygame.Rect(0, 0, 0, 0)

#     # Event loop for handling hover effects and the Continue button
#     waiting = True
#     while waiting:
#         # Clear the screen for a new frame
#         screen.fill(screen_color)

#         # Redraw the quote
#         draw_text(
#             selected_quote,
#             font,
#             text_color,
#             x=0,
#             y=HEIGHT * 0.4,
#             max_width=WIDTH * 0.9,
#             center=True,
#             enable_shadow=True,
#             shadow_color=shadow_color
#         )

#         # Draw the "Continue..." button
#         mouse_pos = pygame.mouse.get_pos()
#         button_rect = draw_text(
#             button_text,
#             button_font,
#             shadow_color if button_rect.collidepoint(mouse_pos) else text_color,
#             x=WIDTH * 0.55,
#             y=HEIGHT * 0.9,
#             enable_shadow=True,
#             shadow_color=shadow_color,
#             return_rect=True
#         )

#         # Handle hover particles for the button
#         if button_rect.collidepoint(mouse_pos):
#             for _ in range(particle_count):
#                 particle_color = random.choice([shadow_color, text_color, screen_color])
#                 particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
#                 particle.lifetime = particle_lifetime
#                 angle = random.uniform(0, 2 * math.pi)
#                 speed = random.uniform(1, 3)
#                 particle.dx = math.cos(angle) * speed
#                 particle.dy = math.sin(angle) * speed
#                 hover_particles.append(particle)

#         # Update and draw hover particles
#         for particle in hover_particles[:]:
#             particle.update()
#             particle.draw(screen)
#             if particle.lifetime <= 0:
#                 hover_particles.remove(particle)

#         # Update the display
#         pygame.display.flip()

#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 if button_rect.collidepoint(event.pos):
#                     waiting = False  # Exit the loop

#         # Cap the frame rate
#         clock.tick(60)
def random_quote_display():
    """
    Selects a random quote with an author, displays it on the screen, 
    reads it aloud, and shows a 'Continue...' button with hover effects.
    """
    # Define a list of quotes as tuples (quote, author)
    quotes = [
        ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("Oh farmers, pray that your summers be wet and your winters clear.", "Virgil"),
        ("Blessed be the fruit of thy cattle, the increase of thy kine, and the flocks of thy sheep.", "The Bible (Deuteronomy 28:4)"),
        ("Do not go where the path may lead, go instead where there is no path and leave a trail.", "Ralph Waldo Emerson"),
        ("In the middle of every difficulty lies opportunity.", "Albert Einstein"),
        ("Whatever you are, be a good one.", "Abraham Lincoln"),
        ("The best way to predict the future is to create it.", "Peter Drucker"),
        ("If you want to lift yourself up, lift up someone else.", "Booker T. Washington"),
        ("A journey of a thousand miles begins with a single step.", "Lao Tzu"),
        ("It is not the strongest of the species that survive, nor the most intelligent, but the one most responsive to change.", "Charles Darwin"),
        ("Education is the most powerful weapon which you can use to change the world.", "Nelson Mandela"),
        ("Whether you think you can or you think you can’t, you’re right.", "Henry Ford"),
        ("An unexamined life is not worth living.", "Socrates"),
        ("Happiness is not something ready-made. It comes from your own actions.", "Dalai Lama"),
        ("You must be the change you wish to see in the world.", "Mahatma Gandhi"),
        ("What you get by achieving your goals is not as important as what you become by achieving your goals.", "Zig Ziglar"),
        ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Edison"),
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("It always seems impossible until it’s done.", "Nelson Mandela"),
        ("To handle yourself, use your head; to handle others, use your heart.", "Eleanor Roosevelt"),
        ("The purpose of our lives is to be happy.", "Dalai Lama"),
        ("Life is what happens when you’re busy making other plans.", "John Lennon"),
        ("If you look at what you have in life, you’ll always have more.", "Oprah Winfrey"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("Tell me and I forget. Teach me and I remember. Involve me and I learn.", "Benjamin Franklin")
    ]

    
    # Choose a random quote
    selected_quote, author = random.choice(quotes)

    # Clear the screen with the background color
    screen.fill(screen_color)

    # Draw the selected quote on the screen
    draw_text(
        selected_quote,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.2,  # Adjust position for quote
        max_width=WIDTH * 0.9,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Draw the author below the quote
    draw_text(
        f"- {author}",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.8,  # Adjust position for author
        max_width=WIDTH * 0.9,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Update the display to show the quote and author
    pygame.display.flip()

    # Read the selected quote aloud using TTS
    speak_english(f"{selected_quote} by {author}")

    # Prepare for the "Continue..." button
    button_font_size = int(get_dynamic_font_size() * 0.8)
    if os.path.isfile(current_font_name_or_path):
        button_font = pygame.font.Font(current_font_name_or_path, button_font_size)
    else:
        button_font = pygame.font.SysFont(current_font_name_or_path, button_font_size)

    button_text = "Continue..."
    hover_particles = []  # To store active hover particles
    particle_count = 3
    particle_lifetime = 30

    # Initialize button_rect to avoid UnboundLocalError
    button_rect = pygame.Rect(0, 0, 0, 0)

    # Event loop for handling hover effects and the Continue button
    waiting = True
    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Redraw the quote
        draw_text(
            selected_quote,
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.2,  # Adjust position for quote
            max_width=WIDTH * 0.9,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Redraw the author
        draw_text(
            f"- {author}",
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.8,  # Adjust position for author
            max_width=WIDTH * 0.9,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Draw the "Continue..." button
        mouse_pos = pygame.mouse.get_pos()
        button_rect = draw_text(
            button_text,
            button_font,
            shadow_color if button_rect.collidepoint(mouse_pos) else text_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color,
            return_rect=True
        )

        # Handle hover particles for the button
        if button_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                hover_particles.append(particle)

        # Update and draw hover particles
        for particle in hover_particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                hover_particles.remove(particle)

        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        # Cap the frame rate
        clock.tick(60)



##############################
### Math Problem Functions ###
##############################

def warm_up_math(session_id):
    """
    Selects and runs a random math warm-up lesson.

    This function randomly chooses one of the available math warm-up lessons
    and executes it. Each lesson provides practice with a different math skill.
    It gathers the results of the lesson, including questions asked, correct answers,
    and average response time, for cumulative tracking.

    Args:
        session_id (int): The session identifier for tracking progress.

    Returns:
        tuple: A summary of the session with total questions, total correct answers,
               and average response time across all lessons.
    """
    # Debug
    log_message(create_log_message("Warm up math begins."))
    
    math_lessons = [
        rainbow_numbers,
        single_digit_addition,
        single_digit_subtraction,
        single_digit_multiplication
    ]
    
    selected_lesson = random.choice(math_lessons)
    lesson_result = selected_lesson(session_id)

    if lesson_result is not None:
        questions_asked, correct_answers, avg_time = lesson_result
        return questions_asked, correct_answers, avg_time
    else:
        log_message(f"Error: {selected_lesson.__name__} did not return a valid result.")
        return 0, 0, 0  # Return defaults if an error occurs


def display_rainbow_math_problem(num1, 
                                 num2, 
                                 user_input, 
                                 first_input, 
                                 line_length_factor=2.5):
    screen.fill(screen_color)
    
    # Dynamically calculate positions based on screen size
    right_x = WIDTH * 0.55  # Right edge for alignment
    num1_y = HEIGHT * 0.4
    num2_y = HEIGHT * 0.5
    line_y = HEIGHT * 0.60
    sum_y = HEIGHT * 0.63
    
    # Draw the first number (right-aligned)
    num1_text = str(num1)
    num1_width = font.size(num1_text)[0]
    draw_text(
        num1_text,
        font,
        text_color, 
        right_x - num1_width, 
        num1_y, 
        center=False, 
        enable_shadow=True
    )

    # Draw the plus sign, aligned to num1's position
    plus_sign_x = right_x - num1_width - WIDTH * 0.1
    draw_text(
        "+", font, text_color, plus_sign_x, num2_y, center=False, enable_shadow=True
    )

    # Draw the second number or input placeholder (right-aligned)
    input_text = "?" if first_input else str(user_input)
    input_width = font.size(input_text)[0]
    draw_text(
        input_text, font, text_color, right_x - input_width, num2_y, center=False, enable_shadow=True
    )

    # Calculate line width based on max width of elements
    max_width = max(num1_width, input_width, font.size(str(num1 + num2))[0])
    line_width = max_width * line_length_factor

    # Draw shadow for the answer line
    shadow_offset = 3  # Offset for the shadow effect
    pygame.draw.line(screen, shadow_color, 
                     (right_x - line_width + shadow_offset, line_y + shadow_offset), 
                     (right_x + shadow_offset, line_y + shadow_offset), 3)
    
    # Draw the actual answer line (sum line)
    pygame.draw.line(screen, text_color, (right_x - line_width, line_y), (right_x, line_y), 3)

    # Draw the sum (right-aligned)
    sum_text = str(num1 + num2)
    sum_width = font.size(sum_text)[0]
    draw_text(
        sum_text, font, text_color, right_x - sum_width, sum_y, center=False, enable_shadow=True
    )

    pygame.display.flip()


def display_result(result_text, image_folder=None, use_lightning=False):
    """
    Display the result text and an optional image from the given folder.
    If an image is provided and 'use_lightning' is True, show lightning instead of particles.
    If 'use_lightning' is False, show a particle effect.
    """
    # global shadow_color
    
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
    global current_student
    
    # Debug
    log_message(create_log_message("Rainbow numbers begins."))
    
    # Initialize the clock for controlling frame rate
    clock = pygame.time.Clock()

    # Connect to the database 
    connection, cursor = get_database_cursor()
    # Retrieve lesson_id for "Rainbow Numbers"
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Rainbow Numbers',))
    result = cursor.fetchone()
    if result:
        rainbow_cats_lesson_id = result[0]
    else:
        log_entry = create_log_message("Rainbow Numbers lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return -1
    cursor.close()
    connection.close()

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Rainbow Numbers')

    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Rainbow Numbers', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

    # Particle effect settings
    particle_count = 3
    particle_lifetime = 30
    particles = []

    # Display the introductory message
    waiting = True
    skip_clicked = False

    # Render the screen for the introductory message
    screen.fill(screen_color)

    # Draw the lesson intro text
    draw_text(
        "Let's work on Rainbow Numbers!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True
    )

    # Draw the "Continue..." button
    continue_rect = draw_continue_button()

    # Draw the "Skip..." button if applicable
    skip_rect = None
    if perfect_score_yesterday:
        skip_rect = draw_skip_button()

    pygame.display.flip()  # Render the introductory screen

    # Play TTS once after rendering the screen
    speak_english("Let's work on Rainbow Numbers!")

    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Redraw the lesson intro text
        draw_text(
            "Let's work on Rainbow Numbers!",
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.4,
            max_width=WIDTH * 0.95,
            center=True,
            enable_shadow=True
        )

        # Redraw the "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(pygame.mouse.get_pos()) else text_color
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Handle hover color and particles for "Skip..." button
        mouse_pos = pygame.mouse.get_pos()
        if skip_rect:
            if skip_rect.collidepoint(mouse_pos):
                draw_skip_button(hovered_over=True)
            else:
                draw_skip_button(hovered_over=False)

        # Generate particles if hovering over "Continue..." or "Skip..."
        if continue_rect.collidepoint(mouse_pos) or (skip_rect and skip_rect.collidepoint(mouse_pos)):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if "Continue..." button is clicked
                if continue_rect.collidepoint(event.pos):
                    waiting = False

                # Check if "Skip..." button is clicked
                elif skip_rect and skip_rect.collidepoint(event.pos):
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

        # Cap the frame rate
        clock.tick(60)

    # If skip was clicked, record session with NULL values for scores and return early
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()

            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert the session lesson with NULL values for performance metrics
            cursor.execute('''
                INSERT INTO session_lessons (
                    session_id, lesson_id, start_time, end_time,
                    total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, rainbow_cats_lesson_id, current_time, current_time,
                None, None, None, None, None  # NULL values for performance metrics
            ))

            connection.commit()
            log_entry = create_log_message("Session recorded as skipped with NULL values.")
            log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()

        finally:
            cursor.close()
            connection.close()

        return 0, 0, None  # Return default values if the lesson was skipped

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

    # Clear the screen with the background color from the theme/config
    screen.fill(screen_color)
    
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
    
    # Particle effect settings
    particles = []  # To store active particles
    particle_count = 3  # Number of particles generated per frame
    particle_lifetime = 30  # Lifetime of each particle
    
    # Event loop for handling "Continue..." interactions
    while True:
        # Clear the screen for a new frame
        screen.fill(screen_color)
    
        # Redraw the final score message
        draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)
        if completion_times:
            draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)
            if correct_answers == total_questions:
                draw_text(perfect_score_message, font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
                if average_time < 3.0:
                    draw_text(mastery_message, font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)
    
        # Draw the "Continue..." button
        continue_rect = draw_continue_button()
    
        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()
    
        # Determine hover color for "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color
    
        # Redraw the "Continue..." button with hover effect
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )
    
        # Generate particles if hovering over the "Continue..." button
        if continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):  # Limit particle generation per frame
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)
    
        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)
    
        pygame.display.flip()  # Update the display
    
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_rect.collidepoint(event.pos):
                    if correct_answers == total_questions:
                        bonus_game_selector()
                    return total_questions, correct_answers, average_time
    
        # Cap the frame rate
        clock.tick(60)


def generate_math_problem(min_val, max_val, operation="add"):
    """Generates two random numbers within the given range and returns the 
    problem and the answer."""
    num1 = random.randint(min_val, max_val)
    num2 = random.randint(min_val, max_val)
    
    if operation == "sub" and num1 < num2:
        # Ensure num1 is always larger to avoid negative answers
        num1, num2 = num2, num1  
    
    if operation == "add":
        answer = num1 + num2
    elif operation == "sub":
        answer = num1 - num2
    elif operation == "mul":
        answer = num1 * num2
    else:
        raise ValueError("Unsupported operation. Use 'add', 'sub', or 'mul'.")
    
    return num1, num2, answer


def display_math_problem(num1, num2, user_input, first_input, operation="add"):
    screen.fill(screen_color)

    # Control for minimum answer line width
    min_line_width = 150  # Adjust this value as needed

    # Dynamically calculate positions based on screen size
    right_x = WIDTH * 0.55  # Right edge for alignment
    num1_y = HEIGHT * 0.4
    num2_y = HEIGHT * 0.5
    line_y = HEIGHT * 0.60
    sum_y = HEIGHT * 0.65

    # Draw the first number (right-aligned)
    num1_text = str(num1)
    num1_width = font.size(num1_text)[0]
    draw_text(num1_text, 
              font,
              text_color, 
              right_x - num1_width, 
              num1_y, 
              center=False, 
              enable_shadow=True)

    # Determine the operation sign and adjust position
    if operation == "add":
        operator_sign = "+"
    elif operation == "sub":
        operator_sign = "-"
    elif operation == "mul":
        operator_sign = "×"
    else:
        raise ValueError("Unsupported operation. Use 'add', 'sub', or 'mul'.")

    # Operator sign, aligned to num1's position with a slight offset
    operator_sign_x = right_x - num1_width - WIDTH * 0.1
    draw_text(operator_sign, 
              font, 
              text_color, 
              operator_sign_x, 
              num2_y, 
              center=False, 
              enable_shadow=True)

    # Draw the second number (right-aligned)
    num2_text = str(num2)
    num2_width = font.size(num2_text)[0]
    draw_text(num2_text, 
              font, 
              text_color, 
              right_x - num2_width, 
              num2_y, 
              center=False, 
              enable_shadow=True)

    # Calculate line width based on max width of elements
    max_width = max(num1_width, num2_width, font.size(str(num1 + num2))[0])
    # Ensures line width is at least min_line_width
    line_width = max(max_width * 1.5, min_line_width)  

    # Draw shadow for the answer line
    shadow_offset = 2
    pygame.draw.line(screen, 
                     shadow_color, 
                     (right_x * 1.05 - line_width + shadow_offset, 
                      line_y + shadow_offset), 
                     (right_x * 1.05 + shadow_offset, 
                      line_y + shadow_offset), 
                     3)

    # Draw the actual answer line (sum line)
    pygame.draw.line(screen, 
                     text_color, 
                     (right_x * 1.05 - line_width, line_y), 
                     (right_x * 1.05, line_y), 
                     3)

    # Draw the sum placeholder or the user input (right-aligned)
    input_text = "?" if first_input else str(user_input)
    input_width = font.size(input_text)[0]
    draw_text(input_text, 
              font, 
              text_color, 
              right_x - input_width, 
              sum_y, 
              center=False, 
              enable_shadow=True)

    # Refresh the display
    pygame.display.flip()


def single_digit_addition(session_id):
    """Presents a single-digit addition quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Initialize the clock for frame rate control
    clock = pygame.time.Clock()

    # Retrieve the lesson_id for Single Digit Addition
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single Digit Addition',))
    result = cursor.fetchone()

    if result:
        addition_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single Digit Addition lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, None  # Return default values if lesson ID not found

    cursor.close()
    connection.close()

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Single Digit Addition')

    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Single Digit Addition', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

    # Particle effect settings
    particles = []
    particle_count = 3
    particle_lifetime = 30

    # Track hover states and frame rendering
    hovered_continue = False  # Ensures particles only generate after a valid hover
    interaction_ready = False  # Wait for the first frame to render properly

    # Display the introductory message
    waiting = True
    skip_clicked = False

    # Frame counter to delay hover effects
    frames_since_display = 0

    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Draw the introductory text
        draw_text(
            "Let's work on Single-Digit Addition!",
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.4,
            max_width=WIDTH * 0.95,
            center=True,
            enable_shadow=True
        )

        # Draw the "Continue..." button
        continue_rect = draw_continue_button()

        # Draw the "Skip..." button if applicable
        skip_rect = None
        if perfect_score_yesterday:
            skip_rect = draw_skip_button()

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Enable hover logic only after a few frames
        if frames_since_display > 10:
            interaction_ready = True

        if interaction_ready:
            # Determine hover color for "Continue..." button
            continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

            # Redraw the "Continue..." button with hover effect
            draw_text(
                "Continue...",
                pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
                continue_color,
                x=WIDTH * 0.55,
                y=HEIGHT * 0.9,
                enable_shadow=True,
                shadow_color=shadow_color
            )

            # Determine hover color for "Skip..." button
            if skip_rect:
                # skip_color = shadow_color if skip_rect.collidepoint(mouse_pos) else text_color
                if skip_rect.collidepoint(mouse_pos):
                    draw_skip_button(hovered_over=True)
                else:
                    draw_skip_button(hovered_over=False)

            # Generate particles if hovering over "Continue..." or "Skip..." buttons
            if continue_rect.collidepoint(mouse_pos):
                hovered_continue = True  # Track hover state
                for _ in range(particle_count):  # Limit particle generation per frame
                    particle_color = random.choice([shadow_color, text_color, screen_color])
                    particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                    particle.lifetime = particle_lifetime
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 3)
                    particle.dx = math.cos(angle) * speed
                    particle.dy = math.sin(angle) * speed
                    particles.append(particle)

            if skip_rect and skip_rect.collidepoint(mouse_pos):
                for _ in range(particle_count):  # Limit particle generation per frame
                    particle_color = random.choice([shadow_color, text_color, screen_color])
                    particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                    particle.lifetime = particle_lifetime
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 3)
                    particle.dx = math.cos(angle) * speed
                    particle.dy = math.sin(angle) * speed
                    particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if "Continue..." button is clicked
                if continue_rect.collidepoint(event.pos):
                    waiting = False
                # Check if "Skip..." button is clicked
                elif skip_rect and skip_rect.collidepoint(event.pos):
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

        # Increment frame counter
        frames_since_display += 1

        # Cap the frame rate
        clock.tick(60)

    # If skip was clicked, record session with NULL values for scores and return early
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()

            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert the session lesson with NULL values for performance metrics
            cursor.execute('''
                INSERT INTO session_lessons (
                    session_id, lesson_id, start_time, end_time,
                    total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, addition_lesson_id, current_time, current_time,
                None, None, None, None, None  # NULL values for performance metrics
            ))

            connection.commit()
            log_entry = create_log_message("Session recorded as skipped with NULL values.")
            log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()

        finally:
            cursor.close()
            connection.close()

        return 0, 0, None  # Return default values if the lesson was skipped

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(1, 9)
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)
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
                    elif event.unicode.isdigit() and len(user_input) < 2:
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

    # Display the final score
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

    # Handle the final "Continue..." button
    frames_since_display = 0  # Reset frame counter
    hovered_continue = False
    while True:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Redraw final score and messages
        draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)
        if completion_times:
            draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True, max_width=WIDTH)
        if correct_answers == total_questions:
            draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
            if average_time < 3.0:
                draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

        # Draw the "Continue..." button
        continue_rect = draw_continue_button()

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover color for "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the "Continue..." button with hover effect
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate particles if hovering over the "Continue..." button
        if frames_since_display > 10:  # Prevent particles during the first 10 frames
            if continue_rect.collidepoint(mouse_pos):
                if not hovered_continue:  # Only allow particles after the first hover detection
                    hovered_continue = True
                for _ in range(particle_count):  # Limit particle generation per frame
                    particle_color = random.choice([shadow_color, text_color, screen_color])
                    particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                    particle.lifetime = particle_lifetime
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 3)
                    particle.dx = math.cos(angle) * speed
                    particle.dy = math.sin(angle) * speed
                    particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_rect.collidepoint(event.pos):
                    if correct_answers == total_questions:
                        bonus_game_selector()
                    return total_questions, correct_answers, average_time

        # Increment frame counter
        frames_since_display += 1

        # Cap the frame rate
        clock.tick(60)


def double_digit_addition(session_id):
    """Presents a double-digit addition quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student
    
    # Debug
    log_message(create_log_message("Double digit addition begins."))

    # Initialize the clock for frame rate control
    clock = pygame.time.Clock()

    # Retrieve the lesson_id for Double Digit Addition
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Double Digit Addition',))
    result = cursor.fetchone()

    if result:
        addition_lesson_id = result[0]
    else:
        log_entry = create_log_message("Double Digit Addition lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, None  # Return default values if lesson ID not found

    cursor.close()
    connection.close()

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Double Digit Addition')

    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Double Digit Addition', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

    # Particle effect settings
    particles = []
    particle_count = 3
    particle_lifetime = 30

    # Display the introductory message
    waiting = True
    skip_clicked = False

    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Draw the introductory text
        draw_text(
            "Let's work on Double-Digit Addition!",
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.4,
            max_width=WIDTH * 0.95,
            center=True,
            enable_shadow=True
        )

        # Draw the "Continue..." button
        continue_rect = draw_continue_button()

        # Draw the "Skip..." button if applicable
        skip_rect = None
        if perfect_score_yesterday:
            skip_rect = draw_skip_button()

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover color for "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the "Continue..." button with hover effect
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Determine hover color for "Skip..." button
        if skip_rect:
            # skip_color = shadow_color if skip_rect.collidepoint(mouse_pos) else text_color
            if skip_rect.collidepoint(mouse_pos):
                draw_skip_button(hovered_over=True)
            else:
                draw_skip_button(hovered_over=False)

        # Generate particles if hovering over "Continue..." or "Skip..."
        if continue_rect.collidepoint(mouse_pos) or (skip_rect and skip_rect.collidepoint(mouse_pos)):
            for _ in range(particle_count):  # Limit particle generation per frame
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if "Continue..." button is clicked
                if continue_rect.collidepoint(event.pos):
                    waiting = False
                # Check if "Skip..." button is clicked
                elif skip_rect and skip_rect.collidepoint(event.pos):
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

        # Cap the frame rate
        clock.tick(60)

    # If skip was clicked, record session with NULL values for scores and return early
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()

            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert the session lesson with NULL values for performance metrics
            cursor.execute('''
                INSERT INTO session_lessons (
                    session_id, lesson_id, start_time, end_time,
                    total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, addition_lesson_id, current_time, current_time,
                None, None, None, None, None  # NULL values for performance metrics
            ))

            connection.commit()
            log_entry = create_log_message("Session recorded as skipped with NULL values.")
            log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()

        finally:
            cursor.close()
            connection.close()

        return 0, 0, None  # Return default values if the lesson was skipped

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    while problem_count < total_questions:
        num1, num2, answer = generate_math_problem(10, 99)
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)
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

    # Display the final score
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

    # Add hover effects and particles for "Continue..."
    while True:
        screen.fill(screen_color)

        # Redraw final messages
        draw_text(final_message, font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)
        if completion_times:
            draw_text(average_time_message, font, text_color, WIDTH // 2, HEIGHT * 0.6, center=True, enable_shadow=True)
        if correct_answers == total_questions:
            draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
            if average_time < 3.0:
                draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

        # Draw the "Continue..." button
        continue_rect = draw_continue_button()

        # Hover effects for the "Continue..." button
        mouse_pos = pygame.mouse.get_pos()
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate particles on hover
        if continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_rect.collidepoint(event.pos):
                    if correct_answers == total_questions:
                        bonus_game_selector()
                    return total_questions, correct_answers, average_time

        clock.tick(60)


def triple_digit_addition(session_id):
    """Presents a triple-digit addition quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Triple Digit Addition
    connection, cursor = get_database_cursor()
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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def quad_digit_addition(session_id):
    """Presents a four-digit addition quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Quad Digit Addition
    connection, cursor = get_database_cursor()
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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def single_digit_subtraction(session_id):
    """Presents a single-digit subtraction quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Single Digit Subtraction
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single Digit Subtraction',))
    result = cursor.fetchone()
    
    if result:
        subtraction_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single Digit Subtraction lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, None  # Return default values if lesson ID not found

    cursor.close()
    connection.close()

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Single Digit Subtraction')
    
    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Single Digit Subtraction', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

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
        enable_shadow=True
    )

    # Draw the "Continue..." and, if applicable, "Skip..." buttons
    continue_rect = draw_continue_button()
    skip_rect = None
    if perfect_score_yesterday:
        skip_rect = draw_skip_button()
    pygame.display.flip()

    # Event loop to wait for the "Continue..." or "Skip..." button click
    waiting = True
    skip_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if continue_rect.collidepoint(mouse_pos):
                    waiting = False
                elif skip_rect and skip_rect.collidepoint(mouse_pos):
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

    # If skip was clicked, record session with NULL values for scores and return early
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()
            
            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert the session lesson with NULL values for performance metrics
            cursor.execute('''
                INSERT INTO session_lessons (
                    session_id, lesson_id, start_time, end_time,
                    total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, subtraction_lesson_id, current_time, current_time,
                None, None, None, None, None  # NULL values for performance metrics
            ))
            
            connection.commit()
            log_entry = create_log_message("Session recorded as skipped with NULL values.")
            log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()
        
        finally:
            cursor.close()
            connection.close()
        
        return 0, 0, None  # Return default values if the lesson was skipped

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
                    elif event.unicode.isdigit() and len(user_input) < 1:  # Limit input to one digit
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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def double_digit_subtraction(session_id):
    """Presents a double-digit subtraction quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student
    
    # Debug
    log_message(create_log_message("Double digit subtraction begins."))

    # Retrieve the lesson_id for Double Digit Subtraction
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Double Digit Subtraction',))
    result = cursor.fetchone()
    
    if result:
        subtraction_lesson_id = result[0]
    else:
        log_entry = create_log_message("Double Digit Subtraction lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, None  # Return default values if lesson ID not found

    cursor.close()
    connection.close()

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Double Digit Subtraction')
    
    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Double Digit Subtraction', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

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
        enable_shadow=True
    )

    # Draw the "Continue..." and, if applicable, "Skip..." buttons
    continue_rect = draw_continue_button()
    skip_rect = None
    if perfect_score_yesterday:
        skip_rect = draw_skip_button()
    pygame.display.flip()

    # Event loop to wait for the "Continue..." or "Skip..." button click
    waiting = True
    skip_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if continue_rect.collidepoint(mouse_pos):
                    waiting = False
                elif skip_rect and skip_rect.collidepoint(mouse_pos):
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

    # If skip was clicked, record session with NULL values for scores and return early
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()
            
            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert the session lesson with NULL values for performance metrics
            cursor.execute('''
                INSERT INTO session_lessons (
                    session_id, lesson_id, start_time, end_time,
                    total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, subtraction_lesson_id, current_time, current_time,
                None, None, None, None, None  # NULL values for performance metrics
            ))
            
            connection.commit()
            log_entry = create_log_message("Session recorded as skipped with NULL values.")
            log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()
        
        finally:
            cursor.close()
            connection.close()
        
        return 0, 0, None  # Return default values if the lesson was skipped

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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def triple_digit_subtraction(session_id):
    """Presents a triple-digit subtraction quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Triple Digit Subtraction
    connection, cursor = get_database_cursor()
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
        # shadow_color=shadow_color
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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def quad_digit_subtraction(session_id):
    """Presents a quad-digit subtraction quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Quad Digit Subtraction
    connection, cursor = get_database_cursor()
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
        # shadow_color=shadow_color
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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def subtraction_borrowing(session_id):
    """Presents a double-digit subtraction quiz with borrowing and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Subtraction with Borrowing
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Subtraction Borrowing',))
    result = cursor.fetchone()
    
    if result:
        subtraction_lesson_id = result[0]
    else:
        log_entry = create_log_message("Subtraction Borrowing lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, None  # Return default values if lesson ID not found

    cursor.close()
    connection.close()

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Subtraction Borrowing')
    
    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Subtraction Borrowing', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

    # Display the introductory message
    screen.fill(screen_color)
    draw_text(
        "Let's work on Subtraction Borrowing!",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True
    )

    # Draw the "Continue..." and, if applicable, "Skip..." buttons
    continue_rect = draw_continue_button()
    skip_rect = None
    if perfect_score_yesterday:
        skip_rect = draw_skip_button()
    pygame.display.flip()

    # Event loop to wait for the "Continue..." or "Skip..." button click
    waiting = True
    skip_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if continue_rect.collidepoint(mouse_pos):
                    waiting = False
                elif skip_rect and skip_rect.collidepoint(mouse_pos):
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

    # If skip was clicked, record session with NULL values for scores and return early
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()
            
            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert the session lesson with NULL values for performance metrics
            cursor.execute('''
                INSERT INTO session_lessons (
                    session_id, lesson_id, start_time, end_time,
                    total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, subtraction_lesson_id, current_time, current_time,
                None, None, None, None, None  # NULL values for performance metrics
            ))
            
            connection.commit()
            log_entry = create_log_message("Session recorded as skipped with NULL values.")
            log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()
        
        finally:
            cursor.close()
            connection.close()
        
        return 0, 0, None  # Return default values if the lesson was skipped

    # Start the lesson timer
    lesson_start_time = time.time()

    correct_answers = 0
    problem_count = 0
    total_questions = 5
    completion_times = []

    clock = pygame.time.Clock()

    while problem_count < total_questions:
        # Generate a subtraction problem that requires borrowing
        num1, num2, answer = generate_borrowing_problem()
        user_input = ""
        first_input = True
        question_complete = False

        # Start the timer for the question
        start_time = time.time()

        while not question_complete:
            screen.fill(screen_color)
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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def generate_borrowing_problem():
    """Generates a double-digit subtraction problem that requires borrowing."""
    # Generate num1 ensuring it does not end in 9
    num1 = random.randint(10, 99)
    while num1 % 10 == 9:
        num1 = random.randint(10, 99)

    # Generate num2 ensuring it ends with a larger digit than num1 and is less than num1
    num2 = random.randint(1, num1 - 1)
    while (num2 % 10) <= (num1 % 10):
        num2 = random.randint(1, num1 - 1)

    answer = num1 - num2
    return num1, num2, answer


def single_digit_multiplication(session_id):
    """Presents a single-digit multiplication quiz with random numbers and updates the session results."""
    global current_student  # Access the global current student

    # Debug
    log_message(create_log_message("Single digit multiplication begins."))
    
    # Retrieve the lesson_id for Single Digit Multiplication
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single Digit Multiplication',))
    result = cursor.fetchone()
    
    if result:
        multiplication_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single Digit Multiplication lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, None  # Return default values if lesson ID not found

    cursor.close()
    connection.close()

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Single Digit Multiplication')
    
    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Single Digit Multiplication', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

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
        enable_shadow=True
    )

    # Draw the "Continue..." and, if applicable, "Skip..." buttons
    continue_rect = draw_continue_button()
    skip_rect = None
    if perfect_score_yesterday:
        skip_rect = draw_skip_button()
    pygame.display.flip()

    # Event loop to wait for the "Continue..." or "Skip..." button click
    waiting = True
    skip_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if continue_rect.collidepoint(mouse_pos):
                    waiting = False
                elif skip_rect and skip_rect.collidepoint(mouse_pos):
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

    # If skip was clicked, record session with NULL values for scores and return early
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()
            
            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert the session lesson with NULL values for performance metrics
            cursor.execute('''
                INSERT INTO session_lessons (
                    session_id, lesson_id, start_time, end_time,
                    total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, multiplication_lesson_id, current_time, current_time,
                None, None, None, None, None  # NULL values for performance metrics
            ))
            
            connection.commit()
            log_entry = create_log_message("Session recorded as skipped with NULL values.")
            log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()
        
        finally:
            cursor.close()
            connection.close()
        
        return 0, 0, None  # Return default values if the lesson was skipped

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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def single_by_double_multiplication(session_id):
    """Presents a single-by-double-digit multiplication quiz and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Single by Double Digit Multiplication
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single by Double Digit Multiplication',))
    result = cursor.fetchone()
    
    if result:
        multiplication_lesson_id = result[0]
    else:
        log_entry = create_log_message("Single by Double Digit Multiplication lesson not found in the database.")
        log_message(log_entry)
        cursor.close()
        connection.close()
        return 0, 0, None  # Return default values if lesson ID not found

    cursor.close()
    connection.close()

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Single by Double Digit Multiplication')
    
    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Single by Double Digit Multiplication', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

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
        enable_shadow=True
    )

    # Draw the "Continue..." and, if applicable, "Skip..." buttons
    continue_rect = draw_continue_button()
    skip_rect = None
    if perfect_score_yesterday:
        skip_rect = draw_skip_button()
    pygame.display.flip()

    # Event loop to wait for the "Continue..." or "Skip..." button click
    waiting = True
    skip_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if continue_rect.collidepoint(mouse_pos):
                    waiting = False
                elif skip_rect and skip_rect.collidepoint(mouse_pos):
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

    # If skip was clicked, record session with NULL values for scores and return early
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()
            
            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert the session lesson with NULL values for performance metrics
            cursor.execute('''
                INSERT INTO session_lessons (
                    session_id, lesson_id, start_time, end_time,
                    total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, multiplication_lesson_id, current_time, current_time,
                None, None, None, None, None  # NULL values for performance metrics
            ))
            
            connection.commit()
            log_entry = create_log_message("Session recorded as skipped with NULL values.")
            log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()
        
        finally:
            cursor.close()
            connection.close()
        
        return 0, 0, None  # Return default values if the lesson was skipped

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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def double_digit_multiplication(session_id):
    """Presents a double-digit multiplication quiz and updates the session results."""
    global current_student  # Access the global current student

    # Retrieve the lesson_id for Double Digit Multiplication
    connection, cursor = get_database_cursor()
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
        # shadow_color=shadow_color
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
        bonus_game_selector()

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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    waiting = False  # Move to the next line


def single_denominator_addition_intro(session_id):
    """
    Display the initial introduction for the Single Denominator Addition quiz with
    three clickable buttons: "What is Same Denominator?", "Continue", and "Skip" if applicable.
    """
    global current_student  # Access the global current student

    # Check if the student got a perfect score on this lesson yesterday
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Single Denominator Fraction Addition')
    
    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Single Denominator Fraction Addition', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

    # Display the introductory message
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
        enable_shadow=True
    )

    # Draw the "What is Same Denominator?" clickable text in the center
    explanation_button_rect = draw_text(
        "Same Denominator?",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.7,
        center=True,
        enable_shadow=True,
        return_rect=True  # Return the rect to check if it's clicked
    )

    # Draw the "Continue" and, if applicable, "Skip" buttons using the standard functions
    continue_rect = draw_continue_button()
    skip_rect = None
    if perfect_score_yesterday:
        skip_rect = draw_skip_button()
    pygame.display.flip()

    # Event loop to wait for clicks on buttons
    waiting = True
    skip_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if explanation_button_rect.collidepoint(mouse_pos):
                    # Show the explanation if "Same Denominator?" is clicked
                    display_same_denominator_explanation()
                    waiting = False
                elif continue_rect.collidepoint(mouse_pos):
                    # Proceed with the lesson if "Continue" is clicked
                    waiting = False
                elif skip_rect and skip_rect.collidepoint(mouse_pos):
                    # Skip the lesson if "Skip" is clicked
                    log_entry = create_log_message("skip clicked")
                    log_message(log_entry)
                    skip_clicked = True
                    waiting = False

    # Handle the skip functionality
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()
            
            # Format the current time to match the desired format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Retrieve lesson ID for recording skip with NULL metrics
            cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Single Denominator Fraction Addition',))
            result = cursor.fetchone()
            if result:
                lesson_id = result[0]
                # Insert the session lesson with NULL values for performance metrics
                cursor.execute('''
                    INSERT INTO session_lessons (
                        session_id, lesson_id, start_time, end_time,
                        total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_id, lesson_id, current_time, current_time,
                    None, None, None, None, None  # NULL values for performance metrics
                ))
                
                connection.commit()
                log_entry = create_log_message("Session recorded as skipped with NULL values.")
                log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()
        
        finally:
            cursor.close()
            connection.close()

        # Return control to handle the skip in session manager or calling function
        return "skip"

    # Return control to proceed with the lesson if not skipped
    return "continue"


def single_denominator_addition(session_id):
    """Presents an addition quiz of fractions with the same denominator and updates the session results."""
    global current_student  # Access the global current student
    
    # Display the introduction with session_id passed as an argument
    intro_result = single_denominator_addition_intro(session_id)
    
    # Handle the outcome based on intro result
    if intro_result == "skip":
        # If skipped, exit early with default values or any specific logic for a skipped lesson
        return 0, 0, None

    # Retrieve the lesson_id for Fraction Addition
    connection, cursor = get_database_cursor()
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
    # single_denominator_addition_intro()

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
                    elif event.unicode.isdigit():
                        if "/" not in user_input:
                            # Before the slash, allow up to two digits for the numerator
                            if len(user_input) < 2:
                                user_input += event.unicode
                        else:
                            # After the slash, allow up to two digits for the denominator
                            if len(user_input.split("/")[1]) < 2:
                                user_input += event.unicode
                    elif event.unicode == "/" and "/" not in user_input and len(user_input) > 0:
                        # Allow the slash to be added only if it's not already present and there is something before it
                        user_input += "/"

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
        bonus_game_selector()

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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    waiting = False  # Move to the next line


def lowest_common_denominator_quiz_intro(session_id):
    """
    Display the initial introduction for the Lowest Common Denominator quiz with
    three clickable buttons: "Lowest Common Denominator?", "Continue", and "Skip" if applicable.
    """
    global current_student  # Access the global current student

    # Check if the student got a perfect score on this lesson recently
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Lowest Common Denominator')
    
    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Lowest Common Denominator', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

    # Display the introductory message
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
        enable_shadow=True
    )

    # Draw the "Lowest Common Denominator?" clickable text
    lcd_button_rect = draw_text(
        "Lowest Common Denominator?",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.7,
        center=True,
        enable_shadow=True,
        return_rect=True
    )

    # Draw the "Continue" and, if applicable, "Skip" buttons
    continue_button_rect = draw_continue_button()
    skip_button_rect = None
    if perfect_score_yesterday:
        skip_button_rect = draw_skip_button()
    pygame.display.flip()

    # Event loop to wait for button clicks
    waiting = True
    skip_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if lcd_button_rect.collidepoint(mouse_pos):
                    # Show LCD explanation
                    display_lcd_explanation()
                    waiting = False
                elif continue_button_rect.collidepoint(mouse_pos):
                    # Move on to the next part if "Continue" is clicked
                    waiting = False
                elif skip_button_rect and skip_button_rect.collidepoint(mouse_pos):
                    # Skip if "Skip" is clicked
                    skip_clicked = True
                    waiting = False

    # Handle skip functionality
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()

            # Get the current time and format without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Retrieve lesson ID for recording skip
            cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Lowest Common Denominator Quiz',))
            result = cursor.fetchone()
            if result:
                lesson_id = result[0]
                # Insert session lesson with NULL values for performance metrics
                cursor.execute('''
                    INSERT INTO session_lessons (
                        session_id, lesson_id, start_time, end_time,
                        total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_id, lesson_id, current_time, current_time,
                    None, None, None, None, None  # NULL values for performance metrics
                ))

                connection.commit()
                log_entry = create_log_message("Session recorded as skipped with NULL values.")
                log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()

        finally:
            cursor.close()
            connection.close()

        # Return "skip" to indicate the lesson was skipped
        return "skip"

    # Return "continue" to proceed with the quiz
    return "continue"


def lowest_common_denominator_quiz(session_id):
    """Presents a quiz on solving for the lowest common denominator and updates the session results."""
    global current_student  # Access the global current student
    
    # Display the introductory screen and get the user's choice to proceed or skip
    intro_result = lowest_common_denominator_quiz_intro(session_id)

    if intro_result == "skip":
        # If the user chose to skip, return default values indicating no questions were asked
        return 0, 0, None

    # Retrieve the lesson_id for LCD Problems
    connection, cursor = get_database_cursor()
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
    # lowest_common_denominator_quiz_intro()

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
        bonus_game_selector()

    return total_questions, correct_answers, average_time


def draw_shape(shape_type):
    """Draw a specific shape on the screen based on the shape type."""
    if shape_type == "circle":
        pygame.draw.circle(screen, text_color, (WIDTH // 2, HEIGHT * 0.6), 100, 5)
    elif shape_type == "oval":
        pygame.draw.ellipse(screen, text_color, (WIDTH // 2 - 100, HEIGHT * 0.6, 200, 100), 5)
    elif shape_type == "square":
        pygame.draw.rect(screen, text_color, (WIDTH // 2 - 75, HEIGHT * 0.6, 150, 150), 5)
    elif shape_type == "rectangle":
        pygame.draw.rect(screen, text_color, (WIDTH // 2 - 100, HEIGHT * 0.6, 200, 100), 5)
    elif shape_type == "triangle":
        pygame.draw.polygon(
            screen, 
            text_color, 
            [
                (WIDTH // 2, HEIGHT // 3),        # New peak point, lowered to HEIGHT // 3
                (WIDTH // 3, HEIGHT // 1.8),      # Left base point slightly lowered
                (2 * WIDTH // 3, HEIGHT // 1.8)   # Right base point slightly lowered
            ], 
            5
        )
    elif shape_type == "pentagon":
        draw_regular_polygon(screen, text_color, (WIDTH // 2, HEIGHT // 2), 100, 5)  # Pentagon with 5 sides
    elif shape_type == "hexagon":
        draw_regular_polygon(screen, text_color, (WIDTH // 2, HEIGHT // 2), 100, 6)  # Hexagon with 6 sides
    elif shape_type == "parallelogram":
        pygame.draw.polygon(
            screen, 
            text_color, 
            [
                (WIDTH // 4, HEIGHT // 1.5),        # Lowered left base point
                (WIDTH // 2, HEIGHT // 1.5),        # Lowered right base point
                (3 * WIDTH // 4, HEIGHT // 2.2),    # Lowered upper right point
                (WIDTH // 2, HEIGHT // 2.2)         # Lowered upper left point
            ], 
            5
        )
    elif shape_type == "rhombus":
        pygame.draw.polygon(
            screen, 
            text_color, 
            [
                (WIDTH // 2, HEIGHT // 2.5),           # Lowered top vertex
                (WIDTH // 3, HEIGHT // 1.7),           # Lowered left vertex
                (WIDTH // 2, HEIGHT // 1.3),           # Lowered bottom vertex
                (2 * WIDTH // 3, HEIGHT // 1.7)        # Lowered right vertex
            ], 
            5
        )



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
    # inner_points = []
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    waiting = False  # Move to the next step


def basic_shapes_quiz_intro(session_id):
    """
    Display the introduction for the basic geometric shapes quiz with
    three clickable buttons: "What are basic shapes?", "Continue", and "Skip" if applicable.
    """
    global current_student  # Access the global current student

    # Check if the student got a perfect score on this lesson recently
    perfect_score_yesterday = perfect_score_lesson_skip(current_student, 'Basic Geometric Shapes')
    
    # Log the result of the perfect score check
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    log_entry = create_log_message(
        f"Student: {current_student}, Lesson: 'Basic Geometric Shapess', "
        f"Date: {yesterday}, 100%: {'Yes' if perfect_score_yesterday else 'No'}"
    )
    log_message(log_entry)

    # Display the introductory message
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
        enable_shadow=True
    )

    # Draw the "What are basic shapes?" clickable text
    explanation_button_rect = draw_text(
        "What are basic shapes?",
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.7,
        center=True,
        enable_shadow=True,
        return_rect=True  # Return the rect to check if it's clicked
    )

    # Draw the "Continue" and "Skip" buttons using the standard functions
    continue_button_rect = draw_continue_button()
    skip_button_rect = None
    if perfect_score_yesterday:
        skip_button_rect = draw_skip_button()
    pygame.display.flip()

    # Event loop to wait for button clicks
    waiting = True
    skip_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if explanation_button_rect.collidepoint(mouse_pos):
                    # Show the explanation if "What are basic shapes?" is clicked
                    display_basic_shapes_explanation()
                    waiting = False
                elif continue_button_rect.collidepoint(mouse_pos):
                    # Move to the next part of the quiz if "Continue" is clicked
                    waiting = False
                elif skip_button_rect and skip_button_rect.collidepoint(mouse_pos):
                    # Skip if "Skip" is clicked
                    skip_clicked = True
                    waiting = False

    # Handle skip functionality
    if skip_clicked:
        try:
            connection, cursor = get_database_cursor()

            # Get the current time without microseconds
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Retrieve lesson ID for recording skip
            cursor.execute("SELECT lesson_id FROM lessons WHERE title = ?", ('Basic Shapes Quiz',))
            result = cursor.fetchone()
            if result:
                lesson_id = result[0]
                # Insert session lesson with NULL values for performance metrics
                cursor.execute('''
                    INSERT INTO session_lessons (
                        session_id, lesson_id, start_time, end_time,
                        total_time, questions_asked, questions_correct, avg_time_per_question, percent_correct
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_id, lesson_id, current_time, current_time,
                    None, None, None, None, None  # NULL values for performance metrics
                ))

                connection.commit()
                log_entry = create_log_message("Session recorded as skipped with NULL values.")
                log_message(log_entry)

        except sqlite3.Error as e:
            log_entry = create_log_message(f"Error recording skipped session: {e}")
            log_message(log_entry)
            connection.rollback()

        finally:
            cursor.close()
            connection.close()

        # Return "skip" to indicate the lesson was skipped
        return "skip"

    # Return "continue" to proceed with the quiz
    return "continue"


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

    # Display the introduction and check if it should be skipped
    intro_result = basic_shapes_quiz_intro(session_id)
    if intro_result == "skip":
        # Exit early with default values if the quiz is skipped
        return 0, 0, None

    # Retrieve the lesson_id for Basic Geometric Shapes
    connection, cursor = get_database_cursor()
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

    # Select 5 unique random shapes without repeating
    selected_shapes = random.sample(shapes, total_questions)

    # Quiz loop
    for shape_question in selected_shapes:
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

        start_time = time.time()  # Start timing for this question

        while not question_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if the student clicked any shape
                    clicked_shape = None
                    for shape_name, rect in shape_rects.items():
                        if rect.collidepoint(mouse_pos):
                            clicked_shape = shape_name
                            break

                    # If they clicked a shape, check if it's correct or not
                    if clicked_shape:
                        time_taken = round(time.time() - start_time, 1)
                        completion_times.append(time_taken)

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
        bonus_game_selector()

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
        draw_text(fibonacci_explanation[sentence_index], font, text_color, x=0, 
                  y=HEIGHT * 0.4, 
                  center=True, 
                  enable_shadow=True, 
                  # shadow_color=shadow_color, 
                  max_width=WIDTH)
        pygame.display.flip()

        # Wait for a mouse click to move to the next sentence
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
    draw_text(completion_message, 
              font, 
              text_color,  # Added the missing color argument here
              x=0, 
              y=HEIGHT * 0.4, 
              center=True, 
              enable_shadow=True, 
              shadow_color=shadow_color,
              max_width=WIDTH)

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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
    draw_text(completion_message, 
              font, 
              text_color, 
              x=0, 
              y=HEIGHT * 0.4, 
              center=True, 
              enable_shadow=True, 
              shadow_color=shadow_color,
              max_width=WIDTH)

    # Update the screen before speaking
    pygame.display.flip()

    # Speak the completion message aloud
    speak_english(completion_message)
    
    # Draw the "Continue..." button after the completion message
    draw_and_wait_continue_button()


# def skip_counting():
#     """Randomly selects a number between 2-9 and performs skip counting up to 100."""
#     global screen_color, text_color, shadow_color, current_font_name_or_path, font  # Access theme-related globals

#     # Define a larger size for the skip-counted numbers
#     large_font_size = 200  # Adjust size as necessary

#     # Initialize the larger font based on whether the current font is a file or system font
#     if os.path.isfile(current_font_name_or_path):
#         large_font = pygame.font.Font(current_font_name_or_path, large_font_size)
#     else:
#         large_font = pygame.font.SysFont(current_font_name_or_path, large_font_size)

#     # Select a random number from 2-9
#     skip_number = random.randint(2, 9)

#     # Particle effect settings
#     particle_count = 3
#     particle_lifetime = 30
#     particles = []

#     # Clear the screen and inform the student about the starting number
#     screen.fill(screen_color)
#     intro_message = f"Let's skip count by {skip_number}!"
    
#     # Display the intro message and update the screen
#     draw_text(intro_message, 
#               font, 
#               text_color, 
#               x=0, 
#               y=HEIGHT * 0.4, 
#               center=True, 
#               enable_shadow=True, 
#               max_width=WIDTH)

#     # Draw the "Continue..." button after intro message
#     continue_rect = draw_continue_button()

#     # Wait for the "Continue..." click with hover effects
#     waiting = True
#     while waiting:
#         # Clear the screen for a new frame
#         screen.fill(screen_color)

#         # Redraw the intro message
#         draw_text(intro_message, 
#                   font, 
#                   text_color, 
#                   x=0, 
#                   y=HEIGHT * 0.4, 
#                   center=True, 
#                   enable_shadow=True, 
#                   max_width=WIDTH)

#         # Get current mouse position
#         mouse_pos = pygame.mouse.get_pos()

#         # Determine hover color for the "Continue..." button
#         continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

#         # Redraw the "Continue..." button with hover effect
#         draw_text(
#             "Continue...",
#             pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
#             continue_color,
#             x=WIDTH * 0.55,
#             y=HEIGHT * 0.9,
#             enable_shadow=True,
#             shadow_color=shadow_color
#         )

#         # Generate particles if hovering over the "Continue..." button
#         if continue_rect.collidepoint(mouse_pos):
#             for _ in range(particle_count):
#                 particle_color = random.choice([shadow_color, text_color, screen_color])
#                 particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
#                 particle.lifetime = particle_lifetime
#                 angle = random.uniform(0, 2 * math.pi)
#                 speed = random.uniform(1, 3)
#                 particle.dx = math.cos(angle) * speed
#                 particle.dy = math.sin(angle) * speed
#                 particles.append(particle)

#         # Update and draw particles
#         for particle in particles[:]:
#             particle.update()
#             particle.draw(screen)
#             if particle.lifetime <= 0:
#                 particles.remove(particle)

#         pygame.display.flip()  # Update the display

#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 # Check if the "Continue..." button is clicked
#                 if continue_rect.collidepoint(event.pos):
#                     waiting = False  # Exit the loop

#         clock.tick(60)

#     # Start counting by the selected number, stopping at 100
#     for i in range(skip_number, 101, skip_number):
#         # Clear the screen before displaying each number
#         screen.fill(screen_color)

#         # Convert the number to string for display
#         number_str = str(i)

#         # Display the number in the center of the screen using the larger font size
#         draw_text(number_str, large_font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True)

#         # Update the screen after drawing the number
#         pygame.display.flip()

#         # Speak the number aloud in English
#         speak_english(number_str)

#         # Pause for a second before showing the next number
#         time.sleep(1)

#     # After completing the skip counting, show a dynamic completion message using the default font
#     completion_message = f"Great job! You just skip counted by {skip_number}!"
#     screen.fill(screen_color)
#     draw_text(
#         completion_message, 
#         font, 
#         text_color, 
#         x=0, 
#         y=HEIGHT * 0.4, 
#         center=True, 
#         enable_shadow=True, 
#         max_width=WIDTH
#     )

#     # Draw the "Continue..." button after the completion message
#     continue_rect = draw_continue_button()

#     # Wait for the "Continue..." click with hover effects
#     waiting = True
#     while waiting:
#         # Clear the screen for a new frame
#         screen.fill(screen_color)

#         # Redraw the completion message
#         draw_text(
#             completion_message, 
#             font, 
#             text_color, 
#             x=0, 
#             y=HEIGHT * 0.4, 
#             center=True, 
#             enable_shadow=True, 
#             max_width=WIDTH
#         )

#         # Get current mouse position
#         mouse_pos = pygame.mouse.get_pos()

#         # Determine hover color for the "Continue..." button
#         continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

#         # Redraw the "Continue..." button with hover effect
#         draw_text(
#             "Continue...",
#             pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
#             continue_color,
#             x=WIDTH * 0.55,
#             y=HEIGHT * 0.9,
#             enable_shadow=True,
#             shadow_color=shadow_color
#         )

#         # Generate particles if hovering over the "Continue..." button
#         if continue_rect.collidepoint(mouse_pos):
#             for _ in range(particle_count):
#                 particle_color = random.choice([shadow_color, text_color, screen_color])
#                 particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
#                 particle.lifetime = particle_lifetime
#                 angle = random.uniform(0, 2 * math.pi)
#                 speed = random.uniform(1, 3)
#                 particle.dx = math.cos(angle) * speed
#                 particle.dy = math.sin(angle) * speed
#                 particles.append(particle)

#         # Update and draw particles
#         for particle in particles[:]:
#             particle.update()
#             particle.draw(screen)
#             if particle.lifetime <= 0:
#                 particles.remove(particle)

#         pygame.display.flip()  # Update the display

#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 # Check if the "Continue..." button is clicked
#                 if continue_rect.collidepoint(event.pos):
#                     waiting = False  # Exit the loop

#         clock.tick(60)
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

    # Clear the screen and display the intro message
    intro_message = f"Let's skip count by {skip_number}!"
    screen.fill(screen_color)
    draw_text(
        intro_message,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        center=True,
        enable_shadow=True,
        max_width=WIDTH
    )

    # Draw the "Continue..." button
    continue_rect = draw_continue_button()

    # Update the display to show the initial screen
    pygame.display.flip()

    # Speak the intro message out loud AFTER the screen is rendered
    speak_english(intro_message)

    # Wait for the "Continue..." click with hover effects
    waiting = True
    particles = []  # Initialize particle effects list
    particle_count = 3
    particle_lifetime = 30

    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Redraw the intro message
        draw_text(
            intro_message,
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.4,
            center=True,
            enable_shadow=True,
            max_width=WIDTH
        )

        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover color for the "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the "Continue..." button with hover effect
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate particles if hovering over the "Continue..." button
        if continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the "Continue..." button is clicked
                if continue_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        clock.tick(60)

    # Start counting by the selected number, stopping at 100
    for i in range(skip_number, 101, skip_number):
        # Clear the screen before displaying each number
        screen.fill(screen_color)

        # Convert the number to string for display
        number_str = str(i)

        # Display the number in the center of the screen using the larger font size
        draw_text(
            number_str,
            large_font,
            text_color,
            x=0,
            y=HEIGHT * 0.4,
            center=True,
            enable_shadow=True
        )

        # Update the screen after drawing the number
        pygame.display.flip()

        # Speak the number aloud in English
        speak_english(number_str)

        # Pause for a second before showing the next number
        time.sleep(1)

    # After completing the skip counting, show a dynamic completion message using the default font
    completion_message = f"Great job! You just skip counted by {skip_number}!"
    screen.fill(screen_color)
    draw_text(
        completion_message,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        center=True,
        enable_shadow=True,
        max_width=WIDTH
    )
    
    # Update the display to show the initial screen
    pygame.display.flip()
    
    # Speak the intro message out loud AFTER the screen is rendered
    speak_english(completion_message)

    # Draw the "Continue..." button after the completion message
    continue_rect = draw_continue_button()

    # Wait for the "Continue..." click with hover effects
    waiting = True
    particles = []  # Reset particle effects list

    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Redraw the completion message
        draw_text(
            completion_message,
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.4,
            center=True,
            enable_shadow=True,
            max_width=WIDTH
        )

        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover color for the "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the "Continue..." button with hover effect
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate particles if hovering over the "Continue..." button
        if continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the "Continue..." button is clicked
                if continue_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        clock.tick(60)


########################################
### Menu and Navigation Functions ###
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

    # Particle effect settings
    particle_count = 1  # Number of particles to generate on hover
    particle_lifetime = 30  # Lifetime for each particle in frames

    particles = []  # List to hold active particles

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
        
        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw the title (not clickable)
        draw_text("Learniverse", font, text_color, 0, HEIGHT * 0.2, screen, center=True, enable_shadow=True, return_rect=False, max_width=WIDTH)

        # Initially draw each text option and get their rects for hover detection
        start_rect = draw_text("Start", font, text_color, 0, HEIGHT * 0.55, screen, center=True, enable_shadow=True, return_rect=True)
        options_rect = draw_text("Options", font, text_color, 0, HEIGHT * 0.7, screen, center=True, enable_shadow=True, return_rect=True)
        explanation_rect = draw_text("Learniverse?", font, text_color, 0, HEIGHT * 0.85, screen, center=True, enable_shadow=True, return_rect=True)

        # Check hover state for each option and set colors accordingly
        start_color = shadow_color if start_rect.collidepoint(mouse_pos) else text_color
        options_color = shadow_color if options_rect.collidepoint(mouse_pos) else text_color
        explanation_color = shadow_color if explanation_rect.collidepoint(mouse_pos) else text_color

        # Redraw each text option with hover effect based on color checks
        draw_text("Start", font, start_color, 0, HEIGHT * 0.55, screen, center=True, enable_shadow=True)
        draw_text("Options", font, options_color, 0, HEIGHT * 0.7, screen, center=True, enable_shadow=True)
        draw_text("Learniverse?", font, explanation_color, 0, HEIGHT * 0.85, screen, center=True, enable_shadow=True)

        # Particle effect on hover
        if start_rect.collidepoint(mouse_pos) or options_rect.collidepoint(mouse_pos) or explanation_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], color)
                particle.lifetime = particle_lifetime  # Override the random lifetime with our controlled particle_lifetime
                
                # Set random angle and speed for 360-degree direction
                angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
                speed = random.uniform(1, 3)  # Adjust speed range as needed
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed

                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:  # Iterate over a copy of the list
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        # Flip the display
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check which option was clicked
                if start_rect.collidepoint(event.pos):
                    return "student_select_menu"  # Return to indicate starting the game
                elif options_rect.collidepoint(event.pos):
                    return "options_menu"  # Return to indicate transitioning to options menu
                elif explanation_rect.collidepoint(event.pos):
                    return "learniverse_explanation"  # Return to indicate transitioning to explanation
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_b:  # Check if the 'b' key is pressed
                    # Skip directly to the bonus game for debug
                    # bonus_game_tuna_tower()
                    # bonus_game_cat_pong()
                    # bonus_game_falling_fish()
                    # bonus_game_fat_tuna() 
                    # bonus_game_selector()

        # Control the frame rate
        clock.tick(120)


def student_select_menu():
    global font, current_student

    # Ensure font is initialized correctly
    if not font:
        font = pygame.font.SysFont('Arial', 32)

    # Initial variables for text input
    input_active = False
    student_input = ''

    # Particle effect settings
    particle_count = 2  # Number of particles to generate per frame when hovered
    particle_lifetime = 30  # Lifetime for each particle in frames
    particles = []  # List to hold active particles

    while True:
        draw_background(main_menu_background)
        students = get_students()  # Fetch students from the database

        # Draw a title for the student selection menu
        draw_text("Select a Student", font, text_color, 0, HEIGHT * 0.1, screen, center=True, enable_shadow=True)

        # Display students as clickable text options with hover effect
        student_rects = []
        mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
        for index, student in enumerate(students):
            student_name = student[1]
            student_y = HEIGHT * (0.2 + 0.1 * index)

            # Measure the text width for precise rectangle creation
            text_width, text_height = font.size(student_name)
            student_rect = pygame.Rect((WIDTH // 2) - (text_width // 2), student_y, text_width, text_height)

            # Check if the mouse is over this student's name and set color accordingly
            is_hovered = student_rect.collidepoint(mouse_pos)
            student_color = shadow_color if is_hovered else text_color

            # Draw the student's name with the appropriate color
            draw_text(student_name, font, student_color, 0, student_y, screen, center=True, enable_shadow=True, return_rect=True)
            student_rects.append((student_rect, student_name))

            # Generate particles if hovered
            if is_hovered:
                for _ in range(particle_count):
                    particle_color = random.choice([shadow_color, text_color, screen_color])
                    particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                    particle.lifetime = particle_lifetime
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 3)
                    particle.dx = math.cos(angle) * speed
                    particle.dy = math.sin(angle) * speed
                    particles.append(particle)

        # Display the input box for adding new students
        input_box_rect = pygame.Rect(WIDTH * 0.33, HEIGHT * 0.80, WIDTH * 0.4, HEIGHT * 0.1)
        # Determine the color of the input box based on hover and active states
        if input_active:
            input_box_color = (255, 0, 0)  # Red when active
        elif input_box_rect.collidepoint(mouse_pos):
            input_box_color = shadow_color  # Shadow color on hover
            # Generate particles if hovered over the input box
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)
        else:
            input_box_color = text_color  # Default color

        pygame.draw.rect(screen, input_box_color, input_box_rect, 2)  # Draw the input box with the determined color

        # Draw the "New Student" label and current input text
        draw_text("New Student:", font, text_color, WIDTH * 0.5, HEIGHT * 0.7, screen, enable_shadow=True, center=True)
        draw_text(student_input, font, text_color, WIDTH * 0.45, HEIGHT * 0.8, screen, enable_shadow=True, center=True)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Check if a student was clicked
                for rect, student_name in student_rects:
                    if rect.collidepoint(mouse_pos):
                        current_student = student_name
                        return "session_manager"  # Transition to the session manager
                
                # Check if the input box is clicked to activate text input
                input_active = input_box_rect.collidepoint(mouse_pos)

            elif event.type == pygame.KEYDOWN and input_active:
                # Handle text input for the new student name
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if student_input.strip():
                        add_student(student_input.strip())
                        student_input = ''
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    student_input = student_input[:-1]
                else:
                    student_input += event.unicode

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
    
    # Step 1, check on an incomplete session BEFORE we start a new one
    is_session_incomplete = was_last_session_incomplete_today(current_student)
    
    # Debug
    # print("Current student variable")
    # print(current_student)
    print("Debug: is the last session today incomplete? (True is BAD)")
    print(is_session_incomplete)
    
    # Step 2: Start the session and log in database
    session_id = start_new_session(current_student)

    # If session could not be started, return to main menu
    if session_id == -1:
        log_entry = create_log_message(f"Error: Failed to start session for {current_student}.")
        log_message(log_entry)
        return "main_menu"
    
    
    
    #####################################
    ### Step 2: Logic for lesson flow ###
    #####################################
    lessons_to_play = ["greet_student",                     #JP
                       # "random_quote_display",              #ENG
                       
                       
                       
                       
                       
                       
                       
                       
                                          
                       ### DEBUG TESTING ###
                       # "bible_verse_selector",              #Eng
                       # "display_next_event",                #JP
                       
                       
                       # "single_digit_addition",             #Math
                       # "double_digit_addition",             #Math
                       # "single_digit_subtraction",          #Math
                       # "double_digit_subtraction",          #Math
                       # "subtraction_borrowing",             #Math
                       # "single_digit_multiplication",       #Math
                       # "single_by_double_multiplication",   #Math
                       # "single_denominator_addition",       #Math
                       # "lowest_common_denominator_quiz",      #Math
                       # "basic_shapes_quiz",
                       
                       # "hiragana_teach",                    #JP
                       # "hiragana_quiz",                     #JP    
                       # "katakana_teach",                    #JP
                       # "katakana_quiz",                     #JP    
                       # "japanese_song_zou_san_teach",       #JP
                       # "japanese_animals_quiz",             #JP
                       # "japanese_animals_teach",            #JP
                       # "skip_counting_japanese",            #JP
                       # "month_of_the_year",                 #JP
                       # "psalm_23",                          #ENG
                       # "numbers_6_24_26",                   #ENG
                       
                       # "japanese_animals_quiz",             #JP
                       # "japanese_body_parts_teach",         #JP
                       # "japanese_colors_teach",              #JP
                       # "japanese_adjectives_teach",         #JP
                       # "japanese_animals_teach",            #JP
                       # "japanese_colors_quiz",              #JP
                       
                       # "japanese_fruits_teach",             #JP
                       # "japanese_fruits_quiz",              #JP
                       # "japanese_colors_teach",             #JP
                       # "japanese_colors_quiz",             #JP
                       # "japanese_song_sanpo_teach",         #JP
                       # "john_3_16",                         #ENG
                       # "skip_counting_japanese",
                       # "psalm_23",                          #ENG
                       # "rainbow_numbers",                   #Math
                       
                       # "psalm_23",                          #ENG
                       # "japanese_body_parts_quiz",          #JP
                       # "skip_counting_kanji",               #JP
                       ## DEBUG TESTING ###
                       
                       
                       
                       
                       "streak_check",                      #ENG
                       "day_of_the_week",                   #JP
                       "skip_counting",                     #Math
                       
                       "bible_verse_selector",              #Eng
                       "month_of_the_year",                 #JP
                       "warm_up_math",                      #Math
                       
                       "random_quote_display",              #ENG
                       "display_next_event",                #JP
                       "skip_counting_primes",              #Math
                       
                       "hiragana_teach",                    #JP
                       "double_digit_addition",             #Math
                       
                       "skip_counting_japanese",            #JP
                       "subtraction_borrowing",             #Math
                       
                       "hiragana_quiz",                     #JP     
                       "skip_counting_fibonacci",           #Math
                       
                       "japanese_colors_teach",             #JP
                       "double_digit_subtraction",          #Math
                       
                       "japanese_colors_quiz",              #JP
                       "single_denominator_addition",       #Math
                       
                       "japanese_body_parts_teach",         #JP
                       "lowest_common_denominator_quiz",    #Math
                       
                       "japanese_body_parts_quiz",          #JP
                       "basic_shapes_quiz",                 #Math
                       
                       
                       # "japanese_animals_teach",            #JP
                      
                       
                       # "japanese_animals_quiz",             #JP
                       
                       
                       "japanese_adjectives_teach",         #JP
                       "single_by_double_multiplication",   #Math
                       
                       "japanese_adjectives_quiz",          #JP
                       
                       
                       # "japanese_family_teach",             #JP
                       
                       
                       # "japanese_family_quiz",              #JP
                       
                       # "skip_counting_kanji",               #JP
                       # "japanese_fruits_teach",             #JP
                       # "japanese_fruits_quiz",              #JP
                       # "japanese_greetings_teach",          #JP
                       # "japanese_greetings_quiz",           #JP
                       # "one_piece_teach",                   #JP
                       # "one_piece_quiz",                    #JP
                       # "japanese_self_introduction_teach",  #JP
                       # "japanese_self_introduction_quiz",   #JP
                       # "japanese_nouns_teach",              #JP
                       # "japanese_nouns_quiz",               #JP
                       # "japanese_time_teach",               #JP
                       # "japanese_time_quiz",                #JP
                       # "japanese_vegtables_teach",          #JP
                       # "japanese_vegtables_quiz",           #JP
                       # "japanese_verbs_teach",              #JP
                       # # "japanese_verbs_quiz",               #JP
                       # "japanese_song_zou_san_teach",       #JP
                       # # "japanese_song_zou_san_quiz",        #JP
                       # "japanese_song_sanpo_teach",         #JP
                       # "japanese_song_sanpo_quiz",          #JP
                       
                       "wrap_up_session",                   #JP
                       ] 
    total_questions = 0
    total_correct = 0
    total_times = []  # List to track the average time across lessons

    # Loop through lessons
    for lesson in lessons_to_play:
        
        ### Intro ###
        if lesson == "greet_student":
            greet_student()
        elif lesson == "streak_check":
            streak_check()
        elif lesson == "day_of_the_week":
            day_of_the_week()
        elif lesson == "month_of_the_year":
            month_of_the_year()
        elif lesson == "display_next_event":
            display_next_event()
            
        ### English ###
        elif lesson == "random_quote_display":
            random_quote_display()
            
        ### Outro ###
        elif lesson == "wrap_up_session":
            wrap_up_session()
        
        ### Jr. Church ###
        elif lesson == "bible_verse_selector":
            bible_verse_selector()
        # elif lesson == "john_3_16":
        #     john_3_16()
        # elif lesson == "john_13_34":
        #     john_13_34()
        # elif lesson == "psalm_23":
        #     psalm_23()
        # elif lesson == "hebrews_11_1":
        #     hebrews_11_1()
        # elif lesson == "philippians_4_6":
        #      philippians_4_6()
        # elif lesson == "ephesians_4_32":
        #     ephesians_4_32()
        # elif lesson == "numbers_6_24_26":
        #     numbers_6_24_26()
            
        ### Maths ###
        elif lesson == "warm_up_math":
            warm_up_math(session_id)
        elif lesson == "skip_counting":
            skip_counting()
        elif lesson == "skip_counting_fibonacci":
            skip_counting_fibonacci()
        elif lesson == "skip_counting_primes":
            skip_counting_primes()
        elif lesson == "rainbow_numbers":
            lesson_result = rainbow_numbers(session_id)
            
            questions_asked, correct_answers, avg_time = lesson_result
            total_questions += questions_asked
            total_correct += correct_answers
            total_times.append(avg_time)
        elif lesson == "single_digit_addition":
            lesson_result = single_digit_addition(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: single_digit_addition did not return a valid result.")
        elif lesson == "double_digit_addition":
            lesson_result = double_digit_addition(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: double_digit_addition did not return a valid result.")
        elif lesson == "triple_digit_addition":
            lesson_result = triple_digit_addition(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: triple_digit_addition did not return a valid result.")
        elif lesson == "quad_digit_addition":
            lesson_result = quad_digit_addition(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: quad_digit_addition did not return a valid result.")
        elif lesson == "single_digit_subtraction":
            lesson_result = single_digit_subtraction(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: single_digit_subtraction did not return a valid result.")
        elif lesson == "double_digit_subtraction":
            lesson_result = double_digit_subtraction(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: double_digit_subtraction did not return a valid result.")
        elif lesson == "subtraction_borrowing":
            lesson_result = subtraction_borrowing(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: subtraction_borrowing did not return a valid result.")
        elif lesson == "triple_digit_subtraction":
            lesson_result = triple_digit_subtraction(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: triple_digit_subtraction did not return a valid result.")
        elif lesson == "quad_digit_subtraction":
            lesson_result = quad_digit_subtraction(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                ("Error: quad_digit_subtraction did not return a valid result.")
        elif lesson == "single_digit_multiplication":
            lesson_result = single_digit_multiplication(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: single_digit_multiplication did not return a valid result.")
        elif lesson == "single_by_double_multiplication":
            lesson_result = single_by_double_multiplication(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: single_by_double_multiplication did not return a valid result.")
        elif lesson == "double_digit_multiplication":
            lesson_result = double_digit_multiplication(session_id)
            
            if lesson_result is not None:  # Ensure the function returned something
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: double_digit_multiplication did not return a valid result.")
        elif lesson == "single_denominator_addition":
            lesson_result = single_denominator_addition(session_id)
            
            if lesson_result is not None:  
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: single_denominator_addition did not return a valid result.")
        elif lesson == "lowest_common_denominator_quiz":
            lesson_result = lowest_common_denominator_quiz(session_id)
            
            if lesson_result is not None:  
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: lowest_common_denominator_quiz did not return a valid result.")
        elif lesson == "basic_shapes_quiz":
            lesson_result = basic_shapes_quiz(session_id)
            
            if lesson_result is not None:  
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: basic_shapes_quiz did not return a valid result.")
       
                
        ################
        ### JAPANESE ###
        ################
        
        elif lesson == "skip_counting_japanese":
            skip_counting_japanese()
        elif lesson == "skip_counting_kanji":
            skip_counting_kanji()
        
        ### J teach
        elif lesson == "hiragana_teach":
            hiragana_teach(session_id)
        elif lesson == "katakana_teach":
            katakana_teach(session_id)
        elif lesson == "japanese_colors_teach":
            vocab_teach(session_id, 'Japanese Colors') 
        elif lesson == "japanese_body_parts_teach":
            vocab_teach(session_id, 'Japanese Body Parts') 
        elif lesson == "japanese_adjectives_teach":
            vocab_teach(session_id, 'Japanese Adjectives')
        elif lesson == "japanese_animals_teach":
            vocab_teach(session_id, 'Japanese Animals')
        elif lesson == "japanese_family_teach":
            vocab_teach(session_id, 'Japanese Family')
        elif lesson == "japanese_fruits_teach":
            vocab_teach(session_id, 'Japanese Fruits')
        elif lesson == "japanese_greetings_teach":
            vocab_teach(session_id, 'Japanese Greetings')
        elif lesson == "one_piece_teach":
            vocab_teach(session_id, 'One Piece Vocab')
        elif lesson == "japanese_self_introduction_teach":
            vocab_teach(session_id, 'Japanese Self Introduction')
        elif lesson == "japanese_nouns_teach":
            vocab_teach(session_id, 'Japanese Nouns')
        elif lesson == "japanese_time_teach":
            vocab_teach(session_id, 'Japanese Time')
        elif lesson == "japanese_vegtables_teach":
            vocab_teach(session_id, 'Japanese Vegtables')
        elif lesson == "japanese_verbs_teach":
            vocab_teach(session_id, 'Japanese Verbs')
        elif lesson == "japanese_song_sanpo_teach":
            vocab_teach(session_id, 'Japanese Song Sanpo')
        elif lesson == "japanese_song_zou_san_teach":
            vocab_teach(session_id, 'Japanese Song Zou-san')
      
        
      
        ### J Quizzes
        elif lesson == "hiragana_quiz":
            lesson_result = hiragana_quiz(session_id)
            questions_asked, correct_answers, avg_time = lesson_result
            total_questions += questions_asked
            total_correct += correct_answers
            total_times.append(avg_time)
        elif lesson == "katakana_quiz":
            lesson_result = katakana_quiz(session_id)
            questions_asked, correct_answers, avg_time = lesson_result
            total_questions += questions_asked
            total_correct += correct_answers
            total_times.append(avg_time)
        elif lesson == "japanese_colors_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Colors') 
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: Japanese Colors Quiz did not return a valid result.")
        elif lesson == "japanese_body_parts_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Body Parts')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: Japanese Body Parts Quiz did not return a valid result.")
        elif lesson == "japanese_adjectives_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Adjectives')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: Japanese Adjectives Quiz did not return a valid result.")
        elif lesson == "japanese_animals_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Animals')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: Japanese Animals Quiz did not return a valid result.")
        elif lesson == "japanese_family_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Family')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: Japanese Family Quiz did not return a valid result.")
        elif lesson == "japanese_fruits_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Fruits')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: Japanese Fruits Quiz did not return a valid result.")
        elif lesson == "japanese_greetings_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Greetings')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: Japanese Greetings Quiz did not return a valid result.")
        elif lesson == "one_piece_quiz":
            lesson_result = lesson_selector(session_id, 'One Piece Vocab')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error: One Piece Quiz did not return a valid result.")
        elif lesson == "japanese_self_introduction_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Self Introduction')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error:Japanese Self Introduction Quiz did not return a valid result.")
        elif lesson == "japanese_nouns_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Nouns')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error:Japanese Nouns Quiz did not return a valid result.")
        elif lesson == "japanese_time_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Time')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error:Japanese Time Quiz did not return a valid result.")
        elif lesson == "japanese_vegtables_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Vegtables')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error:Japanese Vegtables Quiz did not return a valid result.")
        elif lesson == "japanese_verbs_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Verbs')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error:Japanese Verbs Quiz did not return a valid result.")
        elif lesson == "japanese_song_sanpo_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Song Sanpo')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error:Japanese Song Sanpo Quiz did not return a valid result.")
        elif lesson == "japanese_song_zou_san_quiz":
            lesson_result = lesson_selector(session_id, 'Japanese Song Zou-san')
            
            if lesson_result is not None:
                questions_asked, correct_answers, avg_time = lesson_result
                total_questions += questions_asked
                total_correct += correct_answers
                total_times.append(avg_time)
            else:
                log_message("Error:Japanese Song Zou-san Quiz did not return a valid result.")
        
        # Check if there's another lesson or handle lesson completion here
        # You can add more lessons to `lessons_to_play` and logic here
    
    # Step 3: Calculate total stats for the session
    valid_times = [time for time in total_times if time is not None]
    if valid_times:
        overall_avg_time = round(sum(valid_times) / len(valid_times), 1)
    else:
        overall_avg_time = 0
    
    # Step 4: End the session and log overall session stats
    end_session(session_id, total_questions, total_correct, overall_avg_time)
    
    # Return to main menu after all lessons are done
    return "main_menu"


def streak_check():
    global angle_x, angle_y, angle_z, hue  # Declare global for cube rotation and color
    global text_color, shadow_color, screen_color, current_font_name_or_path  # Access the theme-related globals

    # Initialize hover particles for "Continue..." button
    hover_particles = []

    # Query the student's streak
    streak_days = student_streak_query()

    # Check if the student is on a streak and create the message
    if streak_days > 1:
        message = f"Great job! You've been on a streak for {streak_days} days in a row!"
        show_cube = True
    elif streak_days == 1:
        message = "You're on a 1-day streak! Keep it up!"
        show_cube = True
    else:
        message = "Let's start a streak today! Keep it up!"
        show_cube = False

    # Check the current month
    current_month = datetime.now().month
    is_december = current_month == 12
    is_november = current_month == 11
    is_april = current_month == 4

    # Set the background color and particle type based on the month
    if is_december:
        background_color = (10, 10, 40)  # DARK_BLUE for December
        monthly_particle_class = SnowflakeParticle
    elif is_november:
        background_color = (30, 15, 10)  # Dark earthy background for November
        monthly_particle_class = LeafParticle
    elif is_april:
        background_color = (220, 220, 255)  # Light blue spring sky for April
        monthly_particle_class = SakuraBlossom
    else:
        background_color = screen_color  # Default screen color
        monthly_particle_class = None  # No monthly particles in other months

    # Prepare the "Continue..." button
    continue_font_size = int(get_dynamic_font_size() * 0.8)
    if os.path.isfile(current_font_name_or_path):
        button_font = pygame.font.Font(current_font_name_or_path, continue_font_size)
    else:
        button_font = pygame.font.SysFont(current_font_name_or_path, continue_font_size)

    button_text = "Continue..."
    button_color = text_color

    # Get the rect for the button for hover and click detection
    button_rect = draw_text(
        button_text,
        button_font,
        button_color,
        x=WIDTH * 0.55,
        y=HEIGHT * 0.9,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True
    )

    # Draw the initial screen with text
    screen.fill(background_color)

    # Draw the streak message
    draw_text(
        message,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.25,
        max_width=WIDTH * 0.8,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Draw the "Continue..." button
    draw_text(
        button_text,
        button_font,
        button_color,
        x=WIDTH * 0.55,
        y=HEIGHT * 0.9,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Update the display to show everything
    pygame.display.flip()

    # Speak the streak message out loud AFTER the screen is drawn
    speak_english(message)

    # Initialize monthly particles list
    monthly_particles = []

    waiting = True
    while waiting:
        # Clear the screen with the appropriate background color
        screen.fill(background_color)

        # Draw the streak message
        draw_text(
            message, 
            font, 
            text_color, 
            x=0, 
            y=HEIGHT * 0.25, 
            max_width=WIDTH * 0.8, 
            center=True, 
            enable_shadow=True, 
            shadow_color=shadow_color
        )

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check for hover over the "Continue..." button
        if button_rect.collidepoint(mouse_pos):
            button_color = shadow_color
            # Generate hover particles
            for _ in range(3):  # Adjust particle count as needed
                particle_color = random.choice([shadow_color, text_color, background_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particle.lifetime = 30  # Adjust lifetime if needed
                hover_particles.append(particle)
        else:
            button_color = text_color

        # Generate new monthly particles if applicable
        if monthly_particle_class:
            monthly_particles.append(monthly_particle_class())

        # Update and draw hover particles
        for particle in hover_particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                hover_particles.remove(particle)

        # Update and draw monthly particles
        if monthly_particle_class:
            for particle in monthly_particles:
                particle.update()
                particle.draw(screen)

        # Draw the "Continue..." button
        draw_text(
            button_text,
            button_font,
            button_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop when the button is clicked

        # Draw the rotating cube if streak > 0
        if show_cube:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            draw_wireframe_cube(screen, mouse_x, mouse_y)

            # Update the cube's rotation and color
            hue += 0.00833
            if hue > 1.0:
                hue -= 1.0

        # Refresh the display
        pygame.display.flip()
        clock.tick(60)

    return


def lesson_selector(session_id, lesson_title):
    """Presents a quiz based on the lesson_title and returns the result."""
    
    # Fetch the student's current level for the specified lesson
    student_level = get_student_progress(session_id, lesson_title)  # Ensure this is a string like 'Japanese Colors'

    # Dynamically determine the available levels for the lesson
    lesson_data_sets = []
    
    # Populate the lesson_data_sets based on the lesson_title
    if lesson_title == 'Japanese Colors':
        lesson_data_sets = [j_colors1, 
                            j_colors2, 
                            j_colors3, 
                            j_colors4, 
                            j_colors5,
                            j_colors6,
                            j_colors7,
                            j_colors8,
                            j_colors9,
                            j_colors10,
                            ]
    elif lesson_title == 'Japanese Body Parts':
        lesson_data_sets = [j_body_parts1, 
                            j_body_parts2, 
                            j_body_parts3, 
                            j_body_parts4, 
                            j_body_parts5]
    elif lesson_title == 'Japanese Adjectives':
        lesson_data_sets = [j_adjectives1]
    elif lesson_title == 'Japanese Animals':
        lesson_data_sets = [j_animals1, 
                            j_animals2, 
                            j_animals3, 
                            j_animals4, 
                            j_animals5,
                            j_animals6,
                            j_animals7,
                            j_animals8,
                            j_animals9]
    elif lesson_title == 'Japanese Family':
        lesson_data_sets = [j_family1, 
                            j_family2, 
                            j_family3, 
                            j_family4, 
                            j_family5,
                            j_family6,
                            j_family7]
    elif lesson_title == 'Japanese Fruits':
        lesson_data_sets = [j_fruits1, 
                            j_fruits2, 
                            j_fruits3, 
                            j_fruits4, 
                            j_fruits5]
    elif lesson_title == 'Japanese Greetings':
        lesson_data_sets = [j_greetings1, 
                            j_greetings2, 
                            j_greetings3]
    elif lesson_title == 'One Piece Vocab':
        lesson_data_sets = [j_one_piece1, 
                            j_one_piece2, 
                            j_one_piece3,
                            j_one_piece4]
    elif lesson_title == 'Japanese Self Introduction':
        lesson_data_sets = [j_self_introduction1, 
                            j_self_introduction2, 
                            j_self_introduction3, 
                            j_self_introduction4, 
                            j_self_introduction5,
                            j_self_introduction6]
    elif lesson_title == 'Japanese Nouns':
        lesson_data_sets = [j_nouns1, 
                            j_nouns2, 
                            j_nouns3,
                            j_nouns4]
    elif lesson_title == 'Japanese Time':
        lesson_data_sets = [j_time1, 
                            j_time2, 
                            j_time3, 
                            j_time4, 
                            j_time5,
                            j_time6,
                            j_time7]
    elif lesson_title == 'Japanese Vegtables':
        lesson_data_sets = [j_vegtables1, 
                            j_vegtables2, 
                            j_vegtables3, 
                            j_vegtables4, 
                            j_vegtables5]
    elif lesson_title == 'Japanese Verbs':
        lesson_data_sets = [j_verbs1]
    elif lesson_title == 'Japanese Song Sanpo':
        lesson_data_sets = [j_song_sanpo1, 
                            j_song_sanpo2, 
                            j_song_sanpo3]
    elif lesson_title == 'Japanese Song Zou-san':
        lesson_data_sets = [j_song_zou_san1, 
                            j_song_zou_san2]
    else:
        log_message(f"Error: Invalid lesson title {lesson_title}.")
        return None

    # Dynamically set the max level based on the number of datasets
    max_level = len(lesson_data_sets)

    # Cap the student level if they've reached the highest available content
    if student_level > max_level:
        student_level = max_level
        log_message(f"Student has capped out on available content for {lesson_title} (Level {max_level}).")
        # Optionally, notify the student
        screen.fill(screen_color)
        draw_text(
            f"Great job! You've mastered all available levels for {lesson_title}!",
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.4,
            center=True,
            enable_shadow=True,
            max_width=WIDTH
        )
        draw_and_wait_continue_button()
        return None  # Exit, since there’s no new content to show

    # Select the appropriate lesson data based on the student's current level
    lesson_data = lesson_data_sets[student_level - 1]  # Adjust for 0-indexing

    # Start the lesson timer
    lesson_start_time = time.time()

    # Run the quiz using japanese_quiz (pass lesson_title and lesson_data separately)
    total_questions, correct_answers, avg_time = japanese_quiz(session_id, lesson_title, lesson_data)

    # End the lesson timer
    lesson_end_time = time.time()

    # Fetch the lesson_id from the database for the specified lesson title
    lesson_id = fetch_lesson_id(lesson_title)

    # Add session lesson to the database, tracking progress
    add_session_lesson(session_id, lesson_id, lesson_start_time, lesson_end_time, total_questions, correct_answers)

    # Handle perfect score and leveling up
    if correct_answers == total_questions and student_level < max_level + 1:
        set_student_progress(session_id, lesson_title)  # Level up on perfect score
        log_message(f"Student leveled up in {lesson_title}")

    return total_questions, correct_answers, avg_time


def options_menu():
    global music_volume, current_resolution_index, screen, WIDTH, HEIGHT, current_windowed_resolution, current_font_name_or_path, font, text_color, shadow_color, screen_color

    # Particle effect settings
    particle_count = 2  # Number of particles to generate on hover per frame
    particle_lifetime = 30  # Lifetime for each particle in frames
    particles = []  # List to hold active particles

    # Get the filtered fonts list
    filtered_fonts = get_filtered_fonts() or ["arial"]

    # Set the current font index to match the current font
    current_font_index = filtered_fonts.index(current_font_name_or_path) if current_font_name_or_path in filtered_fonts else 0
    current_font_name_or_path = filtered_fonts[current_font_index]

    # Track the current theme index based on the current applied theme
    for theme_name, theme_values in color_themes.items():
        if (text_color == theme_values["text_color"] and
            shadow_color == theme_values["shadow_color"] and
            screen_color == theme_values["screen_color"]):
            current_theme_index = list(color_themes.keys()).index(theme_name)
            break
    else:
        current_theme_index = list(color_themes.keys()).index("light")

    while True:
        font = pygame.font.SysFont(current_font_name_or_path, get_dynamic_font_size())
        draw_background(options_background)
        mouse_pos = pygame.mouse.get_pos()

        # Y positions for consistent alignment
        volume_y, resolution_y, theme_y, font_y, credits_y, back_to_main_y = (
            HEIGHT * 0.1, HEIGHT * 0.25, HEIGHT * 0.4, HEIGHT * 0.55, HEIGHT * 0.7, HEIGHT * 0.85
        )
        left_buffer, right_buffer = 0.05, 0.95

        # Draw each interactive element and calculate hover effects
        back_to_main_menu_rect = draw_text("Back to Main Menu", font, text_color, 0, back_to_main_y, screen, center=True, enable_shadow=True, return_rect=True)
        
        # Volume Label and Percentage
        draw_text("Volume:", font, text_color, WIDTH * (left_buffer * 2), volume_y, screen, enable_shadow=True)
        volume_percentage = f"{int(music_volume * 100)}%"
        draw_text(volume_percentage, font, text_color, WIDTH * 0.5, volume_y, screen, enable_shadow=True)
        minus_rect = draw_text("<", font, text_color, WIDTH * left_buffer, volume_y, screen, enable_shadow=True, return_rect=True)
        plus_rect = draw_text(">", font, text_color, WIDTH * right_buffer, volume_y, screen, enable_shadow=True, return_rect=True)

        # Resolution Controls
        draw_text("Resolution:", font, text_color, WIDTH * (left_buffer * 2), resolution_y, screen, enable_shadow=True)
        resolution_text = f"{AVAILABLE_RESOLUTIONS[current_resolution_index][0]}x{AVAILABLE_RESOLUTIONS[current_resolution_index][1]}"
        draw_text(resolution_text, font, text_color, WIDTH * 0.5, resolution_y, screen, enable_shadow=True)
        resolution_minus_rect = draw_text("<", font, text_color, WIDTH * left_buffer, resolution_y, screen, enable_shadow=True, return_rect=True)
        resolution_plus_rect = draw_text(">", font, text_color, WIDTH * right_buffer, resolution_y, screen, enable_shadow=True, return_rect=True)

        # Theme Label and Current Theme Name
        draw_text("Theme:", font, text_color, WIDTH * (left_buffer * 2), theme_y, screen, enable_shadow=True)
        current_theme_name = list(color_themes.keys())[current_theme_index].capitalize()
        draw_text(current_theme_name, font, text_color, WIDTH * 0.5, theme_y, screen, enable_shadow=True)
        theme_minus_rect = draw_text("<", font, text_color, WIDTH * left_buffer, theme_y, screen, enable_shadow=True, return_rect=True)
        theme_plus_rect = draw_text(">", font, text_color, WIDTH * right_buffer, theme_y, screen, enable_shadow=True, return_rect=True)

        # Font Controls
        left_arrow_rect = draw_text("<", font, text_color, WIDTH * left_buffer, font_y, screen, enable_shadow=True, return_rect=True)
        draw_text(f"Font: {current_font_name_or_path}", font, text_color, WIDTH * 0.5, font_y, screen, center=True, enable_shadow=True)
        right_arrow_rect = draw_text(">", font, text_color, WIDTH * right_buffer, font_y, screen, enable_shadow=True, return_rect=True)

        # Credits
        credits_rect = draw_text("Credits", font, text_color, 0, credits_y, screen, center=True, enable_shadow=True, return_rect=True)

        # Generate hover colors and particles if hovered
        hover_elements = [
            (back_to_main_menu_rect, "Back to Main Menu"),
            (minus_rect, "<"), (plus_rect, ">"),
            (resolution_minus_rect, "<"), (resolution_plus_rect, ">"),
            (theme_minus_rect, "<"), (theme_plus_rect, ">"),
            (left_arrow_rect, "<"), (right_arrow_rect, ">"),
            (credits_rect, "Credits")
        ]

        for rect, text in hover_elements:
            is_hovered = rect.collidepoint(mouse_pos)
            color = shadow_color if is_hovered else text_color
            y_pos = rect.y  # Get the y position from the rect for consistent placement
            draw_text(text, font, color, rect.x, y_pos, screen, center=(text in ["Back to Main Menu", "Credits"]), enable_shadow=True)

            # Generate particles on hover
            if is_hovered:
                for _ in range(particle_count):
                    particle_color = random.choice([shadow_color, text_color, screen_color])
                    particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                    particle.lifetime = particle_lifetime
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 3)
                    particle.dx = math.cos(angle) * speed
                    particle.dy = math.sin(angle) * speed
                    particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                if back_to_main_menu_rect and back_to_main_menu_rect.collidepoint(mouse_pos):
                    save_options()
                    return "main_menu"
                
                elif minus_rect and minus_rect.collidepoint(mouse_pos):
                    decrease_volume()
                
                elif plus_rect and plus_rect.collidepoint(mouse_pos):
                    increase_volume()

                if resolution_minus_rect and resolution_minus_rect.collidepoint(mouse_pos):
                    current_resolution_index = max(0, current_resolution_index - 1)
                    current_windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
                    pygame.display.quit()
                    center_window(current_windowed_resolution[0], current_windowed_resolution[1])
                    screen = pygame.display.set_mode(current_windowed_resolution)
                    WIDTH, HEIGHT = current_windowed_resolution
                    update_positions()

                if resolution_plus_rect and resolution_plus_rect.collidepoint(mouse_pos):
                    current_resolution_index = min(len(AVAILABLE_RESOLUTIONS) - 1, current_resolution_index + 1)
                    current_windowed_resolution = AVAILABLE_RESOLUTIONS[current_resolution_index]
                    pygame.display.quit()
                    center_window(current_windowed_resolution[0], current_windowed_resolution[1])
                    screen = pygame.display.set_mode(current_windowed_resolution)
                    WIDTH, HEIGHT = current_windowed_resolution
                    update_positions()
                
                if theme_minus_rect and theme_minus_rect.collidepoint(mouse_pos):
                    current_theme_index = (current_theme_index - 1) % len(color_themes)
                    apply_theme(list(color_themes.keys())[current_theme_index])
                
                if theme_plus_rect and theme_plus_rect.collidepoint(mouse_pos):
                    current_theme_index = (current_theme_index + 1) % len(color_themes)
                    apply_theme(list(color_themes.keys())[current_theme_index])

                if left_arrow_rect and left_arrow_rect.collidepoint(mouse_pos):
                    current_font_index = (current_font_index - 1) % len(filtered_fonts)
                    current_font_name_or_path = filtered_fonts[current_font_index]
                
                if right_arrow_rect and right_arrow_rect.collidepoint(mouse_pos):
                    current_font_index = (current_font_index + 1) % len(filtered_fonts)
                    current_font_name_or_path = filtered_fonts[current_font_index]

                if credits_rect and credits_rect.collidepoint(mouse_pos):
                    credit_roll()

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


############################
### Jr. Church Functions ###
############################

def bible_verse_selector():
    """
    Selects and launches a random Bible verse module.

    This function randomly chooses one of the available Bible verse modules
    and initiates it. Each module focuses on a specific verse, offering a
    unique lesson and reflection opportunity. Additional modules may be added
    to the selection list in the future.

    Returns:
        None
    """
    bible_verse_modules = [
        john_3_16,
        john_13_34,
        psalm_23,
        hebrews_11_1,
        philippians_4_6,
        ephesians_4_32,
        numbers_6_24_26,
        first_thessalonians_5_18,
        luke_2_11
    ]
    selected_module = random.choice(bible_verse_modules)
    selected_module()
    
    
def display_bible_verse(greeting_message, 
                        verse_title, 
                        verse_text, 
                        split_text=None):
    """Displays a Bible verse with support for any number of text splits."""
    global screen_color, text_color, shadow_color, font  # Use global font

    # Define a larger font size for the Bible verse
    large_font_size = 60  # Adjust size as necessary

    # Initialize the larger font based on whether the current font is a file or system font
    if os.path.isfile(current_font_name_or_path):
        large_font = pygame.font.Font(current_font_name_or_path, large_font_size)
    else:
        large_font = pygame.font.SysFont(current_font_name_or_path, large_font_size)

    # Particle effect settings
    particle_count = 3
    particle_lifetime = 30
    particles = []

    # Clear the screen and display the greeting message
    screen.fill(screen_color)

    # Draw the greeting message
    draw_text(
        greeting_message,
        font,  # Use the global font for the greeting
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        max_width=WIDTH
    )

    # Draw the "Continue..." button
    continue_rect = draw_continue_button()

    # Update the display to show the greeting message
    pygame.display.flip()

    # Speak the greeting message aloud
    speak_english(greeting_message)

    # Wait for the user to click "Continue..." with hover effects and particles
    waiting = True
    while waiting:
        screen.fill(screen_color)

        # Redraw the greeting message
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

        # Handle hover effects and particles for "Continue..." button
        mouse_pos = pygame.mouse.get_pos()
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the "Continue..." button
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate hover particles if hovering over the "Continue..." button
        if continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        clock.tick(60)

    # Display the verse content, one part at a time
    if split_text:
        for part in split_text:
            # Clear the screen
            screen.fill(screen_color)

            # Combine the title and current part of the verse
            display_text = verse_title + "\n" + part if verse_title else part

            # Draw the verse text
            draw_text(
                display_text,
                font,
                text_color,
                x=0,
                y=HEIGHT * 0.1,
                center=True,
                enable_shadow=True,
                shadow_color=shadow_color,
                max_width=WIDTH * 0.9,
                font_override=large_font
            )

            pygame.display.flip()

            # Speak the current part of the verse
            speak_english(part)

            # Wait for "Continue..." click before moving to the next part
            waiting = True
            while waiting:
                screen.fill(screen_color)

                # Redraw the verse text
                draw_text(
                    display_text,
                    font,
                    text_color,
                    x=0,
                    y=HEIGHT * 0.1,
                    center=True,
                    enable_shadow=True,
                    shadow_color=shadow_color,
                    max_width=WIDTH * 0.9,
                    font_override=large_font
                )

                # Handle hover effects and particles for "Continue..." button
                mouse_pos = pygame.mouse.get_pos()
                continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color
                draw_text(
                    "Continue...",
                    pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
                    continue_color,
                    x=WIDTH * 0.55,
                    y=HEIGHT * 0.9,
                    enable_shadow=True,
                    shadow_color=shadow_color
                )

                # Generate hover particles if hovering over the "Continue..." button
                if continue_rect.collidepoint(mouse_pos):
                    for _ in range(particle_count):
                        particle_color = random.choice([shadow_color, text_color, screen_color])
                        particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                        particle.lifetime = particle_lifetime
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(1, 3)
                        particle.dx = math.cos(angle) * speed
                        particle.dy = math.sin(angle) * speed
                        particles.append(particle)

                # Update and draw particles
                for particle in particles[:]:
                    particle.update()
                    particle.draw(screen)
                    if particle.lifetime <= 0:
                        particles.remove(particle)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if continue_rect.collidepoint(event.pos):
                            waiting = False  # Exit the loop

                clock.tick(60)
    else:
        # Display the full verse if no splits are provided
        screen.fill(screen_color)
        display_text = verse_title + "\n" + verse_text if verse_title else verse_text
        draw_text(
            display_text,
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.1,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color,
            max_width=WIDTH * 0.9,
            font_override=large_font
        )

        pygame.display.flip()

        # Speak the full verse aloud
        speak_english(display_text)

        # Wait for the user to click "Continue..." with hover effects and particles
        waiting = True
        while waiting:
            screen.fill(screen_color)

            # Redraw the verse text
            draw_text(
                display_text,
                font,
                text_color,
                x=0,
                y=HEIGHT * 0.1,
                center=True,
                enable_shadow=True,
                shadow_color=shadow_color,
                max_width=WIDTH * 0.9,
                font_override=large_font
            )

            # Handle hover effects and particles for "Continue..." button
            mouse_pos = pygame.mouse.get_pos()
            continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color
            draw_text(
                "Continue...",
                pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
                continue_color,
                x=WIDTH * 0.55,
                y=HEIGHT * 0.9,
                enable_shadow=True,
                shadow_color=shadow_color
            )

            # Generate hover particles if hovering over the "Continue..." button
            if continue_rect.collidepoint(mouse_pos):
                for _ in range(particle_count):
                    particle_color = random.choice([shadow_color, text_color, screen_color])
                    particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                    particle.lifetime = particle_lifetime
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 3)
                    particle.dx = math.cos(angle) * speed
                    particle.dy = math.sin(angle) * speed
                    particles.append(particle)

            # Update and draw particles
            for particle in particles[:]:
                particle.update()
                particle.draw(screen)
                if particle.lifetime <= 0:
                    particles.remove(particle)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if continue_rect.collidepoint(event.pos):
                        waiting = False  # Exit the loop

            clock.tick(60)


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
        "The Lord is my shepherd; I shall not want.",
        "He maketh me to lie down in green pastures: he leadeth me beside the still waters.",
        "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake.",
        "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me.",
        "Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over.",
        "Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the Lord for ever."
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


def first_thessalonians_5_18():
    """Greets the student and introduces the Bible verse 1 Thessalonians 5:18 (NKJV)."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "1 Thessalonians 5:18"
    verse_text = "In everything give thanks; for this is the will of God in Christ Jesus for you."
    display_bible_verse(greeting_message, verse_title, verse_text)


def luke_2_11():
    """Greets the student and introduces the Bible verse Luke 2:11 (NKJV)."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "Luke 2:11"
    verse_text = "For there is born to you this day in the city of David a Savior, who is Christ the Lord."
    display_bible_verse(greeting_message, verse_title, verse_text)


def numbers_6_24_26():
    """Greets the student and introduces the Bible verse Numbers 6:24-26 (NKJV)."""
    greeting_message = "It's time to work on a Bible verse!"
    verse_title = "Numbers 6:24-26"
    split_text = [
        "The Lord bless you and keep you; "
        "The Lord make His face shine upon you, "
        "And be gracious to you;",
        "The Lord lift up His countenance upon you, "
        "And give you peace."
    ]
    display_bible_verse(greeting_message, verse_title, "", split_text)


##########################
### Japanese Functions ###
##########################

def greet_student():
    global current_student
    global text_color, shadow_color, screen_color
    
    stop_mp3()

    # Get the current time
    current_time = datetime.now().time()

    # Determine the appropriate greeting based on the time of day
    if current_time >= datetime.strptime("00:01", "%H:%M").time() and current_time < datetime.strptime("12:00", "%H:%M").time():
        greeting_message_eng = f"Good morning, {current_student}! Welcome to your lesson."
        greeting_message_jp = "おはようございます。"  # Good morning in Japanese
    elif current_time >= datetime.strptime("12:00", "%H:%M").time() and current_time < datetime.strptime("17:00", "%H:%M").time():
        greeting_message_eng = f"Hello, {current_student}! Welcome to your lesson."
        greeting_message_jp = "こんにちは。"  # Hello in Japanese
    else:
        greeting_message_eng = f"Good evening, {current_student}! Welcome to your lesson."
        greeting_message_jp = "こんばんは。"  # Good evening in Japanese

    # Set a static sky blue background with Perlin clouds and static elements
    SKY_BLUE = (135, 206, 235)
    screen.fill(SKY_BLUE)
    cloud_surface = generate_perlin_cloud(0)  # Static clouds
    screen.blit(cloud_surface, (0, 0))

    # Draw trees and static greeting text once
    grow_tree(screen, WIDTH * 0.25, HEIGHT, max_depth=10, max_branches=3)
    grow_tree(screen, WIDTH * 0.75, HEIGHT, max_depth=11, max_branches=3)
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

    # Draw initial Japanese greeting and "Continue..." button text
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
        return_rect=True
    )

    continue_font_size = int(get_dynamic_font_size() * 0.8)
    continue_font = pygame.font.SysFont(current_font_name_or_path, continue_font_size)
    continue_text = "Continue..."
    continue_x_position = WIDTH * 0.55
    continue_y_position = HEIGHT * 0.90
    text_width, text_height = continue_font.size(continue_text)
    continue_rect = pygame.Rect(continue_x_position, continue_y_position, text_width, text_height)

    # Create a static background surface to avoid redrawing static elements every frame
    static_background = screen.copy()  # Save current screen as the static background
    pygame.display.flip()
    speak_japanese(greeting_message_jp)  # Play initial greeting

    # Particle effect settings
    particle_count = 3
    particle_lifetime = 30
    particles = []

    # Main event loop for dynamic elements
    waiting = True
    while waiting:
        # Blit the static background to clear the screen each frame
        screen.blit(static_background, (0, 0))

        # Get current mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover colors for the Japanese text and "Continue..." button
        japanese_text_color = shadow_color if japanese_text_rect.collidepoint(mouse_pos) else text_color
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the hoverable elements without touching the static background
        draw_text(greeting_message_jp, j_font, japanese_text_color, 0, HEIGHT * 0.60, screen, center=True, enable_shadow=True, shadow_color=shadow_color)
        draw_text(continue_text, continue_font, continue_color, continue_x_position, continue_y_position, screen, enable_shadow=True)

        # Generate particles if hovering over Japanese text or "Continue..."
        if japanese_text_rect.collidepoint(mouse_pos) or continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if japanese_text_rect.collidepoint(event.pos):
                    speak_japanese(greeting_message_jp)
                elif continue_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        clock.tick(60)


def calculate_easter(year):
    """Calculate the date of Easter Sunday for a given year."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day).date()


def calculate_thanksgiving(year):
    """Calculate the date of Thanksgiving (4th Thursday of November)."""
    first_day_of_november = datetime(year, 11, 1).date()
    first_thursday = first_day_of_november + timedelta(days=(3 - first_day_of_november.weekday()) % 7)
    thanksgiving = first_thursday + timedelta(weeks=3)
    return thanksgiving


def calculate_mothers_day(year):
    """Calculate the date of Mother's Day (2nd Sunday of May)."""
    first_day_of_may = datetime(year, 5, 1).date()
    first_sunday = first_day_of_may + timedelta(days=(6 - first_day_of_may.weekday()) % 7)
    mothers_day = first_sunday + timedelta(weeks=1)
    return mothers_day


def calculate_fathers_day(year):
    """Calculate the date of Father's Day (3rd Sunday of June)."""
    first_day_of_june = datetime(year, 6, 1).date()
    first_sunday = first_day_of_june + timedelta(days=(6 - first_day_of_june.weekday()) % 7)
    fathers_day = first_sunday + timedelta(weeks=2)
    return fathers_day


def days_until_next_event():
    """
    Calculate the number of days until the next special event.

    Returns:
        tuple: (event_name, days_remaining)
    """
    special_dates = {
        "New Year's Day": "01-01",
        "Groundhog Day": "02-02",
        "Valentine's Day": "02-14",
        "Pi Day": "03-14",
        "St. Patrick's Day": "03-17",
        "April Fool's Day": "04-01",
        "Ethan's birthday": "06-16",
        "4th of July": "07-04",
        "Mommy's birthday": "07-29",
        "Halloween": "10-31",
        "William's birthday": "11-19",
        "Christmas": "12-25",
        "Daddy's birthday": "12-30"
    }

    today = datetime.now().date()
    current_year = today.year

    # Dynamically calculate holiday dates
    def get_next_event_date(event_name, date_function, year):
        """Helper to calculate the next occurrence of a dynamic event."""
        event_date = date_function(year)
        if today > event_date:  # If event has passed, calculate for next year
            event_date = date_function(year + 1)
        return event_date

    easter_date = get_next_event_date("Easter", calculate_easter, current_year)
    thanksgiving_date = get_next_event_date("Thanksgiving", calculate_thanksgiving, current_year)
    mothers_day_date = get_next_event_date("Mother's Day", calculate_mothers_day, current_year)
    fathers_day_date = get_next_event_date("Father's Day", calculate_fathers_day, current_year)

    special_dates_dynamic = {
        "Easter": easter_date,
        "Mother's Day": mothers_day_date,
        "Father's Day": fathers_day_date,
        "Thanksgiving": thanksgiving_date
    }

    # Combine fixed and dynamic dates
    all_events = {**special_dates}
    all_events.update({name: date.strftime("%m-%d") for name, date in special_dates_dynamic.items()})

    next_event = None
    min_days = float('inf')

    for event, date_str in all_events.items():
        event_date = datetime.strptime(date_str, "%m-%d").date().replace(year=current_year)

        # If the event date has passed this year, calculate it for the next year
        if event_date < today:
            event_date = event_date.replace(year=current_year + 1)

        days_remaining = (event_date - today).days
        if days_remaining < min_days:
            min_days = days_remaining
            next_event = event

    return next_event, min_days


def display_next_event():
    """
    Display a message about the next special event and allow the user to continue.
    """
    global text_color, shadow_color, screen_color

    # Get the next event and days remaining
    event_name, days_remaining = days_until_next_event()

    # Prepare the message
    message_eng = f"It's {days_remaining} days until {event_name}!"
    message_jp = f"{event_name}まで、 あと{days_remaining}日です！"  # Japanese equivalent

    # Set the background color
    screen.fill(screen_color)

    # Display the event message in English
    draw_text(
        message_eng,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.30,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Display the static Japanese message (no hover effect)
    draw_text(
        message_jp,
        j_font,
        text_color,
        x=0,
        y=HEIGHT * 0.50,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        max_width=WIDTH
    )

    # Draw "Continue" button and save rect for hover detection
    continue_font_size = int(get_dynamic_font_size() * 0.8)
    continue_font = pygame.font.SysFont(current_font_name_or_path, continue_font_size)
    continue_text = "Continue..."
    continue_x_position = WIDTH * 0.55
    continue_y_position = HEIGHT * 0.90
    text_width, text_height = continue_font.size(continue_text)
    continue_rect = pygame.Rect(continue_x_position, continue_y_position, text_width, text_height)

    draw_text(
        continue_text,
        continue_font,
        text_color,
        continue_x_position,
        continue_y_position,
        enable_shadow=True,
        shadow_color=shadow_color
    )
    
    # Update the screen with all elements drawn
    pygame.display.flip()

    # Speak the English message after everything is displayed
    speak_english(message_eng)

    # Create a static background surface
    static_background = screen.copy()  # Save current screen as the static background
    pygame.display.flip()

    # Particle effect settings
    particle_count = 3
    particle_lifetime = 30
    particles = []

    # Main event loop
    waiting = True
    while waiting:
        # Blit the static background to clear the screen each frame
        screen.blit(static_background, (0, 0))

        # Get current mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()

        # Hover effect for "Continue" button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Generate particles if hovering over "Continue..."
        if continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        # Redraw "Continue" button
        draw_text(
            continue_text,
            continue_font,
            continue_color,
            continue_x_position,
            continue_y_position,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        clock.tick(60)


def wrap_up_session():
    """
    Displays a wrap-up message with interactive hover effects.

    This function shows an English and Japanese wrap-up message. Both messages
    and the "Finish" button are interactive, with hover effects and particle
    effects. The user clicks "Finish" to proceed.
    """
    global current_student
    global text_color, shadow_color, screen_color

    stop_mp3()

    # Prepare wrap-up messages
    wrap_up_message_eng = f"Great job today, {current_student}! See you next time."
    wrap_up_message_jp = "お疲れ様でした。"  # Otsukaresama deshita

    # Set a static sky blue background with Perlin clouds
    SKY_BLUE = (135, 206, 235)
    screen.fill(SKY_BLUE)
    cloud_surface = generate_perlin_cloud(0)  # Static clouds
    screen.blit(cloud_surface, (0, 0))

    # Draw static wrap-up text
    draw_text(
        wrap_up_message_eng,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.20,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Draw Japanese wrap-up message and save rect for hover detection
    japanese_text_rect = draw_text(
        wrap_up_message_jp,
        j_font,
        text_color,
        x=0,
        y=HEIGHT * 0.50,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True
    )

    # Position "Finish" button
    finish_text = "Finish"
    finish_font_size = int(get_dynamic_font_size() * 0.8)
    finish_font = pygame.font.SysFont(current_font_name_or_path, finish_font_size)
    finish_x_position = WIDTH * 0.55
    finish_y_position = HEIGHT * 0.90  # Aligning to 90% down the screen
    text_width, text_height = finish_font.size(finish_text)
    finish_rect = pygame.Rect(finish_x_position, finish_y_position, text_width, text_height)

    draw_text(
        finish_text,
        finish_font,
        text_color,
        finish_x_position,
        finish_y_position,
        screen,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Create a static background surface
    static_background = screen.copy()  # Save current screen as static background
    pygame.display.flip()
    speak_japanese(wrap_up_message_jp)  # Play Japanese wrap-up message

    # Particle effect settings
    particle_count = 3
    particle_lifetime = 30
    particles = []

    # Main event loop
    waiting = True
    while waiting:
        # Blit the static background to clear the screen each frame
        screen.blit(static_background, (0, 0))

        # Get current mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()

        # Hover color logic
        japanese_text_color = shadow_color if japanese_text_rect.collidepoint(mouse_pos) else text_color
        finish_color = shadow_color if finish_rect.collidepoint(mouse_pos) else text_color

        # Redraw hoverable elements
        draw_text(
            wrap_up_message_jp,
            j_font,
            japanese_text_color,
            0,
            HEIGHT * 0.50,
            screen,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        draw_text(
            finish_text,
            finish_font,
            finish_color,
            finish_x_position,
            finish_y_position,
            screen,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate particles on hover
        if japanese_text_rect.collidepoint(mouse_pos) or finish_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if japanese_text_rect.collidepoint(event.pos):
                    speak_japanese(wrap_up_message_jp)
                elif finish_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        clock.tick(60)

        
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

    # Draw the initial "Continue..." button and get its rect
    continue_rect = draw_continue_button()

    # Display the Japanese message and get its rect
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
        return_rect=True
    )

    # Speak the Japanese message aloud using the reusable TTS function
    speak_japanese(japanese_message)

    # Particle effect settings
    particle_count = 3
    particle_lifetime = 30
    particles = []

    # Main event loop for dynamic elements
    waiting = True
    while waiting:
        # Clear the screen each frame
        screen.fill(screen_color)

        # Get current mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover colors for the Japanese text and "Continue..." button
        japanese_text_color = shadow_color if japanese_text_rect.collidepoint(mouse_pos) else text_color
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the Japanese message with hover color
        japanese_text_rect = draw_text(
            japanese_message,
            j_font,
            japanese_text_color,
            x=0,
            y=HEIGHT * 0.25,
            max_width=WIDTH * 0.95,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color,
            return_rect=True
        )

        # Redraw the English message (not hoverable)
        draw_text(
            english_message,
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.45,
            max_width=WIDTH * 0.95,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Redraw the "Continue..." button with hover color
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate particles if hovering over Japanese text or "Continue..."
        if japanese_text_rect.collidepoint(mouse_pos) or continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the Japanese text is clicked
                if japanese_text_rect.collidepoint(event.pos):
                    speak_japanese(japanese_message)  # Replay the Japanese message

                # Check if the "Continue..." button is clicked
                if check_continue_click(event.pos, continue_rect):
                    waiting = False  # Exit the loop

        # Cap frame rate
        clock.tick(60)


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

    # Initialize the text rectangles
    japanese_text_rect = pygame.Rect(0, 0, 0, 0)  # Placeholder for Japanese text rect
    continue_rect = pygame.Rect(0, 0, 0, 0)       # Placeholder for "Continue..." button rect

    # Particle effect settings
    particle_count = 3
    particle_lifetime = 30
    particles = []

    # Render the first frame to display the text and button, then auto-play the audio
    screen.fill(screen_color)

    # Draw the Japanese message and get its rect
    japanese_text_rect = draw_text(
        japanese_message,
        j_font,
        text_color,
        x=0,
        y=HEIGHT * 0.25,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True
    )

    # Draw the English message (non-hoverable)
    draw_text(
        english_message,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.45,
        max_width=WIDTH * 0.95,
        center=True,
        enable_shadow=True,
        shadow_color=shadow_color
    )

    # Draw the "Continue..." button and get its rect
    continue_rect = draw_text(
        "Continue...",
        pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
        text_color,
        x=WIDTH * 0.55,
        y=HEIGHT * 0.9,
        enable_shadow=True,
        shadow_color=shadow_color,
        return_rect=True
    )

    # Update the display with the first frame
    pygame.display.flip()

    # Auto-play the Japanese message
    speak_japanese(japanese_message)

    # Main loop for interaction
    waiting = True
    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover state for Japanese text
        japanese_text_color = shadow_color if japanese_text_rect.collidepoint(mouse_pos) else text_color

        # Redraw the Japanese message with hover effect
        japanese_text_rect = draw_text(
            japanese_message,
            j_font,
            japanese_text_color,
            x=0,
            y=HEIGHT * 0.25,
            max_width=WIDTH * 0.95,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color,
            return_rect=True
        )

        # Redraw the English message (non-hoverable)
        draw_text(
            english_message,
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.45,
            max_width=WIDTH * 0.95,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Determine hover state for the "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the "Continue..." button with hover effect
        continue_rect = draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color,
            return_rect=True
        )

        # Generate particles if hovering over Japanese text or "Continue..."
        if japanese_text_rect.collidepoint(mouse_pos) or continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the Japanese text is clicked
                if japanese_text_rect.collidepoint(event.pos):
                    speak_japanese(japanese_message)  # Replay the Japanese message

                # Check if the "Continue..." button is clicked
                if continue_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        # Cap frame rate
        clock.tick(60)


def skip_counting_japanese(COUNT_TO=30):
    """Performs skip counting in Arabic numerals up to COUNT_TO, while speaking the numbers in Japanese."""
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
    intro_message = f"Let's count in Japanese, up to {COUNT_TO}!"

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

    # Start counting from 1 to COUNT_TO
    for i in range(1, COUNT_TO + 1):
        # Continuously check for events to prevent freezing and handle window focus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.ACTIVEEVENT and event.gain == 1:  # Window regains focus
                pygame.display.flip()  # Redraw the screen

        # Clear the screen before displaying each number
        screen.fill(screen_color)

        # Convert the number to string for display
        number_str = str(i)

        # Display the number in the center of the screen using the larger font size
        draw_text(number_str, large_font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

        # Update the screen after drawing the number
        pygame.display.flip()

        # Speak the number aloud in Japanese 
        speak_japanese(number_str)

        # Pause for a second before showing the next number
        time.sleep(2)

    # After completing the skip counting, show a dynamic completion message using the default font
    completion_message = f"Great job! You counted up to {COUNT_TO}!"
    screen.fill(screen_color)
    draw_text(completion_message, 
              font, 
              text_color, 
              x=0, 
              y=HEIGHT * 0.4, 
              center=True, 
              enable_shadow=True, 
              shadow_color=shadow_color,
              max_width=WIDTH)

    # Draw the "Continue..." button after the completion message
    draw_and_wait_continue_button()


def skip_counting_kanji(COUNT_TO=30):
    """Performs skip counting using kanji, with furigana displayed above the kanji and numbers spoken in Japanese."""
    global screen_color, text_color, shadow_color, current_font_name_or_path, font  # Access theme-related globals

    # Define a larger size for the kanji numerals and furigana
    large_kanji_font_size = 200  # Adjust size as necessary
    furigana_font_size = 60

    # Initialize the fonts for kanji and furigana using a Japanese-supporting font
    if os.path.isfile(current_font_name_or_path):
        kanji_font = pygame.font.Font(current_font_name_or_path, large_kanji_font_size)
        furigana_font = pygame.font.Font(current_font_name_or_path, furigana_font_size)
    else:
        kanji_font = pygame.font.SysFont('msgothic', large_kanji_font_size)  # Example: MS Gothic or another font that supports Kanji
        furigana_font = pygame.font.SysFont('msgothic', furigana_font_size)

    # Dictionary to map numbers (1 to 30) to their corresponding Kanji and Furigana
    kanji_numbers = {
        1: ("一", "いち"), 2: ("二", "に"), 3: ("三", "さん"), 4: ("四", "よん"), 5: ("五", "ご"),
        6: ("六", "ろく"), 7: ("七", "なな"), 8: ("八", "はち"), 9: ("九", "きゅう"), 10: ("十", "じゅう"),
        11: ("十一", "じゅういち"), 12: ("十二", "じゅうに"), 13: ("十三", "じゅうさん"), 14: ("十四", "じゅうよん"),
        15: ("十五", "じゅうご"), 16: ("十六", "じゅうろく"), 17: ("十七", "じゅうなな"), 18: ("十八", "じゅうはち"),
        19: ("十九", "じゅうきゅう"), 20: ("二十", "にじゅう"), 21: ("二十一", "にじゅういち"),
        22: ("二十二", "にじゅうに"), 23: ("二十三", "にじゅうさん"), 24: ("二十四", "にじゅうよん"),
        25: ("二十五", "にじゅうご"), 26: ("二十六", "にじゅうろく"), 27: ("二十七", "にじゅうなな"),
        28: ("二十八", "にじゅうはち"), 29: ("二十九", "にじゅうきゅう"), 30: ("三十", "さんじゅう")
    }

    # Clear the screen and inform the student about the activity
    screen.fill(screen_color)
    intro_message = f"Let's count using kanji up to {COUNT_TO}!"

    # Display the intro message and update the screen using the default global font, with word wrapping
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

    # Start counting from 1 to COUNT_TO
    for i in range(1, COUNT_TO + 1):
        # Process events to prevent freezing and handle window focus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.ACTIVEEVENT and event.gain == 1:  # Window regains focus
                pygame.display.flip()  # Redraw the screen

        # Clear the screen before displaying each kanji
        screen.fill(screen_color)

        # Get the Kanji and Furigana for the current number
        kanji, furigana = kanji_numbers[i]

        # Display furigana above the kanji
        draw_text(furigana, furigana_font, text_color, x=0, y=HEIGHT * 0.3, center=True, enable_shadow=True, shadow_color=shadow_color)

        # Display the kanji in the center of the screen using the larger font size
        draw_text(kanji, kanji_font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color)

        # Update the screen after drawing the kanji and furigana
        pygame.display.flip()

        # Speak the number aloud in Japanese
        speak_japanese(furigana)

        # Pause for a second before showing the next number
        time.sleep(1)

    # After completing the skip counting, show a dynamic completion message using the default font, with word wrapping
    completion_message = f"Great job counting with kanji up to {COUNT_TO}!"
    screen.fill(screen_color)
    draw_text(completion_message, font, text_color, x=0, y=HEIGHT * 0.4, center=True, enable_shadow=True, shadow_color=shadow_color, max_width=WIDTH)

    # Draw the "Continue..." button after the completion message
    draw_and_wait_continue_button()
    

def get_character_subset_by_level(student_level, character_list):
    """Dynamically returns a subset of characters based on the student's level, with specific grouping sizes."""
    
    # Define the group sizes by level
    group_sizes = [5, 5, 5, 5, 5, 5, 5, 3, 5, 3, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

    # Calculate the total number of characters to include based on student level
    max_characters = 0
    for i in range(student_level):
        if i < len(group_sizes):
            max_characters += group_sizes[i]
        else:
            max_characters += 3  # Extend pattern with 3 characters per level after group_sizes

    # Return the subset up to the calculated number of characters
    return character_list[:max_characters]


def display_intro_message(lesson_type, student_level):
    """Displays the intro message for the lesson."""
    # Particle effect settings
    particles = []
    particle_count = 3
    particle_lifetime = 30

    # Main event loop
    waiting = True
    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Display the intro message
        intro_message = f"Let's learn {lesson_type}! You are currently on level {student_level}."
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

        # Draw the "Continue..." button
        continue_rect = draw_continue_button()

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover color for the "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the "Continue..." button with hover effect
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate particles if hovering over the "Continue..." button
        if continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):  # Limit particle generation per frame
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if "Continue..." button is clicked
                if continue_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        # Cap the frame rate
        clock.tick(60)


def display_completion_message(lesson_type, student_level, url):
    """Displays the completion message with a dynamic level and opens a URL if provided."""
    # Open URL if provided
    if url:
        log_message(f"Opening URL: {url}")
        webbrowser.open(url)

    # Particle effect settings
    particles = []
    particle_count = 3
    particle_lifetime = 30

    # Main event loop
    waiting = True
    while waiting:
        # Clear the screen for a new frame
        screen.fill(screen_color)

        # Display the completion message
        completion_message = f"Great job studying {lesson_type} at level {student_level}!"
        draw_text(
            completion_message,
            font,
            text_color,
            x=0,
            y=HEIGHT * 0.4,
            center=True,
            enable_shadow=True,
            shadow_color=shadow_color,
            max_width=WIDTH * 0.95
        )

        # Draw the "Continue..." button
        continue_rect = draw_continue_button()

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine hover color for the "Continue..." button
        continue_color = shadow_color if continue_rect.collidepoint(mouse_pos) else text_color

        # Redraw the "Continue..." button with hover effect
        draw_text(
            "Continue...",
            pygame.font.SysFont(current_font_name_or_path, int(get_dynamic_font_size() * 0.8)),
            continue_color,
            x=WIDTH * 0.55,
            y=HEIGHT * 0.9,
            enable_shadow=True,
            shadow_color=shadow_color
        )

        # Generate particles if hovering over the "Continue..." button
        if continue_rect.collidepoint(mouse_pos):
            for _ in range(particle_count):  # Limit particle generation per frame
                particle_color = random.choice([shadow_color, text_color, screen_color])
                particle = Particle(mouse_pos[0], mouse_pos[1], particle_color)
                particle.lifetime = particle_lifetime
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle.dx = math.cos(angle) * speed
                particle.dy = math.sin(angle) * speed
                particles.append(particle)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if "Continue..." button is clicked
                if continue_rect.collidepoint(event.pos):
                    waiting = False  # Exit the loop

        # Cap the frame rate
        clock.tick(60)


def teach_characters(hiragana_subset, font):
    """Displays each Hiragana character one by one and ensures the screen redraws with each."""
    for char in hiragana_subset:
        # Continuously process events to avoid freezing and handle window focus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.ACTIVEEVENT and event.gain == 1:  # Window regains focus
                pygame.display.flip()  # Redraw the screen

        # Clear the screen with the background color and display the current character
        screen.fill(screen_color)
        character_surface = font.render(char, True, text_color)
        character_rect = character_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(character_surface, character_rect)
        pygame.display.flip()  # Update the display with the new character

        # Play the corresponding WAV file for the character
        speak_japanese(char)  # Use speak_japanese directly

        # Optional: Small delay to control playback speed
        time.sleep(0.5)


def run_teach(session_id, lesson_name, character_list, level_urls):
    """Generalized function to teach Japanese characters based on the student's level."""
    global screen_color, text_color, shadow_color  # Access theme-related globals

    # Set the wait time in milliseconds
    wait_time = 1500  

    # Retrieve the student's current level for the specified lesson
    student_level = get_student_progress(session_id, lesson_name)

    # Get the subset of characters based on the student's level
    character_subset = get_character_subset_by_level(student_level, character_list)

    # Define a larger font for the characters
    large_japanese_font = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", 300)

    # Display the intro message and teach the characters
    display_intro_message(lesson_name, student_level)

    # Main loop to display each character
    for char in character_subset:
        # Continuously check for events to prevent the window from freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.ACTIVEEVENT and event.gain == 1:  # Window regains focus
                pygame.display.flip()  # Redraw the screen

        # Clear the screen and display the current character with a shadow effect
        screen.fill(screen_color)
        
        # Render shadow character slightly offset
        shadow_surface = large_japanese_font.render(char, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(screen.get_width() // 2 + 5, screen.get_height() // 2 + 5))  # Offset shadow slightly
        screen.blit(shadow_surface, shadow_rect)
        
        # Render main character on top of shadow
        character_surface = large_japanese_font.render(char, True, text_color)
        character_rect = character_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(character_surface, character_rect)
        
        pygame.display.flip()  # Update the display

        # Play the WAV file
        speak_japanese(char)

        # Wait for the specified delay before moving to the next character
        pygame.time.delay(wait_time)

    # Show completion message and open the appropriate URL based on level
    completion_url = level_urls.get(student_level, level_urls.get(1))  # Default to level 1 URL if level not found
    display_completion_message(lesson_name, student_level, completion_url)


def hiragana_teach(session_id):
    """Displays Hiragana characters based on the student's level."""
    hiragana_list = [
        # Basic Hiragana
        "あ", "い", "う", "え", "お", 
        "か", "き", "く", "け", "こ", 
        "さ", "し", "す", "せ", "そ", 
        "た", "ち", "つ", "て", "と", 
        "な", "に", "ぬ", "ね", "の", 
        "は", "ひ", "ふ", "へ", "ほ", 
        "ま", "み", "む", "め", "も", 
        "や", "ゆ", "よ", 
        "ら", "り", "る", "れ", "ろ", 
        "わ", "を", "ん",
        
        # Voiced Hiragana - "ga", "za", "da", "ba" columns
        "が", "ぎ", "ぐ", "げ", "ご", 
        "ざ", "じ", "ず", "ぜ", "ぞ", 
        "だ", "ぢ", "づ", "で", "ど", 
        "ば", "び", "ぶ", "べ", "ぼ",
        
        # "Pa" column with handakuten
        "ぱ", "ぴ", "ぷ", "ぺ", "ぽ",
        
        # Contracted Sounds (ya-yōon) 
        "きゃ", "きゅ", "きょ", 
        "しゃ", "しゅ", "しょ", 
        "ちゃ", "ちゅ", "ちょ", 
        "にゃ", "にゅ", "にょ", 
        "ひゃ", "ひゅ", "ひょ", 
        "みゃ", "みゅ", "みょ", 
        "りゃ", "りゅ", "りょ",
        
        # Voiced Contracted Sounds (ya-yōon)
        "ぎゃ", "ぎゅ", "ぎょ", 
        "じゃ", "じゅ", "じょ", 
        "びゃ", "びゅ", "びょ", 
        "ぴゃ", "ぴゅ", "ぴょ"
    ]

    # URLs for each level
    level_urls = {
        # Basic Hiragana
        1: "https://www.youtube.com/watch?v=bEPagHe6iUI",  # あ
        2: "https://www.youtube.com/watch?v=X4mCd2y-k4c",  # か
        3: "https://www.youtube.com/watch?v=J9MvqJnj5kQ",  # さ
        4: "https://www.youtube.com/watch?v=r9aH5OoyloM",  # た
        5: "https://www.youtube.com/watch?v=rsL86uUTJpw",  # な
        6: "https://www.youtube.com/watch?v=z_47dk9eFFs",  # は
        7: "https://www.youtube.com/watch?v=_Hk2d4AO-Uk",  # ま
        8: "https://www.youtube.com/watch?v=HBC2LrtoIWM",  # や
        9: "https://www.youtube.com/watch?v=AmQ9kmom1v8",  # ら
        10: "https://www.youtube.com/watch?v=awAReY29ZGs", # わ-ん
        
        # Voiced Hiragana
        11: "https://www.youtube.com/watch?v=lW8V5uMMM-4", # が
        12: "https://www.youtube.com/watch?v=QaL6JSCbpWo", # ざ
        13: "https://www.youtube.com/watch?v=5yPgd1sR6KY", # だ
        14: "https://www.youtube.com/watch?v=VYCJDaWWcIs", # ば
        15: "https://www.youtube.com/watch?v=EZb3fs4Ntgc", # ぱ
        
        # Contracted Sounds (ya-yōon)
        16: "https://www.youtube.com/watch?v=nGLciw6mZCo", # きゃ
        17: "https://www.youtube.com/watch?v=Asy10OI-lFU", # しゃ
        18: "https://www.youtube.com/watch?v=V34OFinfTbU", # ちゃ
        
        # Missing placeholders for levels with no URLs provided
        19: "",  # にゃ (placeholder)
        20: "",  # ひゃ (placeholder)
        21: "",  # みゃ (placeholder)
        22: "",  # りゃ (placeholder)
        
        # Voiced Contracted Sounds (ya-yōon)
        23: "https://www.youtube.com/watch?v=k4XbM3pCNTs",  # ぎゃ
        24: "",  # じゃ (placeholder)
        25: "",  # びゃ (placeholder)
        26: ""   # ぴゃ (placeholder)
    }

    run_teach(session_id, 'Hiragana', hiragana_list, level_urls)


def katakana_teach(session_id):
    """Displays Katakana characters based on the student's level."""
    katakana_list = [
        # Basic Katakana
        "ア", "イ", "ウ", "エ", "オ", 
        "カ", "キ", "ク", "ケ", "コ", 
        "サ", "シ", "ス", "セ", "ソ", 
        "タ", "チ", "ツ", "テ", "ト", 
        "ナ", "ニ", "ヌ", "ネ", "ノ", 
        "ハ", "ヒ", "フ", "ヘ", "ホ", 
        "マ", "ミ", "ム", "メ", "モ", 
        "ヤ", "ユ", "ヨ", 
        "ラ", "リ", "ル", "レ", "ロ", 
        "ワ", "ヲ", "ン",
        
        # Voiced Katakana - "ga", "za", "da", "ba" columns
        "ガ", "ギ", "グ", "ゲ", "ゴ", 
        "ザ", "ジ", "ズ", "ゼ", "ゾ", 
        "ダ", "ヂ", "ヅ", "デ", "ド", 
        "バ", "ビ", "ブ", "ベ", "ボ",
        
        # "Pa" column with handakuten
        "パ", "ピ", "プ", "ペ", "ポ",
        
        # Contracted Sounds (ya-yōon)
        "キャ", "キュ", "キョ", 
        "シャ", "シュ", "ショ", 
        "チャ", "チュ", "チョ", 
        "ニャ", "ニュ", "ニョ", 
        "ヒャ", "ヒュ", "ヒョ", 
        "ミャ", "ミュ", "ミョ", 
        "リャ", "リュ", "リョ",
        
        # Voiced Contracted Sounds (ya-yōon)
        "ギャ", "ギュ", "ギョ", 
        "ジャ", "ジュ", "ジョ", 
        "ビャ", "ビュ", "ビョ", 
        "ピャ", "ピュ", "ピョ"
    ]

    level_urls = {
        # Define URLs specific to Katakana if available or use placeholders
    }

    run_teach(session_id, 'Katakana', katakana_list, level_urls)


def display_kana_quiz(screen, hiragana_char, options):
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
        # shadow_color=BLACK,
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
            # shadow_color=BLACK,
            return_rect=True
        )
        option_rects.append((option_rect, option))

    pygame.display.flip()
    return option_rects


def quiz_intro_message(session_id, lesson_title, student_level):
    """Displays the introductory quiz message."""
    screen.fill(screen_color)
    intro_message = f"{lesson_title} quiz! You are currently on level {student_level}."
    draw_text(intro_message, font, text_color, x=0, 
              y=HEIGHT * 0.4, 
              max_width=WIDTH * 0.95, 
              center=True, 
              enable_shadow=True, 
              # shadow_color=shadow_color
              )
    draw_and_wait_continue_button()


def quiz_loop(lesson_title, character_subset, total_questions):
    """Handles the quiz loop, ensuring unique questions are selected from the weighted subset."""
    correct_answers = 0
    completion_times = []
    asked_characters = set()  # Track characters that have already been quizzed

    for problem_count in range(total_questions):
        # Select a unique character for the question
        character, correct_english = None, None
        while not character or (character, correct_english) in asked_characters:
            character, correct_english = random.choice(character_subset)

        # Add the chosen character to the set of asked characters
        asked_characters.add((character, correct_english))

        # Select three unique incorrect answers
        all_romaji_options = [ch[1] for ch in character_subset if ch[1] != correct_english]
        incorrect_answers = set()
        while len(incorrect_answers) < 3:
            incorrect_answers.add(random.choice(all_romaji_options))
        incorrect_answers = list(incorrect_answers)

        # Combine correct answer and unique incorrect answers, then shuffle
        options = [correct_english] + incorrect_answers
        random.shuffle(options)
        
        # Display the quiz options and get option rects
        option_rects = display_kana_quiz(screen, character, options)

        # Wait for student to select an option
        start_time = time.time()
        question_complete = False
        while not question_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
    
    return correct_answers, completion_times


def final_score_display(session_id, lesson_id, correct_answers, total_questions, completion_times, lesson_start_time, lesson_end_time, lesson_title):
    """Displays the final score and updates the student's progress."""
    average_time = round(sum(completion_times) / len(completion_times), 1) if completion_times else 0
    add_session_lesson(session_id, lesson_id, lesson_start_time, lesson_end_time, total_questions, correct_answers)

    # Display final score
    screen.fill(screen_color)
    draw_text(f"Final Score: {correct_answers}/{total_questions}", font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)

    if correct_answers == total_questions:
        set_student_progress(session_id, lesson_title)  # Level up on perfect score
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        if average_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()

    if correct_answers == total_questions:
        bonus_game_selector()


def run_quiz(session_id, lesson_name, character_list):
    """Runs a quiz on a set of characters based on the student's level."""
    global screen_color, text_color  # Access theme-related globals

    # Retrieve the student's current level for the specified lesson
    student_level = get_student_progress(session_id, lesson_name)

    # Fetch the lesson ID
    lesson_id = fetch_lesson_id(lesson_name)
    if lesson_id is None:
        return -1  # Exit if lesson_id not found

    # Define total questions
    total_questions = 5

    # Display introductory message with student's current level
    screen.fill(screen_color)
    draw_text(f"{lesson_name} quiz! You are currently on level {student_level}.", font, text_color,
              x=0, y=HEIGHT * 0.4, max_width=WIDTH * 0.95, center=True, 
              enable_shadow=True)

    draw_and_wait_continue_button()

    # Start the lesson timer
    lesson_start_time = time.time()

    # Get the subset of characters based on level
    character_subset = get_character_subset_by_level(student_level, character_list)

    # Favor the last few characters of the subset by duplicating them
    character_subset += character_subset[-5:] * student_level  # Duplicate the last 5 characters for favoring

    # Shuffle to randomize quiz questions
    random.shuffle(character_subset)

    # Run the quiz loop
    correct_answers, completion_times = quiz_loop(lesson_name, character_subset, total_questions)

    # Record lesson end time
    lesson_end_time = time.time()

    # Final score and performance display
    final_score_display(session_id, lesson_id, correct_answers, total_questions, completion_times, 
                        lesson_start_time, lesson_end_time, lesson_title=lesson_name)

    # Return quiz results
    return total_questions, correct_answers, sum(completion_times) / len(completion_times) if completion_times else 0


def hiragana_quiz(session_id):
    """Presents a quiz on Hiragana characters."""
    hiragana_list = [
        # Basic Hiragana
        ('あ', 'a'), ('い', 'i'), ('う', 'u'), ('え', 'e'), ('お', 'o'),  # a, i, u, e, o
        ('か', 'ka'), ('き', 'ki'), ('く', 'ku'), ('け', 'ke'), ('こ', 'ko'),  # ka, ki, ku, ke, ko
        ('さ', 'sa'), ('し', 'shi'), ('す', 'su'), ('せ', 'se'), ('そ', 'so'),  # sa, shi, su, se, so
        ('た', 'ta'), ('ち', 'chi'), ('つ', 'tsu'), ('て', 'te'), ('と', 'to'),  # ta, chi, tsu, te, to
        ('な', 'na'), ('に', 'ni'), ('ぬ', 'nu'), ('ね', 'ne'), ('の', 'no'),  # na, ni, nu, ne, no
        ('は', 'ha'), ('ひ', 'hi'), ('ふ', 'fu'), ('へ', 'he'), ('ほ', 'ho'),  # ha, hi, fu, he, ho
        ('ま', 'ma'), ('み', 'mi'), ('む', 'mu'), ('め', 'me'), ('も', 'mo'),  # ma, mi, mu, me, mo
        ('や', 'ya'), ('ゆ', 'yu'), ('よ', 'yo'),  # ya, yu, yo
        ('ら', 'ra'), ('り', 'ri'), ('る', 'ru'), ('れ', 're'), ('ろ', 'ro'),  # ra, ri, ru, re, ro
        ('わ', 'wa'), ('を', 'wo'), ('ん', 'n'),  # wa, wo, n
    
        # Voiced Hiragana - "ga", "za", "da", "ba" columns
        ('が', 'ga'), ('ぎ', 'gi'), ('ぐ', 'gu'), ('げ', 'ge'), ('ご', 'go'),  # ga, gi, gu, ge, go
        ('ざ', 'za'), ('じ', 'ji'), ('ず', 'zu'), ('ぜ', 'ze'), ('ぞ', 'zo'),  # za, ji, zu, ze, zo
        ('だ', 'da'), ('ぢ', 'ji'), ('づ', 'zu'), ('で', 'de'), ('ど', 'do'),  # da, ji, zu, de, do
        ('ば', 'ba'), ('び', 'bi'), ('ぶ', 'bu'), ('べ', 'be'), ('ぼ', 'bo'),  # ba, bi, bu, be, bo
        
        # "Pa" column with handakuten
        ('ぱ', 'pa'), ('ぴ', 'pi'), ('ぷ', 'pu'), ('ぺ', 'pe'), ('ぽ', 'po'),  # pa, pi, pu, pe, po
    
        # Contracted Sounds (ya-yōon)
        ('きゃ', 'kya'), ('きゅ', 'kyu'), ('きょ', 'kyo'),  # kya, kyu, kyo
        ('しゃ', 'sha'), ('しゅ', 'shu'), ('しょ', 'sho'),  # sha, shu, sho
        ('ちゃ', 'cha'), ('ちゅ', 'chu'), ('ちょ', 'cho'),  # cha, chu, cho
        ('にゃ', 'nya'), ('にゅ', 'nyu'), ('にょ', 'nyo'),  # nya, nyu, nyo
        ('ひゃ', 'hya'), ('ひゅ', 'hyu'), ('ひょ', 'hyo'),  # hya, hyu, hyo
        ('みゃ', 'mya'), ('みゅ', 'myu'), ('みょ', 'myo'),  # mya, myu, myo
        ('りゃ', 'rya'), ('りゅ', 'ryu'), ('りょ', 'ryo'),  # rya, ryu, ryo
    
        # Voiced Contracted Sounds (ya-yōon)
        ('ぎゃ', 'gya'), ('ぎゅ', 'gyu'), ('ぎょ', 'gyo'),  # gya, gyu, gyo
        ('じゃ', 'ja'), ('じゅ', 'ju'), ('じょ', 'jo'),  # ja, ju, jo
        ('びゃ', 'bya'), ('びゅ', 'byu'), ('びょ', 'byo'),  # bya, byu, byo
        ('ぴゃ', 'pya'), ('ぴゅ', 'pyu'), ('ぴょ', 'pyo')   # pya, pyu, pyo
    ]
    return run_quiz(session_id, 'Hiragana', hiragana_list)


def katakana_quiz(session_id):
    """Presents a quiz on Katakana characters."""
    katakana_list = [
        # Basic Katakana
        ('ア', 'a'), ('イ', 'i'), ('ウ', 'u'), ('エ', 'e'), ('オ', 'o'),  # a, i, u, e, o
        ('カ', 'ka'), ('キ', 'ki'), ('ク', 'ku'), ('ケ', 'ke'), ('コ', 'ko'),  # ka, ki, ku, ke, ko
        ('サ', 'sa'), ('シ', 'shi'), ('ス', 'su'), ('セ', 'se'), ('ソ', 'so'),  # sa, shi, su, se, so
        ('タ', 'ta'), ('チ', 'chi'), ('ツ', 'tsu'), ('テ', 'te'), ('ト', 'to'),  # ta, chi, tsu, te, to
        ('ナ', 'na'), ('ニ', 'ni'), ('ヌ', 'nu'), ('ネ', 'ne'), ('ノ', 'no'),  # na, ni, nu, ne, no
        ('ハ', 'ha'), ('ヒ', 'hi'), ('フ', 'fu'), ('ヘ', 'he'), ('ホ', 'ho'),  # ha, hi, fu, he, ho
        ('マ', 'ma'), ('ミ', 'mi'), ('ム', 'mu'), ('メ', 'me'), ('モ', 'mo'),  # ma, mi, mu, me, mo
        ('ヤ', 'ya'), ('ユ', 'yu'), ('ヨ', 'yo'),  # ya, yu, yo
        ('ラ', 'ra'), ('リ', 'ri'), ('ル', 'ru'), ('レ', 're'), ('ロ', 'ro'),  # ra, ri, ru, re, ro
        ('ワ', 'wa'), ('ヲ', 'wo'), ('ン', 'n'),  # wa, wo, n
        
        # Voiced Katakana - "ga", "za", "da", "ba" columns
        ('ガ', 'ga'), ('ギ', 'gi'), ('グ', 'gu'), ('ゲ', 'ge'), ('ゴ', 'go'),  # ga, gi, gu, ge, go
        ('ザ', 'za'), ('ジ', 'ji'), ('ズ', 'zu'), ('ゼ', 'ze'), ('ゾ', 'zo'),  # za, ji, zu, ze, zo
        ('ダ', 'da'), ('ヂ', 'ji'), ('ヅ', 'zu'), ('デ', 'de'), ('ド', 'do'),  # da, ji, zu, de, do
        ('バ', 'ba'), ('ビ', 'bi'), ('ブ', 'bu'), ('ベ', 'be'), ('ボ', 'bo'),  # ba, bi, bu, be, bo
        
        # "Pa" column with handakuten
        ('パ', 'pa'), ('ピ', 'pi'), ('プ', 'pu'), ('ペ', 'pe'), ('ポ', 'po'),  # pa, pi, pu, pe, po
    
        # Contracted Sounds (ya-yōon)
        ('キャ', 'kya'), ('キュ', 'kyu'), ('キョ', 'kyo'),  # kya, kyu, kyo
        ('シャ', 'sha'), ('シュ', 'shu'), ('ショ', 'sho'),  # sha, shu, sho
        ('チャ', 'cha'), ('チュ', 'chu'), ('チョ', 'cho'),  # cha, chu, cho
        ('ニャ', 'nya'), ('ニュ', 'nyu'), ('ニョ', 'nyo'),  # nya, nyu, nyo
        ('ヒャ', 'hya'), ('ヒュ', 'hyu'), ('ヒョ', 'hyo'),  # hya, hyu, hyo
        ('ミャ', 'mya'), ('ミュ', 'myu'), ('ミョ', 'myo'),  # mya, myu, myo
        ('リャ', 'rya'), ('リュ', 'ryu'), ('リョ', 'ryo'),  # rya, ryu, ryo
    
        # Voiced Contracted Sounds (ya-yōon)
        ('ギャ', 'gya'), ('ギュ', 'gyu'), ('ギョ', 'gyo'),  # gya, gyu, gyo
        ('ジャ', 'ja'), ('ジュ', 'ju'), ('ジョ', 'jo'),  # ja, ju, jo
        ('ビャ', 'bya'), ('ビュ', 'byu'), ('ビョ', 'byo'),  # bya, byu, byo
        ('ピャ', 'pya'), ('ピュ', 'pyu'), ('ピョ', 'pyo')   # pya, pyu, pyo
    ]
    return run_quiz(session_id, 'Katakana', katakana_list)


def fetch_lesson_data(lesson_title, student_level):
    """Returns the lesson data for the given lesson title and student level."""
    if lesson_title == 'Japanese Colors':
        lesson_data = globals().get(f'j_colors{student_level}')
    elif lesson_title == 'Japanese Body Parts':
        lesson_data = globals().get(f'j_body_parts{student_level}')
    elif lesson_title == 'Japanese Adjectives':
        lesson_data = globals().get(f'j_adjectives{student_level}')
    elif lesson_title == 'Japanese Animals':
        lesson_data = globals().get(f'j_animals{student_level}')
    elif lesson_title == 'Japanese Family':
        lesson_data = globals().get(f'j_family{student_level}')
    elif lesson_title == 'Japanese Fruits':
        lesson_data = globals().get(f'j_fruits{student_level}')
    elif lesson_title == 'Japanese Greetings':
        lesson_data = globals().get(f'j_greetings{student_level}')
    elif lesson_title == 'One Piece Vocab':
        lesson_data = globals().get(f'j_one_piece{student_level}')
    elif lesson_title == 'Japanese Self Introduction':
        lesson_data = globals().get(f'j_self_introduction{student_level}')
    elif lesson_title == 'Japanese Nouns':
        lesson_data = globals().get(f'j_nouns{student_level}')
    elif lesson_title == 'Japanese Time':
        lesson_data = globals().get(f'j_time{student_level}')
    elif lesson_title == 'Japanese Vegtables':
        lesson_data = globals().get(f'j_vegtables{student_level}')
    elif lesson_title == 'Japanese Verbs':
        lesson_data = globals().get(f'j_verbs{student_level}')
    elif lesson_title == 'Japanese Song Sanpo':
        lesson_data = globals().get(f'j_song_sanpo{student_level}')
    elif lesson_title == 'Japanese Song Zou-san':
        lesson_data = globals().get(f'j_song_zou_san{student_level}')
    else:
        return None
    return lesson_data


def vocab_teach(session_id, lesson_title):
    """Displays vocabulary (furigana, kanji, and translation) and reads them aloud using Japanese TTS."""
    global screen_color, text_color, shadow_color, WIDTH, HEIGHT, current_font_name_or_path  # Access theme-related globals

    # Set the wait time in milliseconds
    wait_time = 5000

    # Get the student's current level for the lesson title
    student_level = get_student_progress(session_id, lesson_title)
    lesson_data = fetch_lesson_data(lesson_title, student_level)

    if lesson_data is None:
        log_message(f"Error: No lesson data found for {lesson_title} at level {student_level}")
        return

    # Font initialization for furigana and translation
    furigana_font = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", 50)
    
    translation_font_size = 50
    if os.path.isfile(current_font_name_or_path):
        translation_font = pygame.font.Font(current_font_name_or_path, translation_font_size)
    else:
        translation_font = pygame.font.SysFont(current_font_name_or_path, translation_font_size)

    # Intro message
    screen.fill(screen_color)
    intro_message = f"Let's learn {lesson_data['quiz_title']}!"
    draw_text(intro_message, translation_font, text_color, x=0, y=HEIGHT * 0.2, center=True, 
              enable_shadow=True, max_width=WIDTH)
    draw_and_wait_continue_button()

    # Loop through each vocabulary item
    for item in lesson_data['questions']:
        screen.fill(screen_color)

        # Adjust the kanji font size dynamically based on kanji length
        kanji_length = len(item['kanji'])
        kanji_font_size = 215 if kanji_length <= 3 else 75
        kanji_font = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", kanji_font_size)

        # Display furigana, kanji, and translation
        draw_text(item['furigana'], furigana_font, text_color, x=0, y=HEIGHT * 0.1, center=True, max_width=WIDTH,
                  enable_shadow=True)
        draw_text(item['kanji'], kanji_font, text_color, x=0, y=HEIGHT * 0.3, center=True, enable_shadow=True)
        draw_text(item['translation'], translation_font, text_color, x=0, y=HEIGHT * 0.75, center=True, 
                  enable_shadow=True, max_width=WIDTH)

        # Update the display after drawing text
        pygame.display.flip()
        
        # Speak the word aloud
        speak_japanese(item['furigana'])
        # time.sleep(1)
        # Replace each instance of time.sleep(1) with:
        pygame.time.delay(wait_time)

        # Handle focus and event processing for each word display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.ACTIVEEVENT and event.gain == 1:
                # If focus is regained, redraw the current word and image
                screen.fill(screen_color)
                draw_text(item['furigana'], furigana_font, text_color, x=0, y=HEIGHT * 0.1, center=True, 
                          max_width=WIDTH, enable_shadow=True)
                draw_text(item['kanji'], kanji_font, text_color, x=0, y=HEIGHT * 0.3, center=True, 
                          enable_shadow=True)
                draw_text(item['translation'], translation_font, text_color, x=0, y=HEIGHT * 0.75, center=True, 
                          enable_shadow=True, max_width=WIDTH)
                pygame.display.flip()

        # Try to show the image, assume JPG first and fallback to PNG
        image_loaded = False
        try:
            # Try loading the image as a JPG first
            jpg_image_path = item['image'].replace(".png", ".jpg") if item['image'].endswith(".png") else item['image'] + ".jpg"
            image = pygame.image.load(jpg_image_path)
            image_loaded = True
        except FileNotFoundError:
            try:
                # If JPG not found, fallback to PNG
                image = pygame.image.load(item['image'])
                image_loaded = True
            except FileNotFoundError:
                log_message(f"Image not found: {jpg_image_path} or {item['image']}. Displaying text only.")

        if image_loaded:
            # Resize and display the image if it was loaded successfully
            image = pygame.transform.scale(image, (WIDTH, HEIGHT))
            screen.blit(image, (0, 0))
            pygame.display.flip()
            speak_japanese(item['furigana'])
            # time.sleep(1)
            # Replace each instance of time.sleep(1) with:
            pygame.time.delay(wait_time)
        else:
            # If no image is found, just display the text
            pygame.display.flip()

    # Completion message and buttons
    screen.fill(screen_color)
    completion_message = f"Great job! You just learned {lesson_data['quiz_title']}!"
    draw_text(completion_message, translation_font, text_color, x=0, y=HEIGHT * 0.4, center=True, 
              enable_shadow=True, max_width=WIDTH)
    
    # Check if there's a URL in the lesson data and open it in the browser
    if 'URL' in lesson_data and lesson_data['URL']:
        log_message(f"Opening URL: {lesson_data['URL']}")
        webbrowser.open(lesson_data['URL'])

    # Draw "Repeat?" and "Continue..." buttons
    continue_font_size = int(get_dynamic_font_size() * 0.8)  
    if os.path.isfile(current_font_name_or_path):
        continue_font = pygame.font.Font(current_font_name_or_path, continue_font_size)
    else:
        continue_font = pygame.font.SysFont(current_font_name_or_path, continue_font_size)

    repeat_button_rect = draw_text("Repeat?", continue_font, text_color, x=WIDTH * 0.05, y=HEIGHT * 0.9, 
                                   enable_shadow=True, return_rect=True)
    continue_button_rect = draw_text("Continue...", continue_font, text_color, x=WIDTH * 0.55, y=HEIGHT * 0.9, 
                                     enable_shadow=True, return_rect=True)

    pygame.display.flip()

    # Wait for input and handle events
    button_clicked = False
    while not button_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.ACTIVEEVENT and event.gain == 1:
                # Redraw completion message and buttons when focus is regained
                screen.fill(screen_color)
                draw_text(completion_message, translation_font, text_color, x=0, y=HEIGHT * 0.4, center=True, 
                          enable_shadow=True, max_width=WIDTH)
                draw_text("Repeat?", continue_font, text_color, x=WIDTH * 0.05, y=HEIGHT * 0.9, enable_shadow=True)
                draw_text("Continue...", continue_font, text_color, x=WIDTH * 0.55, y=HEIGHT * 0.9, enable_shadow=True)
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if repeat_button_rect.collidepoint(mouse_pos):
                    vocab_teach(session_id, lesson_title)
                    button_clicked = True
                elif continue_button_rect.collidepoint(mouse_pos):
                    button_clicked = True


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
                      # shadow_color=shadow_color,
                      max_width=WIDTH)
            pygame.display.flip()

    # Final display and pause before exiting the function
    pygame.display.flip()
    time.sleep(1)  # Pause for 1 second

    # Clear the event queue again after displaying the result
    pygame.event.clear()


def japanese_quiz(session_id, lesson_title, lesson_data):
    """Presents a quiz on the given dataset and returns the result."""
    global screen_color, text_color  # Access theme-related globals
    


    # Display intro screen for the quiz
    screen.fill(screen_color)
    intro_message = f"It's time for a {lesson_data['quiz_title']} Quiz!"
    draw_text(
        intro_message,
        font,
        text_color,
        x=0,
        y=HEIGHT * 0.4,
        center=True,
        enable_shadow=True,
        max_width=WIDTH
    )
    
    draw_and_wait_continue_button()

    # Start the lesson timer here
    lesson_start_time = time.time()

    # Shuffle the questions
    questions = lesson_data['questions']
    random.shuffle(questions)

    total_questions = len(questions)  # Set number of questions to match the data dynamically
    correct_answers = 0
    completion_times = []

    # Quiz loop
    for problem_count in range(total_questions):
        # Pick a question
        question = questions[problem_count]
        correct_answer = question['translation']

        # Generate 3 incorrect answers
        incorrect_answers = random.sample(
            [q['translation'] for q in questions if q['translation'] != correct_answer], min(3, len(questions) - 1))

        # Create the multiple-choice options
        options = [correct_answer] + incorrect_answers
        random.shuffle(options)

        # Display the quiz options and get option rects
        kanji_rect, furigana_rect, option_rects = display_quiz(screen, question['kanji'], question['furigana'], options)

        pygame.display.flip()

        # Speak the furigana aloud
        speak_japanese(question['furigana'])

        start_time = time.time()
        question_complete = False
        answer_clicked = False  # New flag to prevent multiple clicks on the same answer

        while not question_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not answer_clicked:  # Only check clicks if answer not already clicked
                    mouse_pos = event.pos

                    # Check if the kanji or furigana was clicked and repeat the audio if so
                    if kanji_rect.collidepoint(mouse_pos):
                        speak_japanese(question['furigana'])
                    elif furigana_rect.collidepoint(mouse_pos):
                        speak_japanese(question['furigana'])

                    # Check if an answer option was clicked
                    for rect, option in option_rects:
                        if rect.collidepoint(mouse_pos):
                            answer_clicked = True  # Prevent further clicks for this question
                            time_taken = round(time.time() - start_time, 1)
                            completion_times.append(time_taken)

                            if option == correct_answer:
                                correct_answers += 1
                                
                                # Assume JPG and fall back to PNG
                                image_loaded = False
                                image_file = question['image']
                                try:
                                    # Try loading the image as JPG
                                    jpg_image_path = image_file.replace(".png", ".jpg") if image_file.endswith(".png") else image_file + ".jpg"
                                    image = pygame.image.load(jpg_image_path)
                                    image_file = jpg_image_path  # Update to use the JPG file path
                                    image_loaded = True
                                except FileNotFoundError:
                                    try:
                                        # Fallback to PNG if JPG is not found
                                        image = pygame.image.load(image_file)
                                        image_loaded = True
                                    except FileNotFoundError:
                                        log_message(f"Image not found: {jpg_image_path} or {image_file}. Displaying text only.")

                                if image_loaded:
                                    display_result_with_image("Correct!", image_file, use_lightning=(time_taken < 3))
                                else:
                                    display_result_with_image("Correct!")
                            else:
                                display_result_with_image(f"Sorry, the correct answer is {correct_answer}")
                            question_complete = True  # Move to the next question

            pygame.time.Clock().tick(60)

    # Final score and performance
    avg_time = round(sum(completion_times) / len(completion_times), 1) if completion_times else 0

    # Fetch lesson ID
    lesson_id = fetch_lesson_id(lesson_title)

    # End the lesson timer
    lesson_end_time = time.time()

    # Add session lesson to the database (track progress)
    add_session_lesson(session_id, lesson_id, lesson_start_time, lesson_end_time, total_questions, correct_answers)

    # Display the final score and handle perfect scores
    screen.fill(screen_color)
    draw_text(f"Final Score: {correct_answers}/{total_questions}", font, text_color, WIDTH // 2, HEIGHT * 0.25, center=True, enable_shadow=True)
    
    if correct_answers == total_questions:
        draw_text("Perfect score!", font, text_color, WIDTH // 2, HEIGHT * 0.35, center=True, enable_shadow=True)
        if avg_time < 3.0:
            draw_text("MASTERY!", font, text_color, WIDTH // 2, HEIGHT * 0.80, center=True, enable_shadow=True)

    draw_and_wait_continue_button()
    
    if correct_answers == total_questions:
        bonus_game_selector()

    # Return total questions, correct answers, and average time as a tuple
    return total_questions, correct_answers, avg_time


def display_quiz(screen, kanji, furigana, options):
    """
    Draws the kanji, furigana, and multiple-choice options on the screen.
    Returns the rects for kanji, furigana, and the option rects for handling clicks.
    """
    global screen_color, text_color, shadow_color, WIDTH, HEIGHT, current_font_name_or_path  # Access theme-related globals
    screen.fill(screen_color)

    # Draw the Kanji on the screen
    kanji_rect = draw_text(
        kanji,
        j_font,  # Assuming you have a separate kanji font loaded
        text_color,
        x=WIDTH // 2,
        y=HEIGHT // 3,
        center=True,
        enable_shadow=True,
        # shadow_color=BLACK,
        return_rect=True
    )

    # Draw the Furigana above the Kanji
    furigana_rect = draw_text(
        furigana,
        j_font,
        text_color,
        x=WIDTH // 2,
        y=HEIGHT // 5,
        center=True,
        enable_shadow=True,
        # shadow_color=BLACK,
        return_rect=True
    )

    # Draw the multiple-choice options
    option_rects = []
    y_pos = HEIGHT * 0.45
    answer_buffer = HEIGHT * 0.11

    for i, option in enumerate(options):
        option_rect = draw_text(
            option,
            font,  # Use your default or specific font here
            text_color,
            x=WIDTH // 2,
            y=y_pos + i * answer_buffer,
            center=True,
            enable_shadow=True,
            # shadow_color=BLACK,
            return_rect=True
        )

        # Reduce rect size to 95%
        option_rect = option_rect.inflate(-option_rect.width * 0.01, -option_rect.height * 0.25)

        option_rects.append((option_rect, option))

    pygame.display.flip()

    return kanji_rect, furigana_rect, option_rects


### MENUS ###



# Move these to Bonus game section
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
                        self.rect.bottom = platform.rect.top + 14
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


class Bomb:
    def __init__(self, image, x, y, speed):
        """
        Initialize the Bomb object.

        Parameters:
            image (Surface): The image representing the bomb.
            x (int): The initial x-coordinate of the bomb.
            y (int): The initial y-coordinate of the bomb.
            speed (int): The speed at which the bomb falls.
        """
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = 0
        self.particles = []

    def update(self):
        """
        Update the bomb's position, rotation, and particles.

        The bomb falls from the top of the screen, rotating as it descends. It also emits particles.
        """
        self.rect.y += self.speed
        self.angle = (self.angle + 15) % 360
        self.particles = [
            particle for particle in self.particles if particle.lifetime > 0
        ]
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        """
        Draw the bomb and its particles on the screen.

        Parameters:
            screen (Surface): The Pygame surface to draw the bomb and particles on.
        """
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
        if random.randint(0, 1) == 0:
            self.particles.append(Particle(self.rect.centerx, self.rect.top, (255, 0, 0)))
        for particle in self.particles:
            particle.draw(screen)
            

class Fish:
    """
    A class to represent a fish object in the game.

    Attributes:
        image (pygame.Surface): The image representing the fish.
        rect (pygame.Rect): The rectangle area of the fish, used for positioning and collisions.
        speed (int): The vertical speed of the fish, controlling how fast it falls.
        particles (list): A list of particles for visual effects as the fish falls.
    """

    def __init__(self, image, x, y, speed):
        """
        Initialize the fish object with an image, position, and speed.

        Args:
            image (pygame.Surface): The image to represent the fish.
            x (int): The initial x-coordinate of the fish.
            y (int): The initial y-coordinate of the fish.
            speed (int): The speed at which the fish will fall.
        """
        self.image = image  # Store the image of the fish.
        self.rect = self.image.get_rect()  # Get the rectangle of the image.
        self.rect.x = x  # Set the initial x-coordinate.
        self.rect.y = y  # Set the initial y-coordinate.
        self.speed = speed  # Set the falling speed.
        self.particles = []  # Initialize an empty list for particles.

    def update(self):
        """
        Update the fish's position and manage its particles.

        The fish falls by increasing its y-coordinate by its speed. Particles are updated and removed
        if their lifetime is over.
        """
        self.rect.y += self.speed  # Move the fish down by its speed.
        # Remove particles whose lifetime has expired and update remaining particles.
        self.particles = [particle for particle in self.particles if particle.lifetime > 0]
        for particle in self.particles:
            particle.update()  # Update each particle's position and state.

    def draw(self, screen):
        """
        Draw the fish and its associated particles on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the fish and particles on.
        """
        screen.blit(self.image, self.rect.topleft)  # Draw the fish at its current position.
        # Occasionally generate a new particle behind the fish.
        if random.randint(0, 10) < 8:
            self.particles.append(Particle(self.rect.centerx, self.rect.bottom, (50, 50, 255)))
        # Draw all particles on the screen.
        for particle in self.particles:
            particle.draw(screen)

            
#################
# Main function #
#################
def main():
    log_message(create_log_message("Loading options."))
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
        elif current_state == "learniverse_explanation":
            current_state = learniverse_explanation()
        elif current_state == "student_select_menu":
            current_state = student_select_menu()
        elif current_state == "session_manager":
            current_state = session_manager()

if __name__ == "__main__":
    main()
