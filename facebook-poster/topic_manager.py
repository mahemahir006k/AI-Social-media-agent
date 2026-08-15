import json
import random
import os

TOPIC_FILE = "topics.json"


class TopicManager:

    def __init__(self):
        if not os.path.exists(TOPIC_FILE):
            raise FileNotFoundError(f"{TOPIC_FILE} not found.")

    def _load(self):
        with open(TOPIC_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with open(TOPIC_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get_next_topic(self):

        data = self._load()

        topics = data["topics"]
        used = data["used"]

        remaining = [t for t in topics if t not in used]

        if not remaining:
            data["used"] = []
            remaining = topics

        topic = random.choice(remaining)

        data["used"].append(topic)

        self._save(data)

        return topic