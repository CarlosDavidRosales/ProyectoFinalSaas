"""
Django settings for GestorClinicas project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = './static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'GestorClinicas/static'),
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7!o12vl)tt-+be+2&6@(!whm&s0d6jmah4ei@&b)lijlym%0(e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_DOMAIN = '.localtest.me'
SESSION_COOKIE_SECURE = False  # Importante si no usas HTTPS
SESSION_COOKIE_SAMESITE = 'None' if SESSION_COOKIE_SECURE else 'Lax'
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django_tenants',  # Necesario para django-tenants
    # Aplicaciones compartidas
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Tenants',  # Tu aplicación de Tenants
    'UsersTenants',  # Tu aplicación de UserTenants
    # Otras aplicaciones compartidas
]

TENANT_APPS = [
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    'UsersTenants',  # Aplicaciones específicas para cada tenant
    # Otras aplicaciones específicas para cada tenant
]

SHARED_APPS = [
    'django_tenants',  # Necesario para django-tenants
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Tenants'# Tu aplicación de Tenants
    # Otras aplicaciones compartidas
]

# Esta es la lista final de INSTALLED_APPS
INSTALLED_APPS = list(set(SHARED_APPS + TENANT_APPS))


MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'GestorClinicas.middleware.TenantAccessMiddleware',
    'GestorClinicas.middleware.Custom404Middleware',
    'UsersTenants.middleware.TenantContextMiddleware'
]

ROOT_URLCONF = 'GestorClinicas.urls'

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

WSGI_APPLICATION = 'GestorClinicas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'Gestor',
        'USER': 'postgres',
        'PASSWORD': 'carlos',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TENANT_MODEL = "Tenants.Client"
TENANT_DOMAIN_MODEL = "Tenants.Domain"

PUBLIC_SCHEMA_URLCONF = 'Tenants.urls'