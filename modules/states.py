from aiogram.fsm.state import State, StatesGroup

class UserInputState(StatesGroup):
    question = State()
    suggest = State()
    

class AdminInputStates(StatesGroup):
    answer = State()
    