import os
from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&f#do-@&a=21!_n+gx&xp+e*iea=c4t)g#o0lm1t2t2du(d(l('

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
APP_PATH = os.path.dirname(os.path.abspath(__file__))

# 读取运行环境
env = environ.Env()
APP_ENV = env.str('APP_ENV', 'dev')
# 读取相对应的env文件
env_file = '.env.%s' % APP_ENV
env = environ.Env()
env.read_env(env_file=os.path.join(APP_PATH, env_file))

DEBUG_MODE = env('DEBUG_MODE', default='True')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if DEBUG_MODE == 'True' else False

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

SIMPLEUI_HOME_INFO = False  # 隐藏右侧SimpleUI广告链接
SIMPLEUI_ANALYSIS = False  # 使用分析

ROOT_URLCONF = 'app.urls'

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================可选配置============================================
ROUTE_PREFIX = 'api'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

def get_installed_apps(debug):
    apps = [
        'corsheaders',
        'simpleui',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'system_module.apps.SystemModuleConfig',
        'user_module.apps.UserModuleConfig',
        'card_module.apps.CardModuleConfig',
        'memory_module.apps.MemoryModuleConfig',

        'rest_framework',
        # 'rest_framework.authtoken',
        # 'dj_rest_auth',
        'captcha',
        'drf_yasg',
        'nested_inline',
        'solo',

        'debug_toolbar' if debug else None
    ]
    return [app for app in apps if app]  # 过滤掉 None


def get_middleware(debug):
    middleware = [
        "debug_toolbar.middleware.DebugToolbarMiddleware" if debug else None,
        'app.common.exceptionbox.middleware.ExceptionBoxMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    return [mw for mw in middleware if mw]  # 过滤掉 None


INSTALLED_APPS = get_installed_apps(DEBUG)
MIDDLEWARE = get_middleware(DEBUG)
ALLOWED_HOSTS = ["localhost", "localhost:8000", "127.0.0.1", "127.0.0.1:8000", "anyws.myhk.fun","mychats.tech"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'app/data/db.sqlite3',
    }
}

# # 数据库配置
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': DATABASES_NAME,
#         'PORT': DATABASES_PORT,
#         'HOST': DATABASES_HOST,
#         'USER': DATABASES_USER,
#         'PASSWORD': DATABASES_PASSWORD,
#         'CONN_MAX_AGE': 60
#     }
# }

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        # 只使用json渲染
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# 设置jwt的有效期为15天
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=150),
    'ROTATE_REFRESH_TOKENS': True,
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}",
#         "OPTIONS": {
#             "CONNECTION_POOL_KWARGS": {"max_connections": 100}
#         }
#     }
# }

# 使用本地缓存
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

SOLO_CACHE = 'default'
SOLO_CACHE_TIMEOUT = 60 * 60 * 24
SOLO_CACHE_PREFIX = 'solo'
#
LOGIN_URL = "/docs/login/"
LOGOUT_URL = "/docs/logout"

# SWAGGER_SETTINGS = {
#     'LOGIN_URL': '/auth/login/',  # 使用 dj-rest-auth 的登录 URL
#     'LOGOUT_URL': '/auth/logout/',  # 使用 dj-rest-auth 的登出 URL
# }

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 使用redis作为缓存中间件

# 邮件相关配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 发送邮件配置
EMAIL_HOST = 'smtp.qq.com'  # 服务器名称
EMAIL_PORT = 25  # 服务端口
EMAIL_HOST_USER = '3135287831@qq.com'  # 填写自己邮箱
EMAIL_HOST_PASSWORD = 'fkhkoscmrjqbdhde'  # 在邮箱中设置的客户端授权密码
EMAIL_FROM = 'MyDesktopCloud<3135287831@qq.com'  # 收件人看到的发件人
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议
