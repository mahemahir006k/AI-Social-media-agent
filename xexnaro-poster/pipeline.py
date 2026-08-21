from post_context import build_post_context
from caption_generator import generate_caption
from caption_reviewer import review_caption
from news_history import mark_news_used
from topic_manager import TopicManager
from image_generator import PollinationsGenerator
from facebook_publisher import FacebookPublisher

import re


MAX_RETRIES = 2
MIN_REVIEW_SCORE = 80


def ensure_hashtags(caption, topic):
    """
    Make sure the final caption contains 4-6 hashtags.
    This is a safety layer in case Ollama forgets them.
    """

    hashtags = re.findall(
        r"(?<!\w)#[A-Za-z][A-Za-z0-9_]*",
        caption
    )

    # Already has enough hashtags
    if len(hashtags) >= 4:
        return caption

    topic_hashtags = {

        "Recruitment": [
            "#Recruitment",
            "#Hiring",
            "#TalentAcquisition",
            "#HRNews"
        ],

        "Executive Search": [
            "#ExecutiveSearch",
            "#LeadershipHiring",
            "#TalentAcquisition",
            "#HRNews"
        ],

        "Payroll": [
            "#Payroll",
            "#HRSoftware",
            "#HRNews",
            "#HumanResources"
        ],

        "Training & Development": [
            "#TrainingAndDevelopment",
            "#LearningAndDevelopment",
            "#HR",
            "#HRNews"
        ],

        "HR Compliance": [
            "#HRCompliance",
            "#HRNews",
            "#HumanResources",
            "#IndiaHR"
        ],

        "Performance Management": [
            "#PerformanceManagement",
            "#EmployeePerformance",
            "#HR",
            "#HRNews"
        ],

        "Employee Engagement": [
            "#EmployeeEngagement",
            "#EmployeeExperience",
            "#HR",
            "#HRNews"
        ]
    }

    fallback_hashtags = topic_hashtags.get(
        topic,
        [
            "#HRNews",
            "#HumanResources",
            "#HR",
            "#BusinessNews"
        ]
    )

    caption = caption.rstrip()

    caption += "\n\n" + " ".join(
        fallback_hashtags[:4]
    )

    return caption


