# Barreau Lyon Scraper

[English version below / Версия на английском ниже]

---

# 🇷🇺 Barreau Lyon Scraper (Russian)

Это Django-проект для автоматизированного сбора (парсинга) данных об адвокатах с сайта **barreaulyon.com**. Скрипт собирает контактные данные, специализации, адреса и другую информацию в базу данных PostgreSQL, с возможностью экспорта в CSV и JSON.

## Функциональность

1.  **Сбор ссылок**: Проход по страницам каталога и сохранение ссылок на профили.
2.  **Сбор деталей**: Посещение каждого профиля и извлечение детальной информации (Телефон, Email, Факс, Дата присяги, Специализация и т.д.).
3.  **Экспорт**: Выгрузка данных в удобные форматы (CSV, JSON).
4.  **Админка Django**: Просмотр и управление собранными данными через веб-интерфейс.

## Предварительные требования

*   Python 3.8+
*   PostgreSQL
*   Google Chrome (для корректной работы User-Agent, хотя Selenium не используется, только requests)

## Установка

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <ваша-ссылка-на-репозиторий>
    cd <папка-проекта>
    ```

2.  **Создайте виртуальное окружение и активируйте его:**
    ```bash
    python -m venv venv
    # Для Windows:
    venv\Scripts\activate
    # Для Linux/macOS:
    source venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install django psycopg2-binary requests beautifulsoup4
    ```

4.  **Настройка базы данных:**
    В файле `barreaulyon_project/settings.py` прописаны следующие настройки БД:
    *   Имя БД: `barreaulyon_db`
    *   Пользователь: `barreaulyon`
    *   Пароль: `111`
    
    Вам необходимо создать соответствующую базу и пользователя в PostgreSQL или изменить настройки в `settings.py` на свои.

    ```sql
    CREATE DATABASE barreaulyon_db;
    CREATE USER barreaulyon WITH PASSWORD '111';
    GRANT ALL PRIVILEGES ON DATABASE barreaulyon_db TO barreaulyon;
    -- Для Postgres 15+ также может потребоваться:
    GRANT ALL ON SCHEMA public TO barreaulyon;
    ```

5.  **Примените миграции:**
    ```bash
    python manage.py migrate
    ```

6.  **Создайте суперпользователя (для доступа в админку):**
    ```bash
    python manage.py createsuperuser
    ```

## Использование

Скрипты запускаются по очереди:

### 1. Сбор ссылок
Скрипт проходит по страницам пагинации и сохраняет базовую информацию.
```bash
python 1_get_links.py
```
*Примечание: В коде установлен лимит `TOTAL_LIMIT = 50`. Измените это значение в файле, если нужно собрать всех адвокатов.*

### 2. Сбор профилей
Скрипт берет записи со статусом `New` из базы и парсит детальную страницу.
```bash
python 2_get_profiles.py
```
*Примечание: Скрипт обрабатывает по 50 записей за запуск (`PROCESS_LIMIT`). Запускайте повторно или увеличьте лимит.*

### 3. Экспорт данных
Создает папку `results` и выгружает данные.
```bash
python 3_export_data.py
```
Результаты будут в:
*   `results/lawyers.csv`
*   `results/lawyers.json`
*   `results/database_dump.json`

### Дополнительно
*   **Сброс статусов**: Если нужно перепарсить данные, используйте `python reset_statuses.py`.
*   **Админка**: Запустите сервер `python manage.py runserver` и перейдите на `http://127.0.0.1:8000/admin/`.

---

# 🇬🇧 Barreau Lyon Scraper (English)

This is a Django-based project designed to scrape lawyer data from the **barreaulyon.com** directory. It collects contact details, specializations, addresses, and other metadata into a PostgreSQL database, featuring export capabilities to CSV and JSON.

## Features

1.  **Link Scraping**: Crawls directory pages to collect lawyer profiles.
2.  **Profile Scraping**: Visits individual profile URLs to extract detailed info (Phone, Email, Fax, Oath Date, Specialization, etc.).
3.  **Export**: Exports data to standard formats (CSV, JSON).
4.  **Django Admin**: View and manage collected data via a web interface.

## Prerequisites

*   Python 3.8+
*   PostgreSQL
*   Basic knowledge of terminal/command line

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-link>
    cd <project-folder>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # For Windows:
    venv\Scripts\activate
    # For Linux/macOS:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django psycopg2-binary requests beautifulsoup4
    ```

4.  **Database Setup:**
    The `barreaulyon_project/settings.py` file expects the following credentials:
    *   DB Name: `barreaulyon_db`
    *   User: `barreaulyon`
    *   Password: `111`
    
    You need to create this database/user in PostgreSQL or update `settings.py` with your own credentials.

    ```sql
    CREATE DATABASE barreaulyon_db;
    CREATE USER barreaulyon WITH PASSWORD '111';
    GRANT ALL PRIVILEGES ON DATABASE barreaulyon_db TO barreaulyon;
    ```

5.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (to access Django Admin):**
    ```bash
    python manage.py createsuperuser
    ```

## Usage

Run the scripts in the following order:

### 1. Get Links
Crawls pagination pages and saves basic lawyer entries.
```bash
python 1_get_links.py
```
*Note: `TOTAL_LIMIT` is set to 50 in the code. Change this value in the file to scrape more records.*

### 2. Get Profiles
Fetches records with status `New` from the database and scrapes the detail page.
```bash
python 2_get_profiles.py
```
*Note: The script processes 50 records per run (`PROCESS_LIMIT`). Run it multiple times or increase the limit.*

### 3. Export Data
Creates a `results` directory and exports the data.
```bash
python 3_export_data.py
```
Outputs:
*   `results/lawyers.csv`
*   `results/lawyers.json`
*   `results/database_dump.json`

### Extras
*   **Reset Statuses**: Use `python reset_statuses.py` if you need to re-scrape processed items.
*   **Admin Panel**: Run `python manage.py runserver` and go to `http://127.0.0.1:8000/admin/`.
