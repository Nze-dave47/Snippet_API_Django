from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'language', 'is_private')
    list_filter = ('language', 'is_private')
    search_fields = ('title', 'content', 'owner__username')
    raw_id_fields = ('owner',)
