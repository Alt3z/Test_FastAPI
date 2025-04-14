from aiokafka import AIOKafkaProducer
import json

class KafkaManager:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def get_producer(self):
        if not self.producer:
            self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await self.producer.start()
        return self.producer

    async def send_event(self, topic: str, event: dict):
        producer = await self.get_producer()
        await producer.send_and_wait(topic, json.dumps(event).encode())

    async def close(self):
        if self.producer:
            await self.producer.stop()