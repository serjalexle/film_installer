from bs4 import BeautifulSoup


def uakino_parse_short_items(html_content):
    # ? parse cards of movies from uakino
    soup = BeautifulSoup(html_content, "html.parser")

    result = []

    short_items_html = soup.find_all("div", class_="movie-item short-item")

    for short_item in short_items_html:
        title = short_item.find("a", class_="movie-title").get_text(strip=True)
        rating = short_item.find("div", class_="related-item-rating").get_text(
            strip=True
        )
        quality = short_item.find("div", class_="full-quality").get_text(strip=True)
        image_url = f'https://uakino.me{short_item.find("img")["src"]}'
        link = f'{short_item.find("a", class_="movie-title")["href"]}'

        result.append(
            {
                "title": title,
                "rating": rating,
                "quality": quality,
                "image_url": image_url,
                "link": link,
                "details": None,
            }
        )

    return result


def uakino_parse_film_details(html_content):
    # Парсимо деталі фільму з Uakino
    soup = BeautifulSoup(html_content, "html.parser")

    result = {}

    # Знаходимо елементи з детальною інформацією
    film_details_html = soup.find("div", class_="film-info").find_all(
        "div", class_="fi-item clearfix"
    )

    for item in film_details_html:
        # Отримуємо заголовок і значення
        label = item.find("div", class_="fi-label").get_text(strip=True)
        value_tag = item.find("div", class_="fi-desc")

        # Обробляємо інформацію відповідно до заголовків
        if label == "Рік виходу:":
            result["year"] = (
                value_tag.get_text(strip=True) if value_tag else "Не вказано"
            )

        elif label == "Вік. рейтинг:":
            result["age_rating"] = (
                value_tag.get_text(strip=True) if value_tag else "Не вказано"
            )

        elif label == "Країна:":
            result["country"] = (
                value_tag.get_text(strip=True) if value_tag else "Не вказано"
            )

        elif label == "Жанр:":
            genres = [genre.get_text(strip=True) for genre in value_tag.find_all("a")]
            result["genre"] = ", ".join(genres)

        elif label == "Режисер:":
            result["director"] = (
                value_tag.get_text(strip=True) if value_tag else "Не вказано"
            )

        elif label == "Актори:":
            actors = [actor.get_text(strip=True) for actor in value_tag.find_all("a")]
            result["actors"] = ", ".join(actors)

        elif label == "Тривалість:":
            result["duration"] = (
                value_tag.get_text(strip=True) if value_tag else "Не вказано"
            )

        elif label == "Мова озвучення:":
            result["language"] = (
                value_tag.get_text(strip=True) if value_tag else "Не вказано"
            )

        # IMDb рейтинг
        if (
            item.find("img", alt=True)
            and "imdb рейтинг" in item.find("img")["alt"].lower()
        ):
            result["imdb_rating"] = (
                value_tag.get_text(strip=True) if value_tag else "Не вказано"
            )

    
    film_description = soup.find("div", class_="full-text clearfix").get_text(strip=True)
    result["description"] = film_description

    # write soup to file
    with open("soup.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

    trailer = soup.find("iframe", class_="vdd-element")

    if trailer:
        trailer = trailer.get("data-src")

    if trailer:
        result["trailer"] = trailer
    
    else:
        result["trailer"] = "Не вказано"

    result["trailer"] = trailer

    full_video = soup.find("iframe", id="playerfr")

    if not full_video:
        # 
        full_video = soup.find("iframe", id="pre")

    if full_video:
        full_video = full_video.get("src")

    if full_video:

        # if full_video includes geoblock=ua then replace it with empty string
        if "geoblock=ua" in full_video:
            full_video = full_video.replace("geoblock=ua", "")

        result["full_video"] = full_video
    
    else:
        result["full_video"] = "Не вказано"

    result["full_video"] = full_video


    return result
