import re


def is_email(text):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    text = str(text)
    if re.match(pattern, text):
        return True
    else:
        return False