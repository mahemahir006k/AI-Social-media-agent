"""
image_editor.py
Simple image editor for the Facebook Poster API.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

from config import (
    IMAGE_SIZE,
    IMAGE_QUALITY,
    TITLE_FONT,
    SUBTITLE_FONT,
    TITLE_FONT_SIZE,
    SUBTITLE_FONT_SIZE,
    TITLE_WRAP,
    SUBTITLE_WRAP,
    TITLE_Y,
    SUBTITLE_Y,
    TITLE_COLOR,
    SUBTITLE_COLOR,
    OVERLAY_RGBA
)


class ImageEditor:

    def __init__(self):
        self.width, self.height = IMAGE_SIZE

        self.title_font = self._load_font(
            TITLE_FONT,
            TITLE_FONT_SIZE
        )

        self.subtitle_font = self._load_font(
            SUBTITLE_FONT,
            SUBTITLE_FONT_SIZE
        )

    def _load_font(self, font_path, size):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            print(f"Unable to load {font_path}. Using default font.")
            return ImageFont.load_default()

    def open_image(self, image_path):
        image = Image.open(image_path)
        image = image.convert("RGBA")
        image = image.resize(IMAGE_SIZE)
        return image

    def add_overlay(self, image):
        overlay = Image.new("RGBA", image.size, OVERLAY_RGBA)
        return Image.alpha_composite(image, overlay)

    def wrap_title(self, text):
        return textwrap.fill(text, width=TITLE_WRAP)

    def wrap_subtitle(self, text):
        return textwrap.fill(text, width=SUBTITLE_WRAP)

    def draw_center_text(self, draw, text, font, y, color):

        bbox = draw.multiline_textbbox(
            (0, 0),
            text,
            font=font,
            align="center",
            spacing=8
        )

        text_width = bbox[2] - bbox[0]

        x = (self.width - text_width) // 2

        draw.multiline_text(
            (x, y),
            text,
            font=font,
            fill=color,
            align="center",
            spacing=8
        )

    def add_text(self, image, title, subtitle, hiring=False):

        draw = ImageDraw.Draw(image)

        title = self.wrap_title(title)
        subtitle = self.wrap_subtitle(subtitle)

        # -----------------------------
        # Title
        # -----------------------------
        self.draw_center_text(
            draw,
            title,
            self.title_font,
            TITLE_Y,
            TITLE_COLOR
        )

        # -----------------------------
        # Subtitle
        # -----------------------------
        self.draw_center_text(
            draw,
            subtitle,
            self.subtitle_font,
            SUBTITLE_Y,
            SUBTITLE_COLOR
        )

        # -----------------------------
        # WE ARE HIRING Badge
        # -----------------------------
        if hiring:

            badge_text = "WE ARE HIRING"

            try:
                badge_font = ImageFont.truetype(TITLE_FONT, 46)
            except:
                badge_font = ImageFont.load_default()

            padding_x = 35
            padding_y = 20

            bbox = draw.textbbox((0, 0), badge_text, font=badge_font)

            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            badge_w = text_w + padding_x * 2
            badge_h = text_h + padding_y * 2

            x = 40
            y = 40

            draw.rounded_rectangle(
                (x, y, x + badge_w, y + badge_h),
                radius=25,
                fill=(220, 0, 0)
)

            text_x = x + padding_x
            text_y = y + padding_y - bbox[1]

            draw.text(
                (text_x, text_y),
                badge_text,
                font=badge_font,
                fill="white"
)

        return image

    def save_image(self, image, output_path):

        image = image.convert("RGB")

        image.save(
            output_path,
            format="JPEG",
            quality=IMAGE_QUALITY
        )

        return output_path

    def process_image(
        self,
        input_path,
        output_path,
        title,
        subtitle,
        hiring=False
    ):

        image = self.open_image(input_path)

        image = self.add_overlay(image)

        image = self.add_text(
            image=image,
            title=title,
            subtitle=subtitle,
            hiring=hiring
        )

        self.save_image(
            image=image,
            output_path=output_path
        )

        print(f"Final image saved: {output_path}")

        return output_path