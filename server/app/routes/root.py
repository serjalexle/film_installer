from fastapi import APIRouter
from loguru import logger



from app.integration.uakino import get_five_films_from_uakino
from app.models.movie import Movie
from app.services.telegram_service import TelegramService
# from app.services.video_service import VideoService



root_router = APIRouter(
    prefix="/api/root",
    tags=["Root"],
)


@root_router.post("/generate_content")
async def generate_content():
    try:
        # отримую фільми з uakino
        movies = await get_five_films_from_uakino()
        logger.success(f"Отримано {len(movies)} фільмів з uakino")

        # генеруємо пости для телеграм бота
        tg_posts = TelegramService.make_posts_to_channel(movies)
        logger.success(f"Згенеровано {len(tg_posts)} постів для телеграму")

        # скачуємо фільми
        # movie_url = movies[0]["details"]["full_video"]
        # await VideoService.download_hls_video(movie_url)

        # відправляємо пости в телеграм
        response = await TelegramService.send_posts(tg_posts)
        print(f"Відповідь від телеграму: {response}")

        # зберігаю фільми в бд
        result = await Movie.insert_many([Movie(**item) for item in movies])
        logger.success(f"Додано {len(result.inserted_ids)} фільмів")

        return {
            "status": "success",
            "message": f"Додано {len(result.inserted_ids)} фільмів",
        }

    except Exception as e:
        print(f"Помилка: {str(e)}")


