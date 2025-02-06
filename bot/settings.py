from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ################### General Settings ###################
    APPNAME: str = 'bot'
    LOG_LEVEL: str = 'INFO'

    PKI_PUBLIC: str | None = None
    PKI_PRIVATE: str | None = None
    PKI_AUTHORITY: str | bool = False

    REQUEST_SETTINGS: dict = {
        'cert': (PKI_PUBLIC, PKI_PRIVATE),
        'verify': PKI_AUTHORITY
    }

    ################# Application Settings #################
    BASE_TRACKER_HTML_URL: str = 'http://localhost:8000'
    BASE_TRACKER_API_URL: str = 'http://localhost:8000/api'
    TRACKER_API_TOKEN: str = 'TOKEN-TOKEN-TOKEN-TOKEN'
    DISCORD_BOT_TOKEN: str = 'TOKEN-TOKEN-TOKEN-TOKEN'
    DISCORD_GUILD_ID: int = 0

    ################## Database Settings ###################
    DB_URL: str = 'mongodb://root:password@localhost:27017/'
    DB_READ_URL: str = 'mongodb://root:password@localhost:27017/'
    DATABASE_NAME: str = 'r6_stats'

    DATABASES: dict = {
        'owner': {
            'CLIENT': DB_URL,
            'NAME': DATABASE_NAME,
        },
        'default': {
            'CLIENT': DB_READ_URL,
            'NAME': DATABASE_NAME,
        }
    }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
