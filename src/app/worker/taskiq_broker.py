__all__ = ("broker", "scheduler")

import logging

import taskiq_fastapi
from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from core.config import settings

log = logging.getLogger(__name__)
broker = AioPikaBroker(
    url=str(settings.taskiq.url),
    queue_name=settings.taskiq.queue_name,
    exchange_name=settings.taskiq.exchange_name,
    qos=1,
    declare_queues=True,
    declare_exchange=True,
    declare_queues_kwargs={"durable": True},
    declare_exchange_kwargs={"durable": True},
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

taskiq_fastapi.init(broker, "app.main:main_app")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=settings.logging_config.log_level_value,
        format=settings.logging_config.log_format,
        datefmt=settings.logging_config.date_format,
    )
    log.info("Worker startup complete, got state: %s", state)
