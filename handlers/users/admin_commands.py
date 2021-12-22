from asyncio import sleep

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked

from loader import dp
from data.config import ADMINS
from states.admin import AdminState, DirectMessage
from utils.db_api.db_connection import DBCommands


@dp.message_handler(commands=['tell'], state=None)
async def get_message(message: Message):
    for admin in ADMINS:
        if message.from_user.id == int(admin):

            await message.answer('Введите сообщение: ')
            await AdminState.message.set()


@dp.message_handler(state=AdminState.message)
async def send_everyone(message: Message, state: FSMContext):
    user_ids = await DBCommands().get_all_id()
    for user_id in user_ids:
        try:
            await dp.bot.send_message(chat_id=user_id, text=message.text)
            await sleep(0.3)
        except BotBlocked:
            await DBCommands().delete(user_id)

    await state.finish()


@dp.message_handler(commands=['tellone'], state=None)
async def get_id(message: Message):
    for admin in ADMINS:
        if message.from_user.id == int(admin):
            await message.answer('Введите id')
            await DirectMessage.id.set()


@dp.message_handler(state=DirectMessage.id)
async def get_direct_message(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await message.answer('Введите сообщение')
    await DirectMessage.message.set()


@dp.message_handler(state=DirectMessage.message)
async def send_direct(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    try:
        await dp.bot.send_message(chat_id=user_id, text=f'Message from admin: \n{message.text}')
        await message.answer(f'Сообщение отправленно пользователю с id: {user_id}')
    except BotBlocked:
        await DBCommands().delete(user_id)
        await message.answer('Пользователь удален')
    await state.finish()
