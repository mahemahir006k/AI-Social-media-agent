from topic_manager import TopicManager
from fastapi import APIRouter, HTTPException
import os

router = APIRouter()
topic_manager = TopicManager()

TEXT_FILE = "company_text.txt"

# Maximum characters returned to the LLM
MAX_CHARS = 3000


@router.get("/company-text")
def company_text():

    if not os.path.exists(TEXT_FILE):
        raise HTTPException(
            status_code=404,
            detail="company_text.txt not found. Run ai_knowledge_builder.py first."
        )

    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # Reduce token usage
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    return {
        "company_text": text
    }


@router.get("/next-topic")
def next_topic():

    topic = topic_manager.get_next_topic()

    return {
        "topic": topic
    }