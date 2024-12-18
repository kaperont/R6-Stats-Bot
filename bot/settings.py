from typing import Any

from dynaconf import Dynaconf

settings = Dynaconf(load_dotenv=True, envvar_prefix=False, sysenv_fallback=True)

def set_env_with_default(key: str, default: Any):
    settings[key] = settings.get(key) or default

################### General Settings ###################
settings.APPNAME = getattr(settings, 'APPNAME', 'bot')
settings.LOG_LEVEL = getattr(settings, 'LOG_LEVEL', 'INFO')

set_env_with_default('PKI_PUBLIC', None)
set_env_with_default('PKI_PRIVATE', None)
set_env_with_default('PKI_AUTHORITY', None)

settings.REQUEST_SETTINGS = {
    'cert': (settings.PKI_PUBLIC, settings.PKI_PRIVATE),
    'verify': settings.PKI_AUTHORITY
}

################# Application Settings #################
settings.BASE_TRACKER_HTML_URL = getattr(settings, 'BASE_TRACKER_HTML_URL', 'http://localhost:8000')
settings.BASE_TRACKER_API_URL = getattr(settings, 'BASE_TRACKER_API_URL', 'http://localhost:8000/api')
settings.TRACKER_API_TOKEN = getattr(settings, 'TRACKER_API_TOKEN', 'TOKEN-TOKEN-TOKEN-TOKEN')
settings.DISCORD_BOT_TOKEN = getattr(settings, 'DISCORD_BOT_TOKEN', 'TOKEN-TOKEN-TOKEN-TOKEN')
settings.DISCORD_GUILD_ID = int(getattr(settings, 'DISCORD_GUILD_ID', 'GUILD-ID-GUILD-ID'))


settings.DATABASES = {
    'owner': {
        'CLIENT': getattr(settings, 'DB_URL', 'mongodb://root:password@localhost:27017/'),
        'NAME': getattr(settings, 'DATABASE_NAME', 'r6_stats'),
    },
    'default': {
        'CLIENT': getattr(settings, 'DB_READ_URL', 'mongodb://root:password@localhost:27017/'),
        'NAME': getattr(settings, 'DATABASE_NAME', 'r6_stats'),
    }
}
