import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ.get('RENDER_EXTERNAL_HOSTNAME')]

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS_ALLOWED_ORIGINS = [
    
# ]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# "whitenoise.storage.CompressedManifestStaticFilesStorage"


CONNECTION = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]
CONNECTION_STR = {pair.split("=")[0]:pair.split("=")[1] for pair in CONNECTION.split(" ")}


DATABASES = {
    "default": dj_database_url.config(
        default= os.environ['DATABASE_URL'],
        conn_max_age=600
    )
    # {
    #     "Engine": "django.db.backends.postgresql",
    #     "NAME": CONNECTION_STR["dbname"],
    #     "HOST": CONNECTION_STR["host"],
    #     "USER": CONNECTION_STR["user"],
    #     "PASSWORD": CONNECTION_STR["password"],
    # }
}

STATIC_ROOT = BASE_DIR/"staticfiles"