import os
import csv
import json
import subprocess
from load_django import *
from parser_app.models import Lawyer

OUTPUT_DIR = 'results'

def export_data():
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    lawyers = Lawyer.objects.all()
    count = lawyers.count()
    
    if count == 0:
        print("В базе данных нет данных для экспорта. Запустите скрипты 1 и 2.")
        return
        
    print(f"Найдено {count} записей для экспорта.")

    
    fieldnames = [field.name for field in Lawyer._meta.get_fields() if not field.is_relation]
    

    csv_path = os.path.join(OUTPUT_DIR, 'lawyers.csv')
    print(f"Экспорт в CSV: {csv_path}")
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        
        lawyers_data = list(lawyers.values(*fieldnames))
        writer.writerows(lawyers_data)
        
    print("Экспорт в CSV завершен.")
   
  
    json_path = os.path.join(OUTPUT_DIR, 'lawyers.json')
    print(f"Экспорт в JSON: {json_path}")

 
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(lawyers_data, jsonfile, ensure_ascii=False, indent=4)
        
    print("Экспорт в JSON завершен.")


def dump_database():
    """Создает полный дамп базы данных приложения parser_app."""
    dump_path = os.path.join(OUTPUT_DIR, 'database_dump.json')
    print(f"\nСоздание дампа базы данных: {dump_path}")
   
  
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'UTF-8'
    
   
    command = f"python manage.py dumpdata parser_app --indent 4 --output {dump_path}"
    
  
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', env=env)

    if result.returncode == 0:
        print("Дамп базы данных успешно создан.")
    else:
        print("Произошла ошибка при создании дампа базы данных.")
        print("  Код возврата:", result.returncode)
        print("  Stdout:", result.stdout)
        print("  Stderr:", result.stderr)


if __name__ == "__main__":
    export_data()
    dump_database()
    print("\nВсе операции по выгрузке завершены.")