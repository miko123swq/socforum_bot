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


# сделал отдельную функцию, чтобы добавить каталог в блок кнопок
def get_inlinePay_btns(
    *,
    btns: list[tuple[str, str, bool]], 
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, value, pay in btns:
        if pay:
            keyboard.add(InlineKeyboardButton(text=text, pay=True))
        elif '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()