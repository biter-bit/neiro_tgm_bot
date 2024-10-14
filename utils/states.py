from aiogram.fsm.state import StatesGroup, State

class TypeAiState(StatesGroup):
    image = State()
    text = State()

class CreateRefLinkState(StatesGroup):
    create = State()