

class BaseError(Exception):

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return {
            "error_type": self.__class__.__name__,
            "error": self.message,
            "code": self.status_code
        }


class ParameterError(BaseError):
    status_code = 400
