"""
app.py

XEN HRA Facebook Poster API

Workflow:
1. Flowise calls POST /preview-post.
2. Backend generates a unique preview image.
3. Draft is saved in SQLite.
4. ntfy notification is sent with a secure review URL.
5. User opens the review page.
6. User can edit and regenerate the preview.
7. User can approve and publish to Facebook.
"""

import hashlib
import hmac
import json
import os
import random
import secrets
import threading
import traceback
import uuid

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from fastapi import (
    FastAPI,
    HTTPException,
    Request
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import (
    HOST,
    OUTPUT_DIR,
    PORT,
    PUBLIC_APP_URL
)
from database import (
    create_draft,
    get_draft,
    initialize_database,
    update_draft
)
from facebook_publisher import FacebookPublisher
from image_editor import ImageEditor
from image_generator import PollinationsGenerator
from ntfy_service import (
    send_failure_notification,
    send_published_notification,
    send_review_notification
)

from topic_manager import TopicManager
from topic_knowledge import get_topic_knowledge
from knowledge import router as knowledge_router


# ============================================================
# APPLICATION DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TEMPLATES_DIR = os.path.join(
    BASE_DIR,
    "templates"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)


# ============================================================
# STARTUP
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when FastAPI starts.
    Creates the SQLite drafts table if it does not exist.
    """

    initialize_database()

    print("=" * 60)
    print("XEN HRA Facebook Poster API started")
    print(f"Local server: http://127.0.0.1:{PORT}")
    print(f"Public URL: {PUBLIC_APP_URL}")
    print("=" * 60)

    yield

    print("XEN HRA Facebook Poster API stopped")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="XEN HRA Facebook Poster API",
    description=(
        "Generate Facebook post previews, send ntfy review "
        "notifications and publish approved posts."
    ),
    version="3.0.0",
    lifespan=lifespan
)
app.include_router(knowledge_router)


# ============================================================
# STATIC FILES AND TEMPLATES
# ============================================================

app.mount(
    "/output",
    StaticFiles(directory=OUTPUT_DIR),
    name="output"
)

templates = Jinja2Templates(
    directory=TEMPLATES_DIR
)


# ============================================================
# GENERATION LOCK
# ============================================================

# image_generator.py currently writes the initially generated image
# to the shared file output/generated.png.
#
# This lock prevents two simultaneous preview requests from
# overwriting generated.png while an image is being processed.
generation_lock = threading.Lock()

# Prevent two publish requests in this FastAPI process from
# publishing the same draft simultaneously.
publish_lock = threading.Lock()

# ============================================================
# TOPIC MANAGER
# ============================================================

# Manages topic rotation using topics.json.
topic_manager = TopicManager()


# ============================================================
# REQUEST MODELS
# ============================================================

class ImageRequest(BaseModel):
    """
    Request received from the Flowise preview_post tool.
    """

    prompt: str = Field(
        min_length=3,
        max_length=4000
    )

    title: str = Field(
        min_length=1,
        max_length=250
    )

    subtitle: str = Field(
        min_length=1,
        max_length=500
    )

    caption: str = Field(
        min_length=1,
        max_length=10000
    )


class RegenerateRequest(BaseModel):
    """
    Request received from the review page when the user edits
    the post and selects Regenerate Preview.
    """

    token: str = Field(
        min_length=20,
        max_length=500
    )

    prompt: str = Field(
        min_length=3,
        max_length=4000
    )

    title: str = Field(
        min_length=1,
        max_length=250
    )

    subtitle: str = Field(
        min_length=1,
        max_length=500
    )

    caption: str = Field(
        min_length=1,
        max_length=10000
    )


class ReviewPublishRequest(BaseModel):
    """
    Request received when the user approves the draft.
    The caption can be edited without regenerating the image.
    """

    token: str = Field(
        min_length=20,
        max_length=500
    )

    caption: str = Field(
        min_length=1,
        max_length=10000
    )


class LegacyPublishRequest(BaseModel):
    """
    Kept only so old callers receive a clear response.
    The old unrestricted publishing endpoint is disabled.
    """

    caption: Optional[str] = None


# ============================================================
# IMAGE STYLES
# ============================================================

STYLES = [
    "photorealistic, 8k, cinematic lighting",
    "3D blender render, vibrant colors, soft lighting",
    "vector art, flat design, minimalist",
    "modern corporate illustration, professional lighting",
    "digital painting, professional concept art",
    "isometric illustration, modern business office"
]


# ============================================================
# HIRING KEYWORDS
# ============================================================

HIRING_KEYWORDS = [
    "hiring",
    "hire",
    "hired",
    "job",
    "jobs",
    "career",
    "careers",
    "vacancy",
    "vacancies",
    "opening",
    "openings",
    "position",
    "positions",
    "apply",
    "apply now",
    "join us",
    "join our team",
    "join our company",
    "recruitment",
    "recruit",
    "staffing",
    "talent",
    "talent acquisition",
    "walk in",
    "walk-in",
    "interview"
]


# ============================================================
# TOKEN FUNCTIONS
# ============================================================

def create_review_token() -> str:
    """
    Creates the secret token included in the ntfy review URL.
    """

    return secrets.token_urlsafe(32)


def hash_review_token(token: str) -> str:
    """
    Converts a review token into a SHA-256 hash.

    Only the hash is stored in SQLite. The original token is
    included in the review URL.
    """

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def verify_review_token(
    draft: Optional[dict],
    token: Optional[str]
) -> bool:
    """
    Verifies that the supplied token belongs to the selected draft.
    """

    if not draft:
        return False

    if not token:
        return False

    stored_hash = draft.get("token_hash")

    if not stored_hash:
        return False

    supplied_hash = hash_review_token(token)

    return hmac.compare_digest(
        stored_hash,
        supplied_hash
    )


def require_valid_draft(
    draft_id: str,
    token: str
) -> dict:
    """
    Loads the draft and validates its review token.

    Raises:
        404 if the draft does not exist.
        403 if the token is incorrect.
    """

    draft = get_draft(draft_id)

    if not draft:
        raise HTTPException(
            status_code=404,
            detail="Draft not found"
        )

    if not verify_review_token(draft, token):
        raise HTTPException(
            status_code=403,
            detail="Invalid or expired review URL"
        )

    return draft


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value: str) -> str:
    """
    Removes unnecessary spaces around user/agent-generated values.
    """

    return value.strip()


def detect_hiring_post(
    title: str,
    subtitle: str,
    caption: str
) -> bool:
    """
    Determines whether the hiring badge should be displayed.
    """

    searchable_text = (
        f"{title} {subtitle} {caption}"
    ).lower()

    return any(
        keyword in searchable_text
        for keyword in HIRING_KEYWORDS
    )


def build_public_image_url(
    image_name: str
) -> str:
    """
    Creates a public image URL that ntfy and the mobile review page
    can access.

    The version query prevents the phone/browser from displaying
    a cached image.
    """

    cache_version = secrets.token_hex(6)

    return (
        f"{PUBLIC_APP_URL}"
        f"/output/{image_name}"
        f"?version={cache_version}"
    )


def generate_preview_image(
    draft_id: str,
    prompt: str,
    title: str,
    subtitle: str,
    caption: str
) -> dict:
    """
    Generates one unique preview image.

    This function does not publish anything to Facebook.
    """

    generator = PollinationsGenerator()
    editor = ImageEditor()

    random_style = random.choice(STYLES)

    enhanced_prompt = (
        f"{clean_text(prompt)}, "
        f"{random_style}"
    )

    print("=" * 60)
    print(f"Generating preview for draft: {draft_id}")
    print(f"Enhanced prompt: {enhanced_prompt}")
    print("=" * 60)

    # The current PollinationsGenerator writes to generated.png.
    # Protect that shared intermediate file with a lock.
    with generation_lock:
        generated_image_path = generator.generate(
            prompt=enhanced_prompt
        )

        is_hiring = detect_hiring_post(
            title=title,
            subtitle=subtitle,
            caption=caption
        )

        print(f"WE ARE HIRING badge: {is_hiring}")

        # Unique filename for every generation.
        generation_id = secrets.token_hex(6)

        preview_image_name = (
            f"{draft_id}-{generation_id}.jpg"
        )

        preview_image_path = os.path.join(
            OUTPUT_DIR,
            preview_image_name
        )

        editor.process_image(
            input_path=generated_image_path,
            output_path=preview_image_path,
            title=clean_text(title),
            subtitle=clean_text(subtitle),
            hiring=is_hiring
        )

    preview_image_url = build_public_image_url(
        preview_image_name
    )

    return {
        "image_name": preview_image_name,
        "image_path": preview_image_path,
        "image_url": preview_image_url
    }


# ============================================================
# TOPIC MANAGEMENT
# ============================================================

@app.get("/next-topic")
def next_topic():
    """
    Returns a new unused topic from TopicManager.
    """

    try:
        topic = topic_manager.get_next_topic()

        return {
            "status": "success",
            "topic": topic
        }

    except Exception as error:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to get next topic: {error}"
        )


@app.get("/topic-knowledge")
def topic_knowledge(topic: str):
    """
    Returns company knowledge relevant to the selected topic.
    """

    try:
        knowledge = get_topic_knowledge(topic)

        return {
            "status": "success",
            "topic": topic,
            "knowledge": knowledge
        }

    except Exception as error:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to get topic knowledge: {error}"
        )


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    """
    Basic application information.
    """

    return {
        "status": "running",
        "application": "XEN HRA Facebook Poster API",
        "version": "3.0.0",
        "workflow": (
            "Flowise preview -> ntfy review -> "
            "human approval -> Facebook publish"
        ),
        "documentation": "/docs"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    """
    Health-check endpoint.
    """

    return {
        "status": "healthy",
        "version": "3.0.0",
        "public_app_url": PUBLIC_APP_URL
    }


# ============================================================
# PREVIEW ENDPOINT
# ============================================================

@app.post("/preview-post")
def preview_post(data: ImageRequest):
    """
    Called by the Flowise preview_post tool.

    Creates a unique draft, generates an image, saves the draft
    in SQLite and sends an ntfy notification.

    This endpoint never publishes to Facebook.
    """

    print("=" * 60)
    print("New preview requested by Flowise")
    print("=" * 60)

    draft_id = str(uuid.uuid4())
    review_token = create_review_token()

    prompt = clean_text(data.prompt)
    title = clean_text(data.title)
    subtitle = clean_text(data.subtitle)
    caption = clean_text(data.caption)

    try:
        image_result = generate_preview_image(
            draft_id=draft_id,
            prompt=prompt,
            title=title,
            subtitle=subtitle,
            caption=caption
        )

        # Only the token hash is stored in the database.
        create_draft({
            "id": draft_id,
            "token_hash": hash_review_token(
                review_token
            ),
            "prompt": prompt,
            "title": title,
            "subtitle": subtitle,
            "caption": caption,
            "image_path":
                image_result["image_path"],
            "image_url":
                image_result["image_url"]
        })

        review_url = (
            f"{PUBLIC_APP_URL}"
            f"/review/{draft_id}"
            f"?token={review_token}"
        )

        send_review_notification(
            draft_id=draft_id,
            token=review_token,
            title=title,
            caption=caption,
            image_url=image_result["image_url"]
        )

    except Exception as error:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=(
                "Preview generation or ntfy notification "
                f"failed: {error}"
            )
        )

    return {
        "status": "success",
        "message": (
            "Preview generated and sent to ntfy. "
            "Nothing has been published to Facebook."
        ),
        "draft_id": draft_id,
        "preview_image_url":
            image_result["image_url"],
        "review_url": review_url,
        "final_caption": caption
    }


# ============================================================
# REVIEW PAGE
# ============================================================

@app.get(
    "/review/{draft_id}",
    response_class=HTMLResponse
)
def review_page(
    request: Request,
    draft_id: str,
    token: str
):
    """
    Opens when the user taps the ntfy notification.

    Displays the image, prompt, title, subtitle and caption.
    """

    draft = require_valid_draft(
        draft_id=draft_id,
        token=token
    )

    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "draft": draft,
            "token": token
        }
    )


# ============================================================
# GET DRAFT DETAILS
# ============================================================

@app.get("/api/drafts/{draft_id}")
def get_draft_details(
    draft_id: str,
    token: str
):
    """
    Returns draft information for a valid review URL.

    The stored token hash and local image path are not returned.
    """

    draft = require_valid_draft(
        draft_id=draft_id,
        token=token
    )

    return {
        "id": draft["id"],
        "prompt": draft["prompt"],
        "title": draft["title"],
        "subtitle": draft["subtitle"],
        "caption": draft["caption"],
        "image_url": draft["image_url"],
        "status": draft["status"],
        "created_at": draft["created_at"],
        "updated_at": draft["updated_at"],
        "published_at": draft.get(
            "published_at"
        )
    }


# ============================================================
# REGENERATE ENDPOINT
# ============================================================

@app.post(
    "/api/drafts/{draft_id}/regenerate"
)
def regenerate_draft(
    draft_id: str,
    data: RegenerateRequest
):
    """
    Updates the edited fields and generates a new image.

    This endpoint does not publish anything to Facebook.
    """

    draft = require_valid_draft(
        draft_id=draft_id,
        token=data.token
    )

    if draft["status"] == "published":
        raise HTTPException(
            status_code=409,
            detail=(
                "This post was already published and "
                "cannot be regenerated."
            )
        )

    if draft["status"] == "publishing":
        raise HTTPException(
            status_code=409,
            detail=(
                "This post is currently being published."
            )
        )

    prompt = clean_text(data.prompt)
    title = clean_text(data.title)
    subtitle = clean_text(data.subtitle)
    caption = clean_text(data.caption)

    try:
        image_result = generate_preview_image(
            draft_id=draft_id,
            prompt=prompt,
            title=title,
            subtitle=subtitle,
            caption=caption
        )

        update_draft(draft_id, {
            "prompt": prompt,
            "title": title,
            "subtitle": subtitle,
            "caption": caption,
            "image_path":
                image_result["image_path"],
            "image_url":
                image_result["image_url"],
            "status": "pending"
        })

    except Exception as error:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Regeneration failed: {error}"
        )

    return {
        "status": "success",
        "message": (
            "New preview generated. "
            "Nothing has been published."
        ),
        "draft_id": draft_id,
        "preview_image_url":
            image_result["image_url"],
        "final_caption": caption
    }


# ============================================================
# PUBLISH ENDPOINT
# ============================================================

@app.post(
    "/api/drafts/{draft_id}/publish"
)
def publish_draft(
    draft_id: str,
    data: ReviewPublishRequest
):
    """
    Publishes the reviewed draft to Facebook.

    The review token is mandatory.
    Duplicate publishing is blocked.
    """

    with publish_lock:
        draft = require_valid_draft(
            draft_id=draft_id,
            token=data.token
        )

        if draft["status"] == "published":
            raise HTTPException(
                status_code=409,
                detail=(
                    "This post was already published."
                )
            )

        if draft["status"] == "publishing":
            raise HTTPException(
                status_code=409,
                detail=(
                    "This post is currently being published."
                )
            )

        caption = clean_text(data.caption)

        if not caption:
            raise HTTPException(
                status_code=422,
                detail="Caption cannot be empty."
            )

        image_path = draft["image_path"]

        if not os.path.exists(image_path):
            raise HTTPException(
                status_code=400,
                detail=(
                    "The preview image is missing. "
                    "Regenerate the preview first."
                )
            )

        # Mark before calling Facebook to reduce duplicate requests.
        update_draft(draft_id, {
            "caption": caption,
            "status": "publishing"
        })

        try:
            publisher = FacebookPublisher()

            facebook_response = publisher.publish(
                image_path=image_path,
                caption=caption
            )

            published_at = datetime.now(
                timezone.utc
            ).isoformat()

            update_draft(draft_id, {
                "caption": caption,
                "status": "published",
                "facebook_response": json.dumps(
                    facebook_response
                ),
                "published_at": published_at
            })

            try:
                send_published_notification(
                    draft_id
                )
            except Exception as notification_error:
                # Facebook publishing was successful.
                # Do not report publishing as failed only because
                # the success notification failed.
                print(
                    "Unable to send ntfy success "
                    f"notification: {notification_error}"
                )

        except Exception as error:
            traceback.print_exc()

            # Allow the user to retry after a Facebook/API failure.
            update_draft(draft_id, {
                "status": "pending"
            })

            try:
                send_failure_notification(
                    str(error)
                )
            except Exception as notification_error:
                print(
                    "Unable to send ntfy failure "
                    f"notification: {notification_error}"
                )

            raise HTTPException(
                status_code=502,
                detail=(
                    "Facebook publishing failed: "
                    f"{error}"
                )
            )

    return {
        "status": "success",
        "message": (
            "Post published successfully to Facebook."
        ),
        "draft_id": draft_id,
        "facebook_response": facebook_response
    }


# ============================================================
# DISABLE OLD AUTOMATIC-PUBLISHING ENDPOINT
# ============================================================

@app.post("/generate-image")
def generate_image_disabled():
    """
    The old endpoint automatically generated and published posts.
    It is intentionally disabled because ntfy approval is required.
    """

    raise HTTPException(
        status_code=410,
        detail=(
            "Automatic publishing is disabled. "
            "Use POST /preview-post and approve the post "
            "through the ntfy review page."
        )
    )


# ============================================================
# DISABLE OLD UNRESTRICTED PUBLISH ENDPOINT
# ============================================================

@app.post("/publish-post")
def legacy_publish_disabled(
    data: LegacyPublishRequest
):
    """
    The old endpoint did not identify a draft and did not require
    the secure ntfy review token.
    """

    raise HTTPException(
        status_code=410,
        detail=(
            "This publishing endpoint is disabled. "
            "Use POST /api/drafts/{draft_id}/publish "
            "from the secure ntfy review page."
        )
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=True
    )
