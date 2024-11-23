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
            if 'ml' in request.url:  # Замените на нужное ключевое слово для запросов новостей
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

        keywords_pattern = re.compile(
            r"""
            \b(                                 # Граница слова
            (                               # Первая группа: бизнес, предпринимательство
            бизнес|бизн|предприниматель|предпринимател|стартап|микробизнес|фирм|компан|организаци|
            корпорац|производств|индустри|экономик|проект|сектор|продукт|прибыл|доход|услуг|товар|
            рынк|платформа|инновац|производител|маркет|стартов|кредитор|коммерциализ|развити|капитал
            )[а-яё]* |                      # Продолжение слова

        (                               # Вторая группа: поддержка, льготы, субсидии, гранты
            поддержк|субсиди|грант|дотаци|льгот|помощ|содейств|пособ|кредит|выгод|возмещен|снижен|
            ставк|каникул|финанс|софинансир|пособи|пошлин|налог|платеж|возврат|инвест|вклад|гарант|
            компенсац|выплат|стимул|сэконом|пожертв|награда|инвестици|проект|контракт|программа|
            платежи|мера|пошлины|государств|финансировани|государственн|федеральн|региональн
        )[а-яё]* |

        (                               # Третья группа: меры поддержки, программы
            государственн|федеральн|региональн|национальн|муниципальн|инновац|развит|помощ|програм[а-яё]*|
            инициатив|мера|реформа|стратег|предпринимател|экономическ|микробизнес|мал[а-яё]* бизнес|
            средн[а-яё]* бизнес|крупн[а-яё]* бизнес|финансировани[а-яё]* для бизнеса|государств|
            программ[а-яё]* помощи|поддержк[а-яё]*|налогов[а-яё]* каникулы|меры поддержки|субсидии для бизнеса|
            инвестиционные программы|государственное финансирование|помощь малому и среднему бизнесу|
            финансовая помощь предпринимателям|снижение налогов|финансирование стартапов|
            государственные меры поддержки|программы для предпринимателей|программы стимулирования
        )[а-яё]*
    )\b                                 # Граница слова
    """,
            re.IGNORECASE | re.VERBOSE           # Флаг VERBOSE для добавления комментариев
        )


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
                if title and re.search(keywords_pattern, title):
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
