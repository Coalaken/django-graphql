from django.contrib import admin

from .models import Deck


@admin.register(Deck)
class AdminDeck(admin.ModelAdmin):
    list_display = ("title", "description", "last_reviewed")