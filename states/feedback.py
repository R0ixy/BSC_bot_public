from aiogram.dispatcher.filters.state import State, StatesGroup


class Feedback(StatesGroup):
    message = State()
