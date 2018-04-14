from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Article, Tag, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_post')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick_name', 'article')


# Register your models here.
# admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, MarkdownxModelAdmin)
