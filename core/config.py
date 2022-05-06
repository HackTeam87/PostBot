from starlette.config import Config
config = Config(".env")
# Переменная окружения
DATABASE_URL = config("DATABASE_URL", cast=str, default="")
TELEGRAM_TOCKEN = config("TELEGRAM_TOCKEN", cast=str, default="")



