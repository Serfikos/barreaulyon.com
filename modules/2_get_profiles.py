"""
Скрипт для сбора детальной информации о каждом адвокате
путем загрузки его личной страницы по URL и обновления записи в базе данных.
"""
import requests
import time
from bs4 import BeautifulSoup as BS
from load_django import *
from django.db.models import Q
from parser_app.models import Lawyer

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}
PROCESS_LIMIT = 50  

def get_field_value_by_b_tag(soup, header_text):
   
    b_tag = soup.find('b', string=lambda text: text and header_text.strip() in text.strip())
    if not b_tag:
        return None
    
    values = []
    for sibling in b_tag.find_next_siblings():
        if sibling.name == 'b':
            break
        if sibling.name == 'p':
            cleaned_text = ' '.join(sibling.text.split())
            if cleaned_text:
                values.append(cleaned_text)
                
    return ', '.join(values) if values else None

def get_footer_section_text(soup, header_text_options):
    """
    Извлекает текст из разделов в футере по одному из возможных заголовков.
    """
    for header_text in header_text_options:
        header_p_tag = soup.find('p', string=lambda t: t and t.strip() == header_text)
        if header_p_tag:
            container_div = header_p_tag.find_parent('div', class_='entry-footer__item')
            if not container_div:
                continue
            
            all_data_p = container_div.find_all('p', recursive=False)
            if not all_data_p:
                continue
            
            return '\n'.join([p.text.strip() for p in all_data_p])
    return None

def parse_lawyer_profile(html_content):
    """Разбирает HTML-код страницы профиля и возвращает словарь с данными."""
    try:
        soup = BS(html_content, 'html.parser')
        profile = {}

  
        info_block = soup.select_one('article.single-page')
        if not info_block:
         
            return None

        profile['name'] = info_block.find('h1').text.strip() if info_block.find('h1') else None
        profile['full_name_title'] = info_block.find('h2').text.strip() if info_block.find('h2') else None
        
        
        tel_tag = info_block.select_one(".entry-infos__item--tel a")
        profile['phone'] = tel_tag.get('href').replace('tel:', '').strip() if tel_tag else None
        
        mail_tag = info_block.select_one(".entry-infos__item--mail a")
        profile['email'] = mail_tag.get('href').replace('mailto:', '').strip() if mail_tag else None
        
        
        contact_info_div = info_block.select_one('div.entry-infos')
        if contact_info_div:
           
            fax_link_tag = None
            print_icon = contact_info_div.select_one("i.icon-print")
            if print_icon and (container := print_icon.find_parent('div', class_='entry-infos__item')):
                fax_link_tag = container.find('a')
            profile['fax'] = fax_link_tag.get('href').replace('tel:', '').strip() if fax_link_tag else None

            # сайт по иконке 
            website_link_tag = None
            pin_icon = contact_info_div.select_one("i.icon-pin")
            if pin_icon and (container := pin_icon.find_parent('div', class_='entry-infos__item')):
                website_link_tag = container.find('a')
            profile['website'] = website_link_tag.get('href').strip() if website_link_tag else None
       
        
        
        content_block = info_block.select_one('div.entry-content')
        if content_block:
            street = get_field_value_by_b_tag(content_block, 'Rue')
            postal_info = get_field_value_by_b_tag(content_block, 'Code postal')
            address_parts = [part for part in [street, postal_info] if part]
            profile['address'] = ', '.join(address_parts)
            profile['structure'] = get_field_value_by_b_tag(content_block, 'Structure')
            profile['case_number'] = get_field_value_by_b_tag(content_block, 'Case')
            profile['oath_date'] = get_field_value_by_b_tag(content_block, 'Prestation de serment')
            profile['languages'] = get_field_value_by_b_tag(content_block, 'Langues')

        # Специализации
        footer_block = info_block.select_one('div.entry-footer')
        if footer_block:
            profile['specializations'] = get_footer_section_text(footer_block, ['Spécialisation'])
            profile['activity_areas'] = get_footer_section_text(footer_block, ['Activités Dominantes', "Domaines d'activité"])
        
        return {k: v for k, v in profile.items() if v}
    
    except Exception as e:
        print(f"  - Критическая ошибка при разборе HTML: {e}")
        return None

def main():
    
    lawyers_to_process = Lawyer.objects.filter(status='New').order_by('id')[:PROCESS_LIMIT]
    
    if not lawyers_to_process.exists():
        print("Новых записей для обработки нет. Проверяю записи с ошибками...")
        query = Q(status__startswith='Error') | Q(status='Error: Parse failed')
        lawyers_to_process = Lawyer.objects.filter(query).order_by('id')[:PROCESS_LIMIT]
        if not lawyers_to_process.exists():
            print("Записей для обработки не найдено. Запустите '1_get_links.py' или 'reset_statuses.py'.")
            return

    total_count = lawyers_to_process.count()
    print(f"Найдено {total_count} записей для обработки.")

    for i, lawyer in enumerate(lawyers_to_process, 1):
        print(f"[{i}/{total_count}] Парсинг: {lawyer.name} ({lawyer.link})")
        
        try:
            response = requests.get(lawyer.link, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                print(f"  [!] Ошибка статуса {response.status_code}. Пропускаю.")
                lawyer.status = f"Error: {response.status_code}"
                lawyer.save()
                continue

            profile_data = parse_lawyer_profile(response.text)
            
            if profile_data:
                for key, value in profile_data.items():
                    setattr(lawyer, key, value)
                
                lawyer.status = 'Done'
                lawyer.save()
                print(f"  [OK] Сохранено: {lawyer.name}")
            else:
                print(f"  [!] Не удалось разобрать данные: {lawyer.name}")
                lawyer.status = 'Error: Parse failed'
                lawyer.save()

        except requests.RequestException as e:
            print(f"  [!] Критическая ошибка сети для {lawyer.link}: {e}")
            lawyer.status = 'Error: Network'
            lawyer.save()
        
        time.sleep(1)

    print("\nОбработка профилей завершена.")

if __name__ == "__main__":
    main()