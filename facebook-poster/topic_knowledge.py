from pathlib import Path


KNOWLEDGE_FILE = "company_text.txt"


def load_company_knowledge():

    path = Path(KNOWLEDGE_FILE)

    if not path.exists():
        raise FileNotFoundError(
            f"{KNOWLEDGE_FILE} not found."
        )

    return path.read_text(
        encoding="utf-8"
    )


def get_topic_knowledge(topic):

    knowledge = load_company_knowledge()

    topic_keywords = {
        "Recruitment": [
            "recruitment",
            "recruiting",
            "hiring",
            "talent acquisition",
            "candidate"
        ],

        "Payroll": [
            "payroll",
            "salary",
            "wages",
            "compensation"
        ],

        "HR Compliance": [
            "compliance",
            "labour",
            "labor",
            "regulation",
            "policy"
        ],

        "Executive Search": [
            "executive",
            "leadership",
            "senior hiring",
            "executive search"
        ],

        "Employee Engagement": [
            "employee engagement",
            "employee experience",
            "workplace"
        ],

        "Staffing Solutions": [
            "staffing",
            "workforce",
            "temporary staffing",
            "contract staffing"
        ],

        "Talent Acquisition": [
            "talent acquisition",
            "talent",
            "candidate sourcing"
        ],

        "Training & Development": [
            "training",
            "development",
            "upskilling",
            "learning"
        ]
    }

    keywords = topic_keywords.get(
        topic,
        [topic.lower()]
    )

    sections = knowledge.split("\n\n")

    relevant_sections = []

    for section in sections:

        section_lower = section.lower()

        if any(
            keyword.lower() in section_lower
            for keyword in keywords
        ):
            relevant_sections.append(section)

    if not relevant_sections:

        return knowledge[:8000]

    return "\n\n".join(
        relevant_sections
    )