import asyncio
import re

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from settings import parser


async def run_parsing_news():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Перехват запросов
        def handle_request(request):
            if 'news_and_support_business' in request.url:  # Замените на нужное ключевое слово для запросов новостей
                print("Request intercepted:", request.url)

        page.on('route', handle_request)

        url = parser.url_news
        await page.goto(url)
        await page.wait_for_selector(".e-news__item")  # Ждем загрузки первой порции новостей

        SCROLL_PAUSE_TIME = parser.SCROLL_PAUSE_TIME
        MAX_SCROLLS = parser.MAX_SCROLLS
        scroll_count = parser.scroll_count
        last_height = await page.evaluate("document.body.scrollHeight")
        print(f"Initial page height: {last_height}")

        relevant_articles = []

        while scroll_count < MAX_SCROLLS:
            # Прокручиваем страницу постепенно, на 1000px
            await page.evaluate("window.scrollBy(0, 1000);")
            await page.wait_for_selector(".e-news__item", timeout=5000)  # Ждем появления новых новостей
            await asyncio.sleep(SCROLL_PAUSE_TIME)

            # Парсим контент
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            articles = soup.find_all("article", class_="e-news__item")

            if not articles:
                print("No new articles found.")
                break

            for article in articles:
                if len(relevant_articles) >= 8000:
                    break
                title_tag = article.find("header", class_="e-title")
                title = title_tag.get_text(strip=True) if title_tag else None
                link_tag = title_tag.find("a") if title_tag else None
                link = f"https://economy.gov.ru{link_tag['href']}" if link_tag else None
                date_tag = article.find("div", class_="e-date")
                date = date_tag.get_text(strip=True) if date_tag else "Дата не указана"
                if not any(news["link"] == link for news in relevant_articles):
                    relevant_articles.append({"title": title, "date": date, "link": link})

            # Получаем новую высоту страницы и проверяем прокрутку
            new_height = await page.evaluate("document.body.scrollHeight")
            print(f"New height: {new_height}")
            if new_height == last_height:
                print("End of page reached.")
                break
            last_height = new_height
            scroll_count += 1

        await browser.close()
        return relevant_articles
