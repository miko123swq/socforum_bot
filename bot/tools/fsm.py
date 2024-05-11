from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
  name = State()
  surname = State()
  middle_name = State()
  number = State()
  email = State()
