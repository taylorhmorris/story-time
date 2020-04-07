from django.contrib import admin

from .models import Story, Language, Translation

admin.site.register(Story)
admin.site.register(Language)
admin.site.register(Translation)
