from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, ParseMode
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api.db_connection import DBCommands
from keyboards.default.cancel_button import cancel
from keyboards.default.menu import menu
from states.feedback import Feedback
from data.config import ADMINS


settings_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="Wallet", callback_data="wallet"),
    InlineKeyboardButton(text="Tokens visibility", callback_data="visibility"),
    InlineKeyboardButton(text="Feedback", callback_data="feedback"),
    InlineKeyboardButton(text="Bot information", callback_data="info"))

back_button = InlineKeyboardButton(text="Go back", callback_data="back")
wallet_delete = InlineKeyboardMarkup().add(back_button,
                                           InlineKeyboardButton(text="Delete wallet", callback_data="delete_wallet"))

go_back = InlineKeyboardMarkup().add(back_button)


@dp.callback_query_handler(text='back')
async def back(callback_query: CallbackQuery):
    await callback_query.answer(cache_time=60)
    await callback_query.message.edit_text("Choose settings button", reply_markup=settings_buttons)


@dp.callback_query_handler(text='wallet')
async def wallet_info(callback_query: CallbackQuery):
    await callback_query.answer(cache_time=60)
    data = (await DBCommands().get_data(callback_query.message.chat.id))['wallet']
    if data:
        await callback_query.message.edit_text(f"You wallet is: `{data}`",
                                               parse_mode=ParseMode.MARKDOWN, reply_markup=wallet_delete)
    else:
        await callback_query.message.edit_text("You have not added any wallet yet")


@dp.callback_query_handler(text='delete_wallet')
async def delete_wallet(callback_query: CallbackQuery):
    await callback_query.answer(cache_time=60)
    await DBCommands().delete(callback_query.message.chat.id)
    await callback_query.message.answer('Deleted')


@dp.callback_query_handler(text='feedback')
async def feedback(callback_query: CallbackQuery):
    await callback_query.answer(cache_time=60)
    await callback_query.message.delete()
    await callback_query.message.answer('Input your message here and admin will receive it', reply_markup=cancel)
    await Feedback.message.set()


@dp.message_handler(Text(equals='Cancel'), state=Feedback.message)
async def settings(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Canceled", reply_markup=menu)


@dp.message_handler(state=Feedback.message)
async def proceed_feedback(message: Message, state: FSMContext):
    for admin in ADMINS:
        await dp.bot.send_message(admin, f'Сообщение от пользователя \nusername: `{message.from_user.username}`'
                                         f' \nid: `{message.from_user.id}`\n\n{message.text}',
                                  parse_mode=ParseMode.MARKDOWN)
    await message.reply("Message sent to admins! You will receive answer soon!")
    await state.finish()


@dp.callback_query_handler(text='info')
async def get_info(callback_query: CallbackQuery):
    await callback_query.answer(cache_time=60)
    await callback_query.message.edit_text("With BSC Token Explorer you will receive notifications about "
                                           "incoming transactions of your wallet and will be able "
                                           "to check the current balance of your wallet.\n\n"
                                           "All token prices are getting directly from https://pancakeswap.finance/ API"
                                           , disable_web_page_preview=True, reply_markup=go_back)
