import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.config.env import ENVSettings


def parse_movie_details(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        # Отримуємо детальну інформацію
        details = {}

        # Отримуємо такі дані
        sidebar_film_info_list = soup.find_all("div", class_="fi-item clearfix")

        for item in sidebar_film_info_list:
            # Перевіряємо наявність заголовка
            label_div = item.find("div", class_="fi-label")
            if not label_div:
                continue

            info_title = label_div.find("h2")
            if not info_title:
                continue

            info_title = info_title.get_text(strip=True)

            # Перевіряємо, чи задовольняє info_title хоча б один if
            if info_title in [
                "Рік виходу:",
                "Вік. рейтинг:",
                "Країна:",
                "Жанр:",
                "Режисер:",
                "Тривалість:",
                "Мова озвучення:",
            ]:
                # Дістаємо значення тільки якщо знайдена відповідність
                desc_div = item.find("div", class_="fi-desc")
                info_value = desc_div.get_text(strip=True) if desc_div else "Не вказано"

                if info_title == "Рік виходу:":
                    details["year"] = info_value
                    # print(f"Рік виходу: {info_value}")

                elif info_title == "Вік. рейтинг:":
                    details["age_rating"] = info_value
                    # print(f"Вік. рейтинг: {info_value}")

                elif info_title == "Країна:":
                    details["country"] = info_value
                    # print(f"Країна: {info_value}")

                elif info_title == "Жанр:":
                    details["genre"] = info_value
                    # print(f"Жанр: {info_value}")

                elif info_title == "Режисер:":
                    details["director"] = info_value
                    # print(f"Режисер: {info_value}")

                elif info_title == "Тривалість:":
                    details["duration"] = info_value
                    # print(f"Тривалість: {info_value}")

                elif info_title == "Мова озвучення:":
                    details["language"] = info_value
                    # print(f"Мова озвучення: {info_value}")

        print(
            soup.find("iframe", id="pre", class_="vdd-element") == None,
            "trailer_link",
        )

        trailer_link = None

        if soup.find("iframe", id="pre", class_="vdd-element"):
            trailer_link = soup.find("iframe", id="pre", class_="vdd-element").get(
                "data-src", None
            )

        if trailer_link:
            details["trailer_link"] = trailer_link

        return details

    except Exception as e:
        print(f"Не вдалося отримати деталі для {str(e)}")
        return {}


def uakino_parse_online_movies(html_content):
    # ? parse movies which are currently online on the website uakino
    soup = BeautifulSoup(html_content, "html.parser")

    # ? Переконаємося, що папка для зображень існує
    image_folder = "movie_images"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    movies = []
    movie_items = soup.find_all("div", class_="movie-item short-item")

    # filter films is title exist in movie_images, if exist not add to films
    names_without_ext = []
    list_of_image_names = os.listdir("movie_images")
    for image_name in list_of_image_names:
        names_without_ext.append(
            image_name.split(".webp")[0].replace("_", " ").replace("/", "$")
        )

    updated_film_list = []

    for film in movie_items:
        title_tag = film.find("a", class_="movie-title")
        title = title_tag.get_text(strip=True) if title_tag else None

        if title not in names_without_ext:
            updated_film_list.append(film)

    for item in updated_film_list:
        # Отримуємо назву фільму
        title_tag = item.find("a", class_="movie-title")
        title = title_tag.get_text(strip=True) if title_tag else None

        if title in updated_film_list:
            continue

        # Отримуємо посилання на фільм
        film_page_link = (
            urljoin(ENVSettings.UAKINO_BASE_URL, title_tag["href"])
            if title_tag
            else None
        )

        # Отримуємо рейтинг фільму
        rating_tag = item.find("div", class_="related-item-rating")
        rating = rating_tag.get_text(strip=True) if rating_tag else None

        # Отримуємо якість фільму
        quality_tag = item.find("div", class_="full-quality")
        quality = quality_tag.get_text(strip=True) if quality_tag else None

        # Отримуємо URL зображення
        img_tag = item.find("img")
        img_url = (
            urljoin(ENVSettings.UAKINO_BASE_URL, img_tag["src"]) if img_tag else ""
        )

        # Завантажуємо зображення, якщо URL знайдено
        image_path = None
        if img_url:
            try:
                # Визначаємо назву файлу на основі назви фільму

                completed_film_name = title.replace(" ", "_").replace("/", "$")

                image_name = f"{completed_film_name}.webp"
                image_path = os.path.join(image_folder, image_name)

                # Завантажуємо та зберігаємо зображення
                img_data = requests.get(img_url).content
                with open(image_path, "wb") as img_file:
                    img_file.write(img_data)
                # print(f"Зображення збережено: {image_path}")
            except Exception as e:
                print(f"Не вдалося завантажити зображення для '{title}': {str(e)}")

        # Отримуємо деталі для кожного фільму
        # details = parse_movie_details(film_page_link)

        # Формуємо об'єкт фільму
        movie = {
            "title": title,
            "link": film_page_link,
            "rating": rating,
            "quality": quality,
            "image_path": image_path,
        }

        movies.append(movie)

    return movies
