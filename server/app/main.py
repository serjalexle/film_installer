from fastapi import FastAPI
from loguru import logger

from fastapi.middleware.cors import CORSMiddleware
from app.config.database import init_db
from app.routes.index import APP_ROUTES
from app.schedule_methods.index import start_scheduler_tasks, stop_scheduler_tasks


async def lifespan(app: FastAPI):

    # scheduler = start_scheduler_tasks()

    for route in APP_ROUTES:
        app.include_router(route)
    try:
        await init_db()

        logger.success("APP STARTED SUCCESSFULLY")
        yield
    finally:
        logger.error("APP STOPPED")
        # stop_scheduler_tasks(scheduler)


app = FastAPI(
    lifespan=lifespan,
)

for route in APP_ROUTES:
    app.include_router(route)


# disable cors for development


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "https://e4c8-93-175-200-53.ngrok-free.app",
        "http://192.168.1.5:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
