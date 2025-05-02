from pathlib import Path
import os
from dotenv import load_dotenv  # Добавляем поддержку .env

# Загрузка переменных окружения
load_dotenv()
BASE_URL = 'http://89.189.186.231'

BASE_DIR = Path(__file__).resolve().parent.parent


# Перенаправление после входа/выхода
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Для @login_required
LOGIN_URL = 'login'


# Безопасность
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')  
DEBUG = True  
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'yourdomain.com,localhost').split(',')

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'datacdo',
        'USER': 'tim',  # либо $(whoami), либо 'postgres'
        'PASSWORD': '',  # если пароль не нужен
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    'data',
    'django_filters',
    'corsheaders',
    'import_export',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Должно быть перед AuthenticationMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Для админки
    'django.contrib.messages.middleware.MessageMiddleware',  # Для админки
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Для collectstatic
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
ROOT_URLCONF = 'inventory.urls'  # Убедитесь, что имя проекта правильное

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

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


# Оптимизации
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB для импорта
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760