from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Commands: ",
            "/start - Start bot",
            "/help - Show information about commands",
            "/menu - Show menu (if you can't see it now)")
    
    await message.answer("\n".join(text))
