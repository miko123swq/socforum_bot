from aiogram import Router, Dispatcher, F
from aiogram.filters import Command, CommandStart


from .main import *



def register_handlers(dp):
  dp.message.register(cmd_start, CommandStart())
  dp.message.register(add_name, User.name)
  dp.message.register(add_surname, User.surname)
  dp.message.register(add_middle_name, User.middle_name)
  dp.message.register(add_number, User.number)
  dp.message.register(add_email, User.email)
  dp.callback_query.register(catalog, F.data == 'catalog')
  dp.callback_query.register(personal_area, F.data == 'personal_area')
  dp.callback_query.register(payment, F.data == 'payment')
  dp.callback_query.register(list_of_selected_lawyers, F.data == 'list_of_selected_lawyers')
  dp.callback_query.register(pay, F.data == 'pay')
  dp.pre_checkout_query.register(pre_checkout_query)
  dp.callback_query.register(return_to_main_menu_from_pay, F.data == 'return_to_main_menu_from_pay')
  dp.callback_query.register(return_to_main_menu, F.data == 'return_to_main_menu')
  dp.callback_query.register(my_lawyers, F.data == 'my_lawyers')
  dp.message.register(cmd_lawyer, Command('lawyer'))
  dp.message.register(add_lawyer_name, Lawyer.name)
  dp.message.register(add_lawyer_surname, Lawyer.surname)
  dp.message.register(add_lawyer_middle_name, Lawyer.middle_name)
  dp.message.register(add_lawyer_number, Lawyer.number)
  dp.message.register(add_lawyer_email, Lawyer.email)
  dp.message.register(add_lawyer_description, Lawyer.description)
  dp.message.register(add_lawyer_short_description, Lawyer.short_description)
  dp.message.register(add_lawyer_diplomas, Lawyer.diplomas)
  dp.message.register(add_lawyer_experience, Lawyer.experience)
  dp.message.register(add_lawyer_legal_services_section, Lawyer.legal_services_section)
  dp.message.register(add_lawyer_photo, Lawyer.photo)
  dp.callback_query.register(lawyer_personal_area, F.data == 'lawyer_personal_area')



