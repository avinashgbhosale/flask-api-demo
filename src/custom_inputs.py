# - coding: utf-8 --
from datetime import datetime

from src.costants import DATE_YMD_FORMAT


def date_input(value):
    try:
        datetime.strptime(value, DATE_YMD_FORMAT)
    except Exception as e:
        raise ValueError("Input is invalid date string - expected YYYY-MM-dd")
    return value


# Swagger documentation
date_input.__schema__ = {'type': 'string', 'format': 'YYYY-MM-DD'}
