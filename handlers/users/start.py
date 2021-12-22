from aiogram import types

from keyboards.default import menu
from loader import dp


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Hi!\n\nI will help you tracking all transactions with BEP-20 tokens."
                         " Also I will notify you about the balance change."
                         "\n\nTo start working click 'Wallet' button and send the address of your wallet."
                         , reply_markup=menu)


@dp.message_handler(commands=['menu'])
async def show_menu(message: types.Message):
    await message.answer('Choose menu button', reply_markup=menu)
