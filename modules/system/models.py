from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache

from modules.services.utils import unique_slugify

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='url', max_length=255, blank=True, unique=True)
    following = models.ManyToManyField('self', verbose_name='Подписки', related_name='followers', symmetrical=False, blank=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))],
        default='images/avatars/default.jpg',
        )
    bio = models.TextField(verbose_name='Информация о себе', max_length=500, blank=True)
    birth_day = models.DateField(verbose_name='Дата рождения', null=True, blank=True)

    # @property
    # def get_avatar(self):
    #     if self.avatar:
    #         return self.avatar.url
    #     return f"https://ui-avatars.com/api/?size=150&background=random&name={self.slug}"

    class Meta:
        # Сортировка, название таблицы в БД
        db_table = 'app_profile'
        ordering = ('user',)
        verbose_name = 'Профиль',
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        # Сохранение полей модели, если они не заполнены
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Ссылка на профиль
        return reverse('profile_detail', kwargs={'slug': self.slug})

    def is_online(self):
        last_seen = cache.get(f"last-seen-{self.user.id}")
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True
        return False

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Feedback(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    email = models.EmailField(max_length=255, verbose_name='Электронный адрес')
    content = models.TextField(verbose_name='Содержимое')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_adress = models.GenericIPAddressField(verbose_name='IP Отправителя', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'app_feedback'
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']

    def __str__(self):
        return f"Вам письмо от: {self.email}"
