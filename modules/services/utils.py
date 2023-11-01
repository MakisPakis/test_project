import os
from uuid import uuid4
from pytils.translit import slugify
from base import settings
from urllib.parse import urljoin
from datetime import datetime
from django.core.files.storage import FileSystemStorage


#  Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{unique_slug}-{uuid4().hex[:8]}"
    return unique_slug


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip


class CkeditorCustomStorage(FileSystemStorage):
    # Изменение места хранения файлов у Ckeditor
    def get_folder_name(self):
        return datetime.now().strftime('%y/%m/%d')

    def get_valid_name(self, name):
        return name

    def _save(self, name, content):
        folder_name = self.get_folder_name()
        name = os.path.join(folder_name, self.get_valid_name(name))
        return super()._save(name, content)

    location = os.path.join(settings.MEDIA_ROOT, 'uploads/')
    base_url = urljoin(settings.MEDIA_URL, 'uploads/')
