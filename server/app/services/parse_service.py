



import time
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class ParseService:
    @staticmethod
    async def get_page_html(url: str) -> str:
        try:
            # Запуск браузера Chrome
            options = webdriver.ChromeOptions()
            service = Service("/usr/local/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=options)

            # Перехід на вказану сторінку
            driver.get(url)
            driver.implicitly_wait(30)

            # Отримання повного HTML-коду сторінки
            page_html = driver.page_source

            if page_html:
                logger.info("HTML-код сторінки успішно отримано")
            else:
                logger.error("HTML-код сторінки не отримано")
                print(f"HTML-код {page_html}")

            return page_html

        except Exception as e:
            logger.error(f"Помилка при отриманні HTML-коду сторінки: {e}")
        finally:
            # Додайте невелику затримку перед закриттям браузера
            time.sleep(2)
            driver.quit()

    






















