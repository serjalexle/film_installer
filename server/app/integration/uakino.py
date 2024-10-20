



from app.models.movie import Movie
from app.parsers.uakino.index import uakino_parse_film_details, uakino_parse_short_items
from app.services.parse_service import ParseService


async def get_five_films_from_uakino():
    movies = []

    page_count = 1

    while len(movies) < 5:
        print(f"Парсимо сторінку {page_count}. Загальна кількість фільмів: {len(movies)}")
        # отримуємо сторінку з фільмами
        uakino_action_films_html_page = await ParseService.get_page_html(
            f"https://uakino.me/filmy/genre-action/best/page/{page_count}/"
        )

        # парсимо фільми
        uakino_short_items = uakino_parse_short_items(uakino_action_films_html_page)

        # Отримуємо всі назви фільмів з парсингу
        titles = [item["title"] for item in uakino_short_items]

        # Запитуємо базу даних для перевірки наявності фільмів з такими ж назвами
        existing_movies = await Movie.find({"title": {"$in": titles}}).to_list(
            length=None
        )
        existing_titles = set(movie.title for movie in existing_movies)

        # Фільтруємо фільми, яких немає у базі даних
        new_movies = [
            item
            for item in uakino_short_items
            if item["title"] not in existing_titles
        ]

        # додаємо нові фільми до загального списку
        movies.extend(new_movies)

        page_count += 1

    # якщо фільмів більше 5, то обрізаємо список

    movies = movies[:5]

    for movie in movies:
        # отримуємо деталі фільму
        film_details = await get_film_details_from_uakino(movie["link"])

        # додаємо деталі до фільму
        movie["details"] = film_details

    return movies




async def get_film_details_from_uakino(film_url):
    # отримуємо сторінку з фільмом
    uakino_film_html_page = await ParseService.get_page_html(film_url)

    # парсимо сторінку
    film_details = uakino_parse_film_details(uakino_film_html_page)

    return film_details



