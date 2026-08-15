from news_fetcher import get_recent_news

news = get_recent_news("Recruitment")

for article in news:
    print("\nTITLE:", article["title"])
    print("SOURCE:", article["source"])
    print("DATE:", article["published"])
    print("URL:", article["url"])