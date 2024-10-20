from telegram import Bot, InputMediaPhoto, InputMediaVideo
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.request import HTTPXRequest

from app.config.env import ENVSettings
from app.models.movie import MovieDTO


TOKEN = ENVSettings.TELEGRAM_BOT_TOKEN
CHAT_ID = ENVSettings.TELEGRAM_CHAT_ID

bot = Bot(token=TOKEN)


class TelegramService:

    @staticmethod
    def make_posts_to_channel(movies: MovieDTO):
        messages = []

        for movie in movies:
            # Створюємо список, куди будемо додавати частини повідомлення
            message_parts = []

            if "title" in movie:
                message_parts.append(f"📽️ Назва: {movie['title']}")

            if "rating" in movie:
                message_parts.append(f"⭐ Рейтинг: {movie['rating']}")

            if "quality" in movie:
                message_parts.append(f"🎥 Якість: {movie['quality']}")

            if "year" in movie["details"]:
                message_parts.append(f"📅 Рік виходу: {movie['details']['year']}")

            if "age_rating" in movie["details"]:
                message_parts.append(
                    f"🔞 Вік. рейтинг: {movie['details']['age_rating']}"
                )

            if "country" in movie["details"]:
                message_parts.append(f"🌍 Країна: {movie['details']['country']}")

            if "genre" in movie["details"]:
                message_parts.append(f"🎬 Жанр: {movie['details']['genre']}")

            if "director" in movie["details"]:
                message_parts.append(f"🎬 Режисер: {movie['details']['director']}")

            if "actors" in movie["details"]:
                message_parts.append(f"👥 Актори: {movie['details']['actors']}")

            if "duration" in movie["details"]:
                message_parts.append(f"⏰ Тривалість: {movie['details']['duration']}")

            if "language" in movie["details"]:
                message_parts.append(f"🗣️ Мова: {movie['details']['language']}")

            if "imdb_rating" in movie["details"]:
                message_parts.append(
                    f"🌐 IMDb рейтинг: {movie['details']['imdb_rating']}"
                )

            # if "description" in movie["details"]:
            #     message_parts.append(f"📝 Опис: {movie['details']['description']}")

            if "trailer" in movie["details"]:
                message_parts.append(f"🎞️ Трейлер: {movie['details']['trailer']}")

            if "full_video" in movie["details"]:
                message_parts.append(
                    f"🎞️ Повний фільм: {movie['details']['full_video']}"
                )

            # Об'єднуємо всі частини в одне повідомлення
            message = "\n".join(message_parts)
            messages.append(
                {
                    "text": message,
                    "image_url": movie["image_url"],
                    "video_url": movie["details"]["full_video"],
                    "url_button": movie["link"],
                }
            )

        return messages

    @staticmethod
    async def send_posts(posts):
        print(posts)
        request = HTTPXRequest(connect_timeout=300, read_timeout=600)
        bot = Bot(token=TOKEN, request=request)
        
        try:
            for post in posts:
                # Перевірка, чи пост має всі необхідні ключі
                if not all(key in post for key in ["image_url", "text", "url_button"]):
                    print(f"Некоректні дані в пості: {post}")
                    continue

                # Підготуємо медіа для відправки
                media = [
                    InputMediaPhoto(media=post["image_url"], caption=post["text"]),
                    # InputMediaVideo(media=open("help/downloaded_video.mp4", "rb")),
                ]

                # Відправляємо альбом
                await bot.send_media_group(chat_id=CHAT_ID, media=media)
                print("Відео успішно відправлено")

            return {"status": "success", "message": "Пости відправлено"}

        except Exception as e:
            print(f"Помилка: {str(e)}")
            return {"status": "error", "message": str(e)}
