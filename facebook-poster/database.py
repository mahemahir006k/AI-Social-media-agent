import json
import sqlite3
from datetime import datetime, timezone

from config import DATABASE_FILE


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS drafts (
                id TEXT PRIMARY KEY,
                token_hash TEXT NOT NULL,
                prompt TEXT NOT NULL,
                title TEXT NOT NULL,
                subtitle TEXT NOT NULL,
                caption TEXT NOT NULL,
                image_path TEXT NOT NULL,
                image_url TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                facebook_response TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                published_at TEXT
            )
        """)


def create_draft(draft):
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO drafts (
                id, token_hash, prompt, title, subtitle,
                caption, image_path, image_url, status,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)
        """, (
            draft["id"],
            draft["token_hash"],
            draft["prompt"],
            draft["title"],
            draft["subtitle"],
            draft["caption"],
            draft["image_path"],
            draft["image_url"],
            now,
            now
        ))


def get_draft(draft_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM drafts WHERE id = ?",
            (draft_id,)
        ).fetchone()

    return dict(row) if row else None


def update_draft(draft_id, values):
    allowed = {
        "prompt",
        "title",
        "subtitle",
        "caption",
        "image_path",
        "image_url",
        "status",
        "facebook_response",
        "published_at"
    }

    values = {
        key: value
        for key, value in values.items()
        if key in allowed
    }

    values["updated_at"] = datetime.now(timezone.utc).isoformat()

    assignments = ", ".join(f"{key} = ?" for key in values)
    parameters = list(values.values()) + [draft_id]

    with get_connection() as connection:
        connection.execute(
            f"UPDATE drafts SET {assignments} WHERE id = ?",
            parameters
        )