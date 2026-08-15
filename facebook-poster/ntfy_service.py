import requests

from config import (
    NTFY_SERVER,
    NTFY_TOPIC,
    NTFY_TOKEN,
    PUBLIC_APP_URL
)


def send_ntfy_message(payload):
    if not NTFY_TOPIC:
        raise RuntimeError("NTFY_TOPIC is missing")

    payload["topic"] = NTFY_TOPIC

    headers = {
        "Content-Type": "application/json"
    }

    if NTFY_TOKEN:
        headers["Authorization"] = f"Bearer {NTFY_TOKEN}"

    response = requests.post(
        NTFY_SERVER,
        json=payload,
        headers=headers,
        timeout=20
    )
    response.raise_for_status()

    return response.json()


def send_review_notification(
    draft_id,
    token,
    title,
    caption,
    image_url
):
    review_url = (
        f"{PUBLIC_APP_URL}/review/{draft_id}"
        f"?token={token}"
    )

    return send_ntfy_message({
        "title": f"Post ready: {title}",
        "message": caption[:500],
        "priority": 4,
        "tags": ["memo", "camera_flash"],
        "click": review_url,
        "attach": image_url,
        "actions": [
            {
                "action": "view",
                "label": "Review / Edit",
                "url": review_url,
                "clear": True
            },
            {
                "action": "view",
                "label": "Regenerate",
                "url": f"{review_url}&action=regenerate",
                "clear": True
            }
        ]
    })


def send_published_notification(draft_id):
    return send_ntfy_message({
        "title": "Facebook post published",
        "message": f"Draft {draft_id} was published successfully.",
        "priority": 3,
        "tags": ["white_check_mark"]
    })


def send_failure_notification(message):
    return send_ntfy_message({
        "title": "Facebook publishing failed",
        "message": message[:500],
        "priority": 5,
        "tags": ["warning"]
    })