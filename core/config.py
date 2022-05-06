from starlette.config import Config
config = Config(".env")
# Переменная окружения
DATABASE_URL = config("DATABASE_URL", cast=str, default="")
#export DATABASE_URL="mysql+mysqlconnector://bot:qwer1234t5@localhost:3308/bot_db"
TELEGRAM_TOCKEN = config("TELEGRAM_TOCKEN", cast=str, default="")
#export TELEGRAM_TOCKEN="5171909645:AAG8HefH3P9iSSk4eMec70jBde24Vxtb3b8"


