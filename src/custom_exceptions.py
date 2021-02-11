# - coding: utf-8 --

class BaseError(Exception):
    """ Base Error Class"""
    def __init__(self, message='', errors=None):
        super().__init__()
        self.code = 400
        self.message = message
        self.status = "BAD_REQUEST"
        if not errors:
            errors = {}
        self.errors = errors

    def to_dict(self):
        return {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "errors": self.errors
        }


class NotFoundError(BaseError):
    def __init__(self, message, errors=None):
        super().__init__(message, errors)
        self.code = 404
        self.status = "NOT_FOUND"


class ValidationError(BaseError):
    def __init__(self, message, errors=None):
        super().__init__(message, errors)
        self.code = 400
        self.status = "VALIDATION_FAILURE"


class NotAuthorizedError(BaseError):
    def __init__(self, message='Unauthorized'):
        BaseError.__init__(self)
        self.code = 401
        self.message = message
        self.status = 'NOT_AUTHORIZED'


class ServerError(BaseError):
    def __init__(self, message='Internal server error'):
        BaseError.__init__(self)
        self.code = 500
        self.message = message
        self.status = 'SERVER_ERROR'
