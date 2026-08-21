import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
FONT_DIR = BASE_DIR / "fonts"
DATABASE_FILE = BASE_DIR / "drafts.db"

OUTPUT_DIR.mkdir(exist_ok=True)
FONT_DIR.mkdir(exist_ok=True)

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh").rstrip("/")
NTFY_TOPIC = os.getenv("NTFY_TOPIC")
NTFY_TOKEN = os.getenv("NTFY_TOKEN")

PUBLIC_APP_URL = os.getenv(
    "PUBLIC_APP_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

REVIEW_SECRET = os.getenv("REVIEW_SECRET")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt"
REQUEST_TIMEOUT = 120

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1080
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_QUALITY = 95

GENERATED_IMAGE_NAME = "generated.png"

TITLE_FONT = str(FONT_DIR / "Poppins-Bold.ttf")
SUBTITLE_FONT = str(FONT_DIR / "Poppins-Regular.ttf")

TITLE_FONT_SIZE = 72
SUBTITLE_FONT_SIZE = 42
TITLE_WRAP = 22
SUBTITLE_WRAP = 34
TITLE_Y = 500
SUBTITLE_Y = 760

TITLE_COLOR = "white"
SUBTITLE_COLOR = "white"
OVERLAY_RGBA = (0, 0, 0, 110)