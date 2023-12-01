from datetime import datetime, date, time, timedelta
from django.utils import timezone
from django import template
from django.db.models import Count, Q
from taggit.models import Tag

from ..models import Comment, Article

register = template.Library()

# Вывод тегов, с сортировкой по кол-ву статей, которые используют этот тег
@register.simple_tag
def popular_tags():
    tags = Tag.objects.annotate(num_times=Count('article')).order_by('-num_times')
    tag_list = list(tags.values('name', 'num_times', 'slug'))
    return tag_list

# Вывод 5 последних комментариев
@register.inclusion_tag('includes/latest_comments.html')
def show_latest_comments(count=5):
    comments = Comment.objects.select_related('author').filter(status='published').order_by('-time_create')[:count]
    return {'comments': comments}


# Вывод популярных статей по просмотрам
@register.simple_tag
def popular_articles():
    now_time = timezone.now()
    # вычисляем дату начала дня (00:00) 7 дней назад
    start_date = now_time - timedelta(days=7)
    # вычисляем дату начала текущего дня (00:00)
    today_start = timezone.make_aware(datetime.combine(date.today(), time.min))
    # Получаем все статьи и количество их просмотров за последние 7 дней
    articles = Article.objects.annotate(
        total_view_count=Count('views', filter=Q(views__viewed_on__gte=start_date)),
        today_view_count=Count('views', filter=Q(views__viewed_on__gte=today_start))
    ).prefetch_related('views')
    # Cортируем статьи по кол-ву просмотров
    popular_articles_list = articles.order_by('-total_view_count', '-today_view_count')[:10]
    return popular_articles_list
