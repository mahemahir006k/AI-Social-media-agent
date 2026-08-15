"""
config.py
Configuration for the AI Facebook Poster Project
"""
import os
from dotenv import load_dotenv

load_dotenv()

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN") # <--- ADDED THIS

# ... (Keep the rest of your config.py exactly the same) ...
# Just make sure the lines below exist in your file:

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FONT_DIR = os.path.join(BASE_DIR, "fonts")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)

API_TITLE = "AI Facebook Poster API"
API_VERSION = "1.0.0"
HOST = "127.0.0.1"
PORT = 8000

# We don't need Pollinations URL anymore, but keep variables to avoid errors
POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt"
REQUEST_TIMEOUT = 120
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1080
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_FORMAT = "JPEG"
IMAGE_QUALITY = 95

GENERATED_IMAGE_NAME = "generated.png"
FINAL_IMAGE_NAME = "final_post.jpg"

OVERLAY_COLOR = (0, 0, 0)
OVERLAY_ALPHA = 110
OVERLAY_RGBA = (OVERLAY_COLOR[0], OVERLAY_COLOR[1], OVERLAY_COLOR[2], OVERLAY_ALPHA)

TITLE_FONT = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
SUBTITLE_FONT = os.path.join(FONT_DIR, "Poppins-Regular.ttf")
FOOTER_FONT = os.path.join(FONT_DIR, "Poppins-Regular.ttf")

TITLE_FONT_SIZE = 72
SUBTITLE_FONT_SIZE = 42
FOOTER_FONT_SIZE = 30

TITLE_COLOR = "white"
SUBTITLE_COLOR = "white"
FOOTER_COLOR = "white"

TITLE_WRAP = 22
SUBTITLE_WRAP = 34

TITLE_Y = 500
SUBTITLE_Y = 760
FOOTER_Y = 1015

DEFAULT_FOOTER = "Follow for more AI tips"

TEXT_SHADOW_OFFSET = 3
TEXT_OUTLINE_WIDTH = 2

BLUR_RADIUS = 12
PANEL_RADIUS = 35
PANEL_ALPHA = 90

DEBUG = True