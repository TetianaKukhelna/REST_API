import re
from datetime import datetime


VALID_YES = "yes"
VALID_NO = "no"

VALID_BOOL_ANSWER = (VALID_YES, VALID_NO)
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
DATE_FORMAT = "%d-%m-%Y"


def is_valid_date(date_string, fmt=DATE_FORMAT) -> bool:
    try:
        datetime.strptime(date_string, fmt)
        return True
    except ValueError:
        return False


def convert_format(date_string: str, fmt=DATE_FORMAT) -> str:
    if is_valid_date(date_string):
        convert = datetime.strptime(date_string, fmt)
        return convert.strftime("%Y-%m-%d %H:%M:%S")


def is_valid_yes_no(bool_answer: str) -> bool:
    return bool_answer in VALID_BOOL_ANSWER


def is_valid_plate_number(s):
    result = pattern.match(s)
    res = result.group()
    return True
