"""
facebook_publisher.py
Uploads a local image directly to a Facebook Page.
"""

import os
import requests

from config import FACEBOOK_PAGE_ID
from config import FACEBOOK_ACCESS_TOKEN


class FacebookPublisher:

    def __init__(self):

        if not FACEBOOK_PAGE_ID:
            raise Exception("FACEBOOK_PAGE_ID is missing in .env")

        if not FACEBOOK_ACCESS_TOKEN:
            raise Exception("FACEBOOK_PAGE_TOKEN is missing in .env")

        self.page_id = FACEBOOK_PAGE_ID
        self.page_token = FACEBOOK_ACCESS_TOKEN

        self.url = (
            f"https://graph.facebook.com/v25.0/"
            f"{self.page_id}/photos"
        )

    def publish(self, image_path: str, caption: str):

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        print("=" * 60)
        print("Publishing to Facebook...")
        print(f"Page ID: {self.page_id}")
        print(f"Image: {image_path}")
        print("=" * 60)

        with open(image_path, "rb") as image_file:

            files = {
                "source": (
                    os.path.basename(image_path),
                    image_file,
                    "image/jpeg"
                )
            }

            data = {
                "caption": caption,
                "access_token": self.page_token
            }

            try:

                response = requests.post(
                    self.url,
                    files=files,
                    data=data,
                    timeout=120
            )

                print("Status Code:", response.status_code)
                print("Response:", response.text)

                response.raise_for_status()

                return response.json()

            except requests.exceptions.RequestException as e:

                print("\nFacebook request failed!")
                print(type(e).__name__)
                print(str(e))

                raise Exception(f"Facebook request failed: {e}")