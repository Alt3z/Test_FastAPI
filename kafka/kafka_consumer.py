import asyncio
from aiokafka import AIOKafkaConsumer
import json

from src.config import KAFKA_SERVERS

async def consume_logs():
    consumer = AIOKafkaConsumer(
        "hash_log", "enc_log",  # Подписка сразу на 2 темы
        bootstrap_servers=KAFKA_SERVERS,
        group_id="combined-log-consumer"
    )
    await consumer.start()

    try:
        async for msg in consumer:
            try:
                log_event = json.loads(msg.value)
                topic = msg.topic

                if topic == "hash_log":
                    log_file = "hash_log.txt"
                elif topic == "enc_log":
                    log_file = "enc_log.txt"
                else:
                    log_file = "unknown_log.txt"

                event = log_event.get("event", "UNKNOWN_EVENT")
                details = log_event.get("details", {})

                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{topic.upper()}] Event: {event}, Details: {details}\n")
            except Exception as e:
                print(f"Error processing message: {e}")
    finally:
        await consumer.stop()


asyncio.run(consume_logs())
