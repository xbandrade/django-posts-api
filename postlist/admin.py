from django.contrib import admin

from postlist.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'title', 'content', 'created_datetime',
                    'updated_datetime')
    list_filter = 'created_datetime', 'updated_datetime'
    list_display_links = 'id', 'title'
    search_fields = 'id', 'title', 'content'
    list_per_page = 10
    ordering = '-id',
