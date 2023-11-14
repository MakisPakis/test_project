from .models import ViewCount
from modules.services.utils import get_client_ip



class ViewCountMixin:

    def get_object(self):
        # Получение статьи из метода родительского класса
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        # Получаем или создаем запись о просмотре статьи для данного пользователя
        ViewCount.objects.get_or_create(article=obj, ip_address=ip_address)
        return obj
