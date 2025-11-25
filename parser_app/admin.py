# parser_app/admin.py

from django.contrib import admin
from .models import Lawyer

@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'phone', 'email', 'structure')
    list_filter = ('status',)
    search_fields = ('name', 'address', 'specializations', 'activity_areas', 'link')
    readonly_fields = ('link', 'name') 