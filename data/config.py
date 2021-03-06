from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
APIKEY = env.str('APIKEY')

# Analytics
MEASUREMENT_ID = env.str('MEASUREMENT_ID')
API_SECRET = env.str('API_SECRET')
