from aiogram import Router, Dispatcher, F
from aiogram.filters import Command, CommandStart
from .main import *



def register_handlers(dp: Dispatcher):
  dp.message.register(cmd_start, CommandStart())
  dp.message.register(add_name, User.name)
  dp.message.register(add_surname, User.surname)
  dp.message.register(add_middle_name, User.middle_name)
  dp.message.register(add_number, User.number)
  dp.message.register(add_email, User.email)
