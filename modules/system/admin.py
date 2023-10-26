from django.contrib import admin
from .models import Profile, Feedback


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Админ анель модели профиля
    list_display = ('user', 'birth_day', 'slug')
    list_display_links = ('user', 'slug')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip_adress', 'user')
    list_display_links = ('email', 'ip_adress')