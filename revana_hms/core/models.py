from django.db import models

# Create your models here.

class SearchKeyword(models.Model):
    keyword = models.CharField(max_length=100, help_text="The term the user searches for (e.g., 'heart pain')")
    mapped_term = models.CharField(max_length=100, help_text="The medical term to map to (e.g., 'Cardiology')")
    
    def __str__(self):
        return f"{self.keyword} -> {self.mapped_term}"
