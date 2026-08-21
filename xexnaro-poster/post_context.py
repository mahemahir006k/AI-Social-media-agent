from topic_manager import TopicManager
from news_fetcher import get_recent_news
from topic_knowledge import get_topic_knowledge
from news_history import is_news_used

def build_post_context(topic=None):

    topic_manager = TopicManager()


    # --------------------------------
    # 1. Select topic
    # --------------------------------

    if topic is None:

        topic = topic_manager.get_next_topic()


    # --------------------------------
    # 2. Get recent news
    # --------------------------------

    news = get_recent_news(
        topic,
        max_results=5
    )


    if not news:

        raise Exception(
            f"No recent news found for topic: {topic}"
        )


    # --------------------------------
    # 3. Find unused article
    # --------------------------------

    article = None

    for candidate in news:

        url = candidate.get("url", "")

        if not url:
            continue

        if not is_news_used(url):

            article = candidate

            break


    # --------------------------------
    # 4. All articles already used
    # --------------------------------

    if article is None:

        raise Exception(
            f"All recent news articles for "
            f"'{topic}' have already been used."
        )


    # --------------------------------
    # 5. Get company knowledge
    # --------------------------------

    company_knowledge = get_topic_knowledge(
        topic
    )


    # --------------------------------
    # 6. Return complete context
    # --------------------------------

    return {

        "topic": topic,

        "article": article,

        "company_knowledge": company_knowledge
    }