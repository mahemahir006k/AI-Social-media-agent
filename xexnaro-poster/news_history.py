import json
import os


NEWS_HISTORY_FILE = "used_news.json"


def load_used_news():

    if not os.path.exists(NEWS_HISTORY_FILE):
        return []

    with open(
        NEWS_HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return data.get("articles", [])


def save_used_news(articles):

    with open(
        NEWS_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "articles": articles
            },
            f,
            indent=4,
            ensure_ascii=False
        )


def is_news_used(url):

    used_news = load_used_news()

    return url in used_news


def mark_news_used(url):

    used_news = load_used_news()

    if url not in used_news:

        used_news.append(url)

        save_used_news(used_news)