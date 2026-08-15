from topic_manager import TopicManager
from news_fetcher import get_recent_news
from topic_knowledge import get_topic_knowledge


topic_manager = TopicManager()


# --------------------------------
# 1. GET TOPIC
# --------------------------------

topic = topic_manager.get_next_topic()

print("\n================================")
print("SELECTED TOPIC")
print("================================")

print(topic)


# --------------------------------
# 2. GET RECENT NEWS
# --------------------------------

print("\n================================")
print("RECENT NEWS")
print("================================")

news = get_recent_news(topic)


if not news:

    print("❌ No recent news found.")

    exit()


article = news[0]


print("\nTITLE:")
print(article["title"])

print("\nSOURCE:")
print(article["source"])

print("\nDATE:")
print(article["published"])

print("\nURL:")
print(article["url"])


# --------------------------------
# 3. GET XEN HRA KNOWLEDGE
# --------------------------------

print("\n================================")
print("XEN HRA KNOWLEDGE")
print("================================")

knowledge = get_topic_knowledge(topic)

print(knowledge)


# --------------------------------
# 4. FINAL DATA
# --------------------------------

print("\n================================")
print("READY FOR CAPTION GENERATOR")
print("================================")

print("TOPIC:")
print(topic)

print("\nNEWS:")
print(article["title"])

print("\nCOMPANY KNOWLEDGE:")
print(knowledge)