from aiohttp import ClientSession
from fastapi import FastAPI
from loguru import logger


bitrix_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def init_aiohttp_session(app: FastAPI):
    app.state.aiohttp_bitrix_session = ClientSession(
        headers=bitrix_headers,
    )
    logger.success("AIOHTTP SESSION INITIALIZED SUCCESSFULLY")


def close_aiohttp_session(app: FastAPI):
    logger.error("AIOHTTP SESSION CLOSED")
