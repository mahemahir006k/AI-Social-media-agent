import json

from caption_generator import call_ollama


def build_review_prompt(topic, article, company_knowledge, caption):

    return f"""
You are a strict fact-checking reviewer for XEN HRA's
Facebook content.

Review the proposed Facebook caption against the
provided news article and XEN HRA knowledge.

========================
TOPIC
========================

{topic}


========================
NEWS ARTICLE
========================

Title:
{article.get("title", "")}

Source:
{article.get("source", "")}

Published:
{article.get("published", "")}

URL:
{article.get("url", "")}

Summary:
{article.get("description", "")}


========================
XEN HRA KNOWLEDGE
========================

{company_knowledge}


========================
PROPOSED CAPTION
========================

{caption}


========================
CHECK THESE THINGS
========================

========================
REVIEW RULES
========================

The news article is the PRIMARY source of truth.

The XEN HRA knowledge is ONLY background context.

IMPORTANT:

XEN HRA does NOT need to be mentioned in the caption.

A caption about external industry news is completely valid
even if it never mentions XEN HRA.

DO NOT reject a caption merely because XEN HRA is not mentioned.

DO NOT assume that XEN HRA was involved in the news.

DO NOT assume that XEN HRA has any relationship with the
people, companies, organizations, products or events
mentioned in the news article.

Only consider XEN HRA to be involved if the news article
explicitly states that XEN HRA was involved.

Check the caption for:

1. Is it about the selected topic?

2. Are the facts in the caption supported by the news
   article?

3. Does the caption invent information about the people,
   companies or organizations mentioned in the article?

4. Does the caption invent statistics, quotes, partnerships,
   services, achievements or benefits?

5. Does the caption claim XEN HRA was involved when the
   article does not say that?

6. Does the caption make unsupported claims about XEN HRA?

7. Is the source attribution accurate?

8. Is the caption suitable for professional Facebook
   publication?

9. Is the caption reasonably concise?

IMPORTANT APPROVAL RULE:

If the caption accurately summarizes the news and does not
make unsupported claims, APPROVE it even if XEN HRA is
completely absent from the caption.


========================
OUTPUT
========================

Return ONLY this JSON object.

Do NOT use Markdown.

Do NOT use ```.

Do NOT write anything before or after the JSON.

Example:

{{
  "status": "APPROVED",
  "score": 90,
  "issues": [],
  "summary": "The caption accurately summarizes the news."
}}

Allowed status values:

APPROVED
REJECTED

The score must be an integer between 0 and 100.

Approve the caption if it is factually supported by the
news article and does not contain unsupported claims.

Do NOT reject a caption simply because it does not mention
XEN HRA."""


def review_caption(
    topic,
    article,
    company_knowledge,
    caption
):

    prompt = build_review_prompt(
        topic=topic,
        article=article,
        company_knowledge=company_knowledge,
        caption=caption
    )

    response = call_ollama(prompt)

    print("\n")
    print("=" * 60)
    print("RAW REVIEWER RESPONSE")
    print("=" * 60)
    print(response)

    # ---------------------------------------
    # Clean Ollama response
    # ---------------------------------------

    cleaned = response.strip()

    # Remove Markdown code fences
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]

    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    # ---------------------------------------
    # Try to parse JSON
    # ---------------------------------------

    try:

        result = json.loads(cleaned)

        # Make sure required fields exist
        if "status" not in result:
            raise ValueError("Missing status")

        if "score" not in result:
            raise ValueError("Missing score")

        if "issues" not in result:
            raise ValueError("Missing issues")

        if "summary" not in result:
            raise ValueError("Missing summary")

        return result

    except (json.JSONDecodeError, ValueError):

        return {
            "status": "REJECTED",
            "score": 0,
            "issues": [
                "Reviewer returned invalid JSON."
            ],
            "summary": (
                "The reviewer response could not be parsed."
            )
        }