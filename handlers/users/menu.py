from loader import dp
from aiogram.types import Message, ChatActions
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from states.wallet_input import Form
from utils import getBalanceAPI
from utils.db_api.db_connection import DBCommands
import math
from aiogram import types
from keyboards.inline.wallet_option import cancel, wallet_changing
from keyboards.inline.settings import settings_buttons
from eth_abi import is_encodable
from keyboards.default.menu import menu


@dp.message_handler(Text(equals='Get Balance'))
async def get_balance(message: Message):
    await message.answer_chat_action(ChatActions.TYPING)
    data = await DBCommands().get_wallet(message.from_user.id)
    if not data:
        await message.answer('Please add your wallet first')
    elif not is_encodable('address', data):
        await message.answer(f'Please add a correct wallet. Your wallet "{data}" in invalid.'
                             '\n\nYou can change your wallet using "Wallet" button.')
    else:
        tokens, price = await getBalanceAPI.get_balance(data)
        if not tokens or not price:
            await message.answer("No tokens found.")
        else:
            if len(tokens) > 25:
                for i in range(0, math.ceil(len(tokens) / 25)):
                    amount = i * 25
                    if amount + 25 > len(tokens):
                        await message.answer("\n\n".join([tokens[m] for m in range(amount, len(tokens))]),
                                             disable_web_page_preview=True)
                    else:
                        await message.answer("\n\n".join([tokens[m] for m in range(amount, amount + 25)]),
                                             disable_web_page_preview=True)
            else:
                await message.answer("\n\n".join(list(tokens)), disable_web_page_preview=True)

            await message.answer("Amount of tokens: {amount}\nTotal value: {price}$".format(
                amount=len(tokens), price=price))


@dp.message_handler(Text(equals='Wallet'), state=None)
async def add_wallet(message: Message):
    data = await DBCommands().get_wallet(message.from_user.id)
    if data:
        await message.answer(f"You wallet is: `{data}`", parse_mode=types.ParseMode.MARKDOWN,
                             reply_markup=wallet_changing)
    else:
        await message.answer('Input wallet address', reply_markup=cancel)
        await Form.wallet.set()


@dp.message_handler(state=Form.wallet)
async def save_wallet(message: Message, state: FSMContext):
    if await DBCommands().get_wallet(message.from_user.id):
        await DBCommands().update_wallet(message.from_user.id, message.text)
    else:
        await DBCommands().insert_wallet(message.from_user.id, message.text)
    await message.reply("Wallet saved", reply_markup=menu)
    await state.finish()


@dp.message_handler(Text(equals='Donate'))
async def donate(message: Message):
    await message.answer("Donate BNB or BEP-20 tokens to support us. BSC address: "
                         "`0x54893d36926D95651Bf25f7B55DF328DB029Cb6b`"
                         "\n(Tap to copy)", parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(Text(equals='Settings'))
async def settings(message: Message):
    await message.answer("Choose settings button", reply_markup=settings_buttons)