from post_context import build_post_context
from caption_generator import generate_caption


# ====================================
# 1. BUILD CONTEXT
# ====================================

context = build_post_context()


topic = context["topic"]

article = context["article"]

company_knowledge = context["company_knowledge"]


# ====================================
# 2. GENERATE CAPTION
# ====================================

caption = generate_caption(
    topic=topic,
    article=article,
    company_knowledge=company_knowledge
)


# ====================================
# 3. DISPLAY RESULT
# ====================================

print("\n")
print("=" * 70)
print("TOPIC")
print("=" * 70)

print(topic)


print("\n")
print("=" * 70)
print("NEWS")
print("=" * 70)

print(article["title"])

print(article["source"])

print(article["published"])

print(article["url"])


print("\n")
print("=" * 70)
print("FACEBOOK CAPTION")
print("=" * 70)

print(caption)