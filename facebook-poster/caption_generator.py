import re
import requests

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL
)


# ============================================================
# OLLAMA API
# ============================================================

def call_ollama(prompt):
    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        url,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()


# ============================================================
# CAPTION GENERATOR
# ============================================================

def generate_caption(
    topic,
    article,
    company_knowledge=None,
    previous_issues=None
):

    previous_issues = previous_issues or []

    issues_text = "\n".join(
        f"- {issue}" for issue in previous_issues
    )

    prompt = f"""
You are a professional Facebook news caption writer.

Your task is to write a Facebook caption about the
RECENT NEWS ARTICLE below.

========================
TOPIC
========================

{topic}

========================
NEWS ARTICLE
========================

Title:
{article.get("title", "")}

Description:
{article.get("description", "")}

Source:
{article.get("source", "")}

Published:
{article.get("published", "")}


========================
SOURCE RULE
========================

At the end of the caption, include:

Source: <publisher name>

Use ONLY the publisher/source name.

DO NOT include the article URL in the caption.

DO NOT include Google News URLs.

DO NOT include Markdown links.

DO NOT include HTML links.


========================
XEN HRA RULE
========================

DO NOT mention XEN HRA in the caption.

The news is external industry news.

Do not claim XEN HRA was involved in the news.

Do not describe XEN HRA as:

- a leading recruitment agency
- a company involved in the news
- a partner
- a service provider
- an expert quoted in the article

For this task, DO NOT mention XEN HRA.


========================
FACTUAL ACCURACY
========================

The news article is the ONLY source of factual
information for this caption.

Use ONLY information explicitly supported
by the news article.

Do NOT use general knowledge.

Do NOT guess.

Do NOT infer additional facts.

Do NOT invent:

- benefits
- statistics
- achievements
- partnerships
- services
- customer results
- company capabilities
- quotes
- business outcomes
- reasons for an appointment
- future plans

unless explicitly stated in the article.


========================
NO EXAGGERATION
========================

Do not use phrases such as:

"revolutionize"
"game changer"
"transform"
"promises"
"guarantees"
"leading"
"groundbreaking"

unless the article explicitly supports those claims.

Prefer factual wording such as:

"has announced"
"has appointed"
"has launched"
"according to the report"
"the development highlights"
"the company said"


========================
PREVIOUS REVIEW FEEDBACK
========================

{issues_text}

If previous reviewer feedback is provided,
correct those specific problems.


========================
CAPTION STYLE
========================

Use:

1. A short factual opening.
2. 2-3 sentences summarizing the news.
3. Optional short engagement question.
4. Source attribution using ONLY the publisher name.
5. EXACTLY 4-6 relevant hashtags.

HASHTAG RULES:

The caption MUST end with hashtags.

Hashtags must be relevant to the TOPIC and NEWS.

For example:

#HRNews #Payroll #HRCompliance #HumanResources

Do NOT invent company-specific hashtags.

Do NOT use unrelated hashtags.

Do NOT put hashtags in the middle of the caption.

The final line MUST contain the hashtags.


========================
OUTPUT RULE
========================

Return ONLY the final Facebook caption.

DO NOT write:

"Here is a possible Facebook caption."

DO NOT write:

"Here is the caption."

DO NOT explain your answer.

DO NOT return JSON.

DO NOT wrap the entire caption in quotation marks.

DO NOT include the article URL.

The final output MUST contain 4-6 hashtags.

If hashtags are missing, generate them before returning the caption.
"""

    # ========================================================
    # CALL OLLAMA
    # ========================================================

    response = call_ollama(prompt)

    # ========================================================
    # CLEAN AI RESPONSE
    # ========================================================

    cleaned = response.strip()

    # --------------------------------------------------------
    # Remove common AI preambles
    # --------------------------------------------------------

    prefixes = [
        "Here is a possible Facebook caption based on the news article:",
        "Here is a possible Facebook caption:",
        "Here is the Facebook caption:",
        "Here’s a possible Facebook caption based on the news article:",
        "Here’s a possible Facebook caption:",
        "Here is the final Facebook caption:",
        "Facebook Caption:"
    ]

    for prefix in prefixes:
        if cleaned.lower().startswith(prefix.lower()):
            cleaned = cleaned[len(prefix):].strip()
            break

    # ========================================================
    # REMOVE SURROUNDING QUOTATION MARKS
    # ========================================================

    if (
        len(cleaned) >= 2
        and cleaned.startswith('"')
        and cleaned.endswith('"')
    ):
        cleaned = cleaned[1:-1].strip()

    # ========================================================
    # REMOVE MARKDOWN LINKS
    # ========================================================

    cleaned = re.sub(
        r'\[([^\]]+)\]\([^)]+\)',
        r'\1',
        cleaned
    )

    # ========================================================
    # REMOVE GOOGLE NEWS URLS
    # ========================================================

    cleaned = re.sub(
        r'https?://news\.google\.com/\S+',
        '',
        cleaned,
        flags=re.IGNORECASE
    )

    # ========================================================
    # REMOVE OTHER URLS
    # ========================================================

    cleaned = re.sub(
        r'https?://\S+',
        '',
        cleaned,
        flags=re.IGNORECASE
    )

    # ========================================================
    # CLEAN SOURCE LINE
    # ========================================================

    # Example:
    #
    # Source: Nasscom (https://example.com)
    #
    # becomes:
    #
    # Source: Nasscom

    cleaned = re.sub(
        r'(Source:\s*[^\n(]+)\s*\([^)]*https?://[^)]*\)',
        r'\1',
        cleaned,
        flags=re.IGNORECASE
    )

    # ========================================================
    # CLEAN EXTRA SPACES
    # ========================================================

    cleaned = re.sub(
        r'[ \t]+',
        ' ',
        cleaned
    )

    cleaned = re.sub(
        r'\n{3,}',
        '\n\n',
        cleaned
    )

    cleaned = cleaned.strip()

    # ========================================================
    # HASHTAG SAFETY CHECK
    # ========================================================

    hashtags = re.findall(
        r'(?<!\w)#[A-Za-z][A-Za-z0-9_]*',
        cleaned
    )

    # Remove duplicate hashtags while preserving order
    unique_hashtags = []

    for hashtag in hashtags:
        if hashtag.lower() not in {
            h.lower() for h in unique_hashtags
        }:
            unique_hashtags.append(hashtag)

    # ========================================================
    # FALLBACK HASHTAGS
    # ========================================================

    topic_hashtags = {

        "Recruitment": [
            "#Recruitment",
            "#TalentAcquisition",
            "#Hiring",
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

    # ========================================================
    # ENSURE 4-6 HASHTAGS
    # ========================================================

    if len(unique_hashtags) < 4:

        for hashtag in fallback_hashtags:

            if hashtag.lower() not in {
                h.lower() for h in unique_hashtags
            }:
                unique_hashtags.append(hashtag)

            if len(unique_hashtags) >= 4:
                break

    # Limit to maximum 6 hashtags
    unique_hashtags = unique_hashtags[:6]

    # ========================================================
    # REMOVE EXISTING HASHTAGS FROM END
    # ========================================================

    # This prevents duplicate hashtag lines when we rebuild
    # the final hashtag section.

    cleaned = re.sub(
        r'(?:\s*#[A-Za-z][A-Za-z0-9_]*)+\s*$',
        '',
        cleaned
    ).strip()

    # ========================================================
    # ADD FINAL HASHTAG LINE
    # ========================================================

    cleaned += "\n\n" + " ".join(unique_hashtags)

    # ========================================================
    # FINAL RETURN
    # ========================================================

    return cleaned.strip()