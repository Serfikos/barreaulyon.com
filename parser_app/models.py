# parser_app/models.py

from django.db import models

class Lawyer(models.Model):
  
    name = models.CharField(max_length=255, help_text="Имя, полученное со страницы списка")
    link = models.URLField(unique=True, help_text="Ссылка на профиль на barreaulyon.com")
    status = models.CharField(max_length=20, default='New', help_text="Статус обработки записи")

   
    full_name_title = models.CharField(max_length=255, blank=True, null=True, help_text="Maître ...")
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    structure = models.CharField(max_length=255, blank=True, null=True, help_text="Название структуры или кабинета")
    address = models.TextField(blank=True, null=True)
    case_number = models.CharField(max_length=100, blank=True, null=True, help_text="Case")
    oath_date = models.CharField(max_length=100, blank=True, null=True, help_text="Дата присяги")
    languages = models.TextField(blank=True, null=True)
    specializations = models.TextField(blank=True, null=True, help_text="Упомянутые специализации")
    activity_areas = models.TextField(blank=True, null=True, help_text="Сферы деятельности")

    def __str__(self):
        return self.name if self.name else 'N/A'