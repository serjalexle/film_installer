from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
import time
import json
from gtts import gTTS
import os
import pygame

pygame.mixer.init()

options = webdriver.ChromeOptions()
options.debugger_address = "localhost:9223"

logger.info("Спроба підключитися до вже відкритого браузера...")
try:
    driver = webdriver.Chrome(options=options)

    # Перевірка
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")

    logger.info("Підключення успішне!")
    driver.execute_script("console.log('Привіт з Selenium!');")

    logger.info("Виконуємо скрипт...")

    current_time_ms = int(time.time() * 1000)

    gpt_query = {
        "prompt": "Видай розумну цитату, деталі що до формату можна глянути в полі answer_format",
        "time_ms": current_time_ms,
        "answer_format": {
            "time_ms": "сюди вставляєш час який я кинув у змінній time_ms",
            "citation": "сюди вставляєш цитату яку відповів GPT",
            "author": "сюди вставляєш автора цитати якщо є, якщо немає то пустий рядок",
            "key_word": "одне ключове слово цитати для пошуку картинки",
        },
    }

    driver.execute_script(
        f'const promptEl = document.getElementById("prompt-textarea"); console.log(promptEl); promptEl.innerHTML = "<p>{str(gpt_query)}</p>";'
    )

    # Очікування перед натисканням на кнопку, щоб контент встиг оновитися
    time.sleep(5)
    driver.execute_script(
        "document.querySelector('[data-testid=\"send-button\"]').click()"
    )

    time.sleep(25)

    # Дочекатися появи нових елементів 'article' на сторінці
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
    )
    time.sleep(5)

    # Отримуємо повний HTML після оновлення
    updated_html = driver.page_source

    # Парсимо останні 5 блоків з елементом 'article'
    soup2 = BeautifulSoup(updated_html, "html.parser")
    articles = soup2.find_all("article")[-1:]

    # Перетворення знайдених елементів у потрібний формат JSON
    parsed_articles = []
    for article in articles:
        try:
            time_ms = int(
                article.find("span", class_="hljs-attr", text='"time_ms"')
                .find_next_sibling("span", class_="hljs-number")
                .text
            )
            citation = (
                article.find("span", class_="hljs-attr", text='"citation"')
                .find_next_sibling("span", class_="hljs-string")
                .text.strip('"')
            )
            author = (
                article.find("span", class_="hljs-attr", text='"author"')
                .find_next_sibling("span", class_="hljs-string")
                .text.strip('"')
            )

            key_word = (
                article.find("span", class_="hljs-attr", text='"key_word"')
                .find_next_sibling("span", class_="hljs-string")
                .text.strip('"')
            )

            parsed_articles.append(
                {
                    "time_ms": time_ms,
                    "citation": citation,
                    "author": author,
                    "photo_search_url": f"https://www.pexels.com/uk-ua/search/{key_word}",
                }
            )
        except Exception as e:
            logger.error(f"Помилка при парсингу статті: {e}")

    # Запис у файл результату
    with open("parsed_articles.json", "w") as file:
        for article in parsed_articles:
            file.write(json.dumps(article, ensure_ascii=False) + "\n")

    logger.info("Скрипт виконано успішно!")

except Exception as e:
    logger.error(f"Помилка при підключенні до браузера: {e}")
