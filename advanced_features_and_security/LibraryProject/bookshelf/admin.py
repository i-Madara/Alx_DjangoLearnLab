from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # show these columns in list view
    search_fields = ('title', 'author')                     # search by title/author
    list_filter = ('publication_year',)                     # filter by year
