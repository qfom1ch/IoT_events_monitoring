import asyncio

from src.application.use_cases.cross.process_event_usecase import ProcessEventUseCase
from src.consumer.kafka.handlers import handle_kafka_message_process_event
from src.core.config import settings
from src.infrastructure.di.container import create_container
from src.infrastructure.messaging.kafka import get_kafka_consumer
from src.infrastructure.mongodb import init_mongo


async def run() -> None:
    client = await init_mongo()
    container = create_container()
    consumer = get_kafka_consumer()

    async def process_event_handler(msg: dict) -> None:
        async with container() as request_container:
            usecase = await request_container.get(ProcessEventUseCase)
            await handle_kafka_message_process_event(msg, usecase)

    try:
        await consumer.start()

        while True:
            await consumer.consume(
                topic=settings.KAFKA_TOPIC_SENSOR_EVENTS, handler=process_event_handler
            )

    finally:
        client.close()


if __name__ == '__main__':
    asyncio.run(run())
