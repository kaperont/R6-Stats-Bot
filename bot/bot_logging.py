import logging
import logging.config

from .settings import settings

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s ' 
                      '%(process)d %(thread)d %(message)s'
        },
        'generic': {
            'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'rotating_file_handler': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'r6_stats_bot_log.log',
            'maxBytes': 1024 * 1024 * 1,    # 10MB
            'backupCount': 5,
        }
    },
    'loggers': {
        f'{settings.APPNAME}': {
            'level': settings.LOG_LEVEL,
            'handlers': ['console', 'rotating_file_handler'],
            'propagate': False,
        },
        'discord': {
            'level': settings.LOG_LEVEL,
            'handlers': ['console', 'rotating_file_handler'],
            'propagate': False,}
    }
}

logging.config.dictConfig(LOGGING)
