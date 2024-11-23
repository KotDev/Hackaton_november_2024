import asyncio
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def extract_data_from_page(driver, wait, pattern, base_url):
    data = []
    try:
        cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rs-card")))
        for card in cards:
            try:
                content = card.find_element(By.CLASS_NAME, "rs-card__content-cont").text
                match = pattern.search(content)
                if match:
                    # Извлечение полей из текста
                    name = match.group("name").strip()
                    date_start = datetime.strptime(match.group("date_start"), "%d.%m.%Y")
                    date_end = datetime.strptime(match.group("date_end"), "%d.%m.%Y")
                    data.append({
                        "name": name,
                        "date_start": date_start,
                        "date_end": date_end,
                        "link": base_url
                    })
            except Exception as e:
                print("Ошибка извлечения блока:", e)
    except Exception as e:
        print("Ошибка извлечения данных с текущей страницы:", e)
    return data


async def run_parsing_support_business():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Создаем веб-драйвер
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 5)
    all_data = []
    page = 1

    # Регулярка для извлечения данных из текста карточки
    pattern = re.compile(
        r"^(?P<name>.+?)\s+Период приема заявок с\s+(?P<date_start>\d{2}\.\d{2}\.\d{4})\s+по\s+(?P<date_end>\d{2}\.\d{2}\.\d{4})$",
        re.DOTALL
    )

    with ThreadPoolExecutor(max_workers=5) as executor:
        loop = asyncio.get_event_loop()

        while True:
            base_url = f"https://xn--l1agf.xn--p1ai/services/support/filter/?paginationPage={page}"
            driver.get(base_url)

            # Асинхронное извлечение данных
            page_data = await loop.run_in_executor(executor, extract_data_from_page, driver, wait, pattern, base_url)

            if not page_data or page == 50:
                break
            all_data.extend(page_data)
            page += 1
            await asyncio.sleep(2)

    driver.quit()
    return all_data