"""
Скрипт для сбора ссылок на профили адвокатов с сайта barreaulyon.com
и сохранения их в базу данных в качестве новых записей для последующей обработки.
"""
import requests
import time
from bs4 import BeautifulSoup as BS
from load_django import *
from parser_app.models import Lawyer


BASE_URL = "https://www.barreaulyon.com/annuaire/?paged={page}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

TOTAL_LIMIT = 50
LAST_PAGE = 336 #лимит

def parse_all_pages():
    print("Начинаю сбор ссылок и создание записей адвокатов")
    
    collected_count = 0

    for page in range(1, LAST_PAGE + 1):
        if collected_count >= TOTAL_LIMIT:
            print(f"Достигнут установленный лимит в {TOTAL_LIMIT} новых записей. Остановка.")
            break

        url = BASE_URL.format(page=page)
        print(f"Парсинг страницы: {page} | URL: {url}")

        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                print(f"Ошибка: статус {response.status_code}. Пропускаю страницу.")
                continue

            soup = BS(response.text, 'html.parser')
            cards = soup.find_all('article', class_='card-annuaire')

            if not cards:
                print("Не найдено карточек на странице. Возможно, это конец. Остановка.")
                break

            for card in cards:
                if collected_count >= TOTAL_LIMIT:
                    break
                    
                entry_title_tag = card.find('p', class_='entry-title')
                link_tag = card.find('a', class_='entry-link')

                if not entry_title_tag or not link_tag or not link_tag.has_attr('href'):
                    continue

                name = entry_title_tag.text.strip()
                profile_url = link_tag['href']

                if not profile_url:
                    continue

                obj, created = Lawyer.objects.get_or_create(
                    link=profile_url,
                    defaults={'name': name, 'status': 'New'}
                )

                if created:
                    collected_count += 1
                    print(f"Добавлен ({collected_count}/{TOTAL_LIMIT}): {name}")
            
            time.sleep(1)

        except requests.RequestException as e:
            print(f"Критическая ошибка сети на странице {page}: {e}")
            time.sleep(10)
            continue

    total_in_db = Lawyer.objects.count()
    print(f"\nСбор ссылок завершен. Всего в базе: {total_in_db}. Добавлено новых: {collected_count}.")

if __name__ == "__main__":
    parse_all_pages()