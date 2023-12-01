from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Article, Comment, ViewCount


@admin.register(Category)
# Админ панель модели категории
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основная информация', {'fields': ('title', 'slug', 'parent')}),
        ('Описание', {'fields': ('description',)})
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
# Админ панель модели комментариев
class CommentAdminPage(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'time_create', 'status')
    mttp_levl_indent = 2
    list_display_links = ('article',)
    list_filter = ('time_create', 'time_update', 'author')
    list_editable = ('status',)


@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    list_display = ('article', 'viewed_on', 'ip_address')
    list_filter = ('viewed_on',)
    