import os
from pathlib import Path
from . import envvars

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

env_vars = envvars.load_envars(BASE_DIR)

env = []
for linha in env_vars:
    env.append(linha.rstrip())

db_name = env_vars['db_name']
db_user = env_vars['db_user']
db_passwd = env_vars['db_pw']
SECRET_KEY = env_vars['django_secret_key']
debug_mode = env_vars['debug_mode']
email_user = env_vars['email_sistema']
email_pass = env_vars['email_pw']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = debug_mode

ALLOWED_HOSTS = ['*']

try:
    hCAPTCHA_PUBLIC_KEY = env_vars['hCAPTCHA_Public_Key']
    hCAPTCHA_PRIVATE_KEY = env_vars['hCAPTCHA_Secret_Key']
except:
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''

try:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env_vars['GOOGLE_OAUTH2_PUBLIC_KEY']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env_vars['GOOGLE_OAUTH2_SECRET_KEY']

    SOCIAL_AUTH_FACEBOOK_KEY = env_vars['FACEBOOK_DEVELOPER_PUBLIC_KEY']
    SOCIAL_AUTH_FACEBOOK_SECRET = env_vars['FACEBOOK_DEVELOPER_SECRET_KEY']
except:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

    SOCIAL_AUTH_FACEBOOK_KEY = ''
    SOCIAL_AUTH_FACEBOOK_SECRET = ''

INSTALLED_APPS = [
    'mapeamento_cultural',
    'qr_code',
    #APPS DE TERCEIROS
    'fontawesomefree',
    'bootstrap5',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SERVE_QR_CODE_IMAGE_PATH = 'qr-code-image/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cultura.urls'

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

WSGI_APPLICATION = 'cultura.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        'NAME': db_name,
        'PORT': '',

        'USER': db_user,
        'PASSWORD': db_passwd,
        'HOST': '127.0.0.1',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# STATIC_ROOT = '/home/turismo/site/turismo/equipamentos/static'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'cultura/media')

LOGIN_URL='/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_mail")
DEFAULT_FROM_EMAIL = 'Secretaria Municipal de Turismo e Marketing <turismo@sme.novafriburgo.rj.gov.br>'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = email_user
EMAIL_HOST_PASSWORD = email_pass
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
