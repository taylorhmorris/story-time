from django.contrib import admin

from .models import Note, SearchResult, Card, CardType

# Register your models here.
admin.site.register(Note)
admin.site.register(SearchResult)
admin.site.register(Card)
admin.site.register(CardType)
