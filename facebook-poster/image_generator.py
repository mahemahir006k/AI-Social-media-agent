import os
import random
import shutil
import time

import requests

from config import (
    POLLINATIONS_BASE_URL,
    OUTPUT_DIR,
    GENERATED_IMAGE_NAME,
    HEADERS,
)


class PollinationsGenerator:

    def generate(self, prompt: str):

        clean_prompt = requests.utils.quote(prompt)

        random_seed = random.randint(1000, 999999)

        url = (
            f"{POLLINATIONS_BASE_URL}/{clean_prompt}"
            f"?width=1024"
            f"&height=1024"
            f"&seed={random_seed}"
            f"&nologo=true"
        )

        output_path = os.path.join(
            OUTPUT_DIR,
            GENERATED_IMAGE_NAME
        )

        headers = HEADERS.copy()

        headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        print(f"🎨 Generating with Pollinations (Seed: {random_seed})")

        # ---------------------------------------------------
        # Try Pollinations 3 Times
        # ---------------------------------------------------

        for attempt in range(3):

            try:

                print(
                    f"🔄 Pollinations Attempt {attempt+1}/3..."
                )

                response = requests.get(
                    url,
                    headers=headers,
                    timeout=90
                )

                if (
                    response.status_code == 200
                    and len(response.content) > 1000
                ):

                    with open(output_path, "wb") as f:
                        f.write(response.content)

                    print("✅ Pollinations Success")

                    return output_path

                print(
                    f"Pollinations returned {response.status_code}"
                )

            except Exception as e:

                print(e)

            time.sleep(5)

        print("⚠️ Pollinations Failed")

        # ---------------------------------------------------
        # Fallback 1
        # ---------------------------------------------------

        try:

            print("🔄 Trying Picsum...")

            seed = random.randint(1, 999999)

            fallback_url = (
                f"https://picsum.photos/seed/{seed}/1024/1024"
            )

            response = requests.get(
                fallback_url,
                timeout=60,
                allow_redirects=True
            )

            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            print("✅ Picsum Success")

            return output_path

        except Exception as e:

            print(f"⚠️ Picsum Failed: {e}")

        # ---------------------------------------------------
        # Final Local Fallback
        # ---------------------------------------------------

        try:

            print("🖼 Using Local Default Image")

            default_image = os.path.join(
                "assets",
                "default.jpg"
            )

            shutil.copy(
                default_image,
                output_path
            )

            print("✅ Local Default Image Used")

            return output_path

        except Exception as e:

            print(e)

            raise Exception(
                "Image generation failed. Pollinations, Picsum and Local fallback all failed."
            )