import json
from collections.abc import Callable

from aiokafka import AIOKafkaConsumer

from src.core.message_consumer import MessageConsumer


class KafkaMessageConsumer(MessageConsumer):
    def __init__(self, bootstrap_servers: str, group_id: str = 'default_group') -> None:
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None

    async def start(self) -> None:
        if not self.consumer:
            self.consumer = AIOKafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode()),
            )
            await self.consumer.start()

    async def consume(self, topic: str, handler: Callable) -> None:
        if self.consumer is None:
            await self.start()

        self.consumer.subscribe([topic])
        try:
            async for msg in self.consumer:
                await handler(json.loads(msg.value))
        except Exception as e:
            print(f'Error consuming messages from {topic}: {e}')

    async def stop(self) -> None:
        if self.consumer:
            await self.consumer.stop()
