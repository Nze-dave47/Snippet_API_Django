from django.contrib import admin

from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'language', 'is_private')
    list_filter = ('language', 'is_private')
    search_fields = ('title', 'content', 'owner__username')
    raw_id_fields = ('owner',)
