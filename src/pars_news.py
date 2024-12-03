import asyncio
import re

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from settings import parser


async def run_parsing_news():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = parser.url_news
        await page.goto(url)
        await page.wait_for_selector(".e-news__item", timeout=10000)  # Убедитесь, что новости загрузились

        # Прокрутите наверх страницы
        await page.evaluate("window.scrollTo(0, 0);")
        await asyncio.sleep(3)  # Дайте время на полную загрузку контента

        content = await page.content()

        soup = BeautifulSoup(content, "html.parser")
        articles = soup.find_all("article", class_="e-news__item")

        relevant_articles = []
        for article in articles:
            title_tag = article.find("header", class_="e-title")
            title = title_tag.get_text(strip=True) if title_tag else "Без названия"
            link_tag = title_tag.find("a") if title_tag else None
            link = f"https://economy.gov.ru{link_tag['href']}" if link_tag else None
            date_tag = article.find("div", class_="e-date")
            date = date_tag.get_text(strip=True) if date_tag else "Дата не указана"

            if not any(news["link"] == link for news in relevant_articles):
                relevant_articles.append({"title": title, "date": date, "link": link})
                print(f"Added news: {title}, {date}, {link}")
            else:
                print(f"Duplicate news: {link}")

        await browser.close()
        return relevant_articles

