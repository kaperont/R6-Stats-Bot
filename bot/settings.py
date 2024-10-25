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
settings.BASE_TRACKER_API_URL = getattr(settings, 'BASE_TRACKER_API_URL', 'http://localhost:8000/api')
settings.DISCORD_BOT_TOKEN = getattr(settings, 'DISCORD_BOT_TOKEN', 'TOKEN-TOKEN-TOKEN-TOKEN')
settings.DISCORD_GUILD_ID = int(getattr(settings, 'DISCORD_GUILD_ID', 'GUILD-ID-GUILD-ID'))
