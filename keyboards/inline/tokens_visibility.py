import re

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatActions, ParseMode
from eth_abi import is_encodable

from loader import dp
from utils import getBalanceAPI
from utils.db_api.db_connection import DBCommands

hide = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="Hide", callback_data="hide"))
show = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="Show", callback_data="show"))


@dp.callback_query_handler(text='visibility')
async def tokens_visibility(callback_query: CallbackQuery):
    await callback_query.answer(cache_time=60)
    await callback_query.message.edit_text('Click "Hide" to hide token in "Get Balance" section.'
                                           ' You will be able to cancel it later by clicking "Show" button.')

    await callback_query.message.answer_chat_action(ChatActions.TYPING)
    data = await DBCommands().get_data(callback_query.message.chat.id)
    if not data['wallet']:
        await callback_query.message.answer('Please add your wallet first')
    elif not is_encodable('address', data['wallet']):
        await callback_query.message.answer(f'Please add a correct wallet. Your wallet "{data["wallet"]}" in invalid.'
                                            '\n\nYou can change your wallet using "Wallet" button.')
    else:
        tokens, price = await getBalanceAPI.get_all_tokens(data)
        if tokens == 1 and price == 0:
            await callback_query.message.answer(
                f'Your wallet `{data["wallet"]}` is invalid. \n\nNote: only BSC wallets are allowed. '
                f'\nYou can change your wallet using "Wallet" button.',
                parse_mode=ParseMode.MARKDOWN)
        elif not tokens or not price:
            await callback_query.message.answer("No tokens found.")
        else:
            for token in tokens:
                if token['visibility'] is True:
                    await callback_query.message.answer(token['data'],
                                                        disable_web_page_preview=True,
                                                        reply_markup=hide)
                else:
                    await callback_query.message.answer(token['data'],
                                                        disable_web_page_preview=True,
                                                        reply_markup=show)


@dp.callback_query_handler(text='hide')
async def hide_token(callback_query: CallbackQuery):
    address = re.search(r'https://bscscan.com/token/\w+', callback_query.message.html_text)[0].replace(
        'https://bscscan.com/token/', '')
    await DBCommands().update_blacklist(callback_query.message.chat.id, address)
    await callback_query.message.edit_reply_markup(reply_markup=show)
    await callback_query.answer(text='Success! \nThis token won\'t appear in the "Get Balance" section anymore!',
                                show_alert=True)


@dp.callback_query_handler(text='show')
async def show_token(callback_query: CallbackQuery):
    address = re.search(r'https://bscscan.com/token/\w+', callback_query.message.html_text)[0].replace(
        'https://bscscan.com/token/', '')
    await DBCommands().delete_from_blacklist(callback_query.message.chat.id, address)
    await callback_query.message.edit_reply_markup(reply_markup=hide)
    await callback_query.answer(text='Success! \nThis token will appear in the "Get Balance" section again!',
                                show_alert=True)
