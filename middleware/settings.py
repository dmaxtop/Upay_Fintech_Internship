import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'metrics_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'request_metrics.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request_metrics': {
            'handlers': ['metrics_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'myapp.middleware.RequestMetricsLoggerMiddleware',
]