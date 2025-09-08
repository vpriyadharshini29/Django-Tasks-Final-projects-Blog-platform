from django.contrib import admin
from .models import Post, Comment, Category, Tag, Subscriber, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("author", "categories", "tags", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("text",)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Subscriber)
admin.site.register(Profile)
