from pathlib import Path
import os
from dotenv import load_dotenv  # Добавляем поддержку .env

# Загрузка переменных окружения
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')  # Должен быть в .env
DEBUG = False  # В продакшне всегда False!
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'yourdomain.com,localhost').split(',')

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'datacdo'),
        'USER': os.getenv('DB_USER', 'gnom'),
        'PASSWORD': os.getenv('DB_PASSWORD', '(!Akc74yakc74Y#)'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 5,
            'sslmode': 'require' if os.getenv('DB_SSL', 'False') == 'True' else None
        },
    }
}

# Настройки статики и медиа
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Для collectstatic
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Безопасность cookies и сессий
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True  # Если есть SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Дополнительные настройки
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')

# Оптимизации
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB для импорта
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760