import asyncio
import json

from aiokafka import AIOKafkaProducer


async def send_test_event() -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode()
    )
    await producer.start()
    try:
        await producer.send(
            'sensor_events',
            key=b'7ead3ae1-2d21-493a-beba-d741ac9f6253',
            value=json.dumps({
                'device_id': '7ead3ae1-2d21-493a-beba-d741ac9f6253',
                'sensor_type': 'temperature',
                'value': 85.5,
                'metadata': {},
            }),
        )
        print('Sent test event')
    finally:
        await producer.stop()


if __name__ == '__main__':
    asyncio.run(send_test_event())
