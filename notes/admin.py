# admin.py
from django.contrib import admin
from .models import TastingNote, WineCountry

@admin.register(TastingNote)
class TastingNoteAdmin(admin.ModelAdmin):
    list_display = ('wine_name', 'tasting_date', 'is_public')
    list_filter = ('is_public', 'tasting_date')
    search_fields = ('wine_name', 'winery', 'tasting_place')

@admin.register(WineCountry)
class WineCountryAdmin(admin.ModelAdmin):
    list_display = ('name_kr', 'name', 'is_common')
    list_filter = ('is_common',)
    search_fields = ('name', 'name_kr')
    ordering = ('-is_common', 'name_kr')