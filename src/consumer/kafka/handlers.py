from src.application.use_cases.cross.process_event_usecase import ProcessEventUseCase
from src.consumer.kafka.schemas import KafkaSensorEventMessage


async def handle_kafka_message_process_event(msg: dict, usecase: ProcessEventUseCase) -> None:
    event = KafkaSensorEventMessage(**msg)

    await usecase.execute(
        device_id=event.device_id,
        sensor_type=event.sensor_type,
        value=event.value,
        metadata=event.metadata,
    )
