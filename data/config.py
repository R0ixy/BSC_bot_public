import os


BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN = os.environ.get('ADMIN')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
APIKEY = os.environ.get('APIKEY')

# Analytics
MEASUREMENT_ID = os.environ.get('MEASUREMENT_ID')
API_SECRET = os.environ.get('API_SECRET')

# heroku
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)
