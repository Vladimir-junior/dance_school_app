from django.contrib import admin
from posts.models import PostModel


class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'date')
    search_fields = ('title',)


admin.site.register(PostModel, PostModelAdmin)
