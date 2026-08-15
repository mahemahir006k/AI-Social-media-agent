from post_context import build_post_context
from caption_generator import generate_caption
from caption_reviewer import review_caption


# ==================================
# 1. GET CONTEXT
# ==================================

context = build_post_context()

topic = context["topic"]

article = context["article"]

company_knowledge = context["company_knowledge"]


# ==================================
# 2. GENERATE CAPTION
# ==================================

caption = generate_caption(
    topic=topic,
    article=article,
    company_knowledge=company_knowledge
)


# ==================================
# 3. REVIEW CAPTION
# ==================================

review = review_caption(
    topic=topic,
    article=article,
    company_knowledge=company_knowledge,
    caption=caption
)


# ==================================
# 4. DISPLAY
# ==================================

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


print("\n")
print("=" * 70)
print("CAPTION")
print("=" * 70)

print(caption)


print("\n")
print("=" * 70)
print("REVIEW")
print("=" * 70)

print("Status:", review.get("status"))
print("Score:", review.get("score"))

print("\nIssues:")

for issue in review.get("issues", []):
    print("-", issue)

print("\nSummary:")
print(review.get("summary"))