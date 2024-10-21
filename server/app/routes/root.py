from fastapi import APIRouter
from fastapi.responses import FileResponse
from loguru import logger


from app.integration.uakino import get_five_films_from_uakino
from app.models.movie import Movie
from app.services.telegram_service import TelegramService
from app.services.video_service import VideoService

from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    CompositeVideoClip,
)
from moviepy.config import change_settings


from app.utils.get_epic_time_on_audio import get_epic_time_on_audio


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

        logger.info("Починаємо завантаження фільмів")
        # скачуємо фільми
        for movie in movies:
            movie_url = movie["details"]["full_video"]
            await VideoService.download_hls_video(movie_url)

        logger.success("Завантаження фільмів завершено")

        # відправляємо пости в телеграм
        response = await TelegramService.send_posts(tg_posts)
        print(f"Відповідь від телеграму: {response}")
        await TelegramService.send_video()

        # # зберігаю фільми в бд
        result = await Movie.insert_many([Movie(**item) for item in movies])
        logger.success(f"Додано {len(result.inserted_ids)} фільмів")

        return {
            "status": "success",
            "message": f"Додано {len(result.inserted_ids)} фільмів",
        }

    except Exception as e:
        print(f"Помилка: {str(e)}")


@root_router.get("/generate_video")
async def generate_video():
    try:
        # Відкриваємо файл фільму
        change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})
        video = VideoFileClip("output_file.mp4")

        # Відкриваємо аудіофайл
        audio = video.audio
        audio.write_audiofile("output_audio.mp3")

        # Перетворюємо результат у список
        epic_times_list = await get_epic_time_on_audio()

        clip_parts = []

        for epic_time in epic_times_list:
            # Вибираємо частину відео
            clip_part = video.subclip(epic_time["start_time"], epic_time["start_time"] + epic_time["duration"])
            clip_parts.append(clip_part)


        text = TextClip("Film name", fontsize=70, color="red")
        text = text.set_duration(5).set_position(("center", "top"))

        # # Об'єднуємо частини
        trailer = concatenate_videoclips(clip_parts)

        trailer_with_text = CompositeVideoClip([trailer, text])

        # # Зберігаємо трейлер як окремий файл
        trailer_with_text.write_videofile(
            "trailer.mp4", codec="libx264", audio_codec="aac"
        )

        print("Трейлер успішно змонтовано та збережено!")
    except Exception as e:
        print(f"Помилка під час створення трейлера: {str(e)}")
