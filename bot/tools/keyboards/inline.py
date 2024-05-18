from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
  [InlineKeyboardButton(text='Личный кабинет', callback_data='personal_area')],
  [InlineKeyboardButton(text='Оплата', callback_data='payment')],
  [InlineKeyboardButton(text='Мои Юристы', callback_data='my_lawyers')]
]) 


main_menu_for_pay = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Оплатить услуги Юристов', pay=True)],
  [InlineKeyboardButton(text='Возврат в главное меню', callback_data='return_to_main_menu_from_pay')]
]) 


main_menu_in_my_lawyers = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
  [InlineKeyboardButton(text='Личный кабинет', callback_data='personal_area')]
]) 


message_to_layers = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Написать Юристу', callback_data='message_to_layers')]
]) 


menu_in_personal_area = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
  [InlineKeyboardButton(text='Оплата', callback_data='payment')],
  [InlineKeyboardButton(text='Мои Юристы', callback_data='my_lawyers')]
]) 

return_to_main_menu = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Возврат в главное меню', callback_data='return_to_main_menu')]
])


payment = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Список выбранных Юристов', callback_data='list_of_selected_lawyers')],
  [InlineKeyboardButton(text='Оплата юридических услуг', callback_data='pay')],
  [InlineKeyboardButton(text='Возврат в главное меню', callback_data='return_to_main_menu')]
])


payment_layers = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Оплатить', callback_data='pay')],
  [InlineKeyboardButton(text='Возврат в главное меню', callback_data='return_to_main_menu')]
])


#LAWYER
lawyer_main_menu = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Личный кабинет Юриста', callback_data='lawyer_personal_area')],
  [InlineKeyboardButton(text='Переход на сайт', callback_data='catalog')]
]) 