#-*- coding: utf-8 -*-
"""
Django settings for jaydenfoo project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import os.path
import platform

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'blog',
    'tools',
    'hitcount',
    'album',
    'easy_thumbnails',
    'wechat',
    'markdownx',
)

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'jaydenfoo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'jaydenfoo.wsgi.application'

LOGIN_URL = 'login'


# Internationalization
LANGUAGE_CODE = 'zh-hans'
DEFAULT_CHARSET = 'UTF-8'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_collect")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Email settings
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'icebrick@163.com'
EMAIL_HOST_PASSWORD = ''


#hitcout settings
HITCOUNT_KEEP_HIT_ACTIVE = {'days': 1}
HITCOUNT_HITS_PER_IP_LIMIT = 0  # unlimited
HITCOUNT_EXCLUDE_USER_GROUP = ()  # not used
HITCOUNT_KEEP_HIT_IN_DATABASE = {'seconds': 10}


# easy_thumbnails
THUMBNAIL_ALIASES = {
        '':{
            'avatar': {'size': (50,50), 'crop': True},
            },
        }

THUMBNAIL_DEBUG = True


# django markdownx
MARKDOWNX_MARKDOWN_EXTENSIONS = ['markdown.extensions.codehilite', 'markdown.extensions.tables']
MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    'markdown.extensions.codehilite': {
        'linenums': True
    }
}


if os.getenv('ENV') == 'production':
    from production_settings import *  # NOQA
else:
    from local_settings import *  # NOQA
