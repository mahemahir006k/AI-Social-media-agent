from topic_knowledge import get_topic_knowledge


topics = [
    "Recruitment",
    "Payroll",
    "HR Compliance"
]


for topic in topics:

    print("\n")
    print("=" * 70)
    print("TOPIC:", topic)
    print("=" * 70)

    knowledge = get_topic_knowledge(topic)

    print(knowledge)