from fastapi import FastAPI
from loguru import logger


from app.config.database import init_db
from app.routes.index import APP_ROUTES
from app.schedule_methods.index import start_scheduler_tasks, stop_scheduler_tasks


async def lifespan(app: FastAPI):

    scheduler = start_scheduler_tasks()

    for route in APP_ROUTES:
        app.include_router(route)
    try:
        await init_db()

        logger.success("APP STARTED SUCCESSFULLY")
        yield
    finally:
        logger.error("APP STOPPED")
        stop_scheduler_tasks(scheduler)


app = FastAPI(
    lifespan=lifespan,
)

for route in APP_ROUTES:
    app.include_router(route)
