from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inlineMix_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()


# in first button, second argument is 'pay' for payment
main_menu_for_pay = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text='Оплатить услуги Юристов', pay=True)],
  [InlineKeyboardButton(text='Возврат в главное меню', callback_data='return_to_main_menu_from_pay')]
]) 
