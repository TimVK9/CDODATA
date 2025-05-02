from django.apps import AppConfig
from django.core.signals import setting_changed


class DataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data'
    
    def ready(self):
        import data.signals  # Регистрация сигналов


