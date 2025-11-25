from load_django import *
from django.db.models import Q
from parser_app.models import Lawyer

def reset_all_statuses():
   
    print("Сбрасываю статусы у всех обработанных и ошибочных записей...")

   
    query = Q(status='Done') | Q(status__startswith='Error')

    updated_count = Lawyer.objects.filter(query).update(status='New')

    print(f"Готово! Статус 'New' установлен для {updated_count} записей.")
    if updated_count > 0:
        print("Теперь можно запускать '2_get_profiles.py' заново.")
    else:
        print("Не найдено записей, требующих сброса статуса.")


if __name__ == "__main__":
    reset_all_statuses()