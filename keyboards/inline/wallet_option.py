from loader import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from states.wallet_input import Form
from aiogram.dispatcher import FSMContext
from keyboards.default.menu import menu
from aiogram.dispatcher.filters import Text
from keyboards.default.cancel_button import cancel

button = InlineKeyboardButton(text="Change wallet", callback_data="change")
wallet_changing = InlineKeyboardMarkup().add(button)


@dp.callback_query_handler(text='change')
async def change_wallet(callback_query: CallbackQuery):
    await callback_query.answer(cache_time=60)
    await callback_query.message.answer("Input new wallet", reply_markup=cancel)
    await Form.wallet.set()


@dp.message_handler(Text(equals='Cancel'), state=Form.wallet)
async def settings(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Canceled", reply_markup=menu)
