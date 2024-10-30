import subprocess
from fastapi import APIRouter, Response
from loguru import logger
import os

citation_router = APIRouter(
    prefix="/api/citations",
    tags=["Citations"],
)


@citation_router.get("/generate_content")
async def generate_content():
    try:
        # Виконання скрипта gpt-parser/index.py і захоплення його stdout
        result = subprocess.run(
            ["python3", "../gpt-parser/index.py"],  # Використовуй "python" для Windows
            check=True,
            capture_output=True,
            text=True,
        )

        # wait until the file is created
        while not os.path.exists("parsed_articles.json"):
            pass

        # Лог результату для перевірки
        logger.info(result.stdout)

        html_content = result.stdout
        with open("parsed_articles.json", "r") as file:
            json_content = file.read()

        # Повертаємо JSON-контент у відповіді
        return Response(content=json_content, media_type="application/json")

    except subprocess.CalledProcessError as e:
        logger.error(f"Помилка при виконанні скрипта: {e.stderr}")
        return {
            "status": "error",
            "message": str(e.stderr),
        }
    except Exception as e:
        logger.error(f"Неочікувана помилка: {e}")
        return {
            "status": "error",
            "message": str(e),
        }
