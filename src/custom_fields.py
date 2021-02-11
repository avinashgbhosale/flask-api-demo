# - coding: utf-8 --
import re
from datetime import datetime

from flask_restx import fields

from src.costants import DATE_YMD_FORMAT
from src.custom_exceptions import ValidationError


EMAIL_REGEX = re.compile(r'\S+@\S+\.\S+')


def is_valid_image(file):
    """ validate image for extensions: png, jpg, jpeg"""
    return True


def validate_image(file):
    """Validate Image wrto MIME-TYPE, EXTENSIONS, SIZE"""
    errors = dict()
    message = "Validation failed"
    if "image" not in file.mimetype:
        errors[file.name] = "Not valid Image File"
    if errors:
        raise ValidationError(message, errors=errors)


class CustomField(fields.String):
    pass


class EmailField(CustomField):
    """
    Email field
    """
    __schema_type__ = 'string'
    __schema_format__ = 'email'
    __schema_example__ = 'email@domain.com'

    def validate(self, value):
        if not value:
            return False if self.required else True
        if not EMAIL_REGEX.match(value):
            return False
        return True


def validate_payload(payload, api_model):
    # check if any required fields are missing in payload
    message = "Validation Failed"
    errors = dict()
    for key in api_model:
        if api_model[key].required and key not in payload:
            errors[key] = 'Required field \'%s\' missing' % key
    # check payload
    for key in payload:
        field = api_model[key]
        if isinstance(field, fields.List):
            field = field.container
            data = payload[key]
        else:
            data = [payload[key]]

        if isinstance(field, EmailField) and hasattr(field, 'validate'):
            for i in data:
                if not field.validate(i):
                    errors[key] = "not valid email address"
                    message = 'Validation of email field failed'

        elif isinstance(field, CustomField) and hasattr(field, 'validate'):
            for i in data:
                if not field.validate(i):
                    errors[key] = 'Validation of \'%s\' field failed' % key
                    message = 'Validation of \'%s\' field failed' % key
    if errors:
        raise ValidationError(message, errors=errors)


def validate_dates(from_date, to_date):
    if datetime.strptime(from_date, DATE_YMD_FORMAT) > datetime.strptime(to_date, DATE_YMD_FORMAT):
        raise ValidationError(message="invalid date range: Start date should not be greater than End date")
