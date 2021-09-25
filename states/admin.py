from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    message = State()


class DirectMessage(StatesGroup):
    id = State()
    message = State()
