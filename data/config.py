from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
APIKEY = env.str("APIKEY")


