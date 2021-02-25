import re


def validate_amount(amount):
    n = str(amount)
    return bool(re.match(r'^-?\d*(\.\d+)?$', n))
