from django.contrib import admin

from .models import Card


@admin.register(Card)
class AdminCard(admin.ModelAdmin):
    list_display = ("deck", "question", "bucket")
