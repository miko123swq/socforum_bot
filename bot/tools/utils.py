import re


def is_email(text):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    text = str(text)
    if re.match(pattern, text):
        return True
    else:
        return False


def is_valid_phone_number(text):
    if not text.isdigit():
        return (
            False,
            "Произошла ошибка - введённый текст не является номером телефона. Пожалуйста, введите корректный ваш номер.",
        )

    if text.startswith("8"):
        text = "7" + text[1:]

    if len(text) != 11:
        return False, "Номер телефона должен состоять из 11 цифр. Попробуйте ещё раз."

    return True, text
