from topic_manager import TopicManager

tm = TopicManager()

for i in range(10):
    print(tm.get_next_topic())