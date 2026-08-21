from post_context import build_post_context
from caption_reviewer import review_caption


context = build_post_context()

topic = context["topic"]

article = context["article"]

company_knowledge = context["company_knowledge"]


bad_caption = """
XEN HRA has announced a new partnership with the
government to completely transform recruitment in India.
The company has helped more than 500,000 employees
and guarantees better hiring results.
"""


review = review_caption(
    topic=topic,
    article=article,
    company_knowledge=company_knowledge,
    caption=bad_caption
)


print("\n")
print("=" * 70)
print("BAD CAPTION REVIEW")
print("=" * 70)

print("Status:", review.get("status"))

print("Score:", review.get("score"))

print("\nIssues:")

for issue in review.get("issues", []):
    print("-", issue)

print("\nSummary:")
print(review.get("summary"))