def publish_news_pipeline(topic=None):

    topic_manager = TopicManager()

    # ==========================================
    # BUILD POST CONTEXT
    # ==========================================

    context = build_post_context(topic)

    selected_topic = context["topic"]
    article = context["article"]
    company_knowledge = context["company_knowledge"]

    caption = None
    review = None

    # ==========================================
    # CAPTION + REVIEW
    # ==========================================

    previous_issues = []

    for attempt in range(MAX_RETRIES + 1):

        print("=" * 60)
        print(f"CAPTION ATTEMPT {attempt + 1}")
        print("=" * 60)

        # --------------------------------------
        # GENERATE CAPTION
        # --------------------------------------

        caption = generate_caption(
            topic=selected_topic,
            article=article,
            company_knowledge=None,
            previous_issues=previous_issues
        )

        # --------------------------------------
        # ENSURE HASHTAGS
        # --------------------------------------

        caption = ensure_hashtags(
            caption,
            selected_topic
        )

        print("\nCaption:")
        print(caption)

        # --------------------------------------
        # REVIEW CAPTION
        # --------------------------------------

        review = review_caption(
            topic=selected_topic,
            article=article,
            company_knowledge=None,
            caption=caption
        )

        print("\nReview:")
        print(review)

        # --------------------------------------
        # CHECK REVIEW
        # --------------------------------------

        if (
            review.get("status") == "APPROVED"
            and review.get("score", 0) >= MIN_REVIEW_SCORE
        ):

            print("\n✅ Caption approved.")

            break

        # --------------------------------------
        # REJECTED
        # --------------------------------------

        previous_issues = review.get(
            "issues",
            []
        )

        print("\n❌ Caption rejected.")

        if previous_issues:

            print("Reviewer issues:")

            for issue in previous_issues:

                print("-", issue)

    else:

        # ==========================================
        # ALL CAPTION ATTEMPTS FAILED
        # ==========================================

        return {
            "success": False,
            "stage": "review",
            "topic": selected_topic,
            "article": article,
            "review": review
        }

    # ==========================================
    # GENERATE IMAGE
    # ==========================================

    print("=" * 60)
    print("GENERATING IMAGE")
    print("=" * 60)

    image_generator = PollinationsGenerator()

    # ------------------------------------------
    # IMAGE PROMPT
    # ------------------------------------------

    image_prompt = f"""
Create a professional 1080x1080 social media image
for this recent HR industry news.

========================
TOPIC
========================

{selected_topic}

========================
NEWS HEADLINE
========================

{article["title"]}

========================
IMAGE REQUIREMENTS
========================

Create a visually engaging corporate HR/business
news graphic related to the news above.

The image should visually represent the subject
of the news.

IMPORTANT:

Include a SHORT, READABLE headline on the image
based ONLY on the news headline.

The headline should communicate the main news
in approximately 6-12 words.

Do NOT copy the entire article title if it is too long.

Do NOT create paragraphs of text.

Do NOT invent facts.

Do NOT invent statistics.

Do NOT invent company claims.

Do NOT create fake quotes.

Do NOT create fake numbers.

Do NOT add information that is not present
in the news headline.

Do NOT add hashtags to the image.

Do NOT add a website URL.

Do NOT add a fake source.

========================
VISUAL STYLE
========================

Use a professional corporate HR/business style.

Modern business-news aesthetic.

Clean composition.

Professional typography.

Strong readable headline.

HR/business related visual elements.

Suitable for Facebook.

High-quality social media design.

The headline should be clearly visible and
not overlap important visual elements.

Use the news topic to guide the visual design.
"""

    # ==========================================
    # IMAGE GENERATION
    # ==========================================

    try:

        image_path = image_generator.generate(
            image_prompt
        )

    except Exception as e:

        print("=" * 60)
        print("IMAGE GENERATION FAILED")
        print("=" * 60)

        print(e)

        return {
            "success": False,
            "stage": "image",
            "error": str(e),
            "topic": selected_topic,
            "article": article,
            "caption": caption,
            "review": review
        }

    print("\nGenerated image:")
    print(image_path)

    # ==========================================
    # PUBLISH TO FACEBOOK
    # ==========================================

    print("=" * 60)
    print("PUBLISHING TO FACEBOOK")
    print("=" * 60)

    print("\nImage:")
    print(image_path)

    print("\nCaption:")
    print(caption)

    try:

        publisher = FacebookPublisher()

        fb_result = publisher.publish(
            image_path=image_path,
            caption=caption
        )

    except Exception as e:

        print("=" * 60)
        print("FACEBOOK PUBLISH FAILED")
        print("=" * 60)

        print(e)

        return {
            "success": False,
            "stage": "facebook",
            "error": str(e),
            "topic": selected_topic,
            "article": article,
            "caption": caption,
            "image_path": image_path,
            "review": review
        }

    # ==========================================
    # FACEBOOK RESULT
    # ==========================================

    print("\nFacebook response:")
    print(fb_result)

    # ==========================================
    # CHECK FACEBOOK RESULT
    # ==========================================

    if not fb_result.get("success", False):

        print("=" * 60)
        print("FACEBOOK PUBLISHING FAILED")
        print("=" * 60)

        return {
            "success": False,
            "stage": "facebook",
            "topic": selected_topic,
            "article": article,
            "caption": caption,
            "image_path": image_path,
            "review": review,
            "facebook": fb_result
        }

    # ==========================================
    # SAVE ARTICLE HISTORY
    # ==========================================

    print("=" * 60)
    print("SAVING ARTICLE HISTORY")
    print("=" * 60)

    mark_news_used(
        article["url"]
    )

    # ==========================================
    # SUCCESS
    # ==========================================

    print("=" * 60)
    print("✅ FACEBOOK POST SUCCESSFUL")
    print("=" * 60)

    return {
        "success": True,
        "topic": selected_topic,
        "article": article,
        "caption": caption,
        "review": review,
        "image_path": image_path,
        "facebook": fb_result
    }