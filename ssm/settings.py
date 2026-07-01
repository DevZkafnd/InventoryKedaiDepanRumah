from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()


def get_bool_env(var_name):
    return var_name.lower() in ("true", "1", "yes", "on")


BASE_DIR = Path(__file__).resolve().parent.parent
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_env(os.getenv("DJANGO_DEBUG"))
_allowed_hosts_env = [host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")]
ALLOWED_HOSTS = [h for h in _allowed_hosts_env if h]
if DEBUG:
    for h in ["localhost", "127.0.0.1", "testserver"]:
        if h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(h)
ALLOW_PW_CHANGE = get_bool_env(os.getenv("ALLOW_PW_CHANGE"))
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "stock_manager",
    "axes",
    "email_service.apps.EmailServiceConfig",
    "ai_service.apps.AiServiceConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
    "ai_service.middleware.SimpleSecurityMiddleware",
]
AXES_FAILURE_LIMIT = int(os.getenv("AXES_FAILURE_LIMIT"))
AXES_COOLOFF_TIME = int(os.getenv("AXES_COOLOFF_TIME"))
AXES_LOCKOUT_PARAMETERS = ["username", "ip_address"]
AXES_CLIENT_IP_CALLABLE = lambda x: None  # Disable logging IP
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "100/second"},
    "DEFAULT_PAGINATION_CLASS": "stock_manager.pagination.CustomPagination",
}
LOGIN_REDIRECT_URL = "/post-login/"
LOGOUT_REDIRECT_URL = "/"
ROOT_URLCONF = "ssm.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
EMAIL_BACKEND = os.getenv("MAIL_SERVICE_BACKEND")
DEFAULT_FROM_EMAIL = os.getenv("MAIL_DEFAULT_FROM")
SERVER_EMAIL = os.getenv("MAIL_SERVER_EMAIL")
ANYMAIL = {
    "IGNORE_UNSUPPORTED_FEATURES": True,
    "SPARKPOST_API_KEY": os.getenv("MAIL_SERVICE_API_KEY"),
    "SPARKPOST_API_URL": os.getenv("MAIL_SERVICE_API_URL"),
}
WSGI_APPLICATION = "ssm.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.environ.get("DB_NAME"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # folder collectstatic output
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # sumber file statis development
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
LOG_FILE = os.getenv("LOG_FILE")  # this directory & file needs to be created first!
_log_handlers = ["console"]
_handler_config = {
    "console": {
        "level": "DEBUG",
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
}
if LOG_FILE:
    _log_handlers = ["file"]
    _handler_config["file"] = {
        "level": "INFO",
        "class": "logging.FileHandler",
        "filename": LOG_FILE,
        "formatter": "verbose",
    }
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(asctime)s %(levelname)s %(message)s"},
    },
    "handlers": _handler_config,
    "loggers": {
        "django": {
            "handlers": _log_handlers,
            "level": "INFO",
            "propagate": False,
        },
    },
}
