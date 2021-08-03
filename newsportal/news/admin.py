from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory
from modeltranslation.admin import TranslationAdmin


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating')
    list_display_links = ('id', 'user')
    ordering = ('id',)


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    inlines = (PostCategoryInline,)
    list_display = ('id', 'author', 'type_post', 'title', 'get_content', 'created_at', 'rating')
    list_display_links = ('id', 'title', 'get_content',)
    fields = ('author', 'type_post', 'title', 'content', 'rating')

    def get_content(self, obj):
        return ''.join((obj.content[:124], '...'))
    get_content.short_description = 'Текст'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_content', 'created_at', 'rating')
    list_display_links = ('id', 'get_content',)
    ordering = ('id', )

    def get_content(self, obj):
        return ''.join((obj.content[:64], '...'))
    get_content.short_description = 'Комментарий'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    model = Category

