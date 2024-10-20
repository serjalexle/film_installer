import os

from dotenv import load_dotenv



load_dotenv()


class ENVSettings:
    TELEGRAM_BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "your")
    TELEGRAM_CHAT_ID: str = os.environ.get("TELEGRAM_CHAT_ID", "your")

    UAKINO_BASE_URL: str = os.environ.get("UAKINO_BASE_URL", "")

    MONGODB_URL: str = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")

    @staticmethod
    def get_db_url():
        return os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
