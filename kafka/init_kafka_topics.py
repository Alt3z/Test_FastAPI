from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import time

TOPICS_TO_CREATE = ["hash_log", "enc_log"]
BOOTSTRAP_SERVERS = "kafka:9092"

def create_topics():
    admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)

    existing_topics = admin.list_topics()

    topics_to_create = [
        NewTopic(name=topic, num_partitions=1, replication_factor=1)
        for topic in TOPICS_TO_CREATE
        if topic not in existing_topics
    ]

    if topics_to_create:
        try:
            admin.create_topics(new_topics=topics_to_create, validate_only=False)
            print(f"✅ Созданы топики: {[t.name for t in topics_to_create]}")
        except TopicAlreadyExistsError:
            print("⚠️ Некоторые топики уже существуют")
    else:
        print("👌 Все нужные топики уже есть")

if __name__ == "__main__":
    for _ in range(10):
        try:
            create_topics()
            break
        except Exception as e:
            print(f"⏳ Ожидание Kafka... ({e})")
            time.sleep(3)
