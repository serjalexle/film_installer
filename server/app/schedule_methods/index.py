from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.base import JobLookupError
from loguru import logger

from app.routes.root import generate_content

# from app.services.server_system_service import ServerSystemService


tasks = [
    {
        "func": generate_content,
        "interval": {"minutes": 60, "jitter": 10},
    },
]


def start_scheduler_tasks() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    for task in tasks:
        scheduler.add_job(
            task["func"],
            trigger=IntervalTrigger(**task["interval"]),
            id=task["func"].__name__,
            replace_existing=True,
        )

    scheduler.start()
    return scheduler


def stop_scheduler_tasks(scheduler):
    try:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped successfully")
    except JobLookupError as e:
        logger.error(f"Error stopping scheduler: {e}")
