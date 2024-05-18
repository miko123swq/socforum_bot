from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
  name = State()
  surname = State()
  middle_name = State()
  number = State()
  email = State()


class Lawyer(StatesGroup):
  name = State()
  surname = State()
  middle_name = State()
  number = State()
  email = State()
  description = State()
  short_description = State()
  diplomas = State()
  experience = State()
  legal_services_section = State()
  photo = State()