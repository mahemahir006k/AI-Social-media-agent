import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from dotenv import dotenv_values


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEDULE_FILE = os.path.join(BASE_DIR, "schedule.env")

FLOWISE_URL = (
    "http://127.0.0.1:3000/api/v1/prediction/"
    "93e8cf59-c1a5-460c-98c9-baf1aec50ea4"
)

QUESTION = "Create the next social media post."


def load_schedule():
    config = dotenv_values(SCHEDULE_FILE)

    post_time = config.get("POST_TIME", "10:00")
    timezone_name = config.get("TIMEZONE", "Asia/Kolkata")

    return post_time, timezone_name


def trigger_flowise():
    try:
        response = requests.post(
            FLOWISE_URL,
            json={"question": QUESTION},
            timeout=180,
        )

        response.raise_for_status()

        print(
            f"[{datetime.now()}] Flowise workflow triggered successfully.",
            flush=True,
        )

    except Exception as error:
        print(
            f"[{datetime.now()}] Failed to trigger Flowise: {error}",
            flush=True,
        )


def main():
    last_run_date = None

    print("Xexnaro Daily Scheduler started.", flush=True)

    while True:
        try:
            post_time, timezone_name = load_schedule()

            timezone = ZoneInfo(timezone_name)
            now = datetime.now(timezone)

            current_time = now.strftime("%H:%M")
            current_date = now.date()

            if current_time == post_time and last_run_date != current_date:
                print(
                    f"[{now}] Scheduled time reached: {post_time}",
                    flush=True,
                )

                trigger_flowise()
                last_run_date = current_date

            time.sleep(20)

        except Exception as error:
            print(f"Scheduler error: {error}", flush=True)
            time.sleep(20)


if __name__ == "__main__":
    main()
