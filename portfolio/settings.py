import os
from decouple import config
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-o11o_2&ydq*@w0v=c(f0_&n&+tyq0$%z#71e91nu8j#_8q$cbu')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.railway.app', 
    '.up.railway.app',
    'web-production-d54c7.up.railway.app',
    '*'
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-d54c7.up.railway.app',
    'https://*.railway.app',
    'https://*.up.railway.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'portfolio.wsgi.application'

# Database Configuration - Multiple fallback options for Railway
# Priority: DATABASE_PUBLIC_URL > Individual PG variables > DATABASE_URL > SQLite

# Try DATABASE_PUBLIC_URL first (best for Railway external connections)
database_public_url = config('DATABASE_PUBLIC_URL', default=None)
if database_public_url:
    DATABASES = {
        'default': dj_database_url.parse(database_public_url)
    }
# Try individual PostgreSQL variables
elif config('PGHOST', default=None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('PGDATABASE', default='railway'),
            'USER': config('PGUSER', default='postgres'),
            'PASSWORD': config('PGPASSWORD', default=''),
            'HOST': config('PGHOST', default='localhost'),
            'PORT': config('PGPORT', default='5432'),
        }
    }
# Fallback to DATABASE_URL (might have internal hostname issue)
else:
    DATABASES = {
        'default': dj_database_url.parse(
            config('DATABASE_URL', default='sqlite:///db.sqlite3')
        )
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Create static directory if it doesn't exist
STATICFILES_DIRS = []
static_dir = BASE_DIR / 'static'
if static_dir.exists():
    STATICFILES_DIRS.append(static_dir)

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Session configuration
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

# CSRF configuration
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False

# Production settings for Railway
if os.environ.get('RAILWAY_ENVIRONMENT'):
    DEBUG = False
    
    # Admin-specific settings for Railway
    LOGIN_URL = '/admin/login/'
    LOGIN_REDIRECT_URL = '/admin/'
    LOGOUT_REDIRECT_URL = '/admin/login/'
    
    # Less restrictive security for admin to work
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_SSL_REDIRECT = False
    
    # Static files configuration for Railway
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    
    # Force session settings for admin
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = '/'
    
    # Ensure admin static files are served
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

# Debug database configuration (only in development)
if DEBUG and config('DATABASE_URL', default='').startswith('postgresql'):
    print(f"Database Engine: {DATABASES['default']['ENGINE']}")
    print(f"Database Name: {DATABASES['default']['NAME']}")
    print(f"Database Host: {DATABASES['default']['HOST']}")
    print(f"Database Port: {DATABASES['default']['PORT']}")