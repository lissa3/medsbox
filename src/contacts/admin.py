from django.contrib import admin

from .models import NewsLetter


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    """
    after sending letter status as well as
    related posts status should be changd
    """

    list_display_links = ["title"]
    date_hierarchy = "added_at"
    search_fields = ("title", "letter_status")

    list_display = ["id", "title", "letter_status"]

    list_filter = ["added_at", "letter_status"]
    save_on_top = True
    list_per_page = 15
