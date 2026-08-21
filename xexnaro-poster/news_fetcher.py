import feedparser
from urllib.parse import quote
from bs4 import BeautifulSoup

def clean_html(text):

    return BeautifulSoup(
        text,
        "html.parser"
    ).get_text(
        " ",
        strip=True
    )

def get_recent_news(topic, max_results=5):
    query = quote(f"{topic} HR India")

    url = (
        f"https://news.google.com/rss/search?"
        f"q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:max_results]:
        articles.append({
            "title": entry.get("title", ""),
            "description": clean_html(
                entry.get("summary", "")
            ),
            "published": entry.get("published", ""),
            "url": entry.get("link", ""),
            "source": entry.get("source", {}).get("title", "")
            if hasattr(entry.get("source"), "get")
            else ""
        })

    return articles