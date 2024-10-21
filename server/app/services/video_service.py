import subprocess
import os

from bs4 import BeautifulSoup

from app.services.parse_service import ParseService





class VideoService:

    @staticmethod
    async def download_hls_video(url, output_file="output.mp4"):
        try:
            # Перевіряємо наявність ffmpeg
            if not is_ffmpeg_installed():
                print("FFmpeg не знайдено. Будь ласка, встанови FFmpeg та додай його в PATH.")
                return
            
            html_content = await ParseService.get_page_html(url)

            soup = BeautifulSoup(html_content, "html.parser")

            # Отримуємо URL-адресу файлу .m3u8
            m3u8_url = soup.find("video").get("src")

            print(f"Завантаження відео з URL: {m3u8_url}")


            # Команда для завантаження відео
            command = [
                "ffmpeg",
                "-i", m3u8_url,  # Вхідний HLS-потік
                "-c", "copy",  # Копіювання без перекодування
                "output_file.mp4"
            ]

            # Запускаємо команду ffmpeg
            subprocess.run(command, check=True)
            print(f"Завантаження завершено! Відео збережено як {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Помилка під час завантаження відео: {e}")
        except Exception as e:
            print(f"Несподівана помилка: {e}")



def is_ffmpeg_installed():
    """Перевіряємо наявність FFmpeg на системі"""
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False





