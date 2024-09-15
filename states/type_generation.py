from aiogram.fsm.state import StatesGroup, State

class TypeState(StatesGroup):
    image = State()
    text = State()