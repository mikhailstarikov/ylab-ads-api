from django.contrib import admin
from .models import Author, Ad


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "status", "author", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["created_at", "updated_at"]
