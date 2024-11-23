from datetime import datetime
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEDIA_PROFILE_PATH = str(BASE_DIR / "profile" / "static" / "media")

#-------------DB------------------------------------------
class DataBaseSettings(BaseModel):
    url_db: str = "postgresql+asyncpg://root:root@localhost:5436/hakaton_api"
    echo: bool = True
    expire_on_commit: bool = False
    autocommit: bool = False
    autoflush: bool = False


#-------------Token------------------------------------------

class TokenSettings(BaseModel):
    authjwt_private_key: str = str((BASE_DIR / "authorization" / "certs" / "jwt-private.pem").read_text())
    authjwt_public_key: str = str((BASE_DIR / "authorization" / "certs" / "jwt-public.pem").read_text())
    authjwt_algorithm: str = "RS512"
    refresh_expire: int = 15
    access_expire: int = 10


#-------------MiddlewareSettings---------------------------------------

class MiddleWareSettings(BaseModel):
    excluded_path_auth: list[str] = ["/auth/login",
                                     "/auth/register",
                                     "/docs",
                                     "/openapi.json",
                                     "/custom_metrics",
                                     "/news/all_news",
                                     "/news/tags",
                                     "/news/all_news"]


#-------------RedisSettings-----------------------------------------

class RedisSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 6380
    db: int = 0
    decode_responses: bool = True


#------------ParsingSettings-------------------------------------------

class ParsingSettings(BaseModel):
    SCROLL_PAUSE_TIME: int = 5
    MAX_SCROLLS: int = 50
    scroll_count: int = 0
    url_news: str = "https://economy.gov.ru/material/news/"



#-------------BaseSettings----------------------------------
class Settings(BaseSettings):
    database_settings: DataBaseSettings = DataBaseSettings()
    token_settings: TokenSettings = TokenSettings()
    middleware_settings: MiddleWareSettings = MiddleWareSettings()
    redis_settings: RedisSettings = RedisSettings()
    parser_settings: ParsingSettings = ParsingSettings()


settings: Settings = Settings()
database: DataBaseSettings = settings.database_settings
authjwt: TokenSettings = settings.token_settings
middleware: MiddleWareSettings = settings.middleware_settings
redis: RedisSettings = settings.redis_settings
parser: ParsingSettings = settings.parser_settings