from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("help", "Some information about commands"),
            types.BotCommand("menu", "Show menu"),
        ]
    )
