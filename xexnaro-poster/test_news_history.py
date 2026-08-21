from news_history import (
    is_news_used,
    mark_news_used
)


test_url = "https://example.com/test-news"


print("Before marking:")

print(
    is_news_used(test_url)
)


mark_news_used(test_url)


print("\nAfter marking:")

print(
    is_news_used(test_url)
)