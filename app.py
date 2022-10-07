from aiogram import executor

from loader import dp, bot
import middlewares, handlers
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands
from data.config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT


async def on_startup(dispatcher):

    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    await on_shutdown_notify(dispatcher)

    await bot.delete_webhook()


if __name__ == '__main__':

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
