from django.contrib import admin
from .models import SearchKeyword

@admin.register(SearchKeyword)
class SearchKeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'mapped_term')
    search_fields = ('keyword', 'mapped_term')
    help_text = "Manage synonyms for search (e.g., 'heart attack' -> 'Cardiology')"
