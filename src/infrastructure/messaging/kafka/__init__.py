from src.core.config import settings
from src.infrastructure.messaging.kafka.kafka_consumer import KafkaMessageConsumer


def get_kafka_consumer() -> KafkaMessageConsumer:
    return KafkaMessageConsumer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS, group_id=settings.KAFKA_GROUP_ID
    )